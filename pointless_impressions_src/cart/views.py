from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView
from django.conf import settings
from decimal import Decimal
from .utils import get_cart
from .forms import CartItemUpdateForm
from pointless_impressions_src.order.forms import OrderForm
from pointless_impressions_src.artwork.models import (
    Artwork, ArtworkFramingCondition
    )
import json


# Write your views here.
class CheckoutView(TemplateView):
    """
    GET /checkout/)
    Display main checkout page with cart review and payment form

    Context Data:
    - cart_items: List of items in cart with artwork details
    - total_price: Sum of all item totals (decimal)
    - total_quantity: Total number of items in cart (int)
    - delivery_cost: Delivery cost based on total price and tiers (decimal)
    - grand_total: Total including delivery cost (decimal)
    - items_needed_for_free_delivery: Number of items needed to reach free
      delivery threshold (int)

    Features:
    - Retrieves cart from Cart/CartItem models using UUID or user
    - Calculates line totals and grand total
    - Removes items if artwork no longer exists
    - Displays cart summary and checkout form

    Response: Renders checkout.html template with cart context
    """
    template_name = 'cart/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if context.get('cart_is_empty', True):
            return context

        cart = context.get('cart')

        cart_items_data = []
        try:
            cart_items_qs = cart.items.select_related(
                'artwork',
                'framing_condition',
                'artwork__main_photo'
            ).all()

            for item in cart_items_qs:
                if item.artwork:
                    item_form = CartItemUpdateForm(
                        artwork=item.artwork,
                        initial={
                            'quantity': item.quantity,
                            'framing_option': (
                                item.framing_condition.condition_friendly_name
                                if item.framing_condition else None
                            ),
                        },
                        max_quantity=item.artwork.quantity
                    )
                    item.form = item_form
                    cart_items_data.append(item)
        except Exception:
            context['cart_error'] = (
                "Could not load cart items. Due to an error."
            )
            return context

        context['cart_items'] = cart_items_data
        context['order_form'] = OrderForm(user=self.request.user)

        if self.request.user.is_authenticated:
            try:
                customer_profile = context.get('current_user_customer_profile')
                if customer_profile:
                    context['shipping_addresses'] = (
                        customer_profile.user_profile.addresses.filter(
                            address_type='SHIPPING'
                        )
                    )
                    context['billing_addresses'] = (
                        customer_profile.user_profile.addresses.filter(
                            address_type='BILLING'
                            )
                    )
                else:
                    context['shipping_addresses'] = None
                    context['billing_addresses'] = None
            except Exception:
                context['shipping_addresses'] = None
                context['billing_addresses'] = None

        return context


class CartDropdownView(View):
    """
    GET /cart/dropdown/
    Return HTML snippet for cart dropdown in navbar

    Context Data:
    - cart_items: List of items in cart with artwork details
    - total_price: Sum of all item totals (decimal)
    - total_quantity: Total number of items in cart (int)

    Features:
    - Retrieves cart from Cart/CartItem models using session ID
    - Calculates line totals and grand total
    - Returns rendered HTML snippet for dropdown

    Response: JSON with rendered HTML for cart dropdown
    """
    def get(self, request, *args, **kwargs):
        try:
            cart = get_cart(request)
            cart_items_data = []
            total_quantity = 0
            subtotal = Decimal('0.00')
            delivery_cost = Decimal('0.00')
            grand_total = Decimal('0.00')
            items_needed_for_free_delivery = settings.FREE_DELIVERY_THRESHOLD

            if cart:
                try:
                    cart_items = cart.items.select_related(
                        'artwork',
                        'artwork__artist',
                        'artwork__artist__user_profile',
                        'artwork__artist__user_profile__user',
                        'framing_condition',
                        'artwork__main_photo'
                    ).all()

                    for item in cart_items:
                        try:
                            artwork_image_url = None

                            if item.artwork and item.artwork.main_photo:
                                photo = item.artwork.main_photo

                                if (
                                    hasattr(photo, 'get_image_url') and
                                    callable(photo.get_image_url)
                                ):
                                    try:
                                        artwork_image_url = (
                                            photo.get_image_url()
                                            )
                                    except Exception:
                                        pass

                                if not artwork_image_url and hasattr(
                                    photo, 'image'
                                ):
                                    try:
                                        if photo.image:
                                            artwork_image_url = photo.image.url
                                    except (AttributeError, ValueError):
                                        pass

                            framing_name = None
                            if item.framing_condition:
                                framing_name = (
                                    item.framing_condition.
                                    condition_friendly_name or
                                    item.framing_condition.condition_name or
                                    "Standard"
                                )

                            cart_item = {
                                'artwork_name': (
                                    item.artwork.name if item.artwork
                                    else "Deleted Artwork"
                                ),
                                'artwork_image_url': artwork_image_url,
                                'quantity': item.quantity,
                                'notes': item.notes or '',
                                'price': (
                                    item.artwork.price if item.artwork
                                    else Decimal('0.00')
                                ),
                                'framing_condition': framing_name,
                            }

                            cart_items_data.append(cart_item)

                        except Exception:
                            continue

                    total_quantity = cart.get_total_quantity()
                    subtotal = cart.get_subtotal()
                    delivery_cost = cart.get_delivery_cost()
                    grand_total = cart.get_grand_total()

                    if 0 < total_quantity < settings.FREE_DELIVERY_THRESHOLD:
                        items_needed_for_free_delivery = (
                            settings.FREE_DELIVERY_THRESHOLD - total_quantity
                        )
                    else:
                        items_needed_for_free_delivery = 0

                except Exception:
                    raise

            try:
                html = render_to_string(
                    'cart/includes/cart_dropdown.html',
                    {
                        'cart_items': cart_items_data,
                        'total_quantity': total_quantity,
                        'subtotal': subtotal,
                        'delivery_cost': delivery_cost,
                        'grand_total': grand_total,
                        'items_needed_for_free_delivery': (
                            items_needed_for_free_delivery
                            ),
                        'free_delivery_item_threshold': (
                            settings.FREE_DELIVERY_THRESHOLD
                            ),
                    },
                    request=request
                )

            except Exception:
                raise

            return JsonResponse({
                'html': html,
                'cart_count': total_quantity,
                'total_quantity': total_quantity
            })

        except Exception as e:
            return JsonResponse(
                {
                    'error': 'Failed to generate cart dropdown.',
                    'details': (
                        str(e) if settings.DEBUG else 'An error occurred'
                        )
                },
                status=500
            )


class UpdateCartView(View):
    """
    Handles AJAX for updating the cart items

    POST /cart/update/

    Request Data:
    - artwork_id: ID of the artwork to update (int)
    - quantity: New quantity for the artwork (int)
    - framing_option: Framing option selected (string)

    Features:
    - Updates cart item quantity and framing option
    - Cart price recalculated after update
    - Removes item if quantity is set to zero
    - Removes item if remove button is clicked
    - Removes item if artwork out of stock or deleted

    Response: JSON with updated cart summary HTML
    """
    def post(self, request, *args, **kwargs):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Invalid request'}, status=400)

        try:
            try:
                artwork_id = request.POST.get('artwork_id')
                quantity = int(request.POST.get('quantity', 0))
                framing_option = request.POST.get('framing_option', '')
            except ValueError:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid quantity value'
                }, status=400)

            if not artwork_id:
                return JsonResponse({
                    'success': False,
                    'error': 'Artwork ID is required'
                }, status=400)

            try:
                artwork = Artwork.objects.get(id=artwork_id)
            except Artwork.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Artwork not found'
                }, status=404)

            if quantity > artwork.quantity:
                return JsonResponse({
                    'success': False,
                    'error': f'Only {artwork.quantity} available in stock'
                }, status=400)

            cart = get_cart(request)
            if not cart:
                return JsonResponse({
                    'success': False,
                    'error': 'Cart not found'
                }, status=400)

            existing_items_for_artwork = cart.items.filter(artwork=artwork)

            framing_condition = None
            if framing_option:
                try:
                    framing_condition = artwork.selected_conditions.get(
                        id=framing_option
                    )
                except ArtworkFramingCondition.DoesNotExist:
                    pass

            if quantity == 0:
                item_to_remove = cart.items.filter(
                    artwork=artwork,
                    framing_condition=framing_condition
                ).first()
                if item_to_remove:
                    item_to_remove.delete()
                    cart.save()
                    message = 'Item removed from cart'
                else:
                    message = 'Item not found in cart'
            else:
                target_item_exists = existing_items_for_artwork.filter(
                    framing_condition=framing_condition
                ).exists()
                if target_item_exists:
                    item, created = cart.add_or_update_item(
                        artwork=artwork,
                        quantity=quantity,
                        framing_condition=framing_condition,
                        replace_quantity=True,
                    )
                    message = 'Cart quantity updated successfully'
                else:
                    if existing_items_for_artwork.exists():
                        existing_items_for_artwork.delete()
                    item, created = cart.add_or_update_item(
                        artwork=artwork,
                        quantity=quantity,
                        framing_condition=framing_condition,
                        replace_quantity=True,
                    )
                    message = 'Cart updated with new framing option'
                cart.save()

            updated_summary_html = render_to_string(
                'cart/includes/cart_summary.html',
                {
                    'subtotal': cart.get_subtotal(),
                    'delivery_cost': cart.get_delivery_cost(),
                    'grand_total': cart.get_grand_total(),
                    'total_quantity': cart.get_total_quantity(),
                    'items_needed_for_free_delivery': (
                        (
                            settings.FREE_DELIVERY_THRESHOLD -
                            cart.get_total_quantity()
                            )
                        if (
                            0 < cart.get_total_quantity() <
                            settings.FREE_DELIVERY_THRESHOLD
                            )
                        else 0
                    )
                },
                request=request
            )

            return JsonResponse({
                'success': True,
                'message': message,
                'updated_summary_html': updated_summary_html,
                'new_quantity': quantity,
                'new_subtotal': str(cart.get_subtotal()),
                'new_delivery_cost': str(cart.get_delivery_cost()),
                'new_grand_total': str(cart.get_grand_total()),
                'new_framing_condition': (
                    framing_condition.condition_friendly_name
                    if framing_condition else None
                )
            })

        except Exception:
            return JsonResponse({
                'success': False,
                'error': 'An error occurred while updating the cart.'
            }, status=500)


class RemoveCartItemView(View):
    """
    Handles AJAX requests to remove an item from the cart.

    POST /checkout/remove-item/

    Request Data:
    - artwork_id: ID of the artwork to remove (int)

    Features:
    - Removes the specified item from the cart
    - Returns a success message if the item is removed
    - Returns an error message if the item does not exist

    Response: JSON with success or error message
    """
    def post(self, request, *args, **kwargs):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(
                {'error': 'Invalid request'},
                status=400
            )

        try:
            data = json.loads(request.body)
            artwork_id = data.get('artwork_id')

            if not artwork_id:
                return JsonResponse(
                    {'success': False, 'error': 'Artwork ID is required'},
                    status=400
                )

            cart = get_cart(request)

            if not cart:
                return JsonResponse(
                    {'success': False, 'error': 'Cart not found'},
                    status=404
                )

            item = cart.items.filter(artwork_id=artwork_id).first()

            if not item:
                return JsonResponse(
                    {'success': False, 'error': 'Item not found in cart'},
                    status=404
                )

            item.delete()
            cart.save()

            return JsonResponse(
                {'success': True, 'message': 'Item removed successfully'}
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {'success': False, 'error': 'Invalid JSON data'},
                status=400
            )
        except Exception as e:
            return JsonResponse(
                {'success': False, 'error': str(e)},
                status=500
            )

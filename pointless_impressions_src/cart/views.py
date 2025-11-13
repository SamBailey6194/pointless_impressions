from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView
from django.conf import settings
from .utils import get_cart
from .forms import CartItemUpdateForm
from pointless_impressions_src.order.forms import OrderForm
from pointless_impressions_src.profiles.models import Customer, Address
import logging

logger = logging.getLogger(__name__)


# Write your views here.
class CheckoutView(TemplateView):
    """
    GET /checkout/
    Display main checkout page with cart review and payment form

    Context Data:
    - cart_items: List of items in cart with artwork details
    - total_price: Sum of all item totals (float)
    - total_quantity: Total number of items in cart (int)
    - delivery_cost: Delivery cost based on total price and tiers (float)
    - grand_total: Total including delivery cost (float)
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

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        response = self.render_to_response(context)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart = get_cart(self.request)

        if not cart or cart.get_total_quantity() == 0:
            context['cart_empty'] = True
            return context

        cart_items_list = []
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
                        'notes': item.notes,
                        'framing_condition': (
                            item.framing_condition.id
                            if item.framing_condition else None
                        ),
                    }
                )

                item.form = item_form
                cart_items_list.append(item)

        total_quantity = cart.get_total_quantity()
        total_price = cart.get_total_price()
        delivery_cost = cart.get_delivery_cost()
        grand_total = cart.get_grand_total()

        items_needed_for_free_delivery = 0
        if 0 < total_quantity < settings.FREE_DELIVERY_THRESHOLD:
            items_needed_for_free_delivery = (
                settings.FREE_DELIVERY_THRESHOLD - total_quantity
                )

        context.update({
            'cart_empty': False,
            'cart': cart,
            'cart_items': cart_items_list,
            'total_price': total_price,
            'total_quantity': total_quantity,
            'delivery_cost': delivery_cost,
            'grand_total': grand_total,
            'items_needed_for_free_delivery': items_needed_for_free_delivery,
            'free_delivery_item_threshold': settings.FREE_DELIVERY_THRESHOLD,
        })

        context['order_form'] = OrderForm(user=self.request.user)
        if self.request.user.is_authenticated:
            try:
                customer = self.request.user.customer
                context['shipping_address'] = customer.addresses.filter(
                    address_type=Address.SHIPPING
                )
                context['billing_address'] = customer.addresses.filter(
                    address_type=Address.BILLING
                )
            except Customer.DoesNotExist:
                context['shipping_address'] = None
                context['billing_address'] = None

        return context


class CartDropdownView(View):
    """
    GET /cart/dropdown/
    Return HTML snippet for cart dropdown in navbar

    Context Data:
    - cart_items: List of items in cart with artwork details
    - total_price: Sum of all item totals (float)
    - total_quantity: Total number of items in cart (int)

    Features:
    - Retrieves cart from Cart/CartItem models using session ID
    - Calculates line totals and grand total
    - Returns rendered HTML snippet for dropdown

    Response: JSON with rendered HTML for cart dropdown
    """
    def get(self, request, *args, **kwargs):
        cart = get_cart(request)

        cart_items_data = []
        total_quantity = 0
        total_price = 0

        if cart:
            cart_items = cart.items.select_related(
                'artwork', 'framing_condition', 'artwork__main_photo'
            ).all()

            for item in cart_items:
                cart_items_data.append({
                    'artwork': item.artwork,
                    'quantity': item.quantity,
                    'notes': item.notes,
                    'price': item.artwork.price,
                    'framing_condition': (
                        item.framing_condition.condition_friendly_name if
                        item.framing_condition
                        else None
                    ),
                })

            total_quantity = cart.get_total_quantity() if cart else 0
            total_price = cart.get_total_price() if cart else 0
            delivery_cost = cart.get_delivery_cost() if cart else 0
            grand_total = cart.get_grand_total() if cart else 0

            if 0 < total_quantity < settings.FREE_DELIVERY_THRESHOLD:
                items_needed_for_free_delivery = (
                    settings.FREE_DELIVERY_THRESHOLD - total_quantity
                )

        html = render_to_string(
            'cart/includes/cart_dropdown.html',
            {
                'cart_items': cart_items_data,
                'total_quantity': total_quantity,
                'total_price': total_price,
                'delivery_cost': delivery_cost,
                'grand_total': grand_total,
                'items_needed_for_free_delivery': (
                    items_needed_for_free_delivery
                    ),
                'free_delivery_item_threshold': (
                    settings.FREE_DELIVERY_THRESHOLD
                    ),
            }
        )

        return JsonResponse({'html': html})

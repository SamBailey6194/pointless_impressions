from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView
from .utils import get_cart
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

    Features:
    - Retrieves cart from Cart/CartItem models using UUID or user
    - Calculates line totals and grand total
    - Removes items if artwork no longer exists
    - Displays cart summary and checkout form

    Response: Renders checkout.html template with cart context
    """
    template_name = 'checkout/checkout.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        response = self.render_to_response(context)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch the cart for the current user or anonymous session
        cart = get_cart(self.request)

        if not cart or cart.get_total_quantity() == 0:
            context['cart_empty'] = True
            return context

        context.update({
            'cart_empty': False,
            'cart': cart,
            'cart_items': cart.items.select_related(
                'artwork',
                'framing_condition',
                'artwork__main_photo'
            ).all(),
            'total_price': cart.get_total_price(),
            'total_quantity': cart.get_total_quantity(),
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

            total_quantity = cart.get_total_quantity()
            total_price = cart.get_total_price()

        html = render_to_string(
            'cart/includes/cart_dropdown.html',
            {
                'cart_items': cart_items_data,
                'total_quantity': total_quantity,
                'total_price': total_price,
            }
        )

        return JsonResponse({'html': html})

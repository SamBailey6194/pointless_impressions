from decimal import Decimal
from django.conf import settings
from .utils import get_cart


# Write your context processors here.
def cart_context_processor(request):
    """
    Adds cart information to the template context for all templates.

    Provides:
    - cart: The current user's cart or None
    - cart_is_empty: Boolean indicating if cart is empty
    - total_quantity: Total quantity of items in the cart (int)
    - subtotal: Total price of items in the cart (Decimal)
    - delivery_fee: Calculated delivery fee based on cart contents (Decimal)
    - grand_total: Subtotal + delivery fee (Decimal)
    - items_needed_for_free_delivery: Items needed for free delivery (int)
    - free_delivery_item_threshold: Threshold for free delivery from settings
    (int)
    """
    cart = get_cart(request)
    cart_is_empty = not cart or cart.get_total_quantity() == 0

    if cart_is_empty:
        return {
            'cart': None,
            'cart_is_empty': True,
            'total_quantity': 0,
            'subtotal': Decimal('0.00'),
            'delivery_fee': Decimal('0.00'),
            'grand_total': Decimal('0.00'),
            'items_needed_for_free_delivery': settings.FREE_DELIVERY_THRESHOLD,
            'free_delivery_item_threshold': settings.FREE_DELIVERY_THRESHOLD,
        }

    total_quantity = cart.get_total_quantity()
    subtotal = cart.get_subtotal()
    delivery_cost = cart.get_delivery_cost()
    grand_total = cart.get_grand_total()

    items_needed_for_free_delivery = 0
    if 0 < total_quantity < settings.FREE_DELIVERY_THRESHOLD:
        items_needed_for_free_delivery = (
            settings.FREE_DELIVERY_THRESHOLD - total_quantity
        )

    return {
        'cart': cart,
        'cart_is_empty': False,
        'total_quantity': total_quantity,
        'subtotal': subtotal,
        'delivery_fee': delivery_cost,
        'grand_total': grand_total,
        'items_needed_for_free_delivery': items_needed_for_free_delivery,
        'free_delivery_item_threshold': settings.FREE_DELIVERY_THRESHOLD,
    }

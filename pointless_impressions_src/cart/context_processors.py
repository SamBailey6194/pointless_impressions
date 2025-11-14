from decimal import Decimal
from .utils import get_cart, calculate_delivery_cost


# Write your context processors here.
def cart_context_processor(request):
    """
    Adds cart information to the template context for all templates.
    Provides:
    - cart: The current user's cart or None
    - cart_total_quantity: Total quantity of items in the cart (int)
    - cart_total_price: Total price of items in the cart (float)
    - delivery_fee: Calculated delivery fee based on cart contents (float)
    """
    cart = get_cart(request)
    if cart:
        total_quantity = cart.get_total_quantity()
        subtotal = cart.get_subtotal()
    else:
        total_quantity = 0
        subtotal = Decimal('0.00')

    return {
        'cart': cart,
        'total_quantity': total_quantity,
        'subtotal': subtotal,
        'delivery_fee': calculate_delivery_cost(total_quantity),
    }

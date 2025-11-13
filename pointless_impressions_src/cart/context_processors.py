from .utils import get_cart


# Write your context processors here.
def cart_context_processor(request):
    """
    Adds cart information to the template context for all templates.
    Provides:
    - cart: The current user's cart or None
    - cart_total_quantity: Total quantity of items in the cart (int)
    - cart_total_price: Total price of items in the cart (float)
    """
    cart = get_cart(request)
    if cart:
        total_quantity = cart.get_total_quantity()
        total_price = cart.get_total_price()
    else:
        total_quantity = 0
        total_price = 0

    return {
        'cart': cart,
        'total_quantity': total_quantity,
        'total_price': total_price,
    }

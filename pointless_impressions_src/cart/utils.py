from .models import Cart


# Write your utility functions for the cart here
def get_cart(request):
    """
    Gets the cart from the request for either an authenticated
    user or an anonymous session.
    """
    cart = None
    if request.user.is_authenticated:
        try:
            # Get the cart linked to the user account
            cart = request.user.cart
            if not cart.is_active:
                cart = None
        except Cart.DoesNotExist:
            cart = None
    else:
        # User is anonymous, get cart from session
        session_key = request.session.session_key
        if not session_key:
            # If no session, they can't have a cart
            return None

        cart = Cart.objects.filter(
            session_id=session_key, is_active=True
        ).first()
    return cart

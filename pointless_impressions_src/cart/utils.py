from django.conf import settings
from decimal import Decimal


# Write your utility functions for the cart here
def get_cart(request):
    """
    Gets the cart from the request for either an authenticated
    user or an anonymous session. If no cart exists for an authenticated user,
    a new cart is created using the session ID.
    """
    from .models import Cart
    cart = None
    if request.user.is_authenticated:
        try:
            # Get the cart linked to the user account
            cart = request.user.cart
            if not cart.is_active:
                cart = None
        except Cart.DoesNotExist:
            cart = None

        # Create a new cart if none exists
        if not cart:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key

            cart = Cart.objects.create(
                user=request.user,
                session_id=session_key,
                is_active=True
            )
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


def calculate_delivery_cost(total_quantity):
    """
    Calculate delivery cost based on total quantity of items in the cart.
    Uses the FEE_MAP defined in settings.
    """
    if total_quantity == 0:
        return Decimal('0.00')

    if total_quantity >= settings.FREE_DELIVERY_THRESHOLD:
        return Decimal('0.00')

    fee_map = settings.FEE_MAP

    fee = fee_map.get(total_quantity)

    if fee is not None:
        return Decimal(fee)

    if fee_map:
        max_tier_fee = fee_map.get(max(fee_map.keys()))
        return Decimal(max_tier_fee)

    return Decimal('0.00')

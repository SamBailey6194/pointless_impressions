from django.db import transaction
from pointless_impressions_src.cart.models import Cart
from .models import Order, OrderItem


# Write your utility functions here.
@transaction.atomic
def create_order_from_cart(cart: Cart, form_data: dict) -> Order:
    """
    Create an Order and associated OrderItems from the given Cart.

    This is called after payment is successfully processed during checkout.

    Args:
        cart (Cart): The shopping cart to convert into an order.
        form_data (dict): The validated checkout form data containing
                          user info, shipping address, payment details, etc.
    """
    new_order = Order.objects.create(
        user=cart.user,
        guest_email=form_data.get('email') if not cart.user else None,
        total_amount=cart.get_total_price(),
        shipping_address=form_data.get('shipping_address'),
        billing_address=form_data.get('billing_address'),
        status="Processing",
    )

    cart_items = cart.items.select_related(
        'artwork',
        'framing_condition',
        'artwork__artist',
        'artwork__main_photo',
    ).all()

    for cart_items in cart_items:
        image_url = None
        item_name = "Deleted Artwork"

        if cart_items.artwork:
            image_url = cart_items.artwork.image.url
            item_name = cart_items.artwork.name

        OrderItem.objects.create(
            order=new_order,
            artwork=cart_items.artwork,
            item_name=item_name,
            price_at_purchase=cart_items.artwork.price if
            cart_items.artwork
            else 0,
            framing_condition=cart_items.framing_condition.name if
            cart_items.framing_condition
            else "N/A",
            image_url_at_purchase=image_url,
            quantity=cart_items.quantity,
            notes=cart_items.notes,
        )

    cart.delete()

    return new_order

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

    Returns:
        Order: The created Order instance.
    """
    subtotal = cart.get_subtotal()
    delivery_fee = cart.get_delivery_cost()
    grand_total = cart.get_grand_total()

    new_order = Order.objects.create(
        user=cart.user,
        guest_email=form_data.get('email') if not cart.user else None,
        guest_phone=form_data.get('phone') if not cart.user else None,
        subtotal=subtotal,
        delivery_fee=delivery_fee,
        grand_total=grand_total,
        status="Processing",
        shipping_first_name=form_data['shipping_address'][
            'shipping_first_name'
            ],
        shipping_last_name=form_data['shipping_address']['shipping_last_name'],
        shipping_address_line_1=form_data['shipping_address'][
            'shipping_address_line_1'
        ],
        shipping_address_line_2=form_data['shipping_address'][
            'shipping_address_line_2'
        ],
        shipping_city=form_data['shipping_address']['shipping_city'],
        shipping_county=form_data['shipping_address']['shipping_county'],
        shipping_postcode=form_data['shipping_address']['shipping_postcode'],
        shipping_country=form_data['shipping_address']['shipping_country'],
        billing_first_name=form_data['billing_address']['billing_first_name'],
        billing_last_name=form_data['billing_address']['billing_last_name'],
        billing_address_line_1=form_data['billing_address'][
            'billing_address_line_1'
        ],
        billing_address_line_2=form_data['billing_address'][
            'billing_address_line_2'
        ],
        billing_city=form_data['billing_address']['billing_city'],
        billing_county=form_data['billing_address']['billing_county'],
        billing_postcode=form_data['billing_address']['billing_postcode'],
        billing_country=form_data['billing_address']['billing_country'],
    )

    cart_items_qs = cart.items.select_related(
        'artwork',
        'framing_condition',
        'artwork__artist',
        'artwork__main_photo',
    ).all()

    for items in cart_items_qs:
        image_url = None
        item_name = "Deleted Artwork"

        if items.artwork:
            image_url = items.artwork.image.url
            item_name = items.artwork.name

        OrderItem.objects.create(
            order=new_order,
            artwork=items.artwork,
            item_name=item_name,
            price_at_purchase=items.artwork.price if
            items.artwork
            else 0,
            framing_condition=items.framing_condition.condition_friendly_name
            if items.framing_condition else "N/A",
            image_url_at_purchase=image_url,
            quantity=items.quantity,
            notes=items.notes,
        )

    cart.delete()

    return new_order


def build_address_dict(addr: dict) -> dict:
    """
    Build a standardized address dictionary from the given address data.

    Args:
        addr (dict): Address data containing fields like first name, last name,
                     address lines, city, county, postcode, country.

    Returns:
        dict: A dictionary with standardized address fields.
    """
    return {
        'first_name': addr.get('shipping_first_name') or addr.get(
            'billing_first_name', ''
            ),
        'last_name': addr.get('shipping_last_name') or addr.get(
            'billing_last_name', ''
            ),
        'address_line_1': addr.get('shipping_address_line_1') or addr.get(
            'billing_address_line_1', ''
            ),
        'address_line_2': addr.get('shipping_address_line_2') or addr.get(
            'billing_address_line_2', ''
            ),
        'city': addr.get('shipping_city') or addr.get(
            'billing_city', ''
            ),
        'county': addr.get('shipping_county') or addr.get(
            'billing_county', ''
            ),
        'postcode': addr.get('shipping_postcode') or addr.get(
            'billing_postcode', ''
            ),
        'country': addr.get('shipping_country') or addr.get(
            'billing_country', ''
            ),
    }

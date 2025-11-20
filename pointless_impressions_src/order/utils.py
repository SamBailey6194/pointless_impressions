from django.db import transaction
from django.conf import settings
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.core.mail import send_mail
from pointless_impressions_src.cart.models import Cart
from .models import Order, OrderItem
from pointless_impressions_src.pointless_impressions.context_processors \
    import global_context


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


def send_order_confirmation_email(order):
    """
    Send an order confirmation email based on user type.
    """
    request = HttpRequest()
    context = {
        'order': order,
        'domain': settings.DOMAIN,
    }
    context.update(global_context(request))

    if order.user:
        # Authenticated user
        subject = "Your Email Verification Code"
        plain_message = (
            f"Hello {order.user.first_name},\n\nYour order number is: "
            f"{order.order_number}.\n\n"
            "You can see updates on your dashboard.\n"
            f"Click here: {order.get_authenticated_user_link()}\n\n"
            "Thank you!"
        )
        context.update({
            'user': order.user,
            'user_first_name': order.user.first_name,
            'dashboard_link': order.get_authenticated_user_link(),
        })
        html_message = render_to_string(
            'emails/order_confirmation_authenticated.html',
            context
        )
        recipient = order.user.email
    else:
        # Guest user
        subject = "Order Confirmation"
        guest_name = f"{order.shipping_first_name}"
        plain_message = (
            f"Hello {guest_name},\n\nYour order number is: "
            f"{order.order_number}.\n\n"
            "You can see updates here:.\n"
            f"{order.get_guest_user_link()}\n\n"
            "Thank you!"
        )
        context.update({
            'guest_name': guest_name,
            'guest_link': order.get_guest_user_link(),
        })
        html_message = render_to_string(
            'emails/order_confirmation_guest.html',
            context
        )
        recipient = order.guest_email

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [recipient]

    send_mail(
        subject,
        plain_message,
        from_email,
        recipient_list,
        html_message=html_message,
        fail_silently=False,
    )

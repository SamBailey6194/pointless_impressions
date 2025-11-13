from django.db import models
import uuid
import secrets
from django.conf import settings
from pointless_impressions_src.artwork.models import Artwork


# Create your models here.
# ----------------------------------
# Helper Functions
# ----------------------------------
def generate_order_number():
    """
    Generate a unique order number using UUID4.
    Format: ORD-XXXX where XXXX is an incrementing integer.
    """
    last_order = Order.objects.order_by('-created_at').last()
    if not last_order:
        return 'ORD-1001'

    last_id_int = int(last_order.order_number.split('-')[1])
    new_id_int = last_id_int + 1
    return f"ORD-{new_id_int}"


def generate_guest_access_code():
    """
    Generate a secure, random 16 character (could be more)
    alphanumeric code for guest access.
    This is unguessable and unique for each order.
    """
    return secrets.token_urlsafe(16)


# ----------------------------------
# Order Model
# ----------------------------------
class Order(models.Model):
    """
    Stores Order permanent records after checkout completion.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the order"
    )
    order_number = models.CharField(
        max_length=50,
        unique=True,
        default=generate_order_number,
        help_text="Unique order number"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        help_text="User who placed the order"
    )
    guest_email = models.EmailField(
        blank=True,
        null=True,
        help_text="Email of guest user (if applicable)"
    )
    guest_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Phone number of guest user (if applicable)"
    )
    guest_access_code = models.CharField(
        default=generate_guest_access_code,
        max_length=50,
        editable=False,
        unique=True,
        blank=True,
        null=True,
        help_text="Unique access code for guest users to view their order"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the order was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the order was last updated"
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0.00,
        help_text="Total amount for the order"
    )
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        help_text="Current status of the order"
    )
    shipping_address = models.TextField(
        help_text="Shipping address for the order",
        blank=True,
    )
    billing_address = models.TextField(
        help_text="Billing address for the order",
        blank=True,
    )
    staff_updated = models.BooleanField(
        default=False,
        help_text="Flag to indicate if staff updated the order"
    )
    staff_member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff_updated_orders',
        help_text="Staff member who updated the order"
    )
    staff_notes = models.TextField(
        blank=True,
        help_text="Notes added by staff regarding the order",
        max_length=2000,
        null=True
    )

    def save(self, *args, **kwargs):
        """Override save to ensure order number is set."""
        if not self.order_number:
            self.order_number = generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number} - {self.status}"


# ----------------------------------
# OrderItem Model
# ----------------------------------
class OrderItem(models.Model):
    """
    Represents individual items within an order.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        help_text="The order this item belongs to"
    )
    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_items',
        help_text="The artwork associated with this order item"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        help_text="Quantity of the artwork ordered"
    )
    item_name = models.CharField(
        max_length=255,
        default='',
        help_text="Name of the artwork at the time of purchase"
    )
    notes = models.TextField(
        blank=True,
        help_text="Additional notes for this order item"
    )
    price_at_purchase = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price of the artwork at the time of purchase"
    )
    framing_condition = models.CharField(
        max_length=255,
        blank=True,
        help_text="Framing condition selected for the artwork"
    )
    image_url_at_purchase = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
        help_text="URL of the artwork image at the time of purchase"
    )

    def __str__(self):
        return (
            f"OrderItem {self.item_name} "
            f"(x{self.quantity}) in Order {self.order.order_number}"
            )

    def get_total_price(self):
        """Calculate total price for this order item."""
        return self.price_at_purchase * self.quantity

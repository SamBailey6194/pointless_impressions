from django.db import models
from django.conf import settings
from django.utils import timezone
from pointless_impressions_src.artwork.models import (
    Artwork, ArtworkFramingCondition
    )
import uuid
from datetime import timedelta


# Write your models here.
class Cart(models.Model):
    """
    Shopping cart model for storing user's cart data.

    Each user/guest gets a cart identified by UUID.
    Supports both authenticated users and anonymous guests.

    Attributes:
        uuid: Unique identifier for the cart (for anonymous users)
        user: Foreign key to User (for authenticated users, nullable)
        created_at: Timestamp when cart was created
        updated_at: Timestamp when cart was last modified
        expires_at: Timestamp when cart will be deleted (30 days from update)
        is_active: Boolean flag to mark cart as active/inactive

    Usage:
        - Authenticated users: cart.user is set
        - Anonymous users: cart.uuid is used, no user set
        - Cart persists for 30 days from last update
        - Survives private browsing by storing UUID in cookies
    """
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        db_index=True,
        help_text="Unique identifier for cart (used for anonymous users)"
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='cart',
        help_text="Associated user (null for anonymous carts)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When cart was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When cart was last modified"
    )
    expires_at = models.DateTimeField(
        help_text="When cart will expire (30 days from update)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether cart is active"
    )

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['uuid']),
            models.Index(fields=['user']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        return f"Cart {self.uuid}"

    def save(self, *args, **kwargs):
        """Override save to set expires_at on update"""
        if not self.id:  # New cart
            self.expires_at = timezone.now() + timedelta(days=30)
        else:  # Existing cart
            self.expires_at = timezone.now() + timedelta(days=30)
        super().save(*args, **kwargs)

    def get_total_items(self):
        """Get total quantity of items in cart"""
        return sum(item.quantity for item in self.items.all())

    def get_total_price(self):
        """Get total price of all items in cart"""
        return sum(
            float(item.artwork.price) * item.quantity
            for item in self.items.all()
        )

    def get_cart_items_list(self):
        """Get cart items as list of dicts (for API responses)"""
        items = []
        for item in self.items.all():
            items.append({
                'id': item.artwork.id,
                'name': item.artwork.name,
                'price': float(item.artwork.price),
                'quantity': item.quantity,
                'slug': item.artwork.slug,
                'framing_option': item.framing_option,
                'notes': item.notes,
                'total': float(item.artwork.price) * item.quantity,
            })
        return items

    @classmethod
    def get_or_create_from_uuid(cls, cart_uuid):
        """
        Get cart by UUID or create new one if it doesn't exist.

        Args:
            cart_uuid: UUID string or object

        Returns:
            Tuple of (cart, created) like get_or_create
        """
        try:
            uuid_obj = uuid.UUID(str(cart_uuid))
            cart, created = cls.objects.get_or_create(
                uuid=uuid_obj,
                defaults={'is_active': True}
            )
            return cart, created
        except (ValueError, TypeError):
            return None, False


class CartItem(models.Model):
    """
    Individual item in a shopping cart.

    Each CartItem represents one artwork in a cart with its quantity
    and optional customization options.

    Attributes:
        cart: Foreign key to Cart
        artwork: Foreign key to Artwork
        quantity: Number of units
        framing_option: Selected framing condition (optional)
        notes: Special requests or notes (optional)
        created_at: When item was added to cart
        updated_at: When item was last updated

    Usage:
        item = CartItem.objects.create(
            cart=cart,
            artwork=artwork,
            quantity=1,
            framing_option="Framed",
            notes="Gift wrap this"
        )
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        help_text="Parent cart"
    )
    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.CASCADE,
        related_name='cart_items',
        help_text="Artwork in cart"
    )
    framing_condition = models.ForeignKey(
        ArtworkFramingCondition,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cart_items',
        help_text="Selected framing condition from artwork's "
        "selected_conditions"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        help_text="Number of units"
    )
    notes = models.TextField(
        blank=True,
        help_text="Special requests or notes (max 500 chars)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When item was added to cart"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When item was last updated"
    )

    class Meta:
        unique_together = ('cart', 'artwork')
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['cart']),
            models.Index(fields=['artwork']),
        ]

    def __str__(self):
        return f"{self.artwork.name} x{self.quantity} in {self.cart}"

    def get_total(self):
        """Get total price for this line item"""
        return float(self.artwork.price) * self.quantity

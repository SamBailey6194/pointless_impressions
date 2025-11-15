from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import F, Sum, ExpressionWrapper, DecimalField
from datetime import timedelta
from decimal import Decimal
from pointless_impressions_src.artwork.models import (
    Artwork, ArtworkFramingCondition
    )


# Write your models here.
class Cart(models.Model):
    """
    Shopping cart model for storing user's cart data.

    Each user/guest gets a cart identified by UUID.
    Supports both authenticated users and anonymous guests.

    Attributes:
        session_id: Unique identifier for the cart (for anonymous users)
        user: Foreign key to User (for authenticated users, nullable)
        created_at: Timestamp when cart was created
        updated_at: Timestamp when cart was last modified
        expires_at: Timestamp when cart will be deleted (30 days from update)
        is_active: Boolean flag to mark cart as active/inactive
        data: JSON object to store cart data

    Usage:
        - Authenticated users: cart.user is set
        - Anonymous users: cart.session_id is used, no user set
        - Cart persists for 30 days from last update
        - Survives private browsing by storing session_id in cookies
    """
    session_id = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text="Unique identifier for cart (used for anonymous users)"
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
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
            models.Index(fields=['session_id']),
            models.Index(fields=['user']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        return f"Cart {self.session_id}"

    def save(self, *args, **kwargs):
        """
        Override save to set expires_at on update.
        Ensure session_id is set and data is a valid JSON object.
        """
        self.expires_at = timezone.now() + timedelta(days=30)

        super().save(*args, **kwargs)

    @classmethod
    def get_or_create_from_sessionid(cls, session_id):
        """
        Use session_id to get or create cart.
        session_id is used to uniquely identify the cart.
        """
        cart, created = cls.objects.get_or_create(
            session_id=session_id,
            defaults={
                'is_active': True,
                'expires_at': timezone.now() + timedelta(days=30)
            }
        )
        return cart, created

    def add_or_update_item(
            self,
            artwork,
            quantity,
            framing_condition=None,
            notes='',
            replace_quantity=False
            ):
        """
        Add or update an item in the cart.

        :param artwork: Artwork object to add or update
        :param quantity: Quantity to add or replace
        :param framing_condition: Framing option for the artwork
        :param notes: Additional notes for the item
        :param replace_quantity: If True, replace the existing quantity
        """
        try:
            quantity = int(quantity)
            if quantity < 1:
                quantity = 1
        except (ValueError, TypeError):
            return None, False

        lookup_fields = {
            'cart': self,
            'artwork': artwork,
            'framing_condition': framing_condition,
        }

        item, created = CartItem.objects.get_or_create(
            **lookup_fields,
            defaults={
                'quantity': 0,
            }
        )

        if quantity == 0:
            print(
                "Quantity is 0. Deleting item immediately..."
            )  # Debugging log
            item.delete()
            self.save()
            return None, created

        if replace_quantity:
            item.quantity = quantity  # Replace the quantity directly
        else:
            item.quantity = (
                F('quantity') + quantity  # Add to the existing quantity
            )

        if created or notes:
            item.notes = notes

        item.save()
        print(
            f"Item saved. Quantity in memory: {item.quantity}"
        )

        item.refresh_from_db()
        print(
            f"Item refreshed. Quantity in database: {item.quantity}"
        )

        if item.quantity <= 0:
            print(f"Deleting item: {item}")
            item.delete()
            item = None
            print("Item deleted successfully.")

        self.save()

        return item, created

    def get_total_quantity(self):
        """Get total quantity of items in the cart"""
        total = self.items.aggregate(
            cart_quantity=Sum('quantity')
        )
        return total['cart_quantity'] or 0

    def get_subtotal(self):
        """Get total price of all items in the cart"""
        total = self.items.annotate(
            line_item_total=ExpressionWrapper(
                F('artwork__price') * F('quantity'),
                output_field=DecimalField(
                    max_digits=10, decimal_places=2
                )
                )
        ).aggregate(
            cart_total=Sum('line_item_total')
        )
        return total['cart_total'] or Decimal('0.00')

    def get_delivery_cost(self):
        """Get delivery cost based on total price and defined tiers"""
        from .utils import calculate_delivery_cost
        quantity = self.get_total_quantity()

        return calculate_delivery_cost(quantity)

    def get_grand_total(self):
        """Get grand total including delivery cost"""
        subtotal = self.get_subtotal()
        delivery_cost = self.get_delivery_cost()

        return subtotal + delivery_cost


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
        on_delete=models.SET_NULL,
        null=True,
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
        unique_together = ('cart', 'artwork', 'framing_condition')
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['cart']),
            models.Index(fields=['artwork']),
            models.Index(fields=['framing_condition']),
        ]

    def __str__(self):
        return f"{self.artwork.name} x{self.quantity} in {self.cart}"

    def get_total(self):
        """Get total price for this line item"""
        return float(self.artwork.price) * self.quantity

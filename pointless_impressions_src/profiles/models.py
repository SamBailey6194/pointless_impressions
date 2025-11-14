from django.db import models
from django.conf import settings
from pointless_impressions_src.photo.models import Photo


# Create your models here.
class UserProfile(models.Model):
    """
    A universal profile for every user.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='userprofile'
    )

    profile_picture = models.OneToOneField(
        Photo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_profile'
    )

    def __str__(self):
        return f"Profile for {self.user.username}"


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_profile'
    )

    def __str__(self):
        return f"Customer: {self.user.username}"


class Artist(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='artist_profile'
    )
    bio = models.TextField(blank=True)
    portfolio_url = models.URLField(blank=True)
    social_links = models.JSONField(blank=True, default=dict)

    def __str__(self):
        return f"Artist: {self.user.username}"


class Address(models.Model):
    """
    Stores a shipping or billing address for a Customer.
    A Customer can have multiple addresses.
    """
    class AddressType(models.TextChoices):
        SHIPPING = 'SHIPPING', 'Shipping'
        BILLING = 'BILLING', 'Billing'

    label = models.CharField(
        max_length=50,
        blank=True,
        help_text="Label for the address (e.g., Home, Work)"
        )
    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        related_name='addresses'
    )
    address_type = models.CharField(
        max_length=10,
        choices=AddressType.choices,
        default=AddressType.SHIPPING
    )
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer.user.username} - {self.label} Address"


class PaymentInfo(models.Model):
    """
    Stores a tokenized payment method for a Customer.
    A Customer can have multiple cards.
    """
    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        related_name='payment_methods'
    )
    processor_customer_id = models.CharField(max_length=255)
    payment_method_id = models.CharField(max_length=255, unique=True)
    brand = models.CharField(max_length=50)
    last_four_digits = models.CharField(max_length=4)
    expiry_month = models.PositiveSmallIntegerField()
    expiry_year = models.PositiveSmallIntegerField()
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"{self.customer.user.username} - {self.brand} **** "
            f"{self.last_four_digits}"
            )


class BankDetails(models.Model):
    """
    Stores the bank account information for an Artist to receive payouts.
    """
    artist = models.OneToOneField(
        'Artist',
        on_delete=models.CASCADE,
        related_name='bank_details'
    )
    account_holder_name = models.CharField(max_length=255)
    sort_code = models.CharField(max_length=10, blank=True)
    account_number = models.CharField(max_length=20, blank=True)
    iban = models.CharField("IBAN", max_length=34, blank=True)
    swift_bic = models.CharField("SWIFT/BIC", max_length=11, blank=True)
    billing_address_line_1 = models.CharField(max_length=255)
    billing_address_line_2 = models.CharField(
        max_length=255,
        blank=True,
        null=True
        )
    billing_city = models.CharField(max_length=100)
    billing_county = models.CharField(max_length=100, blank=True)
    billing_postcode = models.CharField(max_length=20)
    billing_country = models.CharField(max_length=100)

    def __str__(self):
        return f"Bank Details for {self.artist.user.username}"

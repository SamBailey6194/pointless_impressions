from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from pointless_impressions_src.photo.models import Photo


# Create your models here.
class UserProfile(models.Model):
    """
    A universal profile for every user.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_profile'
    )

    profile_picture = models.OneToOneField(
        Photo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_profile_picture'
    )

    def __str__(self):
        return f"Profile for {self.user.username}"


class Customer(models.Model):
    user_profile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='customer'
    )

    def __str__(self):
        return f"Customer: {self.user_profile.user.username}"


class Artist(models.Model):
    user_profile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='artist'
    )
    bio = models.TextField(blank=True)
    portfolio_url = models.URLField(blank=True, null=True)
    social_links = models.JSONField(blank=True, null=True, default=dict)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        'StaffRole',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_artists'
    )

    def approval_info(self):
        if self.is_approved and self.approved_by:
            approver = (
                self.approved_by.user_profile.user.username
                if self.approved_by else "Unknown"
            )
            return f"Approved by {approver}"
        elif self.is_approved:
            return "Approved"
        return "Not Approved"

    approval_info.short_description = 'Approval Info'

    def __str__(self):
        return (
            f"Artist: {self.user_profile.user.username} "
            f"{self.approval_info()}"
            )


class StaffRole(models.Model):
    """
    Represents a staff role assigned to a user.
    They curate the artwork and blogs on the platform.
    """
    class RoleChoices(models.TextChoices):
        OWNER = 'OWNER', 'Owner'
        MANAGER = 'MANAGER', 'Manager'
        EMPLOYEE = 'EMPLOYEE', 'Employee'

    user_profile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='staff_role'
    )
    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices
    )
    role_friendly_name = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.role}"

    def save(self, *args, **kwargs):
        if not self.role_friendly_name:
            self.role_friendly_name = self.get_role_display()
        super().save(*args, **kwargs)
        group, created = Group.objects.get_or_create(name=self.role)
        self.user_profile.user.groups.add(group)


class Address(models.Model):
    """
    Stores a shipping or billing address for a Customer.
    A Customer can have multiple addresses.
    """
    class AddressType(models.TextChoices):
        SHIPPING = 'SHIPPING', 'Shipping'
        BILLING = 'BILLING', 'Billing'

    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='addresses'
    )
    label = models.CharField(
        max_length=50,
        blank=True,
        help_text="Label for the address (e.g., Home, Work)"
        )
    address_type = models.CharField(
        max_length=10,
        choices=AddressType.choices,
        default=AddressType.SHIPPING
    )
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    address_line_1 = models.CharField(max_length=255, blank=False, null=False)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=False, null=False)
    county = models.CharField(max_length=100, blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=False, null=False)
    country = models.CharField(max_length=100, blank=False, null=False)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"{self.customer.user_profile.user.username} - "
            f"{self.label} Address"
            )


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
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='billing_payment_addresses'
    )

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
        Artist,
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

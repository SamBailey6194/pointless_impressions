from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.conf import settings
from pointless_impressions_src.account.models import CustomUser
from .models import UserProfile, Customer, StaffRole


# Write your signals here.
@receiver(post_save, sender=StaffRole)
def create_user_profile_and_customer_for_staff(
    sender,
    instance,
    created,
    **kwargs
):
    """Ensure UserProfile and Customer exist when StaffRole is created."""
    if getattr(settings, "DISABLE_SIGNALS", False):
        return

    if created:
        user_profile, _ = UserProfile.objects.get_or_create(
            user=instance.user_profile.user
        )
        Customer.objects.get_or_create(user_profile=user_profile)


@receiver(m2m_changed, sender=CustomUser.groups.through)
def ensure_user_profile_and_customer_on_group_change(
    sender,
    instance,
    action,
    pk_set,
    **kwargs
):
    """Ensure UserProfile and Customer exist when user groups change."""
    if getattr(settings, "DISABLE_SIGNALS", False):
        return

    if action in ["post_add", "post_remove", "post_clear"]:
        user_profile, _ = UserProfile.objects.get_or_create(user=instance)
        Customer.objects.get_or_create(user_profile=user_profile)

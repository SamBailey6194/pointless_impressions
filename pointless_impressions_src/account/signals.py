from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EmailVerificationCode, CustomUser
import random


# Write your signals here.
@receiver(post_save, sender=CustomUser)
def create_verification_code(sender, instance, created, **kwargs):
    """Create an email verification code when a new user is created."""
    if created:
        while True:
            code = f"{random.randint(0, 999999):06d}"
            if not EmailVerificationCode.objects.filter(code=code).exists():
                break

        EmailVerificationCode.objects.create(user=instance, code=code)

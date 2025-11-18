from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from .utils import send_verification_email, generate_verification_code


# Write your signals here.
@receiver(post_save, sender=CustomUser)
def create_verification_code(sender, instance, created, **kwargs):
    """
    Create an email verification code and send it when a new user is created.
    """
    if created:
        # Generate a unique 6-digit code
        generate_verification_code(instance)

        # Send the verification email
        send_verification_email(instance)

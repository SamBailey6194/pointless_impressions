from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpRequest
import random
from .models import EmailVerificationCode
from pointless_impressions_src.pointless_impressions.context_processors \
    import global_context


def generate_verification_code(user):
    """
    Generate a new verification code for a user and delete old unused ones.

    Args:
        user (CustomUser): The user to generate a code for.

    Returns:
        EmailVerificationCode: The newly created verification code object.
    """
    EmailVerificationCode.objects.filter(user=user, is_used=False).delete()

    while True:
        code = f"{random.randint(0, 999999):06d}"
        if not EmailVerificationCode.objects.filter(code=code).exists():
            break

    return EmailVerificationCode.objects.create(user=user, code=code)


def send_verification_email(user):
    """
    Sends the existing verification code to the user's email with branding.

    Args:
        user (CustomUser): The user to whom the email will be sent.
    """
    # Retrieve the latest verification code for the user
    verification_code = user.email_verification_codes.latest('created_at')

    request = HttpRequest()
    request.user = user

    context = {
        'user': user,
        'user_first_name': user.first_name,  # Pass first name explicitly
        'verification_code': verification_code.code,
    }
    context.update(global_context(request))

    # Render the HTML email template
    subject = "Your Email Verification Code"
    plain_message = (
        f"Hello {user.first_name},\n\nYour email verification code is: "
        f"{verification_code.code}.\n\n"
        "Please use this code to verify your email address.\n\n"
        "Thank you!"
    )
    html_message = render_to_string(
        'emails/verification_email.html',
        context
    )

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(
        subject,
        plain_message,
        from_email,
        recipient_list,
        html_message=html_message
    )


def send_email_verified_confirmation(user):
    """
    Sends an email confirmation to the user after their email is verified.

    Args:
        user (CustomUser): The user to whom the email will be sent.
    """
    request = HttpRequest()
    request.user = user

    context = {
        'user': user,
        'user_first_name': user.first_name,
    }
    context.update(global_context(request))

    # Render the HTML email template
    subject = "Your Email Has Been Verified!"
    plain_message = (
        f"Hello {user.first_name},\n\n"
        "Your email has been successfully verified. "
        "You can now enjoy all the features of our platform.\n\n"
        "Thank you for being a part of our community!"
    )
    html_message = render_to_string(
        'emails/email_verified_confirmation.html',
        context
    )

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(
        subject,
        plain_message,
        from_email,
        recipient_list,
        html_message=html_message
    )

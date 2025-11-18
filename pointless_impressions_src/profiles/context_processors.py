from .models import (
    Customer, Artist, StaffRole
)
from .forms import LoginForm, LogoutForm, EmailVerificationForm


# Write your context processors here.
def global_profiles_context(request):
    """
    Adds global profile-related context variables to all templates.
    - 'all_artists': A queryset of all active artists (for public lists).
    - 'current_user_customer_profile': The current user's Customer object
    (or None).
    - 'current_user_artist_profile': The current user's Artist object
    (or None).
    - 'current_user_staff_roles': A list of the current user's staff role
    (or None).
    """
    context = {
        # This is for public lists (e.g., gallery filter), so it's OK.
        'all_artists': Artist.objects.select_related(
            'user_profile__user'
        ).filter(
            user_profile__user__is_active=True
        ).order_by('user_profile__user__username'),

        # --- Provide context for the CURRENT user ---
        'current_user_customer_profile': None,
        'current_user_artist_profile': None,
        'current_user_staff_role': None,
    }

    # Only check roles for authenticated users with a profile
    if request.user.is_authenticated and hasattr(request.user, 'user_profile'):
        user_profile = request.user.user_profile

        try:
            context['current_user_customer_profile'] = user_profile.customer
        except Customer.DoesNotExist:
            pass

        try:
            context['current_user_artist_profile'] = user_profile.artist
        except Artist.DoesNotExist:
            pass

        try:
            context['current_user_staff_role'] = user_profile.staff_role
        except StaffRole.DoesNotExist:
            pass

    return context


def auth_forms(request):
    """
    Adds authentication forms to the context for all templates.
    """
    return {
        'login_form': LoginForm(),
        'logout_form': LogoutForm(),
        'email_verification_form': EmailVerificationForm(),
    }

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


# Mixins for role-based access control
class CustomerRequiredMixin(UserPassesTestMixin):
    """
    Checks if the user is authenticated and has a customer profile.
    """
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        try:
            return bool(self.request.user.user_profile.customer)
        except Exception:
            return False

    def handle_no_permission(self):
        raise PermissionDenied("This view is for customers only.")


class ArtistRequiredMixin(UserPassesTestMixin):
    """
    Checks if the user is authenticated and has an artist profile.
    """
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        return hasattr(self.request.user, 'artist_profile')

    def handle_no_permission(self):
        raise PermissionDenied("This view is for artists only.")

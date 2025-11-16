from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages


# Mixins for role-based access control
class CustomerRequiredMixin(UserPassesTestMixin):
    """
    Checks if the user is authenticated and has a customer profile.
    """
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        return hasattr(self.request.user, 'customer_profile')

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


class StaffRequiredMixin(UserPassesTestMixin):
    """
    Checks if the user is authenticated and has a staff role.
    """
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        return hasattr(self.request.user, 'staff_role')

    def handle_no_permission(self):
        raise PermissionDenied("This view is for staff members only.")


class BankDetailsRequiredMixin(ArtistRequiredMixin):
    """
    Checks that an Artist has provided their bank details.
    """
    def test_func(self):
        if not super().test_func():
            return False

        return hasattr(self.request.user.artist_profile, 'bank_details')

    def handle_no_permission(self):
        messages.warning(
            self.request,
            "Please add your bank details before you can list artwork."
            )
        return redirect('profile:artist-dashboard')

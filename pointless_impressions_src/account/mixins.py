from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


# Mixins for role-based access control
class AnonymousRequiredMixin(UserPassesTestMixin):
    """
    Prevents logged-in users from accessing a view (e.g., login/signup page).
    """
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('home')


class EmailNotVerifiedMixin(UserPassesTestMixin):
    """
    Ensures that the user's email is not verified to access certain views.
    """
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        return not self.request.user.profile.is_email_verified

    def handle_no_permission(self):
        return redirect('home')

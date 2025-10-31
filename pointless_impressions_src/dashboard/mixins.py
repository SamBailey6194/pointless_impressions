from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


# Mixins for role-based access control
class StaffRequiredMixin(UserPassesTestMixin):
    """
    Checks if the user is authenticated and is a staff member.
    """
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        allowed_groups = ['Employee', 'Manager', 'Owner']
        has_group = (
            self.request.user.groups.filter(name__in=allowed_groups).exists()
            )

        return has_group

    def handle_no_permission(self):
        raise PermissionDenied(
            "You do not have permissions to view the dashboard"
            )


class OwnerRequiredMixin(UserPassesTestMixin):
    """
    Checks if the user is authenticated and is an owner.
    """
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        return self.request.user.groups.filter(name='Owner').exists()

    def handle_no_permission(self):
        raise PermissionDenied("This view is for owners only.")


class ManagerRequiredMixin(UserPassesTestMixin):
    """
    Checks if the user is authenticated and is a manager or owner.
    """
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        allowed_groups = ['Manager', 'Owner']
        has_group = (
            self.request.user.groups.filter(name__in=allowed_groups).exists()
            )

        return has_group

    def handle_no_permission(self):
        raise PermissionDenied("This view is for managers only.")

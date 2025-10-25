from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


# Mixins for role-based access control
# These mixins can be used in class-based views to restrict access
# based on user roles defined in the CustomUser model.
class OwnerRequiredMixin(UserPassesTestMixin):
    """Only owners can access this dashboard view."""
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_owner

    def handle_no_permission(self):
        raise PermissionDenied("Only owners can access this view.")


class ManagerRequiredMixin(UserPassesTestMixin):
    """Managers and above (owners) can access."""
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_manager or user.is_owner)

    def handle_no_permission(self):
        raise PermissionDenied("Only managers and owners can access this view.")


class CustomerRequiredM
class EmployeeRequiredMixin(UserPassesTestMixin):
    """Employees and above (managers, owners) can access."""
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_employee or user.is_manager or user.is_owner)

    def handle_no_permission(self):
        raise PermissionDenied("Only employees, managers, and owners can access this view.")


class CustomerRequiredMixin(UserPassesTestMixin):
    """Customers and above (employees, managers, owners) can access."""
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_customer or user.is_employee or user.is_manager or user.is_owner)

    def handle_no_permission(self):
        raise PermissionDenied("Only authenticated users can access this view.")

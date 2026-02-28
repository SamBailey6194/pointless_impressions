from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render


# Mixins for role-based access control
class AdminRequiredMixin(UserPassesTestMixin):
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

        public_id = self.kwargs.get('public_id')

        if public_id:
            url_public_id = str(public_id)
            user_public_id = str(self.request.user.public_id)

            if url_public_id != user_public_id:
                return False

        return has_group

    def handle_no_permission(self):
        return render(
            self.request,
            "403.html",
            {"message": "You do not have permissions to view the dashboard."},
            status=403,
        )


class OwnerRequiredMixin(AdminRequiredMixin):
    """
    Checks if the user is authenticated and is an owner.
    """
    def test_func(self):
        if not super().test_func():
            return False

        return self.request.user.groups.filter(name='Owner').exists()

    def handle_no_permission(self):
        raise PermissionDenied("This view is for owners only.")


class ManagerRequiredMixin(AdminRequiredMixin):
    """
    Checks if the user is authenticated and is a manager or owner.
    """
    def test_func(self):
        if not super().test_func():
            return False

        allowed_groups = ['Manager', 'Owner']
        has_group = (
            self.request.user.groups.filter(name__in=allowed_groups).exists()
            )

        return has_group

    def handle_no_permission(self):
        raise PermissionDenied("This view is for managers only.")

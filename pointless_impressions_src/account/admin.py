from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin panel configuration for CustomUser model."""
    model = CustomUser
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_superuser",
        "is_staff",
        "is_owner",
        "is_manager",
        "is_employee",
        "is_customer",
        "is_active",
    )
    list_filter = (
        "is_superuser",
        "is_staff",
        "is_owner",
        "is_manager",
        "is_employee",
        "is_customer",
        "is_active",
    )
    fieldsets = (None, {'fields': ('username', 'email', 'password')}),
    add_fieldsets = (
        None,
        {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
                'is_superuser',
                'is_staff',
                'is_owner',
                'is_manager',
                'is_employee',
                'is_customer',
                'is_active',
            )
        },
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

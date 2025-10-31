from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from pointless_impressions_src.profiles.admin import (
    CustomerInline, ArtistInline
    )


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin panel configuration for CustomUser model."""
    model = CustomUser

    inlines = (CustomerInline, ArtistInline)

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_superuser",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "is_superuser",
        "is_staff",
        "is_active",
    )

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        None,
        {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
            )
        },
    )

    search_fields = ('username', 'email')
    ordering = ('username',)

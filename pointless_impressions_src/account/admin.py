from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, EmailVerificationCode


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
        ('Permissions', {'fields': (
            'is_superuser',
            'is_staff',
            'is_active',
            )}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        None,
        {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'phone',
                'password1',
                'password2',
            )
        },
    )

    search_fields = ('username', 'email')
    ordering = ('username',)


@admin.register(EmailVerificationCode)
class EmailVerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'is_used')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__username', 'code')
    readonly_fields = ('user', 'code', 'created_at', 'is_used')

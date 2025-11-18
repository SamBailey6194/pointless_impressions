from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import CustomUser, EmailVerificationCode
from pointless_impressions_src.home.fields import CustomPhoneField
# 1. Import your existing SignupForm
from pointless_impressions_src.profiles.forms import SignupForm


# 2. This form will be used when EDITING a user
class CustomUserChangeForm(forms.ModelForm):
    """Form for editing a user in the admin."""
    phone = CustomPhoneField(required=True)

    class Meta:
        model = CustomUser
        fields = '__all__'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin panel configuration for CustomUser model.
    """
    add_form = SignupForm

    form = CustomUserChangeForm

    model = CustomUser

    list_display = (
        "username",
        "email",
        "phone",
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
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Permissions', {'fields': (
            'is_superuser',
            'is_staff',
            'is_active',
            )}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username',
                    'first_name',
                    'last_name',
                    'email',
                    'phone',
                    'password1',
                    'password2',
                )
            },
        ),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)


@admin.register(EmailVerificationCode)
class EmailVerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'is_used')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__username', 'code')
    readonly_fields = ('user', 'code', 'created_at', 'is_used')

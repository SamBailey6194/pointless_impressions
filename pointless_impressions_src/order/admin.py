from django.contrib import admin
from django import forms
from .models import Order
from pointless_impressions_src.home.fields import CustomPhoneField


# Register your models here.
class CustomUserAdminForm(forms.ModelForm):
    phone = CustomPhoneField(required=True)

    class Meta:
        model = Order
        fields = '__all__'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 'user', 'guest_email',
        'status', 'created_at', 'grand_total'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'user__username', 'guest_email')
    readonly_fields = (
        'order_number', 'created_at',
        'updated_at', 'guest_access_code'
    )

    fieldsets = (
        (None, {
            'fields': (
                'order_number', 'user', 'guest_email', 'guest_phone',
                'guest_access_code', 'status'
            )
        }),
        ('Shipping Information', {
            'fields': (
                'shipping_first_name', 'shipping_last_name',
                'shipping_address_line_1', 'shipping_address_line_2',
                'shipping_city', 'shipping_county', 'shipping_postcode',
                'shipping_country'
            )
        }),
        ('Billing Information', {
            'fields': (
                'billing_first_name', 'billing_last_name',
                'billing_address_line_1', 'billing_address_line_2',
                'billing_city', 'billing_county', 'billing_postcode',
                'billing_country'
            )
        }),
        ('Financials', {
            'fields': ('delivery_fee', 'subtotal', 'grand_total')
        }),
        ('Staff Notes', {
            'fields': ('staff_updated', 'staff_member', 'staff_notes')
        }),
    )

    def has_delete_permission(self, request, obj=None):
        """
        Prevent deletion of orders via the admin interface.
        """
        return False

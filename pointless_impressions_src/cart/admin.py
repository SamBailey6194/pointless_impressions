from django.contrib import admin
from .models import Cart, CartItem


# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'session_id',
        'is_active',
        'created_at',
        'updated_at',
        'expires_at'
        )
    list_filter = (
        'is_active',
        'created_at',
        'updated_at',
        'expires_at'
        )
    search_fields = ('user__username', 'session_id')
    ordering = ('-updated_at',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cart',
        'artwork',
        'quantity',
        'framing_condition',
        'created_at',
        'updated_at'
        )
    list_filter = ('created_at', 'updated_at')
    search_fields = ('cart__session_id', 'artwork__title')
    ordering = ('-updated_at',)

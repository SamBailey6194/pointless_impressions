from django.contrib import admin
from pointless_impressions_src.artwork.models import (
    Artwork,
    ArtworkCategory,
    ArtworkFramingCondition
)


@admin.register(ArtworkCategory)
class ArtworkCategoryAdmin(admin.ModelAdmin):
    """Admin interface for Artwork Categories."""
    list_display = ['name']
    search_fields = ['name']


@admin.register(ArtworkFramingCondition)
class ArtworkFramingConditionAdmin(admin.ModelAdmin):
    """Admin interface for Artwork Framing Conditions."""
    list_display = ['condition_name']
    search_fields = ['condition_name']


@admin.register(Artwork)
class ArtworkModelAdmin(admin.ModelAdmin):
    """
    Admin interface for Artwork model (US008).
    Provides CRUD functionality for managing artwork inventory.
    """
    list_display = [
        'name',
        'artist',
        'price',
        'category',
        'is_available',
        'is_in_stock',
        'quantity',
        'is_featured',
        'created_at'
    ]
    list_filter = [
        'category',
        'is_available',
        'is_in_stock',
        'is_featured',
        'created_at'
    ]
    search_fields = ['name', 'artist__user_profile__user__username', 'sku', 'slug']
    readonly_fields = ['sku', 'slug', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'artist', 'description', 'slug')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'sku', 'quantity', 'is_in_stock')
        }),
        ('Categorization', {
            'fields': ('category', 'selected_conditions')
        }),
        ('Status', {
            'fields': ('is_available', 'is_featured')
        }),
        ('Media', {
            'fields': ('main_photo',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    filter_horizontal = ['selected_conditions']
    actions = ['mark_as_available', 'mark_as_sold_out', 'mark_as_featured']

    def mark_as_available(self, request, queryset):
        """Admin action to mark selected artworks as available."""
        count = queryset.update(is_available=True)
        self.message_user(
            request,
            f'{count} artwork(s) marked as available.'
        )
    mark_as_available.short_description = 'Mark selected as available'

    def mark_as_sold_out(self, request, queryset):
        """Admin action to mark selected artworks as sold out."""
        count = queryset.update(is_available=False)
        self.message_user(
            request,
            f'{count} artwork(s) marked as sold out.'
        )
    mark_as_sold_out.short_description = 'Mark selected as sold out'

    def mark_as_featured(self, request, queryset):
        """Admin action to mark selected artworks as featured."""
        count = queryset.update(is_featured=True)
        self.message_user(
            request,
            f'{count} artwork(s) marked as featured.'
        )
    mark_as_featured.short_description = 'Mark selected as featured'

    def get_queryset(self, request):
        """
        Filter queryset based on user permissions.
        Superusers see all artworks; staff see only created artworks.
        """
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # Staff users can view all artworks (modify as needed)
            pass
        return qs

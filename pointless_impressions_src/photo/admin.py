from django.contrib import admin
from pointless_impressions_src.photo.models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """
    Admin interface for Photo model.
    CRUD for artwork, profile, and site asset photos.
    """
    list_display = [
        'title',
        'get_photo_type_display',
        'get_parent_object',
        'uploaded_by',
        'uploaded_at',
        'has_image'
    ]
    list_filter = [
        'photo_type',
        'uploaded_at',
        'uploaded_by'
    ]
    search_fields = [
        'title',
        'description',
        'alt_text',
        'asset_identifier',
        'artwork__name'
    ]
    readonly_fields = [
        'uploaded_at',
        'get_image_preview',
        'get_photo_folder'
    ]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'alt_text')
        }),
        ('Photo Type & Assignment', {
            'fields': (
                'photo_type',
                'artwork',
                'asset_identifier'
            )
        }),
        ('Image Upload', {
            'fields': ('image', 'get_image_preview')
        }),
        ('Upload Information', {
            'fields': ('uploaded_by', 'uploaded_at'),
            'classes': ('collapse',)
        }),
        ('Cloudinary Details', {
            'fields': ('get_photo_folder',),
            'classes': ('collapse',)
        })
    )
    filter_horizontal = []

    def get_parent_object(self, obj):
        """Display the parent object this photo is linked to."""
        if obj.photo_type == 'artwork' and obj.artwork:
            return f"Artwork: {obj.artwork.name}"
        elif obj.photo_type == 'site_asset':
            return f"Site Asset: {obj.asset_identifier}"
        return "—"
    get_parent_object.short_description = 'Linked To'

    def has_image(self, obj):
        """Display whether image exists."""
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Image Present'

    def get_image_preview(self, obj):
        """Display a preview of the image if it exists."""
        if obj.image:
            if hasattr(obj.image, 'url'):
                return f'<img src="{obj.image.url}" width="200" />'
            else:
                return f'<img src="{obj.image}" width="200" />'
        return "—"
    get_image_preview.allow_tags = True
    get_image_preview.short_description = 'Image Preview'

    def get_photo_folder(self, obj):
        """Display the Cloudinary folder this photo uses."""
        return obj.get_folder()
    get_photo_folder.short_description = 'Cloudinary Folder'

    def save_model(self, request, obj, form, change):
        """Set the uploaded_by field to the current user if not already set."""
        if not obj.uploaded_by:
            obj.uploaded_by = request.user
        obj.clean()  # Run model validation
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        qs = super().get_queryset(request)
        return qs.select_related('artwork', 'uploaded_by')

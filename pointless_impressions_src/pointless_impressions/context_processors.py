from django.conf import settings
from django.utils.functional import lazy
from pointless_impressions_src.artwork.models import (
    ArtworkCategory, ArtworkFramingCondition
    )
# from pointless_impressions_src.blog.models import BlogCategory
from pointless_impressions_src.photo.models import Photo
from pointless_impressions_src.profiles.models import Artist


# Context processors to add global template variables
def global_context(request):
    """
    Adds global context variables to all templates.
    This replaces the separate environment and navbar_categories functions.
    """

    # --- Logo fetching logic ---
    try:
        site_logo = Photo.objects.get(
            asset_identifier='pointless_impressions_logo'
        )
    except Photo.DoesNotExist:
        site_logo = None

    try:
        site_logo_white_bg = Photo.objects.get(
            asset_identifier='pointless_impressions_logo_white_bg'
        )
    except Photo.DoesNotExist:
        site_logo_white_bg = None

    # --- Placeholder image logic ---
    try:
        placeholder_image = Photo.objects.get(
            asset_identifier='placeholder_image'
        )
    except Photo.DoesNotExist:
        placeholder_image = None

    # --- Dynamic image_to_render logic ---
    def resolve_image_to_render():
        if hasattr(request, 'resolver_match'):
            view_name = request.resolver_match.view_name
            if view_name.startswith('artwork:'):
                return site_logo_white_bg or placeholder_image
            elif view_name.startswith('blog:'):
                return site_logo or placeholder_image
            elif view_name.startswith('profiles:'):
                return placeholder_image
        return placeholder_image

    image_to_render = lazy(resolve_image_to_render, Photo)()

    # --- Return one single context dictionary ---
    return {
        # Production flag
        'production': settings.PRODUCTION,

        # navbar categories
        'artwork_categories': ArtworkCategory.objects.all(),
        'framing_options': ArtworkFramingCondition.objects.all(),
        # 'blog_categories': BlogCategory.objects.all(),
        'artists': Artist.objects.select_related('user').filter(
            user__is_active=True
        ).order_by('user__username'),

        # --- NEWLY ADDED ---
        'site_logo': site_logo,
        'site_logo_white_bg': site_logo_white_bg,
        'placeholder_image': placeholder_image,
        'image_to_render': image_to_render,
    }

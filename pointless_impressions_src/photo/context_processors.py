from .models import Photo


# Write your context processors here.
def site_assets(request):
    """Context processor to add site asset photos to the context."""
    context = {}
    try:
        logo = Photo.objects.get(
            photo_type='site_asset',
            asset_identifier='pointless_impressions_logo'
        )
        logo_white_bg = Photo.objects.get(
            photo_type='site_asset',
            asset_identifier='pointless_impressions_logo_white_bg'
        )
        context['site_logo_white_bg'] = logo_white_bg
        context['site_logo'] = logo
    except Photo.DoesNotExist:
        context['site_logo_white_bg'] = None
        context['site_logo'] = None

    return context

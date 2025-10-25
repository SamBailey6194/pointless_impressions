from .models import Photo


# Utility functions for photo handling
def get_site_asset(asset_identifier):
    """Get a site asset by its identifier."""
    photo = Photo.objects.filter(
        photo_type='site_asset',
        asset_identifier=asset_identifier
    ).first()
    return photo.get_image_url if photo else ''

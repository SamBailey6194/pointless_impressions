from django.conf import settings
from pointless_impressions_src.artwork.models import (
    ArtworkCategory, ArtworkFramingCondition
    )
# from pointless_impressions_src.blog.models import BlogCategory


# Context processors to add global template variables
def environment(request):
    """
    Adds a 'production' boolean to all templates.
    """
    return {
        'production': settings.PRODUCTION
    }


def navbar_categories(request):
    """
    Adds artwork categories to the context for navbar display.
    """
    artwork_categories = ArtworkCategory.objects.all()
    framing_options = ArtworkFramingCondition.objects.all()
    # blog_categories = BlogCategory.objects.all()
    return {
        'artwork_categories': artwork_categories,
        'framing_options': framing_options,
        # 'blog_categories': blog_categories,
    }

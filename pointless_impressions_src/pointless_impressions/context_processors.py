from django.conf import settings


# Context processor to add 'production' variable to templates
def environment(request):
    """
    Adds a 'production' boolean to all templates.
    """
    return {
        'production': settings.PRODUCTION
    }

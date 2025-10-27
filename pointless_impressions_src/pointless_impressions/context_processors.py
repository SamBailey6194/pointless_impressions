from django.conf import settings


# Context processors to add global template variables
def environment(request):
    """
    Adds a 'production' boolean to all templates.
    """
    return {
        'production': settings.PRODUCTION
    }

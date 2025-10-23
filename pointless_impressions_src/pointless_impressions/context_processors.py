from django.conf import settings


# Context processors to add global template variables
def environment(request):
    """
    Adds a 'production' boolean to all templates.
    """
    return {
        'production': settings.PRODUCTION
    }


def static_version(request):
    """
    Adds STATIC_VERSION to templates.
    """
    return {
        'STATIC_VERSION': getattr(settings, 'STATIC_VERSION', '1.0.0')
    }

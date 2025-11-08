"""
Behave environment configuration for Django test database.
This ensures Django ORM operations are properly committed to the test database.
"""
from django.test import Client
from django.conf import settings


def before_all(context):
    """Configure Django settings for Behave tests."""
    # Force DEBUG=True and PRODUCTION=False for test environment
    # Behave-Django sets DEBUG=False by default, but we need it True
    # for local image field support instead of Cloudinary
    settings.DEBUG = True
    settings.PRODUCTION = False


def before_scenario(context, scenario):
    """
    Set up test client for each scenario.
    Ensure we're using the test database.
    """
    # Force DEBUG=True and PRODUCTION=False for test environment
    # Behave-Django sets DEBUG=False by default, but we need it True
    settings.DEBUG = True
    settings.PRODUCTION = False

    if not hasattr(context, 'test_client'):
        context.test_client = Client()
    # Ensure we're in the test database
    from django.db import connections
    for conn in connections.all():
        conn.close()

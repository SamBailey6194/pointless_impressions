"""
Behave environment configuration for Django test database.
This ensures Django ORM operations are properly committed to the test database.
"""
from django.test import Client
from django.db import connection


def before_scenario(context, scenario):
    """
    Set up test client for each scenario.
    Ensure we're using the test database.
    """
    if not hasattr(context, 'test_client'):
        context.test_client = Client()
    # Ensure we're in the test database
    from django.db import connections
    for conn in connections.all():
        conn.close()

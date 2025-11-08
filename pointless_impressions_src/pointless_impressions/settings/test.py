# test.py - Django settings for test database

import os
from .base import *

SECRET_KEY = "test-secret-key"

ENVIRONMENT = "development"
ALLOWED_HOSTS = ['*']
DEBUG = True
PRODUCTION = False

# Use SQLite in-memory database for fast, isolated tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'test_db.sqlite3'),
        'TEST': {
            'NAME': os.path.join(os.path.dirname(__file__), 'test_db.sqlite3'),
        },
    }
}

# Optional: Speed up password hashing for tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Optional: Disable debug toolbar and other dev-only apps
INSTALLED_APPS = [
    app for app in INSTALLED_APPS if app != 'debug_toolbar'
]

# Optional: Reduce logging noise
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'level': 'WARNING',
        },
    },
}

# Force DEBUG and PRODUCTION for test environment
# This ensures image handling uses local ImageField, not Cloudinary
DEBUG = True
PRODUCTION = False

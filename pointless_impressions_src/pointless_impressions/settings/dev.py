"""
Django settings for development environment.
"""

from .base import *
import os

# Environment settings
ENVIRONMENT = "development"
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "dev-secret-key-change-in-production"
)
DEBUG = True
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "web",  # Docker service name
]
PRODUCTION = False

# Development-specific apps
INSTALLED_APPS += [
    "django_browser_reload",
]

# Development-specific middleware
MIDDLEWARE += [
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

# Database configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DEV_DB_NAME", "dev_db"),
        "USER": os.getenv("DEV_DB_USER", "dev_user"),
        "PASSWORD": os.getenv("DEV_DB_PASSWORD", "dev_pass"),
        "HOST": os.getenv("DEV_DB_HOST", "db_dev"),
        "PORT": os.getenv("DEV_DB_PORT", "5432"),
        "OPTIONS": {
            "connect_timeout": 10,
        },
        "CONN_MAX_AGE": 60,  # Connection pooling
    }
}

# Email configuration (using MailDev for development)
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = os.getenv("EMAIL_HOST", "maildev_dev")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 1025))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "False") == "True"
EMAIL_USE_SSL = False
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "dev@example.com")

# Development cache configuration
cache_url = os.getenv("CACHE_URL", "redis://redis_dev:6379/0")
if cache_url.startswith("redis://"):
    CACHES["default"]["LOCATION"] = cache_url
else:
    # Fallback to local memory cache
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake-dev",
        }
    }

# Use a simple static version for development
STATIC_VERSION = "dev"

# File storage (local filesystem for development)
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

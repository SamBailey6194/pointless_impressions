from .base import *
import os

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key")
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DEV_DB_NAME", "dev_db"),
        "USER": os.getenv("DEV_DB_USER", "dev_user"),
        "PASSWORD": os.getenv("DEV_DB_PASSWORD", "dev_pass"),
        "HOST": os.getenv("DEV_DB_HOST", "db_dev"),
        "PORT": os.getenv("DEV_DB_PORT", "5432"),
    }
}

EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "maildev")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 1025))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "False") == "True"
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "dev@example.com")

CACHE_URL = os.getenv("CACHE_URL", "redis://redis:6379/0")

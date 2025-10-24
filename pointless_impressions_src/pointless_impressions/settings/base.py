"""
Django settings for pointless_impressions project.

Base settings that are common across all environments.
Environment-specific settings should be in dev.py, staging.py, or production.py
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables
ENV_PATH = BASE_DIR
load_dotenv(os.path.join(ENV_PATH, ".env"))

# Environment flag - should be overridden in environment-specific settings
ENVIRONMENT = os.getenv("DJANGO_ENVIRONMENT", "development")

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    # Redis cache
    "django_redis",
    # Tailwind CSS integration
    "tailwind",
    # Storage backends
    "cloudinary",
    "storages",
]

LOCAL_APPS = [
    "pointless_impressions_src.pointless_impressions",
    "pointless_impressions_src.home",
    "pointless_impressions_src.theme",
    "pointless_impressions_src.artwork",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "csp.middleware.CSPMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Cache configuration (Redis)
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL", "redis://127.0.0.1:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 20,
                "retry_on_timeout": True,
            },
        },
        "KEY_PREFIX": "pointless_impressions",
        "TIMEOUT": 300,  # 5 minutes default timeout
    }
}

ROOT_URLCONF = "pointless_impressions_src.pointless_impressions.urls"

# Tailwind CSS
TAILWIND_APP_NAME = "pointless_impressions_src.theme"
TAILWIND_CSS_PATH = "css/styles.css"

# Session configuration
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "pointless_impressions.context_processors.environment",
                "pointless_impressions.context_processors.static_version",
            ],
        },
    },
]

WSGI_APPLICATION = "pointless_impressions_src.pointless_impressions.wsgi.application"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
        "OPTIONS": {
            "min_length": 8,
        }
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]

# Internationalization
LANGUAGE_CODE = "en-gb"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Default static version for cache busting
STATIC_VERSION = os.getenv("STATIC_VERSION", "1.0.0")

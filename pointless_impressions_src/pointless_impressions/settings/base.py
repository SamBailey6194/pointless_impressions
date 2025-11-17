"""
Django settings for pointless_impressions project.

Base settings that are common across all environments.
Environment-specific settings should be in dev.py, staging.py, or production.py
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import cloudinary

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables
ENV_PATH = BASE_DIR
load_dotenv(os.path.join(ENV_PATH, ".env"))

# Pull from environment (works with .env.dev locally or Heroku config vars)
_raw_hosts = os.getenv("ALLOWED_HOSTS", "localhost")
ALLOWED_HOSTS = [h.strip() for h in _raw_hosts.split(",") if h.strip()]

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
    "cloudinary_storage",
    # Testing tools
    "behave_django",
    # Form rendering
    "crispy_forms",
    "crispy_tailwind",
    # Phone Support
    "phonenumber_field",
]

LOCAL_APPS = [
    "pointless_impressions_src.pointless_impressions",
    "pointless_impressions_src.home",
    "pointless_impressions_src.theme",
    "pointless_impressions_src.artwork",
    "pointless_impressions_src.photo",
    "pointless_impressions_src.account",
    "pointless_impressions_src.search",
    "pointless_impressions_src.profiles",
    "pointless_impressions_src.dashboard",
    "pointless_impressions_src.cart",
    "pointless_impressions_src.order",
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

# Ensure DebugSessionMiddleware is added after SessionMiddleware
session_middleware_index = MIDDLEWARE.index(
    "django.contrib.sessions.middleware.SessionMiddleware"
)
MIDDLEWARE.insert(
    session_middleware_index + 1,
    "pointless_impressions_src.pointless_impressions.middleware."
    "debug_session_middleware.DebugSessionMiddleware",
)

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

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# Session configuration
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_NAME = "sessionid"

# Session cookie settings
SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = "Lax"

# CSRF configuration
CSRF_TRUSTED_ORIGINS = [
    h if "://" in h else f"https://{h}"
    for h in ALLOWED_HOSTS
]

# CORS configuration
CORS_ALLOWED_ORIGINS = [
    h if "://" in h else f"https://{h}"
    for h in ALLOWED_HOSTS
]
CORS_ALLOW_CREDENTIALS = True

# Phone number field settings
PHONENUMBER_DEFAULT_REGION = "GB"
PHONENUMBER_DB_FORMAT = "E164"
PHONENUMBER_DEFAULT_FORMAT = "E164"

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
                "pointless_impressions_src.pointless_impressions."
                "context_processors.global_context",
                "pointless_impressions_src.cart.context_processors."
                "cart_context_processor",
                "pointless_impressions_src.profiles.context_processors."
                "global_profiles_context",
                "pointless_impressions_src.profiles.context_processors."
                "auth_forms",
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = (
    "pointless_impressions_src.pointless_impressions.wsgi.application"
    )


# Authentication Settings
# Custom user model
AUTH_USER_MODEL = "account.CustomUser"

# Login and logout settings
LOGIN_URL = "/profiles/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/"

# Signup settings
SIGNUP_REDIRECT_URL = "/profiles/verify-email/"

# Verification token expiry time
VERIFICATION_TOKEN_EXPIRY = 604800

# Password validation
PASSWORD_RESET_TIMEOUT = 3600
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "pointless_impressions_src.account.validators."
            "CustomPasswordValidator"
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

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

# Cloudinary storage settings
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True
)

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Free delivery threshold (in GBP)
DELIVERY_FEE_TIERS = [
    (1, 12.00),
    (2, 18.00),
    (3, 25.00),
    (4, 30.00),
]
FREE_DELIVERY_THRESHOLD = 5
FEE_MAP = dict(DELIVERY_FEE_TIERS)

STATIC_VERSION = os.getenv("STATIC_VERSION", "1.0.0")

# # Logging configuration
# APP_LOGGERS = [
#     "pointless_impressions_src.pointless_impressions",
#     "pointless_impressions_src.home",
#     "pointless_impressions_src.theme",
#     "pointless_impressions_src.artwork",
#     "pointless_impressions_src.photo",
#     "pointless_impressions_src.account",
#     "pointless_impressions_src.search",
#     "pointless_impressions_src.profiles",
#     "pointless_impressions_src.dashboard",
#     "pointless_impressions_src.cart",
#     "pointless_impressions_src.order",
# ]

# # Generate the common configuration for all app loggers
# APP_LOGGER_CONFIG = {
#     app_name: {
#         'handlers': ['console', 'file'],
#         'level': 'DEBUG',
#         'propagate': False,
#     }
#     for app_name in APP_LOGGERS
# }

# # The main LOGGING dictionary
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': 'debug.log',
#             'formatter': 'verbose',
#             'maxBytes': 1024 * 1024 * 5,
#             'backupCount': 5,
#         },
#     },
#     'loggers': {
#         **APP_LOGGER_CONFIG,
#         'django': {
#             'handlers': ['console'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#     },
# }

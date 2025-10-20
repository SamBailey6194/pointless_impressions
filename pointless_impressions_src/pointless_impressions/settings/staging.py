from .base import *
import os
import dj_database_url
from datetime import datetime

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "staging-secret-key")
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv(
    "DJANGO_ALLOWED_HOSTS", "staging.example.com"
    ).split(",")
PRODUCTION = True

DATABASES = {
    "default": dj_database_url.config(
        default=f"postgres://{os.getenv('STAGING_DB_USER', 'staging_user')}:"
        f"{os.getenv('STAGING_DB_PASSWORD', 'staging_pass')}@"
        f"{os.getenv('STAGING_DB_HOST', 'db_staging')}:"
        f"5432/{os.getenv('STAGING_DB_NAME', 'staging_db')}",
        conn_max_age=600,
    )
}

# Email setup (e.g. Mailtrap or SendGrid sandbox)
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
    )
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.mailtrap.io")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 1025))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "staging@example.com")

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
}
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# AWS S3 Settings
# Cache control
AWS_S3_OBJECT_PARAMETERS = {
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'CacheControl': 'max-age=94608000',
}
# Bucket Config
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_CUSTOM_DOMAIN = (
    f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
    )

# Static and media files
STORAGES = {
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "region_name": AWS_S3_REGION_NAME,
            "custom_domain": AWS_S3_CUSTOM_DOMAIN,
            "object_parameters": AWS_S3_OBJECT_PARAMETERS,
            "location": "static",
        },
    },
}

# Override static URL in production
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'

# Use timestamp as STATIC_VERSION for cache busting
STATIC_VERSION = datetime.now().strftime("staging-%Y%m%d%H%M%S")

CACHE_URL = os.getenv("CACHE_URL", "redis://redis:6379/0")

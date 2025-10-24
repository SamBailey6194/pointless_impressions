"""
Django settings for staging environment.
"""

from .base import *
import os
import dj_database_url
from datetime import datetime
import cloudinary

# Environment settings
ENVIRONMENT = "staging"
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY environment variable is required")

DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")
PRODUCTION = True

# Database configuration (using course database maker)
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("STAGING_DB_URL"),
        conn_max_age=600,
    )
}

# Email configuration (Mailtrap or similar testing service)
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.mailtrap.io")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv(
    "DEFAULT_FROM_EMAIL",
    "staging@example.com"
)

# Cloudinary storage settings
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
    secure_disctribution=ALLOWED_HOSTS,
    upload_prefix=os.getenv("CLOUDINARY_UPLOAD_PREFIX")
)

# AWS S3 Settings
# AWS Bucket configuration
AWS_REGION = os.getenv('AWS_S3_REGION_NAME')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_BUCKET_NAME_STATIC = os.getenv('AWS_STORAGE_BUCKET_NAME')

# AWS S3 Configuration
# Defines Subdirectory in bucket to store static files
AWS_S3_KEY_PREFIX = 'static'

# Make files publicly accessible
AWS_S3_BUCKET_AUTH_STATIC = False

# Set the maximum age for S3 objects
AWS_S3_MAX_AGE_SECONDS_STATIC = 60 * 60 * 24 * 365  # 1 year

# Enable Gzip compression for files for performance
AWS_S3_GZIP = True

# Public URL for S3 bucket
AWS_S3_CUSTOM_DOMAIN = f'{AWS_S3_BUCKET_NAME_STATIC}.s3.{AWS_REGION}.amazonaws.com'

AWS_DEFAULT_ACL = None

# Storage backends
STORAGES = {
    # Media Files (Replaces DEFAULT_FILE_STORAGE)
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    # Static Files (Replaces STATICFILES_STORAGE)
    "staticfiles": {
        "BACKEND": "django_s3_storage.storage.ManifestStaticS3Storage",
    },
}

STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_S3_KEY_PREFIX}/'

S3_DOMAIN = f'https://{AWS_S3_CUSTOM_DOMAIN}'

# Content Security Policy settings
CSP_DEFAULT_SRC = ("'none'",)

CSP_SCRIPT_SRC = (
    "'self'", 
    S3_DOMAIN,
    'https://res.cloudinary.com',
)

CSP_STYLE_SRC = (
    "'self'", 
    S3_DOMAIN,
)

CSP_IMG_SRC = (
    "'self'", 
    S3_DOMAIN,
    'https://res.cloudinary.com',
    'data:',
)

CSP_CONNECT_SRC = (
    "'self'",
    S3_DOMAIN,
    'https://res.cloudinary.com',
)

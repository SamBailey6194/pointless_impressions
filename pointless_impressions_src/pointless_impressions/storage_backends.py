from storages.backends.s3boto3 import S3Boto3Storage
from django.contrib.staticfiles.storage import ManifestFilesMixin


class ManifestStaticS3Storage(ManifestFilesMixin, S3Boto3Storage):
    pass

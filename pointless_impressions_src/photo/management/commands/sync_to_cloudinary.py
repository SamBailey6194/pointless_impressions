from django.core.management.base import BaseCommand
from django.conf import settings
from photo.models import Photo
import cloudinary
import cloudinary.uploader


class Command(BaseCommand):
    help = 'Sync photo image fields to Cloudinary'

    def add_arguments(self, parser):
        parser.add_argument(
            '--recreate',
            action='store_true',
            help='Force recreate all images even if already synced',
        )

    def handle(self, *args, **options):
        recreate = options.get('recreate', False)

        # Configure Cloudinary
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
        )

        photos = Photo.objects.all()
        self.stdout.write(f"Processing {photos.count()} photos...")

        synced = 0
        skipped = 0
        failed = 0

        for photo in photos:
            try:
                # Skip if already has Cloudinary URL and not recreating
                has_url = hasattr(photo.image, 'url')
                img_url = str(photo.image.url) if has_url else ''
                is_cloudinary = 'cloudinary' in img_url
                if is_cloudinary and not recreate:
                    msg = f"  ⊙ {photo.title} - already synced"
                    self.stdout.write(msg)
                    skipped += 1
                    continue

                # If it's a local file, upload it
                if hasattr(photo.image, 'path'):
                    result = cloudinary.uploader.upload(
                        photo.image.path,
                        folder=f"{settings.CLOUDINARY_UPLOAD_PREFIX}/photos",
                        overwrite=True,
                        resource_type='auto',
                    )
                    photo.image = result['secure_url']
                    photo.save()
                    self.stdout.write(self.style.SUCCESS(f"  ✓ {photo.title}"))
                    synced += 1
                else:
                    self.stdout.write(f"  ⊘ {photo.title} - no local file")
                    skipped += 1

            except Exception as e:
                error_msg = f"  ✗ {photo.title} - {str(e)}"
                self.stdout.write(self.style.ERROR(error_msg))
                failed += 1

        done_msg = (
            f"\n✓ Done! Synced: {synced}, "
            f"Skipped: {skipped}, Failed: {failed}"
        )
        self.stdout.write(self.style.SUCCESS(done_msg))

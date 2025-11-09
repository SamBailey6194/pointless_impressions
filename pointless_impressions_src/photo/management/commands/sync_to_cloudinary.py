from django.core.management.base import BaseCommand
import cloudinary
import cloudinary.uploader
from pathlib import Path
import os


# Write your commands here
class Command(BaseCommand):
    help = 'Upload local images to Cloudinary'

    def add_arguments(self, parser):
        parser.add_argument(
            '--folder',
            type=str,
            help=(
                'Cloudinary folder to upload images into '
                '(overrides default prefix)'
                )
        )

    def handle(self, *args, **options):
        # Config is already loaded from settings - just verify it's set
        config = cloudinary.config()

        cloudinary.config(upload_prefix=None)

        if not config.cloud_name:
            self.stdout.write(self.style.ERROR('Cloudinary not configured!'))
            return

        base_folder = options.get('folder') or os.getenv(
            'CLOUDINARY_UPLOAD_PREFIX', ''
            )

        # Define media directory
        media_dir = Path('pointless_impressions_src/media')

        # Find all image files
        image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.gif']
        image_files = []
        for ext in image_extensions:
            image_files.extend(media_dir.rglob(ext))

        self.stdout.write(f'Found {len(image_files)} images\n')

        uploaded = 0
        failed = 0

        for image_path in image_files:
            try:
                # Determine folder based on path
                relative_path = image_path.relative_to(media_dir)
                sub_folder = str(relative_path.parent)

                if base_folder:
                    full_folder = f'{base_folder}/{sub_folder}'
                else:
                    full_folder = sub_folder

                # Upload with explicit secure=True to force HTTPS
                result = cloudinary.uploader.upload(
                    str(image_path),
                    folder=full_folder,
                    use_filename=True,
                    unique_filename=False,
                    overwrite=True,
                    resource_type='auto',
                    secure=True
                )

                url = result.get("secure_url", "N/A")[:50]
                msg = self.style.SUCCESS(
                    f'✓ {image_path.name} - URL: {url}'
                )
                self.stdout.write(msg)
                uploaded += 1

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'✗ {image_path.name} - {str(e)}'
                    )
                    )
                failed += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Done! Uploaded: {uploaded}, Failed: {failed}'
                )
            )

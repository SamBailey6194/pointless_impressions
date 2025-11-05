"""
Django management command to create test artworks for E2E testing.

⚠️  DEVELOPMENT ONLY - This command creates test data in the test database.
Only use with test.py settings (SQLite test database).
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from pointless_impressions_src.artwork.models import (
    Artwork,
    ArtworkCategory,
    ArtworkFramingCondition
)
from pointless_impressions_src.profiles.models import Artist
from pointless_impressions_src.photo.models import Photo


class Command(BaseCommand):
    help = (
        '⚠️  DEVELOPMENT ONLY: Create test artworks for E2E testing. '
        'Only works with test.py settings.'
    )

    def handle(self, *args, **options):
        """Create test data for Cypress E2E tests."""
        from django.conf import settings

        # SECURITY: Only allow in test mode
        db_name = settings.DATABASES.get('default', {}).get('NAME', '')
        is_test_mode = 'test' in db_name.lower()

        if not is_test_mode:
            self.stdout.write(
                self.style.ERROR(
                    '❌ This command only works with test.py settings '
                    '(test database). Current DB: ' + db_name
                )
            )
            return

        User = get_user_model()

        # Check if test data already exists
        if Artwork.objects.filter(name='Sunset').exists():
            self.stdout.write(
                self.style.SUCCESS(
                    '✅ Test data already exists. Skipping creation.'
                )
            )
            return

        try:
            # Create default artist
            default_artist_user = User.objects.create(
                username='test_artist',
                email='test_artist@example.com',
                phone='1234567890'
            )

            default_artist_profile = Artist.objects.create(
                user=default_artist_user,
                bio="Test artist bio",
                portfolio_url="https://testartist.com"
            )

            # Create default category
            default_category = ArtworkCategory.objects.create(
                name="Pointillism",
                friendly_name="Pointillism Art",
                description="Beautiful pointillism artworks."
            )

            # Create default framing condition
            default_framing_condition = (
                ArtworkFramingCondition.objects.create(
                    condition_name="unframed",
                    condition_description="Artwork is unframed."
                )
            )

            # Create test artworks
            test_artworks = [
                {
                    'name': 'Sunset',
                    'description': (
                        'A beautiful sunset over the mountains.'
                    ),
                    'price': 199.99,
                    'sku': 'SUNSET001',
                    'is_available': True,
                    'is_in_stock': True,
                    'quantity': 5,
                },
                {
                    'name': 'Starry Night',
                    'description': 'A night sky full of stars.',
                    'price': 249.99,
                    'sku': 'STARRY001',
                    'is_available': False,  # Sold out
                    'is_in_stock': False,
                    'quantity': 0,
                }
            ]

            created_count = 0
            for artwork_data in test_artworks:
                art = Artwork.objects.create(
                    name=artwork_data['name'],
                    artist=default_artist_profile,
                    category=default_category,
                    description=artwork_data['description'],
                    price=artwork_data['price'],
                    sku=artwork_data['sku'],
                    is_available=artwork_data['is_available'],
                    is_in_stock=artwork_data['is_in_stock'],
                    is_featured=False,
                    quantity=artwork_data['quantity'],
                    created_at=timezone.now(),
                    updated_at=timezone.now(),
                )
                art.selected_conditions.add(default_framing_condition)
                
                # Create a Photo object for this artwork
                photo = Photo.objects.create(
                    artwork=art,
                    photo_type='artwork',
                    title=f"{art.name} Image",
                    description=f"Image for {art.name} artwork",
                    image=f"artwork/{art.name.lower().replace(' ', '_')}.png",
                    alt_text=f"{art.name} artwork",
                    uploaded_by=default_artist_user
                )
                
                # Set the photo as the main photo for the artwork
                art.main_photo = photo
                art.save()
                
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  ✅ Created: {art.name} (£{art.price}) with photo'
                    )
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✅ Test data created successfully! '
                    f'({created_count} artworks)'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'❌ Error creating test data: {str(e)}'
                )
            )

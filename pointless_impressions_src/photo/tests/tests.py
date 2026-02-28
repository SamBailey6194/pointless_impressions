from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from pointless_impressions_src.photo.forms import (
    ProfilePhotoForm
)
from pointless_impressions_src.artwork.models import (
    Artwork,
    ArtworkCategory
)
from pointless_impressions_src.profiles.models import Artist


User = get_user_model()


def create_test_image():
    """Create a simple test image file."""
    return SimpleUploadedFile(
        name='test_image.jpg',
        content=b'GIF89a\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04\x01\x00'
                b'\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
                b'\x02\x44\x01\x00\x3b',
        content_type='image/gif'
    )


class PhotoFormTest(TestCase):
    """Tests for base PhotoForm with conditional fields (DRY)."""

    def setUp(self):
        """Set up test fixtures."""
        self.user = User.objects.create_user(
            username='user',
            email='user@test.com',
            password='pass123',
            phone='+441234567989'
        )

        artist_user = User.objects.create_user(
            username='artist',
            email='artist@test.com',
            password='pass123',
            phone='+441234567990'
        )
        self.artist = Artist.objects.create(
            user=artist_user,
            bio='Test artist'
        )

        self.category = ArtworkCategory.objects.create(name='Test')
        self.artwork = Artwork.objects.create(
            name='Test Artwork',
            artist=self.artist,
            description='Test',
            price=100.00,
            category=self.category
        )

    def test_photo_form_valid_profile_photo(self):
        """Test PhotoForm with valid profile photo data."""
        form = ProfilePhotoForm(data={
            'photo_type': 'profile',
            'title': 'Profile Picture',
            'description': 'User profile photo',
            'image': 'test_image.jpg'
        })
        self.assertTrue(form.is_valid())

    def test_photo_form_profile_excludes_artwork_and_asset(self):
        """Test profile form only has base fields."""
        form = ProfilePhotoForm(photo_type='profile')
        self.assertNotIn('artwork', form.fields)
        self.assertNotIn('asset_identifier', form.fields)

    def test_photo_form_save_with_user(self):
        """Test form.save() with user assignment."""
        image = create_test_image()
        form_data = {
            'photo_type': 'profile',
            'title': 'Profile Photo',
            'description': 'User profile picture',
            'alt_text': 'profile'
        }
        form = ProfilePhotoForm(
            data=form_data,
            files={'image': image},
            photo_type='profile'
        )
        self.assertTrue(form.is_valid())

        photo = form.save(commit=False, user=self.user)
        self.assertEqual(photo.uploaded_by, self.user)

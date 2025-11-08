from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from pointless_impressions_src.photo.forms import PhotoForm
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
            phone='1234567890'
        )

        artist_user = User.objects.create_user(
            username='artist',
            email='artist@test.com',
            password='pass123',
            phone='1234567890'
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

    def test_photo_form_valid_artwork_photo(self):
        """Test PhotoForm with valid artwork photo data."""
        image = create_test_image()
        form_data = {
            'photo_type': 'artwork',
            'title': 'Artwork Photo',
            'description': 'Photo of artwork',
            'alt_text': 'artwork photo',
            'artwork': self.artwork.id
        }
        form = PhotoForm(
            data=form_data,
            files={'image': image},
            photo_type='artwork'
        )
        self.assertTrue(form.is_valid())

    def test_photo_form_valid_profile_photo(self):
        """Test PhotoForm with valid profile photo data."""
        image = create_test_image()
        form_data = {
            'photo_type': 'profile',
            'title': 'Profile Picture',
            'description': 'User profile photo',
            'alt_text': 'profile photo'
        }
        form = PhotoForm(
            data=form_data,
            files={'image': image},
            photo_type='profile'
        )
        self.assertTrue(form.is_valid())

    def test_photo_form_valid_site_asset(self):
        """Test PhotoForm with valid site asset data."""
        image = create_test_image()
        form_data = {
            'photo_type': 'site_asset',
            'title': 'Logo',
            'description': 'Site logo',
            'alt_text': 'logo',
            'asset_identifier': 'logo_main'
        }
        form = PhotoForm(
            data=form_data,
            files={'image': image},
            photo_type='site_asset'
        )
        self.assertTrue(form.is_valid())

    def test_photo_form_artwork_requires_artwork_field(self):
        """Test artwork photos require artwork selection."""
        form_data = {
            'photo_type': 'artwork',
            'title': 'Artwork Photo',
            'description': 'Photo without artwork',
            'alt_text': 'no artwork'
        }
        form = PhotoForm(data=form_data, photo_type='artwork')
        self.assertFalse(form.is_valid())
        self.assertIn('artwork', form.errors)

    def test_photo_form_site_asset_requires_identifier(self):
        """Test site assets require asset identifier."""
        form_data = {
            'photo_type': 'site_asset',
            'title': 'Asset',
            'description': 'Asset without identifier',
            'alt_text': 'asset'
        }
        form = PhotoForm(data=form_data, photo_type='site_asset')
        self.assertFalse(form.is_valid())
        self.assertIn('asset_identifier', form.errors)

    def test_photo_form_artwork_excludes_asset_identifier(self):
        """Test artwork form doesn't include asset_identifier."""
        form = PhotoForm(photo_type='artwork')
        self.assertNotIn('asset_identifier', form.fields)

    def test_photo_form_site_asset_excludes_artwork(self):
        """Test site asset form doesn't include artwork field."""
        form = PhotoForm(photo_type='site_asset')
        self.assertNotIn('artwork', form.fields)

    def test_photo_form_profile_excludes_artwork_and_asset(self):
        """Test profile form only has base fields."""
        form = PhotoForm(photo_type='profile')
        self.assertNotIn('artwork', form.fields)
        self.assertNotIn('asset_identifier', form.fields)

    def test_photo_form_missing_title(self):
        """Test form validation for missing title."""
        form_data = {
            'photo_type': 'profile',
            'description': 'Photo without title',
            'alt_text': 'test'
        }
        form = PhotoForm(data=form_data, photo_type='profile')
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_photo_form_missing_description(self):
        """Test form validation for missing description."""
        form_data = {
            'photo_type': 'profile',
            'title': 'Photo',
            'alt_text': 'test'
        }
        form = PhotoForm(data=form_data, photo_type='profile')
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    def test_photo_form_title_too_short(self):
        """Test title minimum length validation."""
        form_data = {
            'photo_type': 'profile',
            'title': 'ab',
            'description': 'Description',
            'alt_text': 'test'
        }
        form = PhotoForm(data=form_data, photo_type='profile')
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_photo_form_description_too_short(self):
        """Test description minimum length validation."""
        form_data = {
            'photo_type': 'profile',
            'title': 'Photo',
            'description': 'desc',
            'alt_text': 'test'
        }
        form = PhotoForm(data=form_data, photo_type='profile')
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    def test_photo_form_alt_text_too_long(self):
        """Test alt text maximum length validation."""
        form_data = {
            'photo_type': 'profile',
            'title': 'Photo',
            'description': 'Description',
            'alt_text': 'x' * 300  # Exceeds 255 chars
        }
        form = PhotoForm(data=form_data, photo_type='profile')
        self.assertFalse(form.is_valid())
        self.assertIn('alt_text', form.errors)

    def test_photo_form_save_with_user(self):
        """Test form.save() with user assignment."""
        image = create_test_image()
        form_data = {
            'photo_type': 'profile',
            'title': 'Profile Photo',
            'description': 'User profile picture',
            'alt_text': 'profile'
        }
        form = PhotoForm(
            data=form_data,
            files={'image': image},
            photo_type='profile'
        )
        self.assertTrue(form.is_valid())

        photo = form.save(commit=False, user=self.user)
        self.assertEqual(photo.uploaded_by, self.user)

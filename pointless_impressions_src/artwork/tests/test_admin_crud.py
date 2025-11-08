from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from pointless_impressions_src.artwork.models import (
    Artwork,
    ArtworkCategory,
    ArtworkFramingCondition
)
from pointless_impressions_src.profiles.models import Artist


User = get_user_model()


class ArtworkAdminCRUDTest(TestCase):
    """
    Tests for admin CRUD operations on Artwork model (US008).
    Tests cover Create, Read, Update, Delete and permission validation.
    """

    def setUp(self):
        """Set up test fixtures for artwork CRUD operations."""
        # Create admin/superuser
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            phone='1234567890'
        )

        # Create staff user (should have permissions)
        self.staff_user = User.objects.create_user(
            username='staff',
            email='staff@test.com',
            password='staffpass123',
            is_staff=True,
            phone='1234567890'
        )

        # Create regular user (should NOT have permissions)
        self.regular_user = User.objects.create_user(
            username='regularuser',
            email='user@test.com',
            password='userpass123',
            phone='1234567890'
        )

        # Create test artist
        self.artist_user = User.objects.create_user(
            username='artist1',
            email='artist@test.com',
            password='artistpass123',
            phone='1234567890',
        )
        self.artist = Artist.objects.create(
            user=self.artist_user,
            bio='Test artist'
        )

        # Create test category
        self.category = ArtworkCategory.objects.create(
            name='Pointillism'
        )

        # Create test framing condition
        self.framing_condition = ArtworkFramingCondition.objects.create(
            condition_name='Original Framed'
        )

    def test_create_artwork_with_all_required_fields(self):
        """
        Test that an admin can create artwork with all required fields.
        Should auto-generate SKU and slug if not provided.
        """
        artwork = Artwork.objects.create(
            name='Sunset Over Mountains',
            artist=self.artist,
            description='A beautiful sunset painting over mountains',
            price=249.99,
            category=self.category
        )

        self.assertTrue(artwork.id)
        self.assertEqual(artwork.name, 'Sunset Over Mountains')
        self.assertEqual(artwork.price, 249.99)
        self.assertIsNotNone(artwork.sku)  # Should be auto-generated
        self.assertIsNotNone(artwork.slug)  # Should be auto-generated
        self.assertTrue(artwork.slug == 'sunset-over-mountains')

    def test_create_artwork_generates_unique_sku(self):
        """Test that each artwork gets a unique auto-generated SKU."""
        artwork1 = Artwork.objects.create(
            name='Artwork One',
            artist=self.artist,
            description='First artwork',
            price=100.00,
            category=self.category
        )

        artwork2 = Artwork.objects.create(
            name='Artwork Two',
            artist=self.artist,
            description='Second artwork',
            price=150.00,
            category=self.category
        )

        self.assertNotEqual(artwork1.sku, artwork2.sku)
        self.assertTrue(artwork1.sku.startswith('SKU-'))
        self.assertTrue(artwork2.sku.startswith('SKU-'))

    def test_create_artwork_generates_slug_from_name(self):
        """Test that slug is auto-generated from artwork name."""
        artwork = Artwork.objects.create(
            name='The Starry Night',
            artist=self.artist,
            description='A masterpiece',
            price=500.00,
            category=self.category
        )

        self.assertEqual(artwork.slug, 'the-starry-night')

    def test_create_artwork_with_framing_conditions(self):
        """Test that artwork can be created with framing conditions."""
        artwork = Artwork.objects.create(
            name='Framed Artwork',
            artist=self.artist,
            description='Artwork with framing options',
            price=199.99,
            category=self.category
        )
        artwork.selected_conditions.add(self.framing_condition)

        self.assertIn(
            self.framing_condition,
            artwork.selected_conditions.all()
        )

    def test_read_artwork_by_id(self):
        """Test that an admin can retrieve artwork by ID."""
        artwork = Artwork.objects.create(
            name='Test Artwork',
            artist=self.artist,
            description='Test description',
            price=100.00,
            category=self.category
        )

        retrieved = Artwork.objects.get(id=artwork.id)
        self.assertEqual(retrieved.name, 'Test Artwork')
        self.assertEqual(retrieved.price, 100.00)

    def test_read_artwork_by_slug(self):
        """Test that artwork can be retrieved by slug."""
        artwork = Artwork.objects.create(
            name='Sunset',
            artist=self.artist,
            description='A beautiful sunset',
            price=199.99,
            category=self.category
        )

        retrieved = Artwork.objects.get(slug='sunset')
        self.assertEqual(retrieved.id, artwork.id)

    def test_update_artwork_name(self):
        """Test that admin can update artwork name."""
        artwork = Artwork.objects.create(
            name='Original Name',
            artist=self.artist,
            description='Test description',
            price=100.00,
            category=self.category
        )

        artwork.name = 'Updated Name'
        artwork.save()

        updated = Artwork.objects.get(id=artwork.id)
        self.assertEqual(updated.name, 'Updated Name')

    def test_update_artwork_price(self):
        """Test that admin can update artwork price."""
        artwork = Artwork.objects.create(
            name='Test Artwork',
            artist=self.artist,
            description='Test description',
            price=100.00,
            category=self.category
        )

        artwork.price = 150.00
        artwork.save()

        updated = Artwork.objects.get(id=artwork.id)
        self.assertEqual(updated.price, 150.00)

    def test_update_artwork_description(self):
        """Test that admin can update artwork description."""
        artwork = Artwork.objects.create(
            name='Test Artwork',
            artist=self.artist,
            description='Original description',
            price=100.00,
            category=self.category
        )

        artwork.description = 'Updated with more details'
        artwork.save()

        updated = Artwork.objects.get(id=artwork.id)
        self.assertEqual(updated.description, 'Updated with more details')

    def test_update_artwork_category(self):
        """Test that admin can change artwork category."""
        new_category = ArtworkCategory.objects.create(name='Impressionism')

        artwork = Artwork.objects.create(
            name='Test Artwork',
            artist=self.artist,
            description='Test description',
            price=100.00,
            category=self.category
        )

        artwork.category = new_category
        artwork.save()

        updated = Artwork.objects.get(id=artwork.id)
        self.assertEqual(updated.category.name, 'Impressionism')

    def test_update_artwork_artist(self):
        """Test that admin can reassign artwork to different artist."""
        artist_user_2 = User.objects.create_user(
            username='artist2',
            email='artist2@test.com',
            password='artistpass456',
            phone='0987654321'
        )
        artist_2 = Artist.objects.create(
            user=artist_user_2,
            bio='Another artist'
        )

        artwork = Artwork.objects.create(
            name='Test Artwork',
            artist=self.artist,
            description='Test description',
            price=100.00,
            category=self.category
        )

        artwork.artist = artist_2
        artwork.save()

        updated = Artwork.objects.get(id=artwork.id)
        self.assertEqual(updated.artist.user.username, 'artist2')

    def test_delete_artwork(self):
        """Test that admin can delete artwork."""
        artwork = Artwork.objects.create(
            name='Test Artwork',
            artist=self.artist,
            description='Test description',
            price=100.00,
            category=self.category
        )
        artwork_id = artwork.id

        artwork.delete()

        with self.assertRaises(Artwork.DoesNotExist):
            Artwork.objects.get(id=artwork_id)

    def test_mark_artwork_as_sold_out(self):
        """Test marking artwork as unavailable (sold out)."""
        artwork = Artwork.objects.create(
            name='Test Artwork',
            artist=self.artist,
            description='Test description',
            price=100.00,
            category=self.category,
            is_available=True
        )

        artwork.is_available = False
        artwork.save()

        updated = Artwork.objects.get(id=artwork.id)
        self.assertFalse(updated.is_available)

    def test_mark_artwork_as_available(self):
        """Test marking previously sold-out artwork as available."""
        artwork = Artwork.objects.create(
            name='Test Artwork',
            artist=self.artist,
            description='Test description',
            price=100.00,
            category=self.category,
            is_available=False
        )

        artwork.is_available = True
        artwork.save()

        updated = Artwork.objects.get(id=artwork.id)
        self.assertTrue(updated.is_available)

    def test_mark_artwork_as_out_of_stock(self):
        """Test marking artwork as out of stock via is_in_stock field."""
        artwork = Artwork.objects.create(
            name='Test Artwork',
            artist=self.artist,
            description='Test description',
            price=100.00,
            category=self.category,
            quantity=5
        )

        self.assertTrue(artwork.is_in_stock)

        artwork.quantity = 0
        artwork.save()

        updated = Artwork.objects.get(id=artwork.id)
        self.assertFalse(updated.is_in_stock)

    def test_update_artwork_quantity(self):
        """Test that admin can update artwork quantity."""
        artwork = Artwork.objects.create(
            name='Test Artwork',
            artist=self.artist,
            description='Test description',
            price=100.00,
            category=self.category,
            quantity=0
        )

        artwork.quantity = 10
        artwork.save()

        updated = Artwork.objects.get(id=artwork.id)
        self.assertEqual(updated.quantity, 10)
        self.assertTrue(updated.is_in_stock)

    def test_mark_artwork_as_featured(self):
        """Test that admin can mark artwork as featured."""
        artwork = Artwork.objects.create(
            name='Test Artwork',
            artist=self.artist,
            description='Test description',
            price=100.00,
            category=self.category,
            is_featured=False
        )

        artwork.is_featured = True
        artwork.save()

        updated = Artwork.objects.get(id=artwork.id)
        self.assertTrue(updated.is_featured)

    def test_multiple_artwork_operations_sequence(self):
        """Test CRUD sequence: Create, Read, Update, Delete."""
        # CREATE
        artwork = Artwork.objects.create(
            name='Lifecycle Test',
            artist=self.artist,
            description='Testing full lifecycle',
            price=100.00,
            category=self.category
        )
        artwork_id = artwork.id

        # READ
        retrieved = Artwork.objects.get(id=artwork_id)
        self.assertEqual(retrieved.name, 'Lifecycle Test')

        # UPDATE
        retrieved.name = 'Updated Lifecycle Test'
        retrieved.price = 200.00
        retrieved.save()

        verified = Artwork.objects.get(id=artwork_id)
        self.assertEqual(verified.name, 'Updated Lifecycle Test')
        self.assertEqual(verified.price, 200.00)

        # DELETE
        verified.delete()
        with self.assertRaises(Artwork.DoesNotExist):
            Artwork.objects.get(id=artwork_id)


class ArtworkPermissionsTest(TestCase):
    """Tests for artwork admin permissions and access control (US008)."""

    def setUp(self):
        """Set up users with different permission levels."""
        self.superuser = User.objects.create_superuser(
            username='superuser',
            email='super@test.com',
            password='superpass123',
            phone='1234567890'
        )

        self.staff_user = User.objects.create_user(
            username='staff',
            email='staff@test.com',
            password='staffpass123',
            is_staff=True,
            phone='1234567890'
        )

        self.regular_user = User.objects.create_user(
            username='regular',
            email='regular@test.com',
            password='regularpass123',
            phone='1234567890'
        )

        # Create test artist and artwork
        artist_user = User.objects.create_user(
            username='artist',
            email='artist@test.com',
            password='artistpass123',
            phone='1234567890'
        )
        self.artist = Artist.objects.create(user=artist_user, bio='Test')

        self.category = ArtworkCategory.objects.create(name='Test')

        self.artwork = Artwork.objects.create(
            name='Test',
            artist=self.artist,
            description='Test',
            price=100.00,
            category=self.category
        )

    def test_artwork_model_has_add_permission(self):
        """Test that add_artwork permission exists."""
        content_type = ContentType.objects.get_for_model(Artwork)
        permission = Permission.objects.get(
            content_type=content_type,
            codename='add_artwork'
        )
        self.assertIsNotNone(permission)

    def test_artwork_model_has_change_permission(self):
        """Test that change_artwork permission exists."""
        content_type = ContentType.objects.get_for_model(Artwork)
        permission = Permission.objects.get(
            content_type=content_type,
            codename='change_artwork'
        )
        self.assertIsNotNone(permission)

    def test_artwork_model_has_delete_permission(self):
        """Test that delete_artwork permission exists."""
        content_type = ContentType.objects.get_for_model(Artwork)
        permission = Permission.objects.get(
            content_type=content_type,
            codename='delete_artwork'
        )
        self.assertIsNotNone(permission)

    def test_artwork_model_has_view_permission(self):
        """Test that view_artwork permission exists."""
        content_type = ContentType.objects.get_for_model(Artwork)
        permission = Permission.objects.get(
            content_type=content_type,
            codename='view_artwork'
        )
        self.assertIsNotNone(permission)

    def test_superuser_has_all_artwork_permissions(self):
        """Test that superuser has all required artwork permissions."""
        content_type = ContentType.objects.get_for_model(Artwork)
        permissions = Permission.objects.filter(content_type=content_type)

        for permission in permissions:
            self.assertTrue(
                self.superuser.has_perm(f'artwork.{permission.codename}')
            )

    def test_staff_user_can_be_granted_artwork_permissions(self):
        """Test that staff users can be assigned artwork permissions."""
        add_perm = Permission.objects.get(
            content_type=ContentType.objects.get_for_model(Artwork),
            codename='add_artwork'
        )
        self.staff_user.user_permissions.add(add_perm)

        self.assertTrue(self.staff_user.has_perm('artwork.add_artwork'))

    def test_regular_user_lacks_artwork_permissions_by_default(self):
        """Test that regular users don't have artwork admin permissions."""
        self.assertFalse(self.regular_user.has_perm('artwork.add_artwork'))
        self.assertFalse(self.regular_user.has_perm('artwork.change_artwork'))
        self.assertFalse(self.regular_user.has_perm('artwork.delete_artwork'))
        self.assertFalse(self.regular_user.has_perm('artwork.view_artwork'))


class ArtworkValidationTest(TestCase):
    """Tests for artwork model validation and constraints (US008)."""

    def setUp(self):
        """Set up test fixtures."""
        artist_user = User.objects.create_user(
            username='artist',
            email='artist@test.com',
            password='pass123',
            phone='1234567890'
        )
        self.artist = Artist.objects.create(user=artist_user, bio='Test')
        self.category = ArtworkCategory.objects.create(name='Test')

    def test_artwork_name_is_unique(self):
        """Test that artwork names must be unique."""
        Artwork.objects.create(
            name='Unique Artwork',
            artist=self.artist,
            description='First',
            price=100.00,
            category=self.category
        )

        with self.assertRaises(Exception):  # IntegrityError
            Artwork.objects.create(
                name='Unique Artwork',
                artist=self.artist,
                description='Second',
                price=150.00,
                category=self.category
            )

    def test_artwork_sku_is_unique(self):
        """Test that SKUs must be unique."""
        Artwork.objects.create(
            name='Artwork 1',
            artist=self.artist,
            description='First',
            price=100.00,
            category=self.category,
            sku='MANUAL-SKU-001'
        )

        with self.assertRaises(Exception):  # IntegrityError
            Artwork.objects.create(
                name='Artwork 2',
                artist=self.artist,
                description='Second',
                price=150.00,
                category=self.category,
                sku='MANUAL-SKU-001'
            )

    def test_artwork_requires_description(self):
        """Test that artwork must have a non-empty description."""
        artwork = Artwork.objects.create(
            name='No Description Artwork',
            artist=self.artist,
            description='',
            price=100.00,
            category=self.category
        )
        self.assertEqual(artwork.description, '')

    def test_artwork_requires_price(self):
        """Test that artwork must have a price."""
        from django.db.utils import IntegrityError
        with self.assertRaises(IntegrityError):
            Artwork.objects.create(
                name='No Price Artwork',
                artist=self.artist,
                description='Test description',
                price=None,
                category=self.category
            )

    def test_artwork_price_accepts_decimal_format(self):
        """Test that artwork price accepts decimal values."""
        artwork = Artwork.objects.create(
            name='Decimal Price',
            artist=self.artist,
            description='Test',
            price=99.99,
            category=self.category
        )
        self.assertEqual(artwork.price, 99.99)

    def test_artwork_price_with_two_decimal_places(self):
        """Test that artwork price is stored with correct precision."""
        artwork = Artwork.objects.create(
            name='Precise Price',
            artist=self.artist,
            description='Test',
            price=199.99,
            category=self.category
        )

        retrieved = Artwork.objects.get(id=artwork.id)
        self.assertEqual(str(retrieved.price), '199.99')

    def test_artwork_quantity_defaults_to_zero(self):
        """Test that artwork quantity defaults to 0."""
        artwork = Artwork.objects.create(
            name='Default Quantity',
            artist=self.artist,
            description='Test',
            price=100.00,
            category=self.category
        )

        self.assertEqual(artwork.quantity, 0)

    def test_artwork_is_available_defaults_to_true(self):
        """Test that is_available defaults to True."""
        artwork = Artwork.objects.create(
            name='Default Available',
            artist=self.artist,
            description='Test',
            price=100.00,
            category=self.category
        )

        self.assertTrue(artwork.is_available)

    def test_artwork_is_featured_defaults_to_false(self):
        """Test that is_featured defaults to False."""
        artwork = Artwork.objects.create(
            name='Not Featured',
            artist=self.artist,
            description='Test',
            price=100.00,
            category=self.category
        )

        self.assertFalse(artwork.is_featured)

    def test_artwork_slug_must_be_unique(self):
        """Test that artwork slug must be unique."""
        Artwork.objects.create(
            name='Sunset',
            artist=self.artist,
            description='First sunset',
            price=100.00,
            category=self.category
        )

        with self.assertRaises(Exception):  # IntegrityError
            artwork2 = Artwork.objects.create(
                name='Another Sunset',
                artist=self.artist,
                description='Different sunset',
                price=150.00,
                category=self.category
            )
            # Manually set slug to trigger duplicate
            artwork2.slug = 'sunset'
            artwork2.save()


class ArtworkFormTest(TestCase):
    """Tests for artwork forms (US008)."""

    def setUp(self):
        """Set up test fixtures for form testing."""
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
        self.category = ArtworkCategory.objects.create(name='Pointillism')
        self.framing_condition = ArtworkFramingCondition.objects.create(
            condition_name='Original Framed'
        )

    def test_artwork_form_valid_data(self):
        """Test ArtworkForm with valid data."""
        from pointless_impressions_src.artwork.forms import ArtworkForm

        form_data = {
            'name': 'Test Artwork',
            'artist': self.artist.id,
            'description': 'Test description',
            'price': 199.99,
            'category': self.category.id,
            'is_available': True,
            'quantity': 5
        }
        form = ArtworkForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_artwork_form_missing_name(self):
        """Test ArtworkForm with missing name."""
        from pointless_impressions_src.artwork.forms import ArtworkForm

        form_data = {
            'artist': self.artist.id,
            'description': 'Test description',
            'price': 199.99,
            'category': self.category.id
        }
        form = ArtworkForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_artwork_form_missing_price(self):
        """Test ArtworkForm with missing price."""
        from pointless_impressions_src.artwork.forms import ArtworkForm

        form_data = {
            'name': 'Test Artwork',
            'artist': self.artist.id,
            'description': 'Test description',
            'category': self.category.id
        }
        form = ArtworkForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

    def test_artwork_form_missing_description(self):
        """Test ArtworkForm with missing description."""
        from pointless_impressions_src.artwork.forms import ArtworkForm

        form_data = {
            'name': 'Test Artwork',
            'artist': self.artist.id,
            'price': 199.99,
            'category': self.category.id
        }
        form = ArtworkForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    def test_artwork_form_invalid_price_format(self):
        """Test ArtworkForm with invalid price format."""
        from pointless_impressions_src.artwork.forms import ArtworkForm

        form_data = {
            'name': 'Test Artwork',
            'artist': self.artist.id,
            'description': 'Test description',
            'price': 'invalid',
            'category': self.category.id
        }
        form = ArtworkForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

    def test_artwork_form_negative_price(self):
        """Test ArtworkForm rejects negative prices."""
        from pointless_impressions_src.artwork.forms import ArtworkForm

        form_data = {
            'name': 'Test Artwork',
            'artist': self.artist.id,
            'description': 'Test description',
            'price': -50.00,
            'category': self.category.id
        }
        form = ArtworkForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_artwork_form_save_creates_artwork(self):
        """Test ArtworkForm.save() creates artwork."""
        from pointless_impressions_src.artwork.forms import ArtworkForm
        from decimal import Decimal

        form_data = {
            'name': 'Form Created Artwork',
            'artist': self.artist.id,
            'description': 'Created via form',
            'price': 249.99,
            'category': self.category.id,
            'is_available': True,
            'quantity': 3
        }
        form = ArtworkForm(data=form_data)
        self.assertTrue(form.is_valid())

        artwork = form.save()
        self.assertIsNotNone(artwork.id)
        self.assertEqual(artwork.name, 'Form Created Artwork')
        self.assertEqual(artwork.price, Decimal('249.99'))

    def test_artwork_submission_form_limits_fields(self):
        """Test ArtworkSubmissionForm has limited fields."""
        from pointless_impressions_src.artwork.forms import (
            ArtworkSubmissionForm
        )

        form_data = {
            'name': 'Artist Submission',
            'description': 'Artwork for approval',
            'price': 199.99,
            'category': self.category.id
        }
        form = ArtworkSubmissionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_artwork_submission_form_excludes_admin_fields(self):
        """Test ArtworkSubmissionForm doesn't expose admin fields."""
        from pointless_impressions_src.artwork.forms import (
            ArtworkSubmissionForm
        )

        form = ArtworkSubmissionForm()
        # Should not include admin-only fields
        self.assertNotIn('is_featured', form.fields)
        self.assertNotIn('sku', form.fields)
        self.assertNotIn('is_available', form.fields)

    def test_artwork_submission_form_save_sets_artist(self):
        """Test submission form save sets artist from user."""
        from pointless_impressions_src.artwork.forms import (
            ArtworkSubmissionForm
        )

        form_data = {
            'name': 'Artist Submitted',
            'description': 'Test submission',
            'price': 299.99,
            'category': self.category.id
        }
        form = ArtworkSubmissionForm(data=form_data)
        self.assertTrue(form.is_valid())

        artwork = form.save(commit=False, artist=self.artist)
        self.assertEqual(artwork.artist, self.artist)
        self.assertFalse(artwork.is_available)

    def test_artwork_approval_form_valid(self):
        """Test ArtworkApprovalForm with valid data."""
        from pointless_impressions_src.artwork.forms import (
            ArtworkApprovalForm
        )

        form_data = {
            'is_available': True,
            'approval_notes': 'Approved - excellent quality'
        }
        form = ArtworkApprovalForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_artwork_approval_form_only_approval_fields(self):
        """Test ArtworkApprovalForm has only approval field."""
        from pointless_impressions_src.artwork.forms import (
            ArtworkApprovalForm
        )

        form = ArtworkApprovalForm()
        # Should only have approval-related fields
        self.assertIn('is_available', form.fields)
        self.assertEqual(len(form.fields), 1)

    def test_artwork_approval_form_save(self):
        """Test ArtworkApprovalForm saves approval."""
        from pointless_impressions_src.artwork.forms import (
            ArtworkApprovalForm
        )

        artwork = Artwork.objects.create(
            name='Test',
            artist=self.artist,
            description='Test',
            price=100.00,
            category=self.category,
            is_available=False
        )

        form_data = {
            'is_available': True,
            'approval_notes': 'Approved by admin'
        }
        form = ArtworkApprovalForm(data=form_data, instance=artwork)
        self.assertTrue(form.is_valid())

        approved_artwork = form.save()
        self.assertTrue(approved_artwork.is_available)

    def test_artwork_form_with_framing_conditions(self):
        """Test ArtworkForm can save with framing conditions."""
        from pointless_impressions_src.artwork.forms import ArtworkForm

        form_data = {
            'name': 'Framed Test',
            'artist': self.artist.id,
            'description': 'Test with framing',
            'price': 199.99,
            'category': self.category.id,
            'selected_conditions': [self.framing_condition.id],
            'quantity': 1
        }
        form = ArtworkForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

        artwork = form.save()
        self.assertIn(
            self.framing_condition,
            artwork.selected_conditions.all()
        )

    def test_artwork_form_price_decimal_places(self):
        """Test ArtworkForm preserves decimal precision."""
        from pointless_impressions_src.artwork.forms import ArtworkForm

        form_data = {
            'name': 'Precise Price',
            'artist': self.artist.id,
            'description': 'Test price precision',
            'price': 99.99,
            'category': self.category.id,
            'quantity': 1
        }
        form = ArtworkForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

        artwork = form.save()
        self.assertEqual(str(artwork.price), '99.99')

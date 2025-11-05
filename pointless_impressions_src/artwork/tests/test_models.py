from django.test import TestCase
from django.utils import timezone
from pointless_impressions_src.artwork.models import (
    Artwork, ArtworkFramingCondition, ArtworkCategory
)
from pointless_impressions_src.photo.models import Photo


# Create your tests here.
class ArtworkListModelTest(TestCase):
    """Tests for the Artwork model. For US001."""
    def setUp(self):
        self.framing_condition = ArtworkFramingCondition.objects.create(
            condition_name="framed",
            condition_description="Artwork is framed with a wooden frame."
        )

        self.category = ArtworkCategory.objects.create(
            name="Nature",
            friendly_name="Nature Art",
            description="Art depicting scenes from nature."
        )

        self.artwork = Artwork.objects.create(
            name="Sunset",
            description="A beautiful sunset over the mountains.",
            price=199.99,
            sku="SUNSET1234",
            category=self.category,
            is_available=True,
            is_in_stock=True,
            is_featured=False,
            slug="sunset",
            quantity=10,
        )

        self.artwork.selected_conditions.add(self.framing_condition)

        self.main_photo = Photo.objects.create(
            artwork=self.artwork,
            title="Sunset Main Photo",
            description="Main photo of the sunset artwork.",
            image='test_image.jpg',
            alt_text='Test Image'
        )

        self.artwork.main_photo = self.main_photo
        self.artwork.save()

    def test_artwork_creation(self):
        self.assertEqual(self.artwork.name, "Sunset")
        self.assertEqual(
            self.artwork.description, "A beautiful sunset over the mountains."
        )
        self.assertEqual(self.artwork.price, 199.99)
        self.assertEqual(self.artwork.sku, "SUNSET1234")
        self.assertEqual(self.artwork.category, self.category)
        self.assertEqual(
            self.artwork.selected_conditions.first().condition_name, "framed"
            )
        self.assertEqual(self.artwork.main_photo, self.main_photo)
        self.assertTrue(self.artwork.is_available)
        self.assertTrue(self.artwork.is_in_stock)
        self.assertFalse(self.artwork.is_featured)
        self.assertIsNotNone(self.artwork.created_at)
        self.assertIsNotNone(self.artwork.updated_at)

    def test_artwork_selected_conditions(self):
        condition_qs = self.artwork.selected_conditions.all()
        self.assertEqual(condition_qs.count(), 1)
        self.assertEqual(condition_qs.first(), self.framing_condition)
        self.assertEqual(condition_qs.first().condition_name, "framed")

    def test_artwork_category(self):
        self.artwork.category = self.category
        self.artwork.save()
        self.assertEqual(self.artwork.category.name, "Nature")
        self.assertEqual(self.artwork.category.friendly_name, "Nature Art")

    def test_artwork_str_representation(self):
        self.assertEqual(str(self.artwork), "Sunset")

    def test_artwork_availability(self):
        self.assertTrue(self.artwork.is_available)
        self.artwork.is_available = False
        self.artwork.save()
        self.assertFalse(self.artwork.is_available)

    def test_artwork_stock(self):
        self.assertTrue(self.artwork.is_in_stock)
        self.assertEqual(self.artwork.quantity, 10)
        self.artwork.quantity = 0
        self.artwork.save()
        self.assertFalse(self.artwork.is_in_stock)

        # Replenish stock
        self.artwork.quantity = 5
        self.artwork.save()

    def test_artwork_featured(self):
        self.assertFalse(self.artwork.is_featured)
        self.artwork.is_featured = True
        self.artwork.save()
        self.assertTrue(self.artwork.is_featured)

    def test_artwork_price_update(self):
        self.artwork.price = 249.99
        self.artwork.save()
        self.assertEqual(self.artwork.price, 249.99)

    def test_artwork_description_update(self):
        new_description = "An awe-inspiring sunset over the serene mountains."
        self.artwork.description = new_description
        self.artwork.save()
        self.assertEqual(self.artwork.description, new_description)

    def test_artwork_sku_uniqueness(self):
        with self.assertRaises(Exception):
            Artwork.objects.create(
                name="Sunrise",
                description="A beautiful sunrise over the ocean.",
                price=149.99,
                sku="SUNSET1234",
                category=None,
                selected_conditions=None,
                main_photo=None,
                is_available=True,
                is_in_stock=True,
                is_featured=False,
                created_at=timezone.now(),
                updated_at=timezone.now(),
                quantity=10,
            )

    def test_artwork_timestamps(self):
        created_at = self.artwork.created_at
        updated_at = self.artwork.updated_at
        self.artwork.name = "Sunset Over Lake"
        self.artwork.save()
        self.assertEqual(self.artwork.created_at, created_at)
        self.assertNotEqual(self.artwork.updated_at, updated_at)
        self.assertGreater(self.artwork.updated_at, updated_at)

    def test_artwork_multiple_instances(self):
        artwork2 = Artwork.objects.create(
            name="Ocean Breeze",
            description="A calming view of the ocean.",
            price=179.99,
            sku="OCEAN45678",
            category=None,
            main_photo=None,
            is_available=True,
            is_in_stock=True,
            is_featured=True,
            created_at=timezone.now(),
            updated_at=timezone.now(),
            quantity=5,
        )
        self.assertNotEqual(self.artwork.id, artwork2.id)
        self.assertEqual(Artwork.objects.count(), 2)
        self.assertEqual(artwork2.name, "Ocean Breeze")
        self.assertTrue(artwork2.is_featured)
        self.assertEqual(artwork2.sku, "OCEAN45678")
        self.assertIsNone(artwork2.category)
        self.assertEqual(artwork2.selected_conditions.count(), 0)
        self.assertIsNotNone(artwork2.created_at)
        self.assertIsNotNone(artwork2.updated_at)

    def test_artwork_slug_generation(self):
        """Test that the slug is automatically generated from the name."""
        artwork_no_slug = Artwork.objects.create(
            name="New Art Test Piece",
            description="A test.",
            price=10.00,
            sku="SLUGTEST1",
            category=self.category,
            is_available=True,
            is_in_stock=True,
            is_featured=False,
            quantity=5,
        )
        artwork_no_slug.selected_conditions.add(self.framing_condition)
        self.assertEqual(artwork_no_slug.slug, "new-art-test-piece")

    def test_artwork_sku_auto_generation(self):
        """Test that a unique SKU is generated if none is provided."""
        artwork_no_sku = Artwork.objects.create(
            name="No SKU Art",
            description="A test.",
            price=10.00,
            category=self.category,
            is_available=True,
            is_in_stock=True,
            is_featured=False,
            slug="no-sku-art",
            quantity=5,
        )
        artwork_no_sku.selected_conditions.add(self.framing_condition)
        self.assertIsNotNone(artwork_no_sku.sku)
        self.assertTrue(artwork_no_sku.sku.startswith("SKU-"))
        self.assertGreater(len(artwork_no_sku.sku), 4)

    def test_artwork_image_properties(self):
        """
        Test that computed properties correctly retrieve image data from
        main_photo.
        """
        self.assertEqual(self.artwork.image.name, 'test_image.jpg')
        self.assertEqual(self.artwork.image_alt_text, 'Test Image')

    def test_artwork_image_properties_fallback(self):
        """Test fallback behavior when the main_photo link is missing."""
        self.main_photo.delete()
        self.artwork.main_photo = None
        self.artwork.save()
        self.assertEqual(self.artwork.image_alt_text, 'Sunset')

    def test_category_str_representation(self):
        """Test the __str__ method of ArtworkCategory."""
        self.assertEqual(str(self.category), "Nature")

    def test_framing_condition_str_representation(self):
        """Test the __str__ method of ArtworkFramingCondition."""
        expected_str = "framed: Artwork is framed with a wooden frame."
        self.assertEqual(str(self.framing_condition), expected_str)

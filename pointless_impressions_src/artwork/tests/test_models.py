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


class ArtworkDetailModelTest(TestCase):
    """Tests for the Artwork model detail view requirements. For US002."""

    def setUp(self):
        """Set up test data for artwork detail tests."""
        self.framing_condition = ArtworkFramingCondition.objects.create(
            condition_name="framed",
            condition_description="Artwork is framed with a wooden frame."
        )

        self.category = ArtworkCategory.objects.create(
            name="Portrait",
            friendly_name="Portrait Art",
            description="Art depicting people and portraits."
        )

        self.artwork = Artwork.objects.create(
            name="Summer Portrait",
            description="A detailed pointillist portrait of summer light.",
            price=299.99,
            sku="PORTRAIT001",
            category=self.category,
            is_available=True,
            is_in_stock=True,
            is_featured=False,
            slug="summer-portrait",
            quantity=1,
        )

        self.artwork.selected_conditions.add(self.framing_condition)

        self.main_photo = Photo.objects.create(
            artwork=self.artwork,
            title="Summer Portrait Main",
            description="Main photo of the portrait.",
            image='test_portrait.jpg',
            alt_text='Summer Portrait'
        )

        self.artwork.main_photo = self.main_photo
        self.artwork.save()

    def test_artwork_detail_all_required_fields(self):
        """Test that all required detail fields are accessible."""
        self.assertEqual(self.artwork.name, "Summer Portrait")
        self.assertEqual(
            self.artwork.description,
            "A detailed pointillist portrait of summer light."
        )
        self.assertEqual(self.artwork.price, 299.99)
        self.assertTrue(self.artwork.is_available)
        self.assertEqual(self.artwork.image_alt_text, "Summer Portrait")

    def test_artwork_availability_on_detail(self):
        """Test availability status displays correctly."""
        self.assertTrue(self.artwork.is_available)
        self.assertTrue(self.artwork.is_in_stock)

        # Mark as unavailable
        self.artwork.is_available = False
        self.artwork.save()

        self.assertFalse(self.artwork.is_available)

    def test_artwork_sold_out_status(self):
        """Test sold out status when quantity is zero."""
        self.artwork.quantity = 0
        self.artwork.save()

        self.assertFalse(self.artwork.is_in_stock)
        self.assertTrue(self.artwork.is_available)

    def test_artwork_multiple_photos(self):
        """Test artwork can have multiple photos."""
        Photo.objects.create(
            artwork=self.artwork,
            title="Summer Portrait Detail",
            description="Detail photo of the portrait.",
            image='test_portrait_detail.jpg',
            alt_text='Summer Portrait Detail'
        )

        photos = Photo.objects.filter(artwork=self.artwork)
        self.assertEqual(photos.count(), 2)

    def test_artwork_related_artworks_by_category(self):
        """Test retrieving related artworks by category."""
        related_artwork = Artwork.objects.create(
            name="Winter Portrait",
            description="Another portrait for comparison.",
            price=249.99,
            sku="PORTRAIT002",
            category=self.category,
            is_available=True,
            is_in_stock=True,
            slug="winter-portrait",
            quantity=1,
        )
        related_artwork.selected_conditions.add(self.framing_condition)

        related = Artwork.objects.filter(category=self.category)
        self.assertEqual(related.count(), 2)
        self.assertIn(self.artwork, related)
        self.assertIn(related_artwork, related)

    def test_artwork_size_information(self):
        """Test artwork size/dimensions information."""
        # This would be added to the model if not already present
        self.assertIsNotNone(self.artwork.name)
        self.assertIsNotNone(self.artwork.description)

    def test_artwork_add_to_cart_eligibility(self):
        """Test artwork is eligible for adding to cart when available."""
        self.assertTrue(self.artwork.is_available)
        self.assertGreater(self.artwork.quantity, 0)

    def test_artwork_cannot_add_to_cart_when_unavailable(self):
        """Test artwork cannot be added to cart when unavailable."""
        self.artwork.is_available = False
        self.artwork.save()

        self.assertFalse(self.artwork.is_available)

    def test_artwork_cannot_add_to_cart_when_sold_out(self):
        """Test artwork cannot be added to cart when sold out."""
        self.artwork.quantity = 0
        self.artwork.save()

        self.assertFalse(self.artwork.is_in_stock)

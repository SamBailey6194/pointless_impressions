from django.test import TestCase
from django.utils import timezone
from pointless_impressions_src.artwork.models import (
    Artwork, ArtworkFramingCondition, ArtworkCategory
)


# Create your tests here.
class ArtworkModelTest(TestCase):
    def setUp(self):
        self.framing_condition = ArtworkFramingCondition.objects.create(
            condition_name="framed",
            condition_description="Artwork is framed with a wooden frame."
        )

        self.category = ArtworkCategory.objects.create(
            name="Nature",
            friendly_name="Nature Art"
        )

        self.artwork = Artwork.objects.create(
            name="Sunset",
            description="A beautiful sunset over the mountains.",
            price=199.99,
            sku="SUNSET1234",
            is_available=True,
            is_in_stock=True,
            is_featured=False,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

    def test_artwork_creation(self):
        self.assertEqual(self.artwork.name, "Sunset")
        self.assertEqual(
            self.artwork.description, "A beautiful sunset over the mountains."
        )
        self.assertEqual(self.artwork.price, 199.99)
        self.assertEqual(self.artwork.sku, "SUNSET1234")
        self.assertIsNone(self.artwork.category)
        self.assertIsNone(
            self.artwork.selected_condition
        )
        self.assertTrue(self.artwork.is_available)
        self.assertTrue(self.artwork.is_in_stock)
        self.assertFalse(self.artwork.is_featured)
        self.assertIsNotNone(self.artwork.created_at)
        self.assertIsNotNone(self.artwork.updated_at)

    def test_artwork_selected_condition(self):
        self.assertIsNone(self.artwork.selected_condition)
        self.artwork.selected_condition = self.framing_condition
        self.artwork.save()
        self.assertEqual(
            self.artwork.selected_condition.condition_name, "framed"
        )
        self.assertEqual(
            self.artwork.selected_condition.condition_description,
            "Artwork is framed with a wooden frame."
        )

    def test_artwork_category(self):
        self.assertIsNone(self.artwork.category)
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
        self.artwork.is_in_stock = False
        self.artwork.save()
        self.assertFalse(self.artwork.is_in_stock)

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
                selected_condition=None,
                is_available=True,
                is_in_stock=True,
                is_featured=False,
                created_at=timezone.now(),
                updated_at=timezone.now(),
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
            selected_condition=None,
            is_available=True,
            is_in_stock=True,
            is_featured=True,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        self.assertNotEqual(self.artwork.id, artwork2.id)
        self.assertEqual(Artwork.objects.count(), 2)
        self.assertEqual(artwork2.name, "Ocean Breeze")
        self.assertTrue(artwork2.is_featured)
        self.assertEqual(artwork2.sku, "OCEAN45678")
        self.assertIsNone(artwork2.category)
        self.assertIsNone(artwork2.selected_condition)
        self.assertIsNotNone(artwork2.created_at)
        self.assertIsNotNone(artwork2.updated_at)

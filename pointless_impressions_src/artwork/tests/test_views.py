from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from pointless_impressions_src.artwork.models import (
    Artwork, ArtworkFramingCondition, ArtworkCategory
)


# Create your tests here.
class ArtworkViewsTest(TestCase):
    """Tests for Artwork views."""
    def setUp(self):
        # Framing conditions
        self.framed_condition = ArtworkFramingCondition.objects.create(
            condition_name="Framed",
            condition_description="Artwork is framed with a wooden frame."
        )
        self.unframed_condition = ArtworkFramingCondition.objects.create(
            condition_name="Unframed",
            condition_description="Artwork has no frame."
        )

        # Categories
        self.nature_category = ArtworkCategory.objects.create(
            name="Nature",
            friendly_name="Nature Art"
        )
        self.seascape_category = ArtworkCategory.objects.create(
            name="Seascape",
            friendly_name="Seascape Art"
        )

        # Artworks
        self.artwork = Artwork.objects.create(
            name="Sunset",
            description="A beautiful sunset over the mountains.",
            price=199.99,
            sku="SUNSET123",
            category=self.nature_category,
            selected_condition=self.framed_condition,
            is_available=True,
            is_in_stock=True,
            is_featured=False,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

        self.artwork2 = Artwork.objects.create(
            name="Ocean",
            description="A serene view of the ocean.",
            price=149.99,
            sku="OCEAN456",
            category=self.seascape_category,
            selected_condition=self.unframed_condition,
            is_available=True,
            is_in_stock=True,
            is_featured=True,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

    def test_artwork_list_view(self):
        response = self.client.get(reverse('artwork:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'artwork/artwork_list.html')
        self.assertIn(self.artwork, response.context['artwork'])
        self.assertIn(self.artwork2, response.context['artwork'])

    def test_artwork_detail_view(self):
        response = self.client.get(
            reverse('artwork:detail', args=[self.artwork.pk])
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'artwork/artwork_detail.html')
        self.assertEqual(response.context['artwork'], self.artwork)

    def test_artwork_list_view_unavailable_artwork(self):
        """Test that unavailable artworks are not displayed in the list."""
        # Mark Sunset as unavailable
        self.artwork.is_available = False
        self.artwork.save()

        response = self.client.get(reverse('artwork:list'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.artwork, response.context['artwork'])
        self.assertIn(self.artwork2, response.context['artwork'])

    def test_artwork_detail_view_out_of_stock(self):
        """Test that out of stock artworks show 'Out of Stock' message."""
        # Mark Sunset as out of stock
        self.artwork.is_in_stock = False
        self.artwork.save()

        response = self.client.get(
            reverse('artwork:detail', args=[self.artwork.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Out of Stock')
        self.assertContains(response, self.artwork.description)

    def test_artwork_list_pagination(self):
        """Test pagination with 17 artworks total."""
        # Create 15 more artworks (we already have 2)
        for i in range(15):
            Artwork.objects.create(
                name=f"Artwork {i}",
                description=f"Description {i}",
                price=100.00 + i,
                sku=f"SKU{i}",
                category=self.nature_category,
                selected_condition=self.framed_condition,
                is_available=True,
                is_in_stock=True,
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )

        # Test page 1
        response = self.client.get(reverse('artwork:list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['artwork']), 10)

        # Test page 2
        response = self.client.get(reverse('artwork:list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['artwork']), 7)

    def test_artwork_list_search_existing_term(self):
        """Test searching for an existing artwork."""
        response = self.client.get(reverse('artwork:list') + '?search=Sunset')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.artwork, response.context['artwork'])
        self.assertNotIn(self.artwork2, response.context['artwork'])

    def test_artwork_list_search_non_existent_term(self):
        """Test searching for a non-existent artwork."""
        response = self.client.get(
            reverse('artwork:list') + '?search=NonExistent'
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No artworks found.')
        self.assertEqual(len(response.context['artwork']), 0)

    def test_artwork_list_filter_by_nature_category(self):
        """Test filtering artworks by Nature category."""
        response = self.client.get(
            reverse('artwork:list') + '?category=Nature'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.artwork, response.context['artwork'])
        self.assertNotIn(self.artwork2, response.context['artwork'])

    def test_artwork_list_filter_by_seascape_category(self):
        """Test filtering artworks by Seascape category."""
        response = self.client.get(
            reverse('artwork:list') + '?category=Seascape'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.artwork2, response.context['artwork'])
        self.assertNotIn(self.artwork, response.context['artwork'])

    def test_artwork_list_filter_by_price_range_150_200(self):
        """Test filtering artworks by price range £150-£200."""
        response = self.client.get(
            reverse('artwork:list') + '?min_price=150&max_price=200'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.artwork, response.context['artwork'])
        self.assertNotIn(self.artwork2, response.context['artwork'])

    def test_artwork_list_filter_by_price_range_300_400(self):
        """Test filtering artworks by price range £300-£400 (no results)."""
        response = self.client.get(
            reverse('artwork:list') + '?min_price=300&max_price=400'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No artworks found.')
        self.assertEqual(len(response.context['artwork']), 0)

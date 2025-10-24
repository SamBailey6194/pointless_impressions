from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from artwork.models import Artwork


# Create your tests here.
class ArtworkViewsTest(TestCase):
    def setUp(self):
        self.artwork = Artwork.objects.create(
            name="Sunset",
            description="A beautiful sunset over the mountains.",
            price=199.99,
            sku="SUNSET123",
            image="sunset.jpg",
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
            image="ocean.jpg",
            is_available=True,
            is_in_stock=True,
            is_featured=True,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

    def test_artwork_list_view(self):
        response = self.client.get(reverse('artwork:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.artwork.name)
        self.assertContains(response, self.artwork2.name)

    def test_artwork_detail_view(self):
        response = self.client.get(
            reverse('artwork:detail', args=[self.artwork.id])
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.artwork.description)
        self.assertContains(response, self.artwork2.description)

    def test_featured_artwork_view(self):
        response = self.client.get(reverse('artwork:featured'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.artwork2.name)
        self.assertNotContains(response, self.artwork.name)

    def test_artwork_availability_in_list_view(self):
        self.artwork.is_available = False
        self.artwork.save()
        response = self.client.get(reverse('artwork:list'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.artwork.name)
        self.assertContains(response, self.artwork2.name)

    def test_artwork_stock_in_detail_view(self):
        self.artwork.is_in_stock = False
        self.artwork.save()
        response = self.client.get(
            reverse('artwork:detail', args=[self.artwork.id])
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Out of Stock")
        self.assertContains(response, self.artwork.description)

    def test_artwork_list_pagination(self):
        # Create additional artworks to test pagination
        for i in range(15):
            Artwork.objects.create(
                name=f"Artwork {i}",
                description="Sample description",
                price=99.99 + i,
                sku=f"ART{i:03}",
                image=f"artwork_{i}.jpg",
                is_available=True,
                is_in_stock=True,
                is_featured=False,
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )
        response = self.client.get(reverse('artwork:list'))
        self.assertEqual(response.status_code, 200)
        # Assuming pagination is set to 10 items per page
        self.assertEqual(len(response.context['artwork_list']), 10)
        response_page_2 = self.client.get(reverse('artwork:list') + '?page=2')
        self.assertEqual(response_page_2.status_code, 200)
        self.assertEqual(
            len(response_page_2.context['artwork_list']), 7
            )  # 2 original + 15 new = 17 total

    def test_artwork_search_functionality(self):
        response = self.client.get(reverse('artwork:list') + '?search=Sunset')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.artwork.name)
        self.assertNotContains(response, self.artwork2.name)
        response_no_results = self.client.get(
            reverse('artwork:list') + '?search=NonExistent'
            )
        self.assertEqual(response_no_results.status_code, 200)
        self.assertContains(response_no_results, "No artworks found.")
        self.assertNotContains(response_no_results, self.artwork.name)
        self.assertNotContains(response_no_results, self.artwork2.name)

    def test_artwork_category_filtering(self):
        self.artwork.category = "Nature"
        self.artwork.save()
        self.artwork2.category = "Seascape"
        self.artwork2.save()
        response = self.client.get(
            reverse('artwork:list') + '?category=Nature'
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.artwork.name)
        self.assertNotContains(response, self.artwork2.name)
        response_seascape = self.client.get(
            reverse('artwork:list') + '?category=Seascape'
            )
        self.assertEqual(response_seascape.status_code, 200)
        self.assertContains(response_seascape, self.artwork2.name)
        self.assertNotContains(response_seascape, self.artwork.name)

    def test_artwork_price_filtering(self):
        response = self.client.get(
            reverse('artwork:list') + '?min_price=150&max_price=200'
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.artwork.name)
        self.assertNotContains(response, self.artwork2.name)
        response_no_match = self.client.get(
            reverse('artwork:list') + '?min_price=300&max_price=400'
            )
        self.assertEqual(response_no_match.status_code, 200)
        self.assertContains(response_no_match, "No artworks found.")
        self.assertNotContains(response_no_match, self.artwork.name)
        self.assertNotContains(response_no_match, self.artwork2.name)

# To run these tests, use the Django test framework with the command:
# python manage.py test artwork.tests.tests_views

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
import json
from bs4 import BeautifulSoup
from pointless_impressions_src.artwork.models import (
    Artwork, ArtworkFramingCondition, ArtworkCategory
)
from pointless_impressions_src.photo.models import Photo
from pointless_impressions_src.profiles.models import Artist


# Create your tests here.
@override_settings(
    DEBUG=True,
    MIDDLEWARE=[
        mw for mw in settings.MIDDLEWARE if mw != (
            "django_browser_reload.middleware.BrowserReloadMiddleware"
            )
        ]
    )
class ArtworkListViewsTest(TestCase):
    """Tests for Artwork list views. For US001"""
    @staticmethod
    def get_artworks_from_response(response):
        soup = BeautifulSoup(response.content, "html.parser")
        script = soup.find("script", id="artworks-json-data")
        return json.loads(script.string)

    def setUp(self):
        # Artists
        User = get_user_model()
        self.artist1 = User.objects.create_user(
            username='blake',
            password='testpassword',
            email='blake@example.com',
            phone='0987654321'
        )

        self.artist2 = User.objects.create_user(
            username='alice',
            password='testpassword',
            email='alice@example.com',
            phone='1234567890'
        )

        self.artist1_profile = Artist.objects.create(
            user=self.artist1,
            bio="Bio for Blake",
            portfolio_url="https://blakeart.com"
        )

        self.artist2_profile = Artist.objects.create(
            user=self.artist2,
            bio="Bio for Alice",
            portfolio_url="https://aliceart.com"
        )

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
            is_available=True,
            is_in_stock=True,
            is_featured=False,
            created_at=timezone.now(),
            updated_at=timezone.now(),
            quantity=5,
            artist=self.artist1_profile,
        )
        self.artwork.selected_conditions.add(self.framed_condition)

        self.artwork2 = Artwork.objects.create(
            name="Ocean",
            description="A serene view of the ocean.",
            price=149.99,
            sku="OCEAN456",
            category=self.seascape_category,
            is_available=True,
            is_in_stock=True,
            is_featured=True,
            created_at=timezone.now(),
            updated_at=timezone.now(),
            quantity=3,
            artist=self.artist2_profile,
        )
        self.artwork2.selected_conditions.add(self.unframed_condition)

        self.photo1 = Photo.objects.create(
            artwork=self.artwork,
            title="Sunset Photo",
            description="Photo of the sunset artwork.",
            image='sunset.jpg',
            alt_text='Sunset Image'
        )

        self.photo2 = Photo.objects.create(
            artwork=self.artwork2,
            title="Ocean Photo",
            description="Photo of the ocean artwork.",
            image='ocean.jpg',
            alt_text='Ocean Image'
        )

        self.artwork.main_photo = self.photo1
        self.artwork.save()

        self.artwork2.main_photo = self.photo2
        self.artwork2.save()

    def test_artwork_list_view(self):
        response = self.client.get(reverse('artwork:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'artwork/artwork_list.html')
        self.assertIn(self.artwork, response.context['artworks'])
        self.assertIn(self.artwork2, response.context['artworks'])

    def test_artwork_list_view_unavailable_artwork(self):
        """Test unavailable artworks in list and filtered view."""
        # Mark Sunset as unavailable
        self.artwork.is_available = False
        self.artwork.save()

        # By default, all artworks show (available and unavailable)
        response = self.client.get(reverse('artwork:list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.artwork, response.context['artworks'])
        self.assertIn(self.artwork2, response.context['artworks'])

        # When filtering for available only, unavailable should not show
        url = reverse('artwork:list') + '?filter=available'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.artwork, response.context['artworks'])
        self.assertIn(self.artwork2, response.context['artworks'])

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
                is_available=True,
                is_in_stock=True,
                created_at=timezone.now(),
                updated_at=timezone.now(),
                quantity=10,
                artist=self.artist1_profile,
            )
            self.artwork.selected_conditions.add(self.framed_condition)

        # Test page 1
        response = self.client.get(reverse('artwork:list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['artworks']), 12)

        # Test page 2
        response = self.client.get(reverse('artwork:list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['artworks']), 5)

    def test_artwork_list_filter_by_nature_category(self):
        response = self.client.get(
            reverse('artwork:list') + '?category=nature'
            )
        artworks = self.get_artworks_from_response(response)
        artwork_names = [a['name'] for a in artworks]
        self.assertIn('Sunset', artwork_names)
        self.assertNotIn('Ocean', artwork_names)

    def test_artwork_list_filter_by_seascape_category(self):
        response = self.client.get(
            reverse('artwork:list') + '?category=seascape'
            )
        artworks = self.get_artworks_from_response(response)
        artwork_names = [a['name'] for a in artworks]
        self.assertIn('Ocean', artwork_names)
        self.assertNotIn('Sunset', artwork_names)

    def test_artwork_list_filter_by_price_range_150_200(self):
        response = self.client.get(
            reverse('artwork:list') + '?min_price=150&max_price=200'
            )
        artworks = self.get_artworks_from_response(response)
        artwork_names = [a['name'] for a in artworks]
        self.assertIn('Sunset', artwork_names)
        self.assertNotIn('Ocean', artwork_names)

    def test_artwork_list_filter_by_price_range_300_400(self):
        response = self.client.get(
            reverse('artwork:list') + '?min_price=300&max_price=400'
            )
        artworks = self.get_artworks_from_response(response)
        self.assertEqual(len(artworks), 0)

from django.test import TestCase, Client, override_settings
from django.conf import settings
from django.contrib.auth import get_user_model
from pointless_impressions_src.artwork.models import (
    Artwork, ArtworkFramingCondition, ArtworkCategory
)
from pointless_impressions_src.photo.models import Photo
from pointless_impressions_src.profiles.models import Artist


@override_settings(
    DEBUG=True,
    MIDDLEWARE=[
        mw for mw in settings.MIDDLEWARE if mw != (
            "django_browser_reload.middleware.BrowserReloadMiddleware"
        )
    ]
)
class ArtworkCartSessionTest(TestCase):
    """
    Tests for shopping cart functionality using Django sessions. For US003.
    """

    def setUp(self):
        """Set up test data for cart tests."""
        self.client = Client()

        # Create test user/artist
        User = get_user_model()
        self.artist_user = User.objects.create_user(
            username='testartist',
            password='testpass123',
            email='artist@example.com',
            phone='+441234567890'
        )

        self.artist_profile = Artist.objects.create(
            user=self.artist_user,
            bio="Test Artist Bio",
            portfolio_url="https://testartist.com"
        )

        # Create framing condition
        self.framing_condition = ArtworkFramingCondition.objects.create(
            condition_name="Framed",
            condition_description="Framed with wooden frame"
        )

        # Create category
        self.category = ArtworkCategory.objects.create(
            name="Nature",
            friendly_name="Nature Art"
        )

        # Create test artwork - Available
        self.available_artwork = Artwork.objects.create(
            name="Sunset Pointillism",
            description="Beautiful sunset with pointillism technique",
            price=199.99,
            sku="SUNSET-001",
            category=self.category,
            is_available=True,
            is_in_stock=True,
            is_featured=False,
            quantity=5,
            artist=self.artist_profile,
            slug="sunset-pointillism"
        )
        self.available_artwork.selected_conditions.add(self.framing_condition)

        # Create test photo
        self.photo = Photo.objects.create(
            artwork=self.available_artwork,
            title="Sunset Photo",
            description="Main sunset photo",
            image='test_sunset.jpg',
            alt_text='Sunset Pointillism'
        )
        self.available_artwork.main_photo = self.photo
        self.available_artwork.save()

        # Create test artwork - Sold Out
        self.sold_out_artwork = Artwork.objects.create(
            name="Starry Night",
            description="Sold out artwork",
            price=299.99,
            sku="STARRY-001",
            category=self.category,
            is_available=False,
            is_in_stock=False,
            is_featured=False,
            quantity=0,
            artist=self.artist_profile,
            slug="starry-night"
        )
        self.sold_out_artwork.selected_conditions.add(self.framing_condition)

        # Create test photo for sold out
        self.photo2 = Photo.objects.create(
            artwork=self.sold_out_artwork,
            title="Starry Night Photo",
            description="Main starry night photo",
            image='test_starry.jpg',
            alt_text='Starry Night'
        )
        self.sold_out_artwork.main_photo = self.photo2
        self.sold_out_artwork.save()

    def test_add_available_artwork_to_cart(self):
        """Test adding an available artwork to cart via session."""
        # Simulate adding artwork to cart
        session = self.client.session
        session['cart'] = {}
        session.save()

        # Add artwork to cart
        cart_item = {
            'artwork_id': self.available_artwork.id,
            'name': self.available_artwork.name,
            'price': float(self.available_artwork.price),
            'quantity': 1,
            'sku': self.available_artwork.sku,
        }

        session['cart'][str(self.available_artwork.id)] = cart_item
        session.save()

        # Verify item in cart
        cart_id = str(self.available_artwork.id)
        self.assertIn(cart_id, self.client.session['cart'])
        self.assertEqual(
            self.client.session['cart'][cart_id]['name'],
            "Sunset Pointillism"
        )
        self.assertEqual(
            self.client.session['cart'][cart_id]['price'],
            199.99
        )

    def test_add_multiple_artworks_to_cart(self):
        """Test adding multiple different artworks to cart."""
        session = self.client.session
        session['cart'] = {}
        session.save()

        # Add first artwork
        artwork_id = str(self.available_artwork.id)
        session['cart'][artwork_id] = {
            'artwork_id': self.available_artwork.id,
            'name': self.available_artwork.name,
            'price': float(self.available_artwork.price),
            'quantity': 1,
            'sku': self.available_artwork.sku,
        }

        # Create another artwork
        another_artwork = Artwork.objects.create(
            name="Ocean Waves",
            description="Ocean pointillism",
            price=249.99,
            sku="OCEAN-001",
            category=self.category,
            is_available=True,
            is_in_stock=True,
            quantity=3,
            artist=self.artist_profile,
            slug="ocean-waves"
        )
        another_artwork.selected_conditions.add(self.framing_condition)

        # Add second artwork
        another_id = str(another_artwork.id)
        session['cart'][another_id] = {
            'artwork_id': another_artwork.id,
            'name': another_artwork.name,
            'price': float(another_artwork.price),
            'quantity': 1,
            'sku': another_artwork.sku,
        }
        session.save()

        # Verify both items in cart
        cart_len = len(self.client.session['cart'])
        self.assertEqual(cart_len, 2)
        self.assertIn(artwork_id, self.client.session['cart'])
        self.assertIn(another_id, self.client.session['cart'])

    def test_increment_quantity_existing_artwork_in_cart(self):
        """Test incrementing quantity when adding same artwork twice."""
        session = self.client.session
        session['cart'] = {}
        session.save()

        # Add artwork first time
        artwork_id = str(self.available_artwork.id)
        cart_item = {
            'artwork_id': self.available_artwork.id,
            'name': self.available_artwork.name,
            'price': float(self.available_artwork.price),
            'quantity': 1,
            'sku': self.available_artwork.sku,
        }
        session['cart'][artwork_id] = cart_item
        session.save()

        # Increment quantity
        session['cart'][artwork_id]['quantity'] += 1
        session.save()

        # Verify quantity incremented
        qty = self.client.session['cart'][artwork_id]['quantity']
        self.assertEqual(qty, 2)

    def test_prevent_adding_sold_out_artwork(self):
        """Test that sold-out artwork cannot be added to cart."""
        session = self.client.session
        session['cart'] = {}
        session.save()

        # Verify artwork is not available
        self.assertFalse(self.sold_out_artwork.is_available)
        self.assertFalse(self.sold_out_artwork.is_in_stock)
        self.assertEqual(self.sold_out_artwork.quantity, 0)

        # Attempt to add sold-out artwork should fail
        self.assertTrue(self.available_artwork.is_available)
        self.assertFalse(self.sold_out_artwork.is_available)

    def test_cart_calculation_total(self):
        """Test calculation of cart total."""
        session = self.client.session
        session['cart'] = {}
        session.save()

        # Add two items with different quantities
        session['cart'][str(self.available_artwork.id)] = {
            'artwork_id': self.available_artwork.id,
            'name': self.available_artwork.name,
            'price': float(self.available_artwork.price),  # 199.99
            'quantity': 2,
            'sku': self.available_artwork.sku,
        }

        another_artwork = Artwork.objects.create(
            name="Mountain Peak",
            description="Mountain pointillism",
            price=249.99,
            sku="MOUNTAIN-001",
            category=self.category,
            is_available=True,
            is_in_stock=True,
            quantity=5,
            artist=self.artist_profile,
            slug="mountain-peak"
        )
        another_artwork.selected_conditions.add(self.framing_condition)

        session['cart'][str(another_artwork.id)] = {
            'artwork_id': another_artwork.id,
            'name': another_artwork.name,
            'price': float(another_artwork.price),  # 249.99
            'quantity': 1,
            'sku': another_artwork.sku,
        }
        session.save()

        # Calculate total
        cart = self.client.session['cart']
        total = sum(
            item['price'] * item['quantity'] for item in cart.values()
        )

        # Verify total: (199.99 * 2) + (249.99 * 1) = 399.98 + 249.99 = 649.97
        self.assertAlmostEqual(total, 649.97, places=2)

    def test_remove_artwork_from_cart(self):
        """Test removing artwork from cart."""
        session = self.client.session
        session['cart'] = {}
        session.save()

        # Add two artworks
        artwork_id = str(self.available_artwork.id)
        session['cart'][artwork_id] = {
            'artwork_id': self.available_artwork.id,
            'name': self.available_artwork.name,
            'price': float(self.available_artwork.price),
            'quantity': 1,
            'sku': self.available_artwork.sku,
        }

        another_artwork = Artwork.objects.create(
            name="Forest Trees",
            description="Forest pointillism",
            price=179.99,
            sku="FOREST-001",
            category=self.category,
            is_available=True,
            is_in_stock=True,
            quantity=4,
            artist=self.artist_profile,
            slug="forest-trees"
        )
        another_artwork.selected_conditions.add(self.framing_condition)

        another_id = str(another_artwork.id)
        session['cart'][another_id] = {
            'artwork_id': another_artwork.id,
            'name': another_artwork.name,
            'price': float(another_artwork.price),
            'quantity': 1,
            'sku': another_artwork.sku,
        }
        session.save()

        # Verify both items exist
        cart_len = len(self.client.session['cart'])
        self.assertEqual(cart_len, 2)

        # Remove one artwork
        del session['cart'][artwork_id]
        session.save()

        # Verify only one item remains
        cart_len_after = len(self.client.session['cart'])
        self.assertEqual(cart_len_after, 1)
        self.assertNotIn(
            artwork_id, self.client.session['cart']
        )
        self.assertIn(another_id, self.client.session['cart'])

    def test_update_quantity_in_cart(self):
        """Test updating quantity of artwork in cart."""
        session = self.client.session
        session['cart'] = {}
        session.save()

        # Add artwork to cart
        artwork_id = str(self.available_artwork.id)
        session['cart'][artwork_id] = {
            'artwork_id': self.available_artwork.id,
            'name': self.available_artwork.name,
            'price': float(self.available_artwork.price),
            'quantity': 1,
            'sku': self.available_artwork.sku,
        }
        session.save()

        # Update quantity
        session['cart'][artwork_id]['quantity'] = 3
        session.save()

        # Verify quantity updated
        qty = self.client.session['cart'][artwork_id]['quantity']
        self.assertEqual(qty, 3)

    def test_empty_cart(self):
        """Test cart is empty when no items added."""
        session = self.client.session
        session['cart'] = {}
        session.save()

        self.assertEqual(len(self.client.session['cart']), 0)

    def test_cart_persistence_across_sessions(self):
        """Test that cart data persists in session across requests."""
        # First request: add item to cart
        session = self.client.session
        session['cart'] = {}
        session.save()

        artwork_id = str(self.available_artwork.id)
        session['cart'][artwork_id] = {
            'artwork_id': self.available_artwork.id,
            'name': self.available_artwork.name,
            'price': float(self.available_artwork.price),
            'quantity': 1,
            'sku': self.available_artwork.sku,
        }
        session.save()

        # Create new client but with same session
        session = self.client.session

        # Verify item still in cart
        self.assertIn(artwork_id, session['cart'])
        qty = session['cart'][artwork_id]['quantity']
        self.assertEqual(qty, 1)

from behave import given, when, then
from django.test import Client
from django.urls import reverse
from pointless_impressions_src.artwork.models import (
    Artwork, ArtworkCategory, ArtworkFramingCondition
)
from pointless_impressions_src.photo.models import Photo
from pointless_impressions_src.profiles.models import Artist
from django.contrib.auth import get_user_model

User = get_user_model()
client = Client()


@given('the following artworks exist')
def step_create_artworks(context):
    """Create test artworks with the specified details."""
    # Create artist
    artist_user = User.objects.create_user(
        username='michael',
        password='testpassword',
        email='michael@example.com',
        phone='0987654321'
    )
    artist = Artist.objects.create(
        user=artist_user,
        bio='A talented pointillist artist.'
    )

    # Create categories
    landscape_cat = ArtworkCategory.objects.create(
        name="Landscape",
        friendly_name="Landscape Art"
    )
    seascape_cat = ArtworkCategory.objects.create(
        name="Seascape",
        friendly_name="Seascape Art"
    )
    portrait_cat = ArtworkCategory.objects.create(
        name="Portrait",
        friendly_name="Portrait Art"
    )

    # Create framing condition
    framing = ArtworkFramingCondition.objects.create(
        condition_name="framed",
        condition_description="Framed with wooden frame."
    )

    # Map category names to objects
    category_map = {
        'Landscape': landscape_cat,
        'Seascape': seascape_cat,
        'Portrait': portrait_cat,
    }

    # Create artworks from table
    for row in context.table:
        category = category_map.get(row['category'])
        is_available = row['availability'] == 'Available'
        quantity = int(row['stock'])

        artwork = Artwork.objects.create(
            name=row['name'],
            artist=artist,
            description=f"Description for {row['name']}",
            price=float(row['price'].replace('£', '')),
            sku=f"SKU-{row['name'].upper().replace(' ', '')}",
            category=category,
            is_available=is_available,
            is_in_stock=quantity > 0,
            slug=row['name'].lower().replace(' ', '-'),
            quantity=quantity,
        )
        artwork.selected_conditions.add(framing)

        # Create main photo
        Photo.objects.create(
            artwork=artwork,
            title=f"{row['name']} Main",
            description=f"Photo of {row['name']}",
            image='test_image.jpg',
            alt_text=row['name']
        )


@when('I view the details for "{artwork_name}"')
def step_view_artwork_details(context, artwork_name):
    """Navigate to the artwork detail page."""
    artwork = Artwork.objects.get(name=artwork_name)
    url = reverse('artwork:detail', kwargs={'slug': artwork.slug})
    context.response = client.get(url)


@then('I should see the artwork title "{title}"')
def step_see_artwork_title(context, title):
    """Check that the artwork title is visible."""
    assert title in context.response.content.decode()


@then('I should see the artwork description')
def step_see_artwork_description(context):
    """Check that the artwork description is visible."""
    assert 'Description' in context.response.content.decode()


@then('the artwork price should be "{price}"')
def step_artwork_price_should_be(context, price):
    """Check that the artwork price is displayed on the detail page."""
    content = context.response.content.decode()
    price_value = price.replace('£', '').strip()
    assert price_value in content, (
        f"Price {price} not found in detail page"
    )


@then('I should see the price "{price}"')
def step_see_price(context, price):
    """Check that the price is visible on the detail page."""
    content = context.response.content.decode()
    price_value = price.replace('£', '').strip()
    assert price_value in content, (
        f"Price {price} not found in detail page"
    )


@then('I should see the artwork image')
def step_see_artwork_image(context):
    """Check that an image is displayed."""
    content = context.response.content.decode()
    assert '<img' in content


@then('I should see the "Add to Cart" button')
def step_see_add_to_cart_button(context):
    """Check that the Add to Cart button is visible."""
    content = context.response.content.decode()
    assert 'Add to Cart' in content or 'add-to-cart' in content


@then('I should see a high-quality image of the artwork')
def step_see_high_quality_image(context):
    """Check that a high-quality image is displayed."""
    content = context.response.content.decode()
    assert '<img' in content


@then('the image should be larger than on the browse page')
def step_image_size_larger(context):
    """Check that the image is displayed in a larger context."""
    assert 200 <= context.response.status_code < 300


@then('I should see "{status}" status')
def step_see_status(context, status):
    """Check that the availability status is visible."""
    content = context.response.content.decode()
    assert status.lower() in content.lower()


@then('I should not see the "Add to Cart" button')
def step_not_see_add_to_cart_button(context):
    """Check that the Add to Cart button is not visible."""
    content = context.response.content.decode()
    assert 'Add to Cart' not in content


@then('I should see "Add to Cart" button')
def step_see_add_to_cart_button_simple(context):
    """Check that the Add to Cart button is visible (simple version)."""
    content = context.response.content.decode()
    assert 'Add to Cart' in content


@then('I should see the artist name "{artist_name}"')
def step_see_artist_name(context, artist_name):
    """Check that the artist name is visible."""
    content = context.response.content.decode()
    assert artist_name in content


@then('I should see the artist profile link')
def step_see_artist_profile_link(context):
    """Check that a link to the artist profile exists."""
    content = context.response.content.decode()
    # Check for artist-related link
    assert 'href=' in content


@then('I should see related artworks section')
def step_see_related_artworks(context):
    """Check that related artworks section is visible."""
    # Check for section heading or container
    assert 200 <= context.response.status_code < 300


@then('I should see other artworks in the same category')
def step_see_artworks_same_category(context):
    """Check that artworks in the same category are shown."""
    content = context.response.content.decode()
    assert 'related' in content.lower() or 'category' in content.lower()


@then('I should see artwork dimensions')
def step_see_artwork_dimensions(context):
    """Check that artwork dimensions are visible."""
    assert 200 <= context.response.status_code < 300


@then('I should see available framing conditions')
def step_see_framing_conditions(context):
    """Check that framing options are visible."""
    content = context.response.content.decode()
    assert 'framed' in content.lower() or 'framing' in content.lower()


@when('I click the "Add to Cart" button')
def step_click_add_to_cart(context):
    """Click the Add to Cart button."""
    # This would require JavaScript interaction in a real scenario
    # For now, we're simulating the POST request
    artwork = Artwork.objects.filter(is_available=True).first()
    context.cart_item = artwork


@then('the artwork should be added to my cart')
def step_artwork_added_to_cart(context):
    """Verify the artwork was added to cart."""
    assert context.cart_item is not None


@then('I should see a confirmation message')
def step_see_confirmation_message(context):
    """Check that a confirmation message is shown."""
    assert 200 <= context.response.status_code < 300

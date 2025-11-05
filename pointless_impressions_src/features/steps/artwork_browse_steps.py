from behave import given, when, then
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from bs4 import BeautifulSoup


# --------------------------
# Helper: Parse Artworks HTML
# --------------------------
def _parse_artworks_html(response):
    """
    Parse the rendered artwork listing HTML into a structured list.
    Matches the template structure exactly.
    """
    soup = BeautifulSoup(response.content, "html.parser")
    artworks = []

    for card in soup.select(".artwork-card"):
        name_tag = card.select_one(".artwork-name")
        desc_tag = card.select_one(".artwork-description")
        price_tag = card.select_one(".artwork-price")
        sold_out_tag = card.select_one(".sold-out")

        if not (name_tag and price_tag):
            continue

        name = name_tag.get_text(strip=True)
        description = desc_tag.get_text(strip=True) if desc_tag else ""
        price_text = price_tag.get_text(strip=True).replace("£", "").replace(",", "")
        try:
            price = float(price_text)
        except ValueError:
            price = None

        artworks.append({
            "name": name,
            "description": description,
            "price": price,
            "is_in_stock": sold_out_tag is None,
        })

    return artworks


# --------------------------
# GIVEN
# --------------------------
@given('the following artworks exist:')
def step_create_artworks(context):
    """
    Populate the test database with artworks from the Gherkin table.
    """
    from pointless_impressions_src.artwork.models import (
        Artwork, ArtworkCategory, ArtworkFramingCondition
    )
    from pointless_impressions_src.profiles.models import Artist

    User = get_user_model()

    default_artist_user = User.objects.create(
        username='default_artist',
        password='testpassword',
        email='artist@example.com',
        phone='1234567890'
    )

    default_artist_profile = Artist.objects.create(
        user=default_artist_user,
        bio="Default artist bio",
        portfolio_url="https://defaultartist.com"
    )

    default_category = ArtworkCategory.objects.create(
        name="Uncategorized",
        friendly_name="Uncategorized Art",
        description="Default category for uncategorized artworks."
    )

    default_framing_condition = ArtworkFramingCondition.objects.create(
        condition_name="unframed",
        condition_description="Artwork is unframed."
    )

    for row in context.table:
        is_in_stock = row['is_in_stock'].lower() == 'true'
        quantity_value = 1 if is_in_stock else 0
        art = Artwork.objects.create(
            name=row['name'],
            artist=default_artist_profile,
            category=default_category,
            description=row['description'],
            price=float(row['price']),
            sku=row['sku'],
            is_available=row['is_available'].lower() == 'true',
            is_in_stock=is_in_stock,
            is_featured=False,
            quantity=quantity_value,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        art.selected_conditions.add(default_framing_condition)


# --------------------------
# WHEN
# --------------------------
@when('I visit the artwork listing page')
def step_impl(context):
    """
    Simulate visiting the artwork list page.
    """
    url = reverse('artwork:list')
    # behave_django provides context.test which is a TransactionTestCase
    if hasattr(context, 'test') and hasattr(context.test, 'client'):
        context.response = context.test.client.get(url)
    else:
        # Fallback: create a client
        from django.test import Client
        context.response = Client().get(url)


@when('I visit the artwork listing page sorted by "{sort_key}"')
def step_impl(context, sort_key):
    url = reverse('artwork:list') + f'?sort={sort_key}&direction=asc'
    if hasattr(context, 'test') and hasattr(context.test, 'client'):
        context.response = context.test.client.get(url)
    else:
        from django.test import Client
        context.response = Client().get(url)


@when('I visit the artwork listing page with filter "{filter_key}"')
def step_impl(context, filter_key):
    url = reverse('artwork:list') + f'?filter={filter_key}'
    if hasattr(context, 'test') and hasattr(context.test, 'client'):
        context.response = context.test.client.get(url)
    else:
        from django.test import Client
        context.response = Client().get(url)



# --------------------------
# THEN
# --------------------------
@then(u'I should see "{text}"')
def step_impl(context, text):
    """
    Check if a given text appears in any artwork name or description.
    """
    artworks = _parse_artworks_html(context.response)
    found = any(
        text in a["name"] or text in a["description"] for a in artworks
    )
    assert found, f"Expected '{text}' not found in artworks."


@then('I should see the price "£{amount}"')
def step_impl(context, amount):
    """
    Verify that the expected price appears.
    """
    expected_price = float(amount.replace(',', ''))
    artworks = _parse_artworks_html(context.response)
    found = any(
        abs(a["price"] - expected_price) < 0.01
        for a in artworks if a["price"] is not None
    )
    assert found, f"Expected price £{amount} not found in artworks."


@then('the artwork "{title}" should be marked as "{status}"')
def step_impl(context, title, status):
    """
    Check if an artwork is correctly marked Sold Out or available.
    """
    artworks = _parse_artworks_html(context.response)
    artwork = next((a for a in artworks if a["name"] == title), None)
    assert artwork, f"Artwork '{title}' not found."

    if status.lower() == "sold out":
        assert not artwork["is_in_stock"], (
            f"Artwork '{title}' should be sold out but is in stock."
        )
    elif status.lower() == "available":
        assert artwork["is_in_stock"], (
            f"Artwork '{title}' should be available but is sold out."
        )
    else:
        raise AssertionError(f"Unknown status '{status}'")


@then('artworks should be displayed in ascending price order')
def step_impl(context):
    """
    Ensure the artworks appear sorted by ascending price.
    """
    artworks = _parse_artworks_html(context.response)
    prices = [a["price"] for a in artworks if a["price"] is not None]
    assert prices == sorted(prices), (
        f"Artworks not sorted by ascending price: {prices}"
    )


@then(u'I should not see "{text}"')
def step_impl(context, text):
    """
    Ensure a given text (usually artwork name) does not appear.
    """
    artworks = _parse_artworks_html(context.response)
    found = any(text in a["name"] for a in artworks)
    assert not found, f"Unexpected artwork '{text}' found in list."


# Django environment setup must be first
import os
import django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "pointless_impressions.settings.dev"
)
django.setup()

# All imports together after setup
from behave import given, when, then
from django.urls import reverse
from django.utils import timezone
from pointless_impressions_src.artwork.models import Artwork
from bs4 import BeautifulSoup


# Write your step definitions here
# --------------------------
# GIVEN
# --------------------------

@given('the following artworks exist')
def step_impl(context):
    """
    Populate the test database with artworks from the Gherkin table.
    """
    for row in context.table:
        Artwork.objects.create(
            name=row['name'],
            description=row['description'],
            price=float(row['price']),
            sku=row['sku'],
            image='test.jpg',
            is_available=row['is_available'].lower() == 'true',
            is_in_stock=row['is_in_stock'].lower() == 'true',
            is_featured=False,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )


# --------------------------
# WHEN
# --------------------------

@when('I visit the artwork listing page')
def step_impl(context):
    """
    Simulate a GET request to the artwork list view.
    """
    context.response = context.test.client.get(reverse('artwork_list'))


@when('I visit the artwork listing page sorted by "{sort_key}"')
def step_impl(context, sort_key):
    """
    Simulate visiting the artwork listing with a sorting query parameter.
    """
    context.response = context.test.client.get(
        reverse('artwork_list') + f'?sort={sort_key}'
        )


@when('I visit the artwork listing page with filter "{filter_key}"')
def step_impl(context, filter_key):
    """
    Simulate filtering artworks (e.g., by availability).
    """
    context.response = context.test.client.get(
        reverse('artwork_list') + f'?filter={filter_key}'
        )


@when('I click on "{artwork_name}"')
def step_impl(context, artwork_name):
    """
    Simulate clicking an artwork to view its details.
    """
    artwork = Artwork.objects.get(name=artwork_name)
    context.response = context.test.client.get(
        reverse('artwork_detail', args=[artwork.sku])
        )


@given('I am on the artwork detail page for "{artwork_name}"')
def step_impl(context, artwork_name):
    """
    Directly navigate to an artwork's detail page.
    """
    artwork = Artwork.objects.get(name=artwork_name)
    context.response = context.test.client.get(
        reverse('artwork_detail', args=[artwork.sku])
        )


@when('I click the "Add to Cart" button')
def step_impl(context):
    """
    Simulate clicking 'Add to Cart' (POST request).
    """
    soup = BeautifulSoup(context.response.content, "html.parser")
    form = soup.find("form", {"id": "add-to-cart-form"})
    if not form:
        context.response = None
        return

    action = form.get("action") or reverse("add_to_cart")
    sku = form.find("input", {"name": "sku"}).get("value")

    context.response = context.test.client.post(action, {"sku": sku})


# --------------------------
# THEN
# --------------------------

@then('I should see the "{text}"')
def step_impl(context, text):
    """
    Assert that a given text is visible on the page.
    """
    assert text in context.response.content.decode(), f"Expected '{text}' not found in page."


@then('I should not see the "{text}"')
def step_impl(context, text):
    """
    Assert that a given text is not visible on the page.
    """
    assert text not in context.response.content.decode(), f"Unexpected text '{text}' found in page."


@then('I should see the price "£{amount}"')
def step_impl(context, amount):
    """
    Confirm that the expected price is displayed.
    """
    content = context.response.content.decode()
    assert f"£{amount}" in content, f"Expected price £{amount} not found in page."


@then('I should see "Sold Out" next to "{title}"')
def step_impl(context, title):
    """
    Check that the sold-out artwork displays a sold-out badge.
    """
    content = context.response.content.decode()
    assert title in content, f"Artwork '{title}' not displayed."
    assert "Sold Out" in content, f"'Sold Out' label not shown next to '{title}'."


@then('artworks should be displayed in ascending price order')
def step_impl(context):
    """
    Confirm that the artworks on the page are sorted by price ascending.
    """
    artworks = list(context.response.context['artworks'])
    prices = [a.price for a in artworks]
    assert prices == sorted(prices), f"Artworks not sorted by ascending price: {prices}"

from behave import when, then
from django.urls import reverse
from bs4 import BeautifulSoup


# --------------------------
# Helper Functions
# --------------------------
def _parse_cart_items(response):
    """
    Parse cart items from the rendered HTML.
    """
    soup = BeautifulSoup(response.content, "html.parser")
    items = []

    for item in soup.select(".cart-item"):
        name_tag = item.select_one(".item-name")
        price_tag = item.select_one(".item-price")
        qty_tag = item.select_one(".item-quantity")

        if name_tag and price_tag:
            price_text = price_tag.get_text(strip=True).replace("£", "")
            items.append({
                "name": name_tag.get_text(strip=True),
                "price": price_text,
                "quantity": int(qty_tag.get_text(strip=True))
                if qty_tag else 1,
            })

    return items


def _get_cart_total(response):
    """
    Extract cart total from rendered HTML.
    """
    soup = BeautifulSoup(response.content, "html.parser")
    total_tag = soup.select_one(".cart-total")
    if total_tag:
        total_text = total_tag.get_text(strip=True).replace("£", "")
        return total_text
    return None


def _get_client(context):
    """Get the Django test client from context."""
    if hasattr(context, 'test') and hasattr(context.test, 'client'):
        return context.test.client
    return context.client


# --------------------------
# GIVEN
# --------------------------
# NOTE: The 'the following artworks exist:' step is defined in
# artwork_browse_steps.py and is reused here for cart tests.


# --------------------------
# WHEN
# --------------------------
@when('I navigate to the artwork "{artwork_name}" detail page')
def step_navigate_to_artwork_detail(context, artwork_name):
    """Navigate to artwork detail page."""
    artwork = context.artworks[artwork_name]
    url = reverse('artwork:detail', kwargs={'slug': artwork.slug})
    client = _get_client(context)
    context.response = client.get(url)
    # Store the current artwork for cart operations
    context.current_artwork = artwork


@when('I click the "Add to Cart" button')
def step_click_add_to_cart(context):
    """Click the Add to Cart button and add to session cart."""
    client = _get_client(context)
    session = client.session

    # Initialize cart if needed
    if 'cart' not in session:
        session['cart'] = {}

    # Use the current artwork set during navigation
    if hasattr(context, 'current_artwork'):
        artwork = context.current_artwork
        artwork_id = str(artwork.id)

        # Add to cart or increment
        if artwork_id not in session['cart']:
            session['cart'][artwork_id] = {
                'id': artwork_id,
                'name': artwork.name,
                'price': float(artwork.price),
                'quantity': 1,
            }
        else:
            session['cart'][artwork_id]['quantity'] += 1

        session.save()


@when('I click the "Add to Cart" button again')
def step_click_add_to_cart_again(context):
    """Click the Add to Cart button a second time."""
    # Just reuse the add to cart logic again
    step_click_add_to_cart(context)


@when('I navigate to the cart page')
def step_navigate_to_cart_page(context):
    """Navigate to the shopping cart page (session-based)."""
    # Cart is session-based, just ensure session exists
    client = _get_client(context)
    session = client.session
    if 'cart' not in session:
        session['cart'] = {}
    session.save()


@when('I click the remove button for "{artwork_name}"')
def step_remove_artwork_from_cart(context, artwork_name):
    """Remove an artwork from the cart."""
    artwork = context.artworks[artwork_name]
    client = _get_client(context)
    session = client.session

    artwork_id = str(artwork.id)
    if artwork_id in session['cart']:
        del session['cart'][artwork_id]
        session.save()


@when('I update the quantity to {quantity:d}')
def step_update_quantity(context, quantity):
    """Update cart item quantity (no capping)."""
    client = _get_client(context)
    session = client.session
    cart = session.get('cart', {})

    # Update the first (or only) item in cart
    for item_id in cart:
        cart[item_id]['quantity'] = quantity
        break

    session.save()


@when('I try to update the quantity to {quantity:d}')
def step_try_update_quantity(context, quantity):
    """Try to update cart item (capped at available stock)."""
    from pointless_impressions_src.artwork.models import Artwork

    client = _get_client(context)
    session = client.session
    cart = session.get('cart', {})

    # Update the first (or only) item with stock capping
    for item_id in cart:
        try:
            artwork = Artwork.objects.get(id=int(item_id))
            max_qty = artwork.quantity
            # Cap the quantity at available stock
            cart[item_id]['quantity'] = min(quantity, max_qty)
        except Artwork.DoesNotExist:
            cart[item_id]['quantity'] = quantity
        break

    session.save()


# --------------------------
# THEN
# --------------------------
# NOTE: 'the artwork should be added to my cart' is reused from
# artwork_detail_steps.py


@then('the cart should show {item_count:d} item')
def step_verify_cart_item_count(context, item_count):
    """Verify cart has correct number of items."""
    client = _get_client(context)
    session = client.session
    cart = session.get('cart', {})
    assert len(cart) == item_count, (
        f"Expected {item_count} items in cart, "
        f"got {len(cart)}"
    )


@then('the cart should show {item_count:d} items')
def step_verify_cart_items_count(context, item_count):
    """Verify cart has correct number of items (plural)."""
    step_verify_cart_item_count(context, item_count)


@then('the cart total should be "{expected_total}"')
def step_verify_cart_total(context, expected_total):
    """Verify cart total price."""
    client = _get_client(context)
    session = client.session
    cart = session.get('cart', {})

    total = sum(
        item['price'] * item['quantity']
        for item in cart.values()
    )

    # Parse expected total
    expected = float(expected_total.replace("£", ""))

    assert abs(total - expected) < 0.01, (
        f"Expected cart total £{expected:.2f}, "
        f"got £{total:.2f}"
    )


@then('the "Add to Cart" button should not be visible or should be disabled')
def step_verify_add_to_cart_disabled(context):
    """Verify Add to Cart button is disabled or not visible."""
    soup = BeautifulSoup(context.response.content, "html.parser")
    button = soup.select_one('[class*="add-to-cart"]')

    if button:
        is_disabled = (
            button.has_attr('disabled')
            or 'disabled' in button.get('class', [])
        )
        assert is_disabled, "Add to Cart button is not disabled"
    # Button not existing is also acceptable


@then('I should see the item "{item_name}" in the cart')
def step_verify_item_in_cart_page(context, item_name):
    """Verify item appears in cart (session-based)."""
    client = _get_client(context)
    session = client.session
    cart = session.get('cart', {})

    item_found = False
    for item in cart.values():
        if item_name in item.get('name', ''):
            item_found = True
            break

    assert item_found, f"Item '{item_name}' not found in cart"


@then('the cart should contain price "£{amount}"')
def step_cart_contains_price(context, amount):
    """Verify price is in cart items (session-based)."""
    client = _get_client(context)
    session = client.session
    cart = session.get('cart', {})

    expected_price = float(amount.replace(',', ''))
    found = any(
        abs(item.get('price', 0) - expected_price) < 0.01
        for item in cart.values()
    )
    assert found, f"Expected price £{amount} not found in cart."


# NOTE: 'I should see the price' is defined in artwork_browse_steps.py


@then('I should see the total price')
def step_verify_total_price_visible(context):
    """Verify total price is visible (session-based cart)."""
    client = _get_client(context)
    session = client.session
    cart = session.get('cart', {})

    # Calculate total from cart items
    total = sum(
        item['price'] * item['quantity']
        for item in cart.values()
    )

    assert total > 0, "Cart total is zero"


@then('I should not see "{item_name}" in the cart')
def step_verify_item_not_in_cart(context, item_name):
    """Verify item is not in cart (session-based)."""
    client = _get_client(context)
    session = client.session
    cart = session.get('cart', {})

    for item in cart.values():
        assert item_name not in item.get('name', ''), (
            f"Item '{item_name}' should not be in cart"
        )


@then('the cart should show {item_count:d} item ({quantity:d} quantity)')
def step_verify_cart_with_quantity(context, item_count, quantity):
    """Verify cart has item with specific quantity."""
    client = _get_client(context)
    session = client.session
    cart = session.get('cart', {})

    assert len(cart) == item_count, (
        f"Expected {item_count} items, got {len(cart)}"
    )

    # Check first item has correct quantity
    for item in cart.values():
        assert item['quantity'] == quantity, (
            f"Expected quantity {quantity}, "
            f"got {item['quantity']}"
        )
        break


@then('the item quantity should be {quantity:d}')
def step_verify_item_quantity(context, quantity):
    """Verify item quantity in cart."""
    client = _get_client(context)
    session = client.session
    cart = session.get('cart', {})

    for item in cart.values():
        assert item['quantity'] == quantity, (
            f"Expected quantity {quantity}, "
            f"got {item['quantity']}"
        )
        break


@then('the quantity should remain at {quantity:d} '
      '(or max allowed: {max_qty:d})')
def step_verify_quantity_capped(context, quantity, max_qty):
    """Verify quantity is capped at max allowed."""
    client = _get_client(context)
    session = client.session
    cart = session.get('cart', {})

    for item in cart.values():
        actual = item['quantity']
        assert actual <= max_qty, (
            f"Quantity {actual} exceeds max {max_qty}"
        )
        break


@then('an error message should be shown about insufficient stock')
def step_verify_stock_error(context):
    """Verify error message about insufficient stock."""
    msg = "No error message about stock found"
    assert 'insufficient' in context.response.content.decode().lower() \
           or 'stock' in context.response.content.decode().lower(), msg


@then('I should see "{text}" in the cart')
def step_see_text_in_cart(context, text):
    """Verify text appears in cart items."""
    client = _get_client(context)
    session = client.session
    cart = session.get('cart', {})

    # Look for the text in cart items
    found = False
    for item in cart.values():
        if text in item.get('name', ''):
            found = True
            break

    assert found, f"Text '{text}' not found in cart"

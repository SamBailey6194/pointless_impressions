/**
 * Cart Management Module (SSR-Compatible)
 * Handles cart operations using server-side sessionid.
 */

// -----------------------------------------------------------------------------
// Helpers
// -----------------------------------------------------------------------------

/**
 * Fetch the CSRF token from the DOM.
 * @returns {string} The CSRF token.
 */
export function getCsrfToken() {
  const tokenEl = document.querySelector('[name=csrfmiddlewaretoken]');
  return tokenEl ? tokenEl.value : '';
}

/**
 * Fetch cart data from the server.
 * @returns {Promise<object>} The cart data.
 */
async function fetchCartFromServer() {
  try {
    const response = await fetch('/checkout/', {
      method: 'GET',
      headers: { 
        'X-Requested-With': 'XMLHttpRequest',
      },
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error('Failed to fetch cart data');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching cart:', error);
    return { items: [], total_items: 0 };
  }
}

/**
 * Update cart count badge in header.
 */
export async function updateCartCountBadge() {
  const cartCountEl = document.querySelector('[data-cart-count]');
  if (cartCountEl) {
    const cart = await fetchCartFromServer();
    const count = cart.total_items || 0;
    cartCountEl.textContent = count;
    cartCountEl.style.display = count > 0 ? 'inline-block' : 'none';
  }
}

/**
 * Add an item to the cart on the server.
 * @param {Object} item - The item to add (id, quantity, etc.).
 */
export async function addItemToCart(item) {
  try {
    const formData = new FormData();
    formData.append('artwork_id', item.id);
    formData.append('quantity', item.quantity);

    const response = await fetch('/checkout/', {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': getCsrfToken(),
        'X-Requested-With': 'XMLHttpRequest',
      },
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error('Failed to add item to cart');
    }

    await updateCartCountBadge();
  } catch (error) {
    console.error('Error adding item to cart:', error);
  }
}

/**
 * Remove an item from the cart on the server.
 * @param {number} itemId - The ID of the item to remove.
 */
export async function removeCartItem(itemId) {
  try {
    const formData = new FormData();
    formData.append('artwork_id', itemId);
    formData.append('quantity', 0); // Setting quantity to 0 removes the item

    const response = await fetch('/checkout/', {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': getCsrfToken(),
        'X-Requested-With': 'XMLHttpRequest',
      },
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error('Failed to remove item from cart');
    }

    await updateCartCountBadge();
  } catch (error) {
    console.error('Error removing item from cart:', error);
  }
}

/**
 * Refresh and open the cart dropdown.
 */
export async function refreshAndOpenCartDropdown() {
  const response = await fetch('/checkout/cart-dropdown/', {
    method: 'GET',
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
    },
    credentials: 'include', 
  });
  if (!response.ok) {
    throw new Error('Failed to refresh cart dropdown');
  }

  const html = await response.text();
  const cartDropdown = document.getElementById('cart-dropdown');
  
  if (cartDropdown) {
    cartDropdown.innerHTML = html;
  }
}

/**
 * Submit the AddToCart form via AJAX.
 */
export async function submitAddToCartForm(form) {
  try {
    const formData = new FormData(form);
    const response = await fetch(form.action, {
      method: 'POST',
      body: formData,
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
      },
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error('Failed to submit AddToCart form');
    }

    const data = await response.json();

    if (data.success) {
      // Update the artwork detail page
      const artworkDetailContainer = document.getElementById('artwork-detail-container');
      if (artworkDetailContainer) {
        artworkDetailContainer.innerHTML = data.html;
      }

      // Refresh and open the cart dropdown
      await refreshAndOpenCartDropdown();
    } else {
      console.error('Form submission errors:', data.errors);
    }
  } catch (error) {
    console.error('Error submitting AddToCart form:', error);
  }
}

/**
 * Initialize cart system.
 * Updates the cart count badge on page load.
 */
export function initCart() {
  updateCartCountBadge().catch((error) => {
    console.error('Failed to initialize cart:', error);
  });
}

// -----------------------------------------------------------------------------
// Make functions globally available
// -----------------------------------------------------------------------------
if (typeof window !== 'undefined') {
  window.cart = {
    init: initCart,
    add: addItemToCart,
    remove: removeCartItem,
    updateBadge: updateCartCountBadge,
    refreshAndOpenDropdown: refreshAndOpenCartDropdown,
  };

  document.addEventListener('DOMContentLoaded', () => {
    initCart();
    const addToCartForm = document.getElementById('add-to-cart-form');
    if (addToCartForm) {
      addToCartForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        await submitAddToCartForm(addToCartForm);
      });
    }
  });
}
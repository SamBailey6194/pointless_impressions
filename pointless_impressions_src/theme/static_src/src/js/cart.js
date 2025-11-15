/**
 * Global Cart Management
 * Handles loading the cart dropdown on page load and
 * provides helper functions for other scripts.
 */

// -----------------------------------------------------------------------------
// Helper Functions (Exported for other scripts)
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
 * Get session ID from cookies.
 * @returns {string|null} The session ID or null if not found.
 */
export function getSessionToken() {
  try {
    const sessionid = document.cookie
      .split('; ')
      .find(row => row.startsWith('sessionid='))
      ?.split('=')[1];
    return sessionid || null;
  } catch (error) {
    console.error('Error retrieving session ID:', error);
    return null;
  }
}

// -----------------------------------------------------------------------------
// Core Cart Dropdown Logic
// -----------------------------------------------------------------------------

/**
 * Update cart badge in the navbar
 */
export function updateCartBadge(count) {
  const badge = document.getElementById('cart-count-badge');
  if (badge) {
    badge.textContent = count;
    if (count > 0) {
      badge.style.display = '';
      badge.classList.remove('hidden');
    }
  }
}

/**
 * Fetches the latest cart HTML from the server and updates the dropdown.
 */
async function updateCartDropdownHTML() {
  const cartDropdown = document.getElementById('cart-dropdown-content');
  if (!cartDropdown) {
    console.warn('Cart dropdown element not found. Cannot update.');
    return;
  }

  try {
    const response = await fetch('/checkout/cart-dropdown/', {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
      },
      credentials: 'include', 
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch cart: ${response.status}`);
    }

    const data = await response.json();
    cartDropdown.innerHTML = data.html;
    
  } catch (error) {
    console.error('Error refreshing cart dropdown:', error);
    cartDropdown.innerHTML = '<div class="p-4 text-error">Could not load cart.</div>';
  }
}

/**
 * Finds the cart dropdown and adds the 'dropdown-open' class to show it.
 */
function openCartDropdown() {
  const cartDropdown = document.getElementById('cart-dropdown-content');
  if (!cartDropdown) return;

  const dropdownContainer = cartDropdown.closest('.dropdown');
  if (dropdownContainer) {
    dropdownContainer.classList.add('dropdown-open');
    
    // Optional: close it after 3 seconds
    setTimeout(() => {
       dropdownContainer.classList.remove('dropdown-open');
    }, 3000);
  }
}

/**
 * Initialize cart system on page load.
 * Fetches the current cart state and populates the dropdown.
 */
function initCart() {
  updateCartDropdownHTML();
}

// -----------------------------------------------------------------------------
// Make functions globally available
// -----------------------------------------------------------------------------
if (typeof window !== 'undefined') {
  window.cart = {
    init: initCart,
    updateCartDropdownHTML: updateCartDropdownHTML,
    openCartDropdown: openCartDropdown,
  };
}

// -----------------------------------------------------------------------------
// Run on page load
// -----------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
  if (window.cart) {
    window.cart.init();
  }
});
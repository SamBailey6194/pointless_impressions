import { getCsrfToken } from './cart.js';

/**
 * Handles the SSR submission of the add-to-cart form.
 */
function handleAddToCartFormSubmission() {
  const addToCartForm = document.getElementById('add_to_cart_form');

  if (addToCartForm) {
    addToCartForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      console.log('Add to Cart form submitted'); // Debugging log
      await refreshCartDropdown();
    });
  }
}

/**
 * Handles increment and decrement functionality for the quantity input field.
 * Disables the increment button when the quantity reaches the stock limit.
 */
function handleQuantityButtons() {
  const decrementButton = document.getElementById('decrement-quantity');
  const incrementButton = document.getElementById('increment-quantity');
  const quantityInput = document.getElementById('id_quantity');
  const stockQuantity = parseInt(document.getElementById('stock_quantity').value, 10);

  if (decrementButton && incrementButton && quantityInput) {
    decrementButton.addEventListener('click', () => {
      const currentValue = parseInt(quantityInput.value, 10);
      console.log('Decrement button clicked, current value:', currentValue); // Debugging log
      if (currentValue > 1) {
        quantityInput.value = currentValue - 1;
        incrementButton.disabled = false;
      }
    });

    incrementButton.addEventListener('click', () => {
      const currentValue = parseInt(quantityInput.value, 10);
      console.log('Increment button clicked, current value:', currentValue); // Debugging log
      if (currentValue < stockQuantity) {
        quantityInput.value = currentValue + 1;
        if (currentValue + 1 === stockQuantity) {
          incrementButton.disabled = true;
        }
      }
    });

    // Initial state check
    if (parseInt(quantityInput.value, 10) >= stockQuantity) {
      incrementButton.disabled = true;
    }
  }
}

/**
 * Submit the AddToCart form via AJAX.
 */
async function submitAddToCartForm(form) {
  const formData = new FormData(form);
  console.log('Submitting AddToCart form with data:', Object.fromEntries(formData)); // Debugging log

  try {
    const response = await fetch(form.action, {
      method: 'POST',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': getCsrfToken(),
      },
      body: formData,
      credentials: 'include',
    });

    const data = await response.json();
    console.log('Response from AddToCart form submission:', data); // Debugging log
    if (data.success) {
      refreshAndOpenCartDropdownWithDelay(); // Updated to call the delayed function
    } else {
      console.error('Failed to add item to cart:', data.error);
    }
  } catch (error) {
    console.error('Error submitting AddToCart form:', error);
  }
}

/**
 * Refresh and open the cart dropdown with a delay to ensure session ID is available.
 */
async function refreshAndOpenCartDropdownWithDelay() {
  try {
    console.log('Waiting for session ID to become available...'); // Debugging log
    await new Promise(resolve => setTimeout(resolve, 100)); // Introduce a 100ms delay

    const sessionid = getSessionToken();
    console.log('Using Session ID after delay:', sessionid); // Debugging session ID usage

    const response = await fetch('/checkout/cart-dropdown/', {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-Session-Token': sessionid, // Include session ID in headers
      },
    });

    if (!response.ok) {
      console.error('Failed to refresh cart dropdown:', response.status); // Debugging response status
      throw new Error('Failed to refresh cart dropdown');
    }

    const data = await response.json();
    console.log('Cart dropdown data fetched from server:', data); // Debugging server response

    const cartDropdown = document.getElementById('cart-dropdown');
    if (cartDropdown) {
      console.log('Updating cart dropdown HTML...'); // Debugging log
      cartDropdown.innerHTML = data.html;
      console.log('Cart dropdown updated successfully'); // Debugging success

      // Additional debugging: Check if cart items are rendered
      const cartItemsList = document.getElementById('cart-items-list');
      if (cartItemsList) {
        console.log('Cart items list found. Items:', cartItemsList.innerHTML); // Debugging log
      } else {
        console.warn('Cart items list not found in updated dropdown.'); // Debugging warning
      }
    } else {
      console.warn('Cart dropdown element not found'); // Debugging missing element
    }
  } catch (error) {
    console.error('Error refreshing and opening cart dropdown:', error); // Debugging error
  }
}

/**
 * Get session ID from cookies.
 * @returns {string|null} The session ID or null if not found.
 */
export function getSessionToken() {
  try {
    console.log('Attempting to retrieve session ID from cookies...'); // Debugging log
    console.log('Document cookies:', document.cookie); // Log all cookies

    const sessionid = document.cookie
      .split('; ')
      .find(row => row.startsWith('sessionid='))
      ?.split('=')[1];

    if (!sessionid) {
      console.warn('Session ID not found in cookies. Ensure the sessionid cookie is set and accessible.');
    } else {
      console.log('Session ID retrieved successfully:', sessionid); // Debugging session ID
    }

    return sessionid || null;
  } catch (error) {
    console.error('Error retrieving session ID from cookies:', error);
    return null;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  console.log('Document loaded, initializing AddToCart functionality'); // Debugging log

  handleAddToCartFormSubmission();
  handleQuantityButtons();

  const addToCartForm = document.getElementById('add_to_cart_form');

  if (addToCartForm) {
    addToCartForm.addEventListener('submit', (event) => {
      event.preventDefault();
      console.log('AddToCart form submit event triggered');
      submitAddToCartForm(addToCartForm);
    });
  }

  // Debugging: Ensure cart initialization happens on page load
  console.log('Initializing cart on page load...');
  window.cart.init();

  // Debugging: Check if cart dropdown is refreshed on reload
  const cartDropdown = document.getElementById('cart-dropdown');
  if (cartDropdown) {
    console.log('Cart dropdown element found on page load:', cartDropdown); // Debugging log
  } else {
    console.warn('Cart dropdown element not found on page load.'); // Debugging warning
  }
});

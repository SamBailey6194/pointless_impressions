/**
 * Artwork Detail Page - Add to Cart
 * Handles quantity buttons and AJAX form submission.
 */

// Import the one function we need from the global cart script
import { getCsrfToken } from './cart.js';

/**
 * Handles increment and decrement functionality for the quantity input field.
 */
function handleQuantityButtons() {
  const decrementButton = document.getElementById('decrement-quantity');
  const incrementButton = document.getElementById('increment-quantity');
  const quantityInput = document.getElementById('id_quantity');
  const stockQuantityEl = document.getElementById('stock_quantity');
  
  if (!decrementButton || !incrementButton || !quantityInput || !stockQuantityEl) {
    return;
  }
  
  const stockQuantity = parseInt(stockQuantityEl.value, 10);

  decrementButton.addEventListener('click', () => {
    const currentValue = parseInt(quantityInput.value, 10);
    if (currentValue > 1) {
      quantityInput.value = currentValue - 1;
      incrementButton.disabled = false;
    }
  });

  incrementButton.addEventListener('click', () => {
    const currentValue = parseInt(quantityInput.value, 10);
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

/**
 * Submit the AddToCart form via AJAX.
 */
async function submitAddToCartForm(form) {
  const formData = new FormData(form);

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

    if (data.success) {
      if (window.Toast) {
        window.Toast.show(data.message, 'success');
      }

      if (window.cart) {
        await window.cart.updateCartDropdownHTML();
        window.scrollTo({ top: 0, behavior: 'smooth' });
        window.cart.openCartDropdown();
      }
      
    } else {
      let errorMsg = 'Failed to add item. Please try again.';
      if (data.errors) {
        errorMsg = Object.values(data.errors).map(e => e[0]).join(' ');
      }
      if (window.Toast) {
         window.Toast.show(errorMsg, 'error');
      }
      console.error('Failed to add item to cart:', data.errors);
    }
  } catch (error) {
    console.error('Error submitting AddToCart form:', error);
    if (window.Toast) {
       window.Toast.show('An unexpected error occurred.', 'error');
    }
  }
}

// -----------------------------------------------------------------------------
// Run on page load
// -----------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
  console.log('AddToCart functionality loaded');

  handleQuantityButtons();

  const addToCartForm = document.getElementById('add_to_cart_form');
  if (addToCartForm) {
    addToCartForm.addEventListener('submit', (event) => {
      event.preventDefault();
      console.log('AddToCart form submit intercepted by AJAX');
      submitAddToCartForm(addToCartForm);
    });
  }
});
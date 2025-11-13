import { getCsrfToken } from './cart.js';

/**
 * Handles updating or removing an item via AJAX.
 * @param {string} artworkId - The ID of the artwork.
 * @param {number} quantity - The new quantity. 0 to remove.
 * @param {string} framing - The framing option.
 */
async function updateCartItem(artworkId, quantity, framing) {
  const formData = new FormData();
  formData.append('artwork_id', artworkId);
  formData.append('quantity', quantity);
  formData.append('framing_option', framing);
  formData.append('notes', '');
  
  try {
    console.warn("This file is complex. Let's simplify.");
    
  } catch (error) {
    console.error('Error updating item:', error);
  }

document.addEventListener('DOMContentLoaded', function () {

  async function refreshOrderSummary() {
    console.log('Refreshing page to update totals...');
    window.location.reload();
  }
  
  // This function sends the AJAX request
  async function handleCartUpdate(form) {
    const formData = new FormData(form);
    const artworkId = formData.get('artwork_id');
    const quantity = formData.get('quantity');
    const framing = formData.get('framing_option');
    
    console.log(`Updating ${artworkId} to ${quantity}`);

    try {
      const response = await fetch('/checkout/update-cart/', {
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
        if (window.Toast) window.Toast.show(data.message, 'success');
        await refreshOrderSummary();
      } else {
        if (window.Toast) window.Toast.show(data.error, 'error');
      }
    } catch (err) {
      console.error('Failed to submit form:', err);
      if (window.Toast) window.Toast.show('Error updating cart.', 'error');
    }
  }

  // Event listener for all update/remove buttons
  document.body.addEventListener('submit', function(e) {
    if (e.target.classList.contains('js-cart-item-form')) {
      e.preventDefault();
      handleCartUpdate(e.target);
    }
  });

  // Handle quantity buttons
  document.body.addEventListener('click', function (e) {
    const btn = e.target.closest('.js-qty-plus, .js-qty-minus');
    if (!btn) return;

    e.preventDefault();
    const form = btn.closest('.js-cart-item-form');
    if (!form) return;

    const qtyInput = form.querySelector('input[name="quantity"]');
    if (!qtyInput) return;

    let val = parseInt(qtyInput.value, 10) || 0;
    const max = parseInt(qtyInput.getAttribute('max'), 10) || 999;
    const min = 0;

    if (btn.classList.contains('js-qty-plus') && val < max) {
      qtyInput.value = val + 1;
    } else if (btn.classList.contains('js-qty-minus') && val > min) {
      qtyInput.value = val - 1;
    }
  });

  document.body.addEventListener('click', function(e) {
    const btn = e.target.closest('.js-remove-item');
    if (!btn) return;
    
    e.preventDefault();
    const form = btn.closest('.js-cart-item-form');
    if (!form) return;
    
    const qtyInput = form.querySelector('input[name="quantity"]');
    if (!qtyInput) return;
  
    qtyInput.value = 0;
    handleCartUpdate(form);
  });
})};
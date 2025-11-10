import { updateCartDisplay, updateQuantityViaAPI, removeFromCartViaAPI } from './cart.js';

document.addEventListener('DOMContentLoaded', function () {

  async function refreshOrderSummary() {
    const orderSummary = document.querySelector('#order-summary-section');
    if (!orderSummary) {
      window.location.reload();
      return;
    }
    try {
      const response = await fetch(window.location.href, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
      if (!response.ok) throw new Error('Failed to fetch updated order summary');
      const html = await response.text();
      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = html;
      const newSummary = tempDiv.querySelector('#order-summary-section');
      if (newSummary) {
        orderSummary.replaceWith(newSummary);
      } else {
        window.location.reload();
      }
    } catch (err) {
      window.location.reload();
    }
  }

  async function handleRemove(artworkId, form) {
    try {
      await removeFromCartViaAPI(artworkId);
      if (form) {
          const row = form.closest('tr');
          if (row) {
            row.remove();
          } else {
            form.closest('.border.rounded-lg').remove();
          }
      }
      await refreshOrderSummary();
      if (window.updateCartDisplay) window.updateCartDisplay();
    } catch (err) {
      alert('Failed to remove cart item.');
    }
  }

  async function updateFramingOption(artworkId, framingOption) {
    return Promise.resolve();
  }

  document.body.addEventListener('click', async function (e) {
    
    if (e.target.classList.contains('js-qty-plus')) {
      e.preventDefault();
      const form = e.target.closest('.js-cart-item-form');
      if (!form) return;
      
      const qtyInput = form.querySelector('input[name="quantity"]');
      if (!qtyInput) return;

      let val = parseInt(qtyInput.value, 10) || 0;
      const max = parseInt(qtyInput.getAttribute('max'), 10) || 999;
      if (val < max) {
        qtyInput.value = val + 1;
        qtyInput.dispatchEvent(new Event('change', { bubbles: true }));
      }
    }

    if (e.target.classList.contains('js-qty-minus')) {
      e.preventDefault();
      const form = e.target.closest('.js-cart-item-form');
      if (!form) return;

      const qtyInput = form.querySelector('input[name="quantity"]');
      if (!qtyInput) return;

      let val = parseInt(qtyInput.value, 10) || 0;
      const min = parseInt(qtyInput.getAttribute('min'), 10) || 0;
      if (val > min) {
        qtyInput.value = val - 1;
        qtyInput.dispatchEvent(new Event('change', { bubbles: true }));
      }
    }

    if (e.target.classList.contains('js-remove-item')) {
      e.preventDefault();
      const form = e.target.closest('.js-cart-item-form');
      const artworkId = e.target.getAttribute('data-artwork-id') || form?.getAttribute('data-artwork-id');
      
      console.log('[checkout.js] Remove item:', artworkId);
      await handleRemove(artworkId, form);
    }
  });

  document.body.addEventListener('submit', async function (e) {

    if (e.target.classList.contains('js-cart-item-form')) {
      e.preventDefault();
      const form = e.target;
      
      const artworkId = form.getAttribute('data-artwork-id');
      const quantityInput = form.querySelector('input[name="quantity"]');
      const framingSelect = form.querySelector('select[name="framing_option"]');
      
      const quantity = parseInt(quantityInput ? quantityInput.value : 1, 10);
      const framingOption = framingSelect ? framingSelect.value : '';

      console.log('[checkout.js] Submit update:', { artworkId, quantity, framingOption });

      if (quantity === 0) {
        await handleRemove(artworkId, form);
        return;
      }
      
      try {
        await updateQuantityViaAPI(artworkId, quantity);
        if (framingSelect) {
          await updateFramingOption(artworkId, framingOption);
        }
        await refreshOrderSummary();
        if (window.updateCartDisplay) window.updateCartDisplay();
      } catch (err) {
        console.error('[checkout.js] Failed to update cart item:', err);
        alert('Failed to update cart item.');
      }
    }
  });
});
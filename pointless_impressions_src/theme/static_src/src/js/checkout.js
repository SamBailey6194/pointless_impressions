import { getCsrfToken } from './cart.js';

/**
 * Handles updating or removing an item via AJAX.
 * @param {string} artworkId - The ID of the artwork.
 * @param {number} quantity - The new quantity. 0 to remove.
 * @param {string} framing - The framing option.
 */
async function refreshOrderSummary() {
  window.location.reload();
}

async function handleCartUpdate(form) {
  const formData = new FormData(form);
  const artworkId = form.querySelector('input[name="artwork_id"]').value;
  const quantity = formData.get('quantity');
  const framing = formData.get('framing_option');

  if (!artworkId) {
    console.error('Artwork ID is missing in the form.');
    return;
  }

  try {
    const response = await fetch('/checkout/update/', {
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

/**
 * Populate and handle the order confirmation modal and form submission.
 */
function populateConfirmationModal() {
  const shipping = {
    firstName: document.getElementById('id_shipping_first_name').value,
    lastName: document.getElementById('id_shipping_last_name').value,
    line1: document.getElementById('id_shipping_address_line_1').value,
    line2: document.getElementById('id_shipping_address_line_2').value,
    city: document.getElementById('id_shipping_city').value,
    county: document.getElementById('id_shipping_county').value,
    postcode: document.getElementById('id_shipping_postcode').value,
    countryEl: document.getElementById('id_shipping_country'),
  };
  shipping.country = shipping.countryEl.options[shipping.countryEl.selectedIndex].text;

  document.getElementById('modal-shipping-first-name').textContent = shipping.firstName;
  document.getElementById('modal-shipping-last-name').textContent = shipping.lastName;
  document.getElementById('modal-shipping-line1').textContent = shipping.line1;
  document.getElementById('modal-shipping-city').textContent = shipping.city;
  document.getElementById('modal-shipping-postcode').textContent = shipping.postcode;
  document.getElementById('modal-shipping-country').textContent = shipping.country;

  const shippingLine2Wrapper = document.getElementById('modal-shipping-line2-wrapper');
  if (shipping.line2) {
    document.getElementById('modal-shipping-line2').textContent = shipping.line2;
    shippingLine2Wrapper.style.display = 'block';
  } else {
    shippingLine2Wrapper.style.display = 'none';
  }

  const shippingCountyWrapper = document.getElementById('modal-shipping-county-wrapper');
  if (shipping.county) {
    document.getElementById('modal-shipping-county').textContent = shipping.county;
    shippingCountyWrapper.style.display = 'block';
  } else {
    shippingCountyWrapper.style.display = 'none';
  }

  const isSameAsShipping = document.getElementById('id_billing_same_as_shipping').checked;
  let billing;

  if (isSameAsShipping) {
    billing = { ...shipping };
  } else {
    billing = {
      firstName: document.getElementById('id_billing_first_name').value,
      lastName: document.getElementById('id_billing_last_name').value,
      line1: document.getElementById('id_billing_address_line_1').value,
      line2: document.getElementById('id_billing_address_line_2').value,
      city: document.getElementById('id_billing_city').value,
      county: document.getElementById('id_billing_county').value,
      postcode: document.getElementById('id_billing_postcode').value,
      countryEl: document.getElementById('id_billing_country'),
    };
    billing.country = billing.countryEl.options[billing.countryEl.selectedIndex].text;
  }

  document.getElementById('modal-billing-first-name').textContent = billing.firstName;
  document.getElementById('modal-billing-last-name').textContent = billing.lastName;
  document.getElementById('modal-billing-line1').textContent = billing.line1;
  document.getElementById('modal-billing-city').textContent = billing.city;
  document.getElementById('modal-billing-postcode').textContent = billing.postcode;
  document.getElementById('modal-billing-country').textContent = billing.country;

  const billingLine2Wrapper = document.getElementById('modal-billing-line2-wrapper');
  if (billing.line2) {
    document.getElementById('modal-billing-line2').textContent = billing.line2;
    billingLine2Wrapper.style.display = 'block';
  } else {
    billingLine2Wrapper.style.display = 'none';
  }

  const billingCountyWrapper = document.getElementById('modal-billing-county-wrapper');
  if (billing.county) {
    document.getElementById('modal-billing-county').textContent = billing.county;
    billingCountyWrapper.style.display = 'block';
  } else {
    billingCountyWrapper.style.display = 'none';
  }
}

/**
 * Gets the current Shipping Address values and formats them as a HTML string.
 */
function getFormattedShippingAddress() {
  const parts = [];
  const firstName = document.getElementById('id_shipping_first_name').value;
  const lastName = document.getElementById('id_shipping_last_name').value;
  const line1 = document.getElementById('id_shipping_address_line_1').value;
  const line2 = document.getElementById('id_shipping_address_line_2').value;
  const city = document.getElementById('id_shipping_city').value;
  const county = document.getElementById('id_shipping_county').value;
  const postcode = document.getElementById('id_shipping_postcode').value;
  const countryEl = document.getElementById('id_shipping_country');
  const country = countryEl.options[countryEl.selectedIndex].text;

  if (firstName || lastName) parts.push(firstName + ' ' + lastName);
  if (line1) parts.push(line1);
  if (line2) parts.push(line2);
  if (city) parts.push(city);
  if (county) parts.push(county);
  if (postcode) parts.push(postcode);
  if (country) parts.push(country);

  return parts.join('<br>');
}

document.addEventListener('DOMContentLoaded', function () {

  const placeOrderButton = document.getElementById('place-order-button');
  const confirmModal = document.getElementById('confirm-order-modal');
  const finalConfirmBtn = document.getElementById('modal-confirm-btn');
  const modalLoadingSpinner = document.getElementById('modal-loading-spinner');
  const checkoutForm = document.getElementById('checkout-form');


  const billingFields = document.getElementById('billing-fields-container');
  const billingConfirmationContainer = document.querySelector('.billing-confirmation-container');
  const billingCheckbox = document.getElementById('id_billing_same_as_shipping');
  const billingConfirmationText = document.getElementById('billing-confirmation-text');
  const shippingFields = document.getElementById('shipping-fields-container');
  const billingInputs = billingFields ? billingFields.querySelectorAll('input, select') : [];

  /**
   * Function to toggle billing fields if checkbox is ticked
   */
  function toggleBillingFields() {
    if (!billingCheckbox || !billingFields || !billingConfirmationContainer ) {
      return
    };

    if (billingCheckbox.checked) {
      billingFields.style.display = 'none';
      billingConfirmationContainer.style.display = 'block';
      billingConfirmationText.innerHTML = getFormattedShippingAddress();
      copyShippingToBilling();
    } else {
      billingFields.style.display = 'block';
      billingConfirmationContainer.style.display = 'none';
      billingConfirmationText.innerHTML = '';
    }
  }

  /**
   * Function to copy shipping address values to billing address fields
   */
  function copyShippingToBilling() {
    const fieldsMap = [
      ['id_shipping_first_name', 'id_billing_first_name'],
      ['id_shipping_last_name', 'id_billing_last_name'],
      ['id_shipping_address_line_1', 'id_billing_address_line_1'],
      ['id_shipping_address_line_2', 'id_billing_address_line_2'],
      ['id_shipping_city', 'id_billing_city'],
      ['id_shipping_county', 'id_billing_county'],
      ['id_shipping_postcode', 'id_billing_postcode'],
      ['id_shipping_country', 'id_billing_country'],
    ];

    fieldsMap.forEach(([shippingId, billingId]) => {
      const shippingField = document.getElementById(shippingId);
      const billingField = document.getElementById(billingId);
      if (shippingField && billingField) {
        billingField.value = shippingField.value;
      }
    });
  }

  if (billingCheckbox && shippingFields) {
    billingCheckbox.addEventListener('change', toggleBillingFields);

    const shippingInputs = shippingFields.querySelectorAll('input, select');

    shippingInputs.forEach(input => {
      const eventType = input.tagName === 'SELECT' ? 'change' : 'input';
      input.addEventListener(eventType, () => {
        if (billingCheckbox.checked) {
          billingConfirmationText.innerHTML = getFormattedShippingAddress();
        }
      });
    });
    toggleBillingFields();
  }

  if (placeOrderButton && confirmModal && finalConfirmBtn) {
    placeOrderButton.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      populateConfirmationModal();
      confirmModal.showModal();
    });

    finalConfirmBtn.addEventListener('click', async function () {
      if (modalLoadingSpinner) {
        modalLoadingSpinner.style.display = 'block';
      }
      finalConfirmBtn.disabled = true;

      if (billingCheckbox && billingCheckbox.checked) {
        copyShippingToBilling();
      }

      checkoutForm.submit();
    });
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
    const artworkId = btn.getAttribute('data-artwork-id');

    if (!artworkId) {
      console.error('Artwork ID not found for removal.');
      return;
    }

    // Send AJAX request to remove the item immediately
    fetch(`/checkout/remove-item/`, {
      method: 'POST',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': getCsrfToken(),
      },
      body: JSON.stringify({ artwork_id: artworkId }),
      credentials: 'include',
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          if (window.Toast) window.Toast.show(data.message, 'success');
          refreshOrderSummary();
        } else {
          if (window.Toast) window.Toast.show(data.error, 'error');
        }
      })
      .catch(err => {
        console.error('Failed to remove item:', err);
        if (window.Toast) window.Toast.show('Error removing item.', 'error');
      });
  });
});
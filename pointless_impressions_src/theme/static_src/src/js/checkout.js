import { getCsrfToken } from './cart.js';

let card = null; // Holds the Square Card instance
let paymentInProgress = false; // Prevent multiple submissions

/**
 * Detect if the current theme is dark mode
 * @returns {boolean} True if dark mode, else false
 */
function isDarkMode() {
  return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
}

/**
 * Get Square Card styles based on theme
 */
function getSquareCardStyles() {
  // Check if dark mode is enabled
  const isDark = isDarkMode();

  // Define colors based on theme - Have to use # values due to Square limitations
  const pointlessWhite = "#FAFAFA";
  const pointlessBlack = "#050505";
  const pointlessBlue = "#2563EB";

  return {
    '.input-container': {
      borderColor: pointlessBlue,
      borderRadius: '4px',
      borderWidth: '1px',
    },
    'input': {
      backgroundColor: pointlessWhite,
      color: pointlessBlack,
      fontSize: '16px',
    },
    'input::placeholder': {
      color: pointlessBlack,
    },
    '.message-text': {
      color: '#ef4444',
    },
    '.message-icon': {
      color: '#ef4444',
    },
  };
}

/**
 * Initialize Square Payments
 */
async function initializeSquare() {
  const appIdElement = document.getElementById('square-app-id');
  const locIdElement = document.getElementById('square-location-id');

  if (!appIdElement || !locIdElement) {
    console.error('Square Credentials not found in DOM');
    return;
  }

  const appId = JSON.parse(appIdElement.textContent);
  const locationId = JSON.parse(locIdElement.textContent);

  try {
    if (!window.Square) {
      throw new Error("Square.js script not loaded");
    }
    const payments = window.Square.payments(appId, locationId);
    const cardStyles = getSquareCardStyles();
    card = await payments.card({ style: cardStyles });
    await card.attach('#card-container');

    // Listen for theme changes to update styles
    const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
    darkModeQuery.addEventListener('change', async () => {
      try {
        if (card) {
          await card.destroy();
        }
        const newStyles = getSquareCardStyles();
        card = await payments.card({ style: newStyles });
        await card.attach('#card-container');
      } catch (e) {
        console.error('Error updating Square card styles:', e);
      }
    });
  } catch (e) {
    console.error('Error initializing Square Payments:', e);
    if (window.Toast) window.Toast.show('Error initializing payment form.', 'error');
  }
}

async function refreshOrderSummary() {
  window.location.reload();
}

async function handleCartUpdate(form) {
  const formData = new FormData(form);
  const artworkId = form.querySelector('input[name="artwork_id"]').value;

  if (!artworkId) return;

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

// ... Helper functions ...
function getSelectText(id) {
    const el = document.getElementById(id);
    if (el && el.selectedIndex !== -1) {
        return el.options[el.selectedIndex].text;
    }
    return '';
}

function getValue(id) {
    const el = document.getElementById(id);
    return el ? el.value : '';
}

/**
 * Validate form fields before showing confirmation modal
 */
function validateCheckoutForm() {
  const errors = [];
  const checkoutForm = document.getElementById('checkout-form');

  if (!checkoutForm) {
    errors.push('Checkout form not found.');
    return errors;
  }

  const requiredShippingFields = [
    { id: 'id_shipping_first_name', label: 'Shipping First Name' },
    { id: 'id_shipping_last_name', label: 'Shipping Last Name' },
    { id: 'id_shipping_address_line_1', label: 'Shipping Address' },
    { id: 'id_shipping_city', label: 'Shipping City' },
    { id: 'id_shipping_postcode', label: 'Shipping Postcode' },
    { id: 'id_shipping_country', label: 'Shipping Country' },
  ];

  requiredShippingFields.forEach(field => {
    const el = document.getElementById(field.id);
    if (!el || el.value.trim() === '') {
      errors.push(`${field.label} is required.`);
    }
  });

  const billingCheckbox = document.getElementById('id_billing_same_as_shipping');
  if (billingCheckbox && !billingCheckbox.checked) {
    const requiredBillingFields = [
      { id: 'id_billing_first_name', label: 'Billing First Name' },
      { id: 'id_billing_last_name', label: 'Billing Last Name' },
      { id: 'id_billing_address_line_1', label: 'Billing Address' },
      { id: 'id_billing_city', label: 'Billing City' },
      { id: 'id_billing_postcode', label: 'Billing Postcode' },
      { id: 'id_billing_country', label: 'Billing Country' },
    ];

    requiredBillingFields.forEach(field => {
      const el = document.getElementById(field.id);
      if (!el || el.value.trim() === '') {
        errors.push(`${field.label} is required.`);
      }
    });
  }
  return errors;
}

/**
 * Populate confirmation modal with form data
 */
function populateConfirmationModal() {
  const shipping = {
    firstName: getValue('id_shipping_first_name'),
    lastName: getValue('id_shipping_last_name'),
    line1: getValue('id_shipping_address_line_1'),
    line2: getValue('id_shipping_address_line_2'),
    city: getValue('id_shipping_city'),
    county: getValue('id_shipping_county'),
    postcode: getValue('id_shipping_postcode'),
    country: getSelectText('id_shipping_country'),
  };

  const set = (id, val) => { 
      const el = document.getElementById(id);
      if(el) el.textContent = val; 
  };

  set('modal-shipping-first-name', shipping.firstName);
  set('modal-shipping-last-name', shipping.lastName);
  set('modal-shipping-line1', shipping.line1);
  set('modal-shipping-city', shipping.city);
  set('modal-shipping-postcode', shipping.postcode);
  set('modal-shipping-country', shipping.country);

  const line2Wrap = document.getElementById('modal-shipping-line2-wrapper');
  if (line2Wrap) line2Wrap.style.display = shipping.line2 ? 'block' : 'none';
  if (shipping.line2) set('modal-shipping-line2', shipping.line2);

  const countyWrap = document.getElementById('modal-shipping-county-wrapper');
  if (countyWrap) countyWrap.style.display = shipping.county ? 'block' : 'none';
  if (shipping.county) set('modal-shipping-county', shipping.county);

  const isSameAsShipping = document.getElementById('id_billing_same_as_shipping');
  let billing;

  if (isSameAsShipping && isSameAsShipping.checked) {
    billing = { ...shipping };
  } else {
    billing = {
      firstName: getValue('id_billing_first_name'),
      lastName: getValue('id_billing_last_name'),
      line1: getValue('id_billing_address_line_1'),
      line2: getValue('id_billing_address_line_2'),
      city: getValue('id_billing_city'),
      county: getValue('id_billing_county'),
      postcode: getValue('id_billing_postcode'),
      country: getSelectText('id_billing_country'),
    };
  }

  set('modal-billing-first-name', billing.firstName);
  set('modal-billing-last-name', billing.lastName);
  set('modal-billing-line1', billing.line1);
  set('modal-billing-city', billing.city);
  set('modal-billing-postcode', billing.postcode);
  set('modal-billing-country', billing.country);

  const billingLine2Wrap = document.getElementById('modal-billing-line2-wrapper');
  if (billingLine2Wrap) billingLine2Wrap.style.display = billing.line2 ? 'block' : 'none';
  if (billing.line2) set('modal-billing-line2', billing.line2);

  const billingCountyWrap = document.getElementById('modal-billing-county-wrapper');
  if (billingCountyWrap) billingCountyWrap.style.display = billing.county ? 'block' : 'none';
  if (billing.county) set('modal-billing-county', billing.county);
}

function getFormattedShippingAddress() {
  const parts = [];
  const firstName = getValue('id_shipping_first_name');
  const lastName = getValue('id_shipping_last_name');
  const line1 = getValue('id_shipping_address_line_1');
  const line2 = getValue('id_shipping_address_line_2');
  const city = getValue('id_shipping_city');
  const county = getValue('id_shipping_county');
  const postcode = getValue('id_shipping_postcode');
  const country = getSelectText('id_shipping_country');

  if (firstName || lastName) parts.push(firstName + ' ' + lastName);
  if (line1) parts.push(line1);
  if (line2) parts.push(line2);
  if (city) parts.push(city);
  if (county) parts.push(county);
  if (postcode) parts.push(postcode);
  if (country) parts.push(country);

  return parts.join('<br>');
}

document.addEventListener('DOMContentLoaded', async function () {

  await initializeSquare();

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

  function toggleBillingFields() {
    if (!billingCheckbox || !billingFields || !billingConfirmationContainer ) return;

    if (billingCheckbox.checked) {
      billingFields.style.display = 'none';
      billingConfirmationContainer.style.display = 'block';
      if(billingConfirmationText) billingConfirmationText.innerHTML = getFormattedShippingAddress();
      copyShippingToBilling();
    } else {
      billingFields.style.display = 'block';
      billingConfirmationContainer.style.display = 'none';
      if(billingConfirmationText) billingConfirmationText.innerHTML = '';
    }
  }

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
        if (billingCheckbox.checked && billingConfirmationText) {
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

      const validationErrors = validateCheckoutForm();
      if (validationErrors.length > 0) {
        const errorMsg = validationErrors.join('\n');
        if (window.Toast) {
          validationErrors.forEach(err => window.Toast.show(err, 'error', 8000));
        } else {
          alert(errorMsg);
        }
        return;
      }

      if (billingCheckbox && billingCheckbox.checked) {
        copyShippingToBilling();
      }

      populateConfirmationModal();
      confirmModal.showModal();
    });

    finalConfirmBtn.addEventListener('click', async function (e) {
      e.preventDefault();
      e.stopPropagation();

      // Prevent multiple submissions
      if (paymentInProgress) {
        console.warn('Payment already in progress. Please wait.');
        return;
      }

      const modalContent = confirmModal.querySelector('.modal-box');
      if (modalContent) {
        modalContent.scrollTop = 0;
      }

      paymentInProgress = true;
      if (modalLoadingSpinner) modalLoadingSpinner.style.display = 'block';
      finalConfirmBtn.disabled = true;

      if (billingCheckbox && billingCheckbox.checked) {
        copyShippingToBilling();
      }

      const formDataObj = Object.fromEntries(new FormData(checkoutForm).entries());

      try {
        if (!card) throw new Error("Payment form not initialized, please refresh the page.");

        let billingPostcode = '';
        const isSameAsShipping = document.getElementById('id_billing_same_as_shipping');

        if (isSameAsShipping && isSameAsShipping.checked) {
          billingPostcode = getValue('id_shipping_postcode');
        } else {
          billingPostcode = getValue('id_billing_postcode');
        }

        if (!billingPostcode) throw new Error("Billing postcode is required.");
        
        const tokenResult = await card.tokenize();

        if (tokenResult.status !== 'OK') {
          const errorMsg = tokenResult.errors?.[0]?.message || 'Tokenization failed';
          throw new Error(errorMsg);
        }

        const response = await fetch(checkoutForm.action, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCsrfToken(),
          },
          body: JSON.stringify({
            sourceId: tokenResult.token,
            formData: formDataObj,
          }),
          credentials: 'include',
        });

        const contentType = response.headers.get('Content-Type');
        if (!contentType || !contentType.includes('application/json')) {
          throw new Error('Unexpected response from server.');
        }

        const serverData = await response.json();

        if (response.ok && serverData.status === 'success') {
          window.location.href = serverData.redirect_url;
        } else {
          let msg = serverData.message || 'Payment processing failed.';
          if (serverData.errors) {
            msg += ' (' + serverData.errors.join(' ') + ')';
          }
          throw new Error(msg);
        }
      } catch (err) {
        console.error('Payment failed:', err);
        if (modalLoadingSpinner) modalLoadingSpinner.style.display = 'none';
        finalConfirmBtn.disabled = false;
        paymentInProgress = false;
        confirmModal.close();

        const errorMessage = err.message || 'An error occurred during payment processing.';
        if (window.Toast) {
          window.Toast.show(errorMessage, 'error');
        } else {
          alert("Error: " + errorMessage);
        }
      }
    });
  }

  document.body.addEventListener('submit', function(e) {
    if (e.target.classList.contains('js-cart-item-form')) {
      e.preventDefault();
      handleCartUpdate(e.target);
    }
  });

  document.body.addEventListener('click', function (e) {
    const qtyBtn = e.target.closest('.js-qty-plus, .js-qty-minus');
    if (qtyBtn) {
        e.preventDefault();
        const form = qtyBtn.closest('.js-cart-item-form');
        if (form) {
            const qtyInput = form.querySelector('input[name="quantity"]');
            if (qtyInput) {
                let val = parseInt(qtyInput.value, 10) || 0;
                const max = parseInt(qtyInput.getAttribute('max'), 10) || 999;
                const min = 0;
                if (qtyBtn.classList.contains('js-qty-plus') && val < max) {
                    qtyInput.value = val + 1;
                } else if (qtyBtn.classList.contains('js-qty-minus') && val > min) {
                    qtyInput.value = val - 1;
                }
            }
        }
        return;
    }

    const removeBtn = e.target.closest('.js-remove-item');
    if (removeBtn) {
        e.preventDefault();
        const artworkId = removeBtn.getAttribute('data-artwork-id');
        if (!artworkId) return;

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
    }
  });
});
import { getCsrfToken } from './cart.js';

let card = null; // Holds the Square Card instance
let payments = null; // Holds the Square Payments instance
let paymentInProgress = false; // Prevent multiple submissions
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Get Square Card styles based on theme
 */
function getSquareCardStyles() {
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
    payments = window.Square.payments(appId, locationId);
    const cardStyles = getSquareCardStyles();
    card = await payments.card({ style: cardStyles });
    await card.attach('#card-container');
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

async function handleRemoveItem(artworkId) {
  try {
    const response = await fetch('/checkout/remove-item/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': getCsrfToken(),
      },
      body: JSON.stringify({ artwork_id: artworkId }),
      credentials: 'include',
    });
    const data = await response.json();
    if (data.success) {
      window.location.reload();
    } else {
      if (window.Toast) window.Toast.show(data.error || 'Failed to remove item.', 'error');
    }
  } catch (err) {
    console.error('Failed to remove item:', err);
    if (window.Toast) window.Toast.show('Error removing item.', 'error');
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

// Main DOMContentLoaded Event
// ----------------------------------------------------------
// Initialize Square and setup event listeners
// Handles billing/shipping address toggling and copying
// Opens confirmation modal on place order button click
// Process payment on final confirmation button click
// Allows only one payment submission at a time
// Enables SCA compliance with Square payments
// ----------------------------------------------------------
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

  document.querySelectorAll('.js-qty-minus').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const input = btn.closest('form').querySelector('input[name="quantity"]');
      if (!input) return;
      const current = parseInt(input.value, 10) || 1;
      if (current > 1) input.value = current - 1;
    });
  });

  document.querySelectorAll('.js-qty-plus').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const input = btn.closest('form').querySelector('input[name="quantity"]');
      if (!input) return;
      const current = parseInt(input.value, 10) || 1;
      const max = parseInt(input.max, 10) || 999;
      if (current < max) input.value = current + 1;
    });
  });

  document.querySelectorAll('.js-cart-item-form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      handleCartUpdate(form);
    });
  });

  document.querySelectorAll('.js-remove-item').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const artworkId = btn.dataset.artworkId;
      if (artworkId) handleRemoveItem(artworkId);
    });
  });

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

        const countryVal = getValue('id_billing_country') || getValue('id_shipping_country');

        const isoCountry = countryVal.length ? countryVal.trim().substring(0, 2).toUpperCase() : 'GB';

        // Guest User Phone Handling
        const phonePrefixInput = document.getElementById('id_phone_0');
        const phoneNumberInput = document.getElementById('id_phone_1');

        // Auth User Phone Handling
        const authPhoneInput = document.getElementById('id_phone');

        let fullPhone = '';

        if(phonePrefixInput && phoneNumberInput && phonePrefixInput.offsetParent !== null) {
          const rawPrefix = phonePrefixInput.value;
          const cleanPrefix = rawPrefix.replace(/[^0-9+]/g, '');
          fullPhone = (cleanPrefix + phoneNumberInput.value).trim();
        } else if (authPhoneInput) {
          fullPhone = authPhoneInput.value.replace(/[^0-9+]/g, '').trim();
        } else {
          let rawString = formDataObj['phone'] || formDataObj['id_phone_0'] + formDataObj['id_phone_1'] || '';
          fullPhone = rawString.replace(/[^0-9+]/g, '').trim();
        }

        formDataObj['phone'] = fullPhone;

        console.log('Full Phone:', fullPhone);

        let finalEmail = getValue('id_email') || formDataObj['email'] || '';
        if (!finalEmail) {
          const hiddenEmailInput = document.getElementById('id-email');
          if (hiddenEmailInput) {
            finalEmail = hiddenEmailInput.value;
          }
        }

        const amountClean = finalConfirmBtn.dataset.amount;
        if (!amountClean) throw new Error("Payment amount not found.");
        const amountString = amountClean.replace(/,/g, '');

        const billingContact = {
          givenName: getValue('id_billing_first_name') || getValue('id_shipping_first_name'),
          familyName: getValue('id_billing_last_name') || getValue('id_shipping_last_name'),
          email: finalEmail,
          addressLines: [
            getValue('id_billing_address_line_1') || getValue('id_shipping_address_line_2'),
          ],
          city: getValue('id_billing_city') || getValue('id_shipping_city'),
          postalCode: getValue('id_billing_postcode') || getValue('id_shipping_postcode'),
          state: getValue('id_billing_county') || getValue('id_shipping_county'),
          countryCode: isoCountry,
        };

        const line2 = getValue('id_billing_address_line_2') || getValue('id_shipping_address_line_2');
        if (line2) {
          billingContact.addressLines.push(line2);
        }

        const stateVal = getValue('id_billing_county') || getValue('id_shipping_county');
        if (stateVal) {
          billingContact.state = stateVal;
        }

        if (fullPhone && fullPhone.length > 5) {
          billingContact.phone = fullPhone;
        }

        console.log('Billing Contact:', billingContact);

        const verificationDetails = {
          amount: amountString,
          billingContact: billingContact,
          currencyCode: 'GBP',
          intent: 'CHARGE',
          customerInitiated: true,
          sellerKeyedIn: false,
        };

        console.log('Verification Details:', verificationDetails);

        await delay(3000);
        confirmModal.close();

        if (placeOrderButton) {
          placeOrderButton.innerHTML = '<i class="fa-solid fa-shield-halved fa-spin mr-2"></i> Verifying Security...';
          placeOrderButton.disabled = true;
        }

        const tokenResult = await card.tokenize(verificationDetails);

        if (tokenResult.status !== 'OK') {
          const errorMsg = tokenResult.errors?.[0]?.message || 'Tokenization failed';
          throw new Error(errorMsg);
        }

        if (placeOrderButton) {
             placeOrderButton.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-2"></i> Finalizing Order...';
        }

        const response = await fetch('/order/confirmation/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCsrfToken()
          },
          body: JSON.stringify({
            sourceId: tokenResult.token,
            formData: formDataObj
          }),
          credentials: 'include',
        });

        const result = await response.json();

        if (result.status === 'success') {
          window.location.href = result.redirect_url;
        } else {
          throw new Error(result.message || 'Payment failed');
        }
      } catch (err) {
        console.error('Payment failed:', err);
        if (modalLoadingSpinner) modalLoadingSpinner.style.display = 'none';
        finalConfirmBtn.disabled = false;
        paymentInProgress = false;

        if (placeOrderButton) {
          placeOrderButton.disabled = false;
          placeOrderButton.innerHTML = '<i class="fa-solid fa-credit-card mr-2"></i> Confirm & Pay';
        } 

        const errorMessage = err.message || 'An error occurred during payment processing.';
        if (window.Toast) {
          window.Toast.show(errorMessage, 'error');
        } else {
          alert("Error: " + errorMessage);
        }
      }
    });
  }
});
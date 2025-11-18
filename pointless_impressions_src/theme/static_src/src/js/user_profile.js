import { getCsrfToken } from './cart.js';

/**
 * Fetch order data from the server.
 * @param {string} orderId - The ID of the order to fetch.
 * @returns {Promise<object>} - The order data.
 */
async function fetchOrderData(orderId) {
  try {
    const response = await fetch(`/orders/${orderId}/`, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': getCsrfToken(),
      },
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch order: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching order data:', error);
    return null;
  }
}

/**
 * Prepare the SignupForm for editing user info by excluding password fields.
 * @param {object} formData - The user data to populate the form.
 */
function populateEditUserInfoModal(formData) {
  const modal = document.getElementById('edit-user-info-modal');
  if (!modal || !formData) return;

  modal.querySelector('input[name="first_name"]').value = formData.first_name || '';
  modal.querySelector('input[name="last_name"]').value = formData.last_name || '';
  modal.querySelector('input[name="username"]').value = formData.username || '';
  modal.querySelector('input[name="email"]').value = formData.email || '';
  modal.querySelector('input[name="phone"]').value = formData.phone || '';

  modal.showModal();
}

/**
 * Populate the combined order modal with fetched data.
 * @param {object} orderData - The order data to populate the modal.
 */
function populateCombinedOrderModal(orderData) {
  const modal = document.getElementById('order-modal');
  if (!modal || !orderData) return;

  // Populate order summary section
  modal.querySelector('.order-id').textContent = orderData.id;
  modal.querySelector('.order-total').textContent = orderData.total;
  modal.querySelector('.order-items').innerHTML = orderData.items
    .map(item => `<li>${item.name} - ${item.quantity} x ${item.price}</li>`)
    .join('');

  // Populate edit form section
  const editForm = modal.querySelector('#edit-order-form');
  if (editForm) {
    editForm.querySelector('textarea[name="edit_notes"]').value = '';
  }
}

/**
 * Close a modal by its ID.
 * @param {string} modalId - The ID of the modal to close.
 */
function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.close();
  }
}

/**
 * Open a modal by its ID.
 * @param {string} modalId - The ID of the modal to open.
 */
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.showModal();
  }
}

/**
 * Toggle edit mode in the order modal.
 */
function toggleEditMode() {
  const editOrderForm = document.getElementById('edit-order-form');
  const orderActions = document.getElementById('order-actions');

  if (editOrderForm && orderActions) {
    editOrderForm.classList.toggle('hidden');
    orderActions.classList.toggle('hidden');
  }
}

// Attach event listener for toggling edit mode
const toggleEditModeButton = document.getElementById('toggle-edit-mode');
if (toggleEditModeButton) {
  toggleEditModeButton.addEventListener('click', toggleEditMode);
}

/**
 * Increment or decrement the quantity in the order modal.
 */
function updateQuantity(button, increment) {
  const quantityInput = button.closest('.quantity-control').querySelector('.quantity-input');
  if (!quantityInput) return;

  let currentQuantity = parseInt(quantityInput.value, 10) || 0;
  const maxQuantity = parseInt(quantityInput.getAttribute('max'), 10) || Infinity;
  const minQuantity = parseInt(quantityInput.getAttribute('min'), 10) || 0;

  if (increment) {
    currentQuantity = Math.min(currentQuantity + 1, maxQuantity);
  } else {
    currentQuantity = Math.max(currentQuantity - 1, minQuantity);
  }

  quantityInput.value = currentQuantity;
}

// Attach event listeners for quantity buttons
document.addEventListener('click', (event) => {
  const incrementButton = event.target.closest('.quantity-increment');
  const decrementButton = event.target.closest('.quantity-decrement');

  if (incrementButton) {
    updateQuantity(incrementButton, true);
  }

  if (decrementButton) {
    updateQuantity(decrementButton, false);
  }
});

/**
 * Populate the address modal with data for editing or reset for adding a new address.
 * @param {object|null} addressData - The address data to populate the form, or null for a new address.
 */
function populateAddressModal(addressData) {
  const modal = document.getElementById('edit-address-modal');
  const form = modal.querySelector('form');

  if (!modal || !form) return;

  // Reset the form for adding a new address
  form.reset();
  
  // Set form action dynamically
  if (addressData) {
    form.action = `/dashboard/user-profile/edit-address/${addressData.id}/`;
  } else {
    form.action = '/dashboard/user-profile/add-address/';
  }

  // Populate the form fields if editing an existing address
  if (addressData) {
    const setFieldValue = (name, value) => {
      const field = form.querySelector(`[name="${name}"]`);
      if (field) field.value = value || '';
    };

    setFieldValue('label', addressData.label);
    setFieldValue('first_name', addressData.first_name);
    setFieldValue('last_name', addressData.last_name);
    setFieldValue('address_line_1', addressData.address_line_1);
    setFieldValue('address_line_2', addressData.address_line_2);
    setFieldValue('city', addressData.city);
    setFieldValue('county', addressData.county);
    setFieldValue('postcode', addressData.postcode);
    setFieldValue('country', addressData.country);
  }

  modal.showModal();
}

// Event listener for opening the address modal
document.addEventListener('click', async (event) => {
  const addAddressBtn = event.target.closest('.js-add-address-btn');
  const editAddressBtn = event.target.closest('.js-edit-address-btn');

  if (addAddressBtn) {
    populateAddressModal(null);
  }

  if (editAddressBtn) {
    const addressData = {
        id: editAddressBtn.dataset.addressId,
        label: editAddressBtn.dataset.addressLabel,
        first_name: editAddressBtn.dataset.addressFirstName,
        last_name: editAddressBtn.dataset.addressLastName,
        address_line_1: editAddressBtn.dataset.addressLine1,
        address_line_2: editAddressBtn.dataset.addressLine2,
        city: editAddressBtn.dataset.addressCity,
        county: editAddressBtn.dataset.addressCounty,
        postcode: editAddressBtn.dataset.addressPostcode,
        country: editAddressBtn.dataset.addressCountry,
    };

    try {
      const response = await fetch(`/dashboard/edit-address/${addressId}/`, {
        method: 'GET',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCsrfToken(),
        },
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch address: ${response.status}`);
      }

      const addressData = await response.json();
      populateAddressModal(addressData);
    } catch (error) {
      console.error('Error fetching address data:', error);
    }
  }
});

/**
 * Event listener to open modals and fetch data.
 */
document.addEventListener('click', async (event) => {
  const changePasswordBtn = event.target.closest('.js-change-password-btn');
  const editUserInfoBtn = event.target.closest('.js-edit-user-info-btn');
  const closeModalBtn = event.target.closest('.js-close-modal-btn');
  const combinedOrderBtn = event.target.closest('.js-combined-order-btn');

  if (changePasswordBtn) {
    openModal('change-password-modal');
  }

  if (editUserInfoBtn) {
    const userId = editUserInfoBtn.getAttribute('data-user-id');

    try {
      const response = await fetch(`/users/${userId}/`, {
        method: 'GET',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCsrfToken(),
        },
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch user info: ${response.status}`);
      }

      const userData = await response.json();
      populateEditUserInfoModal(userData);
      openModal('edit-user-info-modal');
    } catch (error) {
      console.error('Error fetching user info:', error);
    }
  }

  if (combinedOrderBtn) {
    const orderId = combinedOrderBtn.getAttribute('data-order-id');
    const orderData = await fetchOrderData(orderId);
    populateCombinedOrderModal(orderData);
    openModal('order-modal');
  }

  if (closeModalBtn) {
    const modalId = closeModalBtn.getAttribute('data-modal-id');
    closeModal(modalId);
  }
});
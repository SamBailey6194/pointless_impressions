document.addEventListener('DOMContentLoaded', () => {
    const updateButtons = document.querySelectorAll('.js-update-order-btn');

    updateButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const orderId = button.dataset.order;

            if (orderId) {
                openUpdateOrderModal(orderId);
            }
        });
    });

    const deleteButtons = document.querySelectorAll('.js-delete-order-btn');

    deleteButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const orderId = button.dataset.order;

            if (orderId) {
                openDeleteOrderModal(orderId);
            }
        });
    });
});

function openUpdateOrderModal(orderId) {

    const modalContainer = document.getElementById('update-order-modal-container');
    if (!modalContainer) {
        console.error('Modal container not found.');
        return;
    }

    fetch(`/dashboard/user-profile/${orderId}/order/update/`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        })
        .then(response => {
            if (!response.ok) throw new Error('Failed to fetch modal content');
            return response.text();
        })
        .then(html => {
            modalContainer.innerHTML = html;

            const modal = document.getElementById('update-order-modal');
            if (modal) {
                modal.showModal();

                attachFormSubmitListener(modal);

                const closeBtn = modal.querySelector('.js-close-modal-btn');
                if (closeBtn) {
                    closeBtn.addEventListener('click', () => {
                        modal.close();
                    });
                }
            } else {
                console.error('Modal element not found after fetching content.');
            }
        })
        .catch(err => {
            console.error('Error fetching update order modal:', err);
            if (window.Toast) window.Toast.show('Failed to load modal.', 'error');
        });
}

// Helper function to handle the form submission
function getValue(id) {
    const element = document.getElementById(id);
    return element ? element.value : '';
}

function getSelectText(id) {
    const element = document.getElementById(id);
    return element ? element.options[element.selectedIndex].text : '';
}

// Explicitly express all fields for shipping and billing
function getShippingFields() {
    return {
        firstName: getValue('id_shipping_first_name'),
        lastName: getValue('id_shipping_last_name'),
        addressLine1: getValue('id_shipping_address_line_1'),
        addressLine2: getValue('id_shipping_address_line_2'),
        city: getValue('id_shipping_city'),
        county: getValue('id_shipping_county'),
        postcode: getValue('id_shipping_postcode'),
    };
}

function getBillingFields() {
    return {
        firstName: getValue('id_billing_first_name'),
        lastName: getValue('id_billing_last_name'),
        addressLine1: getValue('id_billing_address_line_1'),
        addressLine2: getValue('id_billing_address_line_2'),
        city: getValue('id_billing_city'),
        county: getValue('id_billing_county'),
        postcode: getValue('id_billing_postcode'),
    };
}

function attachFormSubmitListener(modal) {
    const updateOrderForm = document.getElementById('update-order-form');

    if (updateOrderForm) {
        updateOrderForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const orderId = updateOrderForm.dataset.orderId;
            const formData = new FormData(updateOrderForm);

            try {
                const response = await fetch(`/dashboard/user-profile/${orderId}/order/update/`, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    body: formData,
                    credentials: 'include',
                });

                const result = await response.json();

                // Ensure the page reloads after updating the order
                if (result.success) {
                    // Update the order card with new data
                    updateOrderCard(orderId, result.updated_shipping_address, result.updated_billing_address);

                    // Reload the page to ensure the changes are fully reflected
                    window.location.reload();

                    // Close the modal
                    modal.close();

                    // Show success message
                    if (window.Toast) window.Toast.show('Order updated successfully.', 'success');
                } else {
                    console.error('Failed to update order:', result.errors);
                    if (window.Toast) window.Toast.show('Failed to update order.', 'error');
                }
            } catch (err) {
                console.error('Error submitting update order form:', err);
                if (window.Toast) window.Toast.show('An error occurred while updating the order.', 'error');
            }
        });
    } else {
        console.error('Update order form not found in modal.');
    }
}

function updateOrderCard(orderId, updatedShipping, updatedBilling) {
    const orderCard = document.querySelector(`[data-order="${orderId}"]`).closest('.rounded-lg');

    if (orderCard) {
        const shippingEl = orderCard.querySelector('.shipping-address');
        const billingEl = orderCard.querySelector('.billing-address');

        if (shippingEl) {
            shippingEl.textContent = updatedShipping;
        } else {
            console.error('Shipping fields container not found in the DOM.');
        }

        if (billingEl) {
            billingEl.textContent = updatedBilling;
        } else {
            console.error('Billing fields container not found in the DOM.');
        }
    } else {
        console.error('Order card not found in the DOM.');
    }
}

function openDeleteOrderModal(orderId) {
    const modalContainer = document.getElementById('delete-order-modal-container');
    if (!modalContainer) {
        console.error('Delete modal container not found.');
        return;
    }

    fetch(`/dashboard/user-profile/${orderId}/order/delete/`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        })
        .then(response => {
            if (!response.ok) throw new Error('Failed to fetch delete modal content');
            return response.text();
        })
        .then(html => {
            modalContainer.innerHTML = html;

            const modal = document.getElementById('delete-order-modal');
            if (modal) {
                modal.showModal();

                attachDeleteFormSubmitListener(modal);

                const closeBtn = modal.querySelector('.js-close-modal-btn');
                if (closeBtn) {
                    closeBtn.addEventListener('click', () => {
                        modal.close();
                    });
                }
            } else {
                console.error('Delete modal element not found after fetching content.');
            }
        })
        .catch(err => {
            console.error('Error fetching delete order modal:', err);
            if (window.Toast) window.Toast.show('Failed to load delete modal.', 'error');
        });
}

function getCSRFToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfToken ? csrfToken.value : '';
}

function attachDeleteFormSubmitListener(modal) {
    const deleteOrderForm = document.getElementById('delete-order-form');

    if (deleteOrderForm) {
        deleteOrderForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const orderId = deleteOrderForm.dataset.orderId;

            try {
                const response = await fetch(`/dashboard/user-profile/${orderId}/order/delete/`, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': getCSRFToken(),
                    },
                    credentials: 'include',
                });

                const result = await response.json();

                if (result.success) {
                    // Remove the order card from the DOM
                    const orderCard = document.querySelector(`[data-order="${orderId}"]`).closest('.rounded-lg');
                    if (orderCard) {
                        orderCard.remove();
                    } else {
                        console.error('Order card not found in the DOM.');
                    }

                    // Close the modal
                    modal.close();

                    // Show success message
                    if (window.Toast) window.Toast.show('Order deleted successfully.', 'success');
                } else {
                    console.error('Failed to delete order:', result.message);
                    if (window.Toast) window.Toast.show('Failed to delete order.', 'error');
                }
            } catch (err) {
                console.error('Error submitting delete order form:', err);
                if (window.Toast) window.Toast.show('An error occurred while deleting the order.', 'error');
            }
        });
    } else {
        console.error('Delete order form not found in modal.');
    }
}
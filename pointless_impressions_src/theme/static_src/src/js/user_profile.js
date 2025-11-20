document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded event fired.');

    const updateButtons = document.querySelectorAll('.js-update-order-btn');
    console.log(`Found ${updateButtons.length} update buttons.`);

    updateButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const orderId = button.dataset.order;
            console.log(`Update button clicked. Order ID: ${orderId}`);

            if (orderId) {
                openUpdateOrderModal(orderId);
            }
        });
    });
});

function openUpdateOrderModal(orderId) {
    console.log(`Opening update order modal for Order ID: ${orderId}`);

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
            console.log(`Fetch response status: ${response.status}`);
            if (!response.ok) throw new Error('Failed to fetch modal content');
            return response.text();
        })
        .then(html => {
            console.log('Modal content fetched successfully.');
            modalContainer.innerHTML = html;

            const modal = document.getElementById('update-order-modal');
            if (modal) {
                console.log('Modal element found. Displaying modal.');
                modal.showModal();

                attachFormSubmitListener(modal);

                const closeBtn = modal.querySelector('.js-close-modal-btn');
                if (closeBtn) {
                    closeBtn.addEventListener('click', () => {
                        console.log('Close button clicked. Closing modal.');
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
                    console.log('Order updated successfully.');

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
            console.log('Updated shipping address:', updatedShipping);
        } else {
            console.error('Shipping fields container not found in the DOM.');
        }

        if (billingEl) {
            billingEl.textContent = updatedBilling;
            console.log('Updated billing address:', updatedBilling);
        } else {
            console.error('Billing fields container not found in the DOM.');
        }
    } else {
        console.error('Order card not found in the DOM.');
    }
}
document.addEventListener('DOMContentLoaded', () => {
    const publicIdInput = document.querySelector('input[name="public_id"]');

    if (!publicIdInput) {
        console.error('Public ID not found in the document.');
        return;
    }
    const publicId = publicIdInput.value;

    document.addEventListener('click', (e) => {
        if (e.target.closest('.js-edit-artwork-btn')) {
            e.preventDefault();
            const btn = e.target.closest('.js-edit-artwork-btn');
            const artworkSlug = btn.dataset.artworkSlug;
            if (artworkSlug) {
                openEditArtworkModal(publicId, artworkSlug);
            } else {
                console.error("Artwork slug missing on button");
            }
        }

        if (e.target.closest('.js-delete-artwork-btn')) {
            e.preventDefault();
            const btn = e.target.closest('.js-delete-artwork-btn');

            const artworkSlug = btn.dataset.artworkSlug;
            openDeleteArtworkModal(publicId, artworkSlug);
        }

        if (e.target.closest('.js-approve-artwork-btn')) {
            e.preventDefault();
            const btn = e.target.closest('.js-approve-artwork-btn');
            const artworkSlug = btn.dataset.artworkSlug;
            approveArtwork(publicId, artworkSlug, btn);
        }

        if (e.target.closest('.js-add-artwork-btn')) {
            e.preventDefault();
            openAddArtworkModal(publicId);
        }

        if (e.target.closest('.js-edit-order-btn')) {
            e.preventDefault();
            const btn = e.target.closest('.js-edit-order-btn');
            const orderId = btn.dataset.orderId;
            openEditOrderModal(publicId, orderId);
        }

        if (e.target.closest('.js-delete-order-btn')) {
            e.preventDefault();
            const btn = e.target.closest('.js-delete-order-btn');
            const orderId = btn.dataset.orderId;
            openDeleteOrderModal(publicId, orderId);
        }
    });

    const artworkPaginationContainer = document.querySelector('#artwork-pagination-container');
    if (artworkPaginationContainer) {
        artworkPaginationContainer.addEventListener('click', function(e) {
            const paginationLink = e.target.closest('a[href*="artwork_page="]');
            if (paginationLink) {
                e.preventDefault();
                const url = paginationLink.getAttribute('href');
                loadArtworkPage(url);
            }
        });
    }

    const orderPaginationContainer = document.querySelector('#order-pagination-container');
    if (orderPaginationContainer) {
        orderPaginationContainer.addEventListener('click', function(e) {
            const paginationLink = e.target.closest('a[href*="order_page="]');
            if (paginationLink) {
                e.preventDefault();
                const url = paginationLink.getAttribute('href');
                loadOrderPage(url);
            }
        });
    }

    function loadArtworkPage(url) {
        const artworkTableContainer = document.querySelector('#artwork-table-container');
        const paginationContainer = document.querySelector('#artwork-pagination-container');

        artworkTableContainer.style.opacity = '0.5';
        artworkTableContainer.style.pointerEvents = 'none';

        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');

            const newTable = doc.querySelector('#artwork-table-container');
            if (newTable) {
                artworkTableContainer.innerHTML = newTable.innerHTML;
            }

            const newPagination = doc.querySelector('#artwork-pagination-container');
            if (newPagination) {
                paginationContainer.innerHTML = newPagination.innerHTML;
            }

            artworkTableContainer.style.opacity = '1';
            artworkTableContainer.style.pointerEvents = 'auto';

            document.querySelector('#artwork-section').scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            });

            window.history.pushState({}, '', url);
        })
        .catch(error => {
            console.error('Error loading artwork page:', error);
            artworkTableContainer.style.opacity = '1';
            artworkTableContainer.style.pointerEvents = 'auto';
        });
    }

    function loadOrderPage(url) {
        const orderTableContainer = document.querySelector('#order-table-container');
        const paginationContainer = document.querySelector('#order-pagination-container');

        orderTableContainer.style.opacity = '0.5';
        orderTableContainer.style.pointerEvents = 'none';

        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');

            const newTable = doc.querySelector('#order-table-container');
            if (newTable) {
                orderTableContainer.innerHTML = newTable.innerHTML;
            }

            const newPagination = doc.querySelector('#order-pagination-container');
            if (newPagination) {
                paginationContainer.innerHTML = newPagination.innerHTML;
            }

            orderTableContainer.style.opacity = '1';
            orderTableContainer.style.pointerEvents = 'auto';

            document.querySelector('#order-section').scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            });

            window.history.pushState({}, '', url);
        })
        .catch(error => {
            console.error('Error loading order page:', error);
            orderTableContainer.style.opacity = '1';
            orderTableContainer.style.pointerEvents = 'auto';
        });
    }

    window.addEventListener('popstate', function() {
        location.reload();
    });
});

function setupModalCloseHandlers(modalId, containerId) {
    const container = document.getElementById(containerId);
    const modal = container.querySelector('dialog');
    const cancelBtn = container.querySelector('.js-close-modal-btn');

    if (cancelBtn) {
        cancelBtn.addEventListener('click', () => {
            closeModal(containerId);
        });
    }

    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal(containerId);
            }
        });
    }
}

function openEditArtworkModal(publicId, artworkSlug) {
    // Uses slug in URL as defined in urls.py
    const url = `/dashboard/admin-dashboard/${publicId}/edit-artwork/${artworkSlug}/`;

    fetch(url)
        .then(response => response.text())
        .then(html => {
            const modalContainer = document.getElementById('edit-artwork-modal-container');
            modalContainer.innerHTML = html;

            const modal = modalContainer.querySelector('dialog');
            if (modal) {
                modal.showModal();
                setupEditArtworkForm(publicId, artworkSlug);
            }
        })
        .catch(error => {
            console.error('Error loading edit artwork modal:', error);
            showNotification('Failed to load artwork details', 'error');
        });
}

function setupEditArtworkForm(publicId, artworkSlug) {
    const form = document.querySelector('#edit-artwork-form');
    if (!form) return;

    setupModalCloseHandlers('edit-artwork-modal', 'edit-artwork-modal-container');

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        const url = `/dashboard/admin-dashboard/${publicId}/edit-artwork/${artworkSlug}/`;
        
        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(data.message, 'success');
                closeModal('edit-artwork-modal-container');
                location.reload();
            } else {
                showNotification(data.message || 'Failed to update artwork', 'error');
                displayFormErrors(form, data.errors);
            }
        })
        .catch(error => {
            console.error('Error updating artwork:', error);
            showNotification('An unexpected error occurred.', 'error');
        });
    });
}

function openAddArtworkModal(publicId) {
    const url = `/dashboard/admin-dashboard/${publicId}/add-artwork/`;

    fetch(url)
        .then(response => response.text())
        .then(html => {
            const modalContainer = document.getElementById('add-artwork-modal-container');
            modalContainer.innerHTML = html;

            const modal = modalContainer.querySelector('dialog');
            if (modal) {
                modal.showModal();
                setupModalCloseHandlers('add-artwork-modal', 'add-artwork-modal-container');
                setupAddArtworkForm(publicId);
            }
        })
        .catch(error => {
            console.error('Error loading add artwork modal:', error);
            showNotification('Failed to load form', 'error');
        });
}

function setupAddArtworkForm(publicId) {
    const form = document.querySelector('#add-artwork-form');
    if (!form) return;

    setupModalCloseHandlers('add-artwork-modal', 'add-artwork-modal-container');

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        const url = `/dashboard/admin-dashboard/${publicId}/add-artwork/`;

        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(data.message, 'success');
                closeModal('add-artwork-modal-container');
                location.reload();
            } else {
                showNotification(data.message || 'Failed to add artwork', 'error');
                displayFormErrors(form, data.errors);
            }
        })
        .catch(error => {
            console.error('Error adding artwork:', error);
            showNotification('An unexpected error occurred.', 'error');
        });
    });
}

function openDeleteArtworkModal(publicId, artworkSlug) {
    const url = `/dashboard/admin-dashboard/${publicId}/delete-artwork/${artworkSlug}/`;

    fetch(url)
        .then(response => response.text())
        .then(html => {
            const modalContainer = document.getElementById('delete-artwork-modal-container');
            modalContainer.innerHTML = html;

            const modal = modalContainer.querySelector('dialog');
            if (modal) {
                modal.showModal();
                setupDeleteArtworkForm(publicId, artworkSlug);
            }
        })
        .catch(error => {
            console.error('Error loading delete artwork modal:', error);
            showNotification('Failed to load confirmation', 'error');
        });
}

function setupDeleteArtworkForm(publicId, artworkSlug) {
    const form = document.querySelector('#delete-artwork-form');
    if (!form) return;

    setupModalCloseHandlers('delete-artwork-modal', 'delete-artwork-modal-container');

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const url = `/dashboard/admin-dashboard/${publicId}/delete-artwork/${artworkSlug}/`;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(data.message, 'success');
                closeModal('delete-artwork-modal-container');
                location.reload();
            } else {
                showNotification(data.message || 'Failed to delete artwork', 'error');
            }
        })
        .catch(error => {
            console.error('Error deleting artwork:', error);
            showNotification('An unexpected error occurred.', 'error');
        });
    });
}

function openEditOrderModal(publicId, orderId) {
    const url = `/dashboard/admin-dashboard/${publicId}/edit-order/${orderId}/`;
    
    fetch(url)
        .then(response => response.text())
        .then(html => {
            const modalContainer = document.getElementById('edit-order-modal-container');
            modalContainer.innerHTML = html;
            
            const modal = modalContainer.querySelector('dialog');
            if (modal) {
                modal.showModal();
                setupEditOrderForm(publicId, orderId);
            }
        })
        .catch(error => {
            console.error('Error loading edit order modal:', error);
            showNotification('Failed to load order details', 'error');
        });
}

function setupEditOrderForm(publicId, orderId) {
    const form = document.querySelector('#edit-order-form');
    if (!form) return;

    setupModalCloseHandlers('edit-order-modal', 'edit-order-modal-container');

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        const url = `/dashboard/admin-dashboard/${publicId}/edit-order/${orderId}/`;

        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(data.message, 'success');
                closeModal('edit-order-modal-container');
                location.reload();
            } else {
                showNotification(data.message || 'Failed to update order', 'error');
                displayFormErrors(form, data.errors);
            }
        })
        .catch(error => {
            console.error('Error updating order:', error);
            showNotification('An unexpected error occurred.', 'error');
        });
    });
}

function openDeleteOrderModal(publicId, orderId) {
    const url = `/dashboard/admin-dashboard/${publicId}/delete-order/${orderId}/`;
    
    fetch(url)
        .then(response => response.text())
        .then(html => {
            const modalContainer = document.getElementById('delete-order-modal-container');
            modalContainer.innerHTML = html;
            
            const modal = modalContainer.querySelector('dialog');
            if (modal) {
                modal.showModal();
                setupDeleteOrderForm(publicId, orderId);
            }
        })
        .catch(error => {
            console.error('Error loading delete order modal:', error);
            showNotification('Failed to load confirmation', 'error');
        });
}

function setupDeleteOrderForm(publicId, orderId) {
    const form = document.querySelector('#delete-order-form');
    if (!form) return;

    setupModalCloseHandlers('delete-order-modal', 'delete-order-modal-container');

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const url = `/dashboard/admin-dashboard/${publicId}/delete-order/${orderId}/`;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(data.message, 'success');
                closeModal('delete-order-modal-container');
                location.reload();
            } else {
                showNotification(data.message || 'Failed to delete order', 'error');
            }
        })
        .catch(error => {
            console.error('Error deleting order:', error);
            showNotification('An unexpected error occurred.', 'error');
        });
    });
}

function approveArtwork(publicId, artworkSlug, btn) {
    const url = `/dashboard/admin-dashboard/${publicId}/approve-artwork/${artworkSlug}/`;

    btn.disabled = true;
    btn.textContent = 'Approving…';

    fetch(url, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
            location.reload();
        } else {
            showNotification(data.message || 'Failed to approve artwork', 'error');
            btn.disabled = false;
            btn.textContent = 'Approve';
        }
    })
    .catch(error => {
        console.error('Error approving artwork:', error);
        showNotification('An unexpected error occurred.', 'error');
        btn.disabled = false;
        btn.textContent = 'Approve';
    });
}

function closeModal(containerId) {
    const modalContainer = document.getElementById(containerId);
    if (modalContainer) {
        const modal = modalContainer.querySelector('dialog');
        if (modal) {
            modal.close();
        }
        setTimeout(() => {
            modalContainer.innerHTML = '';
        }, 300);
    }
}

function displayFormErrors(form, errors) {
    form.querySelectorAll('.error-message').forEach(el => el.remove());
    form.querySelectorAll('.input-error').forEach(el => el.classList.remove('input-error'));

    for (const [field, messages] of Object.entries(errors)) {
        const input = form.querySelector(`[name="${field}"]`);
        if (input) {
            input.classList.add('input-error');
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message text-red-500 text-sm mt-1';
            errorDiv.textContent = messages.join(', ');
            input.parentElement.appendChild(errorDiv);
        }
    }
}

function showNotification(message, type = 'info') {
    if (window.Toast && typeof window.Toast.show === 'function') {
        window.Toast.show(message, type);
    } else {
        console.warn('Toast system not loaded. Falling back to default notification.');
        const notification = document.createElement('div');
        notification.className = `alert ${type === 'success' ? 'alert-success' : 'alert-error'} fixed top-4 right-4 z-50 max-w-md shadow-lg`;
        notification.innerHTML = `
            <span>${message}</span>
            <button class="btn btn-sm btn-ghost" onclick="this.parentElement.remove()">✕</button>
        `;
        
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

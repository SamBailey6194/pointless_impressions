document.addEventListener('DOMContentLoaded', function() {
    const editArtworkModal = document.getElementById('edit-artwork-modal');
    const addArtworkModal = document.getElementById('add-artwork-modal');

    function openModal(modal) {
        if (modal) {
            modal.showModal();
        }
    }

    function closeModal(modal) {
        if (modal) {
            modal.close();
        }
    }

    document.querySelectorAll('.js-edit-artwork-btn').forEach(button => {
        button.addEventListener('click', function() {
            const artworkId = this.dataset.artworkId;
            fetch(`/api/artworks/${artworkId}/`) // Fetch artwork details
                .then(response => response.json())
                .then(data => {
                    // Populate modal fields with fetched data
                    document.querySelector('#edit-artwork-modal input[name="name"]').value = data.name;
                    document.querySelector('#edit-artwork-modal input[name="price"]').value = data.price;
                    document.querySelector('#edit-artwork-modal input[name="stock"]').value = data.stock;
                    openModal(editArtworkModal);
                });
        });
    });

    document.querySelectorAll('.js-remove-artwork-btn').forEach(button => {
        button.addEventListener('click', function() {
            const artworkId = this.dataset.artworkId;
            if (confirm('Are you sure you want to remove this artwork?')) {
                fetch(`/artwork/remove/${artworkId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                }).then(response => {
                    if (response.ok) {
                        location.reload();
                    } else {
                        alert('Failed to remove artwork.');
                    }
                });
            }
        });
    });

    document.querySelector('.js-add-artwork-btn').addEventListener('click', function() {
        openModal(addArtworkModal);
    });

    document.querySelectorAll('.js-close-modal-btn').forEach(button => {
        button.addEventListener('click', function() {
            const modalId = this.dataset.modalId;
            const modal = document.getElementById(modalId);
            closeModal(modal);
        });
    });
});
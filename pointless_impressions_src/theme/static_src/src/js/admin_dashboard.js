document.addEventListener('DOMContentLoaded', () => {
    // Function to open a modal
    const openModal = (modalId) => {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.showModal();
        }
    };

    // Function to close a modal
    const closeModal = (modalId) => {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.close();
        }
    };

    // Add event listeners to open modal buttons
    document.querySelectorAll('[data-modal-open]').forEach(button => {
        button.addEventListener('click', (event) => {
            const modalId = event.target.getAttribute('data-modal-open');
            openModal(modalId);
        });
    });

    // Add event listeners to close modal buttons
    document.querySelectorAll('[data-modal-close]').forEach(button => {
        button.addEventListener('click', (event) => {
            const modalId = event.target.getAttribute('data-modal-close');
            closeModal(modalId);
        });
    });
});
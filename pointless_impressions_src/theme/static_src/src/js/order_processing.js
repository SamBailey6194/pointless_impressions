document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('admin-order-detail-modal');

    function updateOrderStatus(orderId, status, notes) {
        fetch(`/api/orders/${orderId}/update/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                status: status,
                staff_notes: notes
            })
        }).then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert('Failed to update order status.');
            }
        });
    }

    modal.addEventListener('click', function(event) {
        const target = event.target;
        if (target.matches('.js-update-order-btn')) {
            const orderId = modal.dataset.orderId;
            const status = target.dataset.status;
            const notes = document.getElementById('adminStaffNotes').value;
            updateOrderStatus(orderId, status, notes);
        }
    });
});
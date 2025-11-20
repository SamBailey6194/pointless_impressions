(() => {
  // pointless_impressions_src/theme/static_src/src/js/user_profile.js
  document.addEventListener("DOMContentLoaded", () => {
    const updateButtons = document.querySelectorAll(".js-update-order-btn");
    updateButtons.forEach((button) => {
      button.addEventListener("click", (e) => {
        e.preventDefault();
        const orderId = button.dataset.order;
        if (orderId) {
          openUpdateOrderModal(orderId);
        }
      });
    });
    const deleteButtons = document.querySelectorAll(".js-delete-order-btn");
    deleteButtons.forEach((button) => {
      button.addEventListener("click", (e) => {
        e.preventDefault();
        const orderId = button.dataset.order;
        if (orderId) {
          openDeleteOrderModal(orderId);
        }
      });
    });
  });
  function openUpdateOrderModal(orderId) {
    const modalContainer = document.getElementById("update-order-modal-container");
    if (!modalContainer) {
      console.error("Modal container not found.");
      return;
    }
    fetch(`/dashboard/user-profile/${orderId}/order/update/`, {
      method: "GET",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json"
      },
      credentials: "include"
    }).then((response) => {
      if (!response.ok) throw new Error("Failed to fetch modal content");
      return response.text();
    }).then((html) => {
      modalContainer.innerHTML = html;
      const modal = document.getElementById("update-order-modal");
      if (modal) {
        modal.showModal();
        attachFormSubmitListener(modal);
        const closeBtn = modal.querySelector(".js-close-modal-btn");
        if (closeBtn) {
          closeBtn.addEventListener("click", () => {
            modal.close();
          });
        }
      } else {
        console.error("Modal element not found after fetching content.");
      }
    }).catch((err) => {
      console.error("Error fetching update order modal:", err);
      if (window.Toast) window.Toast.show("Failed to load modal.", "error");
    });
  }
  function attachFormSubmitListener(modal) {
    const updateOrderForm = document.getElementById("update-order-form");
    if (updateOrderForm) {
      updateOrderForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const orderId = updateOrderForm.dataset.orderId;
        const formData = new FormData(updateOrderForm);
        try {
          const response = await fetch(`/dashboard/user-profile/${orderId}/order/update/`, {
            method: "POST",
            headers: {
              "X-Requested-With": "XMLHttpRequest"
            },
            body: formData,
            credentials: "include"
          });
          const result = await response.json();
          if (result.success) {
            updateOrderCard(orderId, result.updated_shipping_address, result.updated_billing_address);
            window.location.reload();
            modal.close();
            if (window.Toast) window.Toast.show("Order updated successfully.", "success");
          } else {
            console.error("Failed to update order:", result.errors);
            if (window.Toast) window.Toast.show("Failed to update order.", "error");
          }
        } catch (err) {
          console.error("Error submitting update order form:", err);
          if (window.Toast) window.Toast.show("An error occurred while updating the order.", "error");
        }
      });
    } else {
      console.error("Update order form not found in modal.");
    }
  }
  function updateOrderCard(orderId, updatedShipping, updatedBilling) {
    const orderCard = document.querySelector(`[data-order="${orderId}"]`).closest(".rounded-lg");
    if (orderCard) {
      const shippingEl = orderCard.querySelector(".shipping-address");
      const billingEl = orderCard.querySelector(".billing-address");
      if (shippingEl) {
        shippingEl.textContent = updatedShipping;
      } else {
        console.error("Shipping fields container not found in the DOM.");
      }
      if (billingEl) {
        billingEl.textContent = updatedBilling;
      } else {
        console.error("Billing fields container not found in the DOM.");
      }
    } else {
      console.error("Order card not found in the DOM.");
    }
  }
  function openDeleteOrderModal(orderId) {
    const modalContainer = document.getElementById("delete-order-modal-container");
    if (!modalContainer) {
      console.error("Delete modal container not found.");
      return;
    }
    fetch(`/dashboard/user-profile/${orderId}/order/delete/`, {
      method: "GET",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json"
      },
      credentials: "include"
    }).then((response) => {
      if (!response.ok) throw new Error("Failed to fetch delete modal content");
      return response.text();
    }).then((html) => {
      modalContainer.innerHTML = html;
      const modal = document.getElementById("delete-order-modal");
      if (modal) {
        modal.showModal();
        attachDeleteFormSubmitListener(modal);
        const closeBtn = modal.querySelector(".js-close-modal-btn");
        if (closeBtn) {
          closeBtn.addEventListener("click", () => {
            modal.close();
          });
        }
      } else {
        console.error("Delete modal element not found after fetching content.");
      }
    }).catch((err) => {
      console.error("Error fetching delete order modal:", err);
      if (window.Toast) window.Toast.show("Failed to load delete modal.", "error");
    });
  }
  function getCSRFToken() {
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]");
    return csrfToken ? csrfToken.value : "";
  }
  function attachDeleteFormSubmitListener(modal) {
    const deleteOrderForm = document.getElementById("delete-order-form");
    if (deleteOrderForm) {
      console.log("Delete form found. Attaching submit listener.");
      deleteOrderForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const orderId = deleteOrderForm.dataset.orderId;
        console.log(`Submitting delete request for order ID: ${orderId}`);
        try {
          const response = await fetch(`/dashboard/user-profile/${orderId}/order/delete/`, {
            method: "POST",
            headers: {
              "X-Requested-With": "XMLHttpRequest",
              "X-CSRFToken": getCSRFToken()
            },
            credentials: "include"
          });
          const result = await response.json();
          console.log("Delete response:", result);
          if (result.success) {
            console.log("Order deleted successfully.");
            const orderCard = document.querySelector(`[data-order="${orderId}"]`).closest(".rounded-lg");
            if (orderCard) {
              orderCard.remove();
            } else {
              console.error("Order card not found in the DOM.");
            }
            modal.close();
            if (window.Toast) window.Toast.show("Order deleted successfully.", "success");
          } else {
            console.error("Failed to delete order:", result.message);
            if (window.Toast) window.Toast.show("Failed to delete order.", "error");
          }
        } catch (err) {
          console.error("Error submitting delete order form:", err);
          if (window.Toast) window.Toast.show("An error occurred while deleting the order.", "error");
        }
      });
    } else {
      console.error("Delete order form not found in modal.");
    }
  }
})();
//# sourceMappingURL=user_profile.js.map

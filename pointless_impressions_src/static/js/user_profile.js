(() => {
  // pointless_impressions_src/theme/static_src/src/js/cart.js
  function getCsrfToken() {
    const tokenEl = document.querySelector("[name=csrfmiddlewaretoken]");
    return tokenEl ? tokenEl.value : "";
  }
  async function updateCartDropdownHTML() {
    const cartDropdown = document.getElementById("cart-dropdown-content");
    if (!cartDropdown) {
      console.warn("Cart dropdown element not found. Cannot update.");
      return;
    }
    try {
      const response = await fetch("/checkout/cart-dropdown/", {
        method: "GET",
        headers: {
          "X-Requested-With": "XMLHttpRequest"
        },
        credentials: "include"
      });
      if (!response.ok) {
        throw new Error(`Failed to fetch cart: ${response.status}`);
      }
      const data = await response.json();
      cartDropdown.innerHTML = data.html;
    } catch (error) {
      console.error("Error refreshing cart dropdown:", error);
      cartDropdown.innerHTML = '<div class="p-4 text-error">Could not load cart.</div>';
    }
  }
  function openCartDropdown() {
    const cartDropdown = document.getElementById("cart-dropdown-content");
    if (!cartDropdown) return;
    const dropdownContainer = cartDropdown.closest(".dropdown");
    if (dropdownContainer) {
      dropdownContainer.classList.add("dropdown-open");
      setTimeout(() => {
        dropdownContainer.classList.remove("dropdown-open");
      }, 3e3);
    }
  }
  function initCart() {
    updateCartDropdownHTML();
  }
  if (typeof window !== "undefined") {
    window.cart = {
      init: initCart,
      updateCartDropdownHTML,
      openCartDropdown
    };
  }
  document.addEventListener("DOMContentLoaded", () => {
    if (window.cart) {
      window.cart.init();
    }
  });

  // pointless_impressions_src/theme/static_src/src/js/user_profile.js
  async function fetchOrderData(orderId) {
    try {
      const response = await fetch(`/orders/${orderId}/`, {
        method: "GET",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": getCsrfToken()
        },
        credentials: "include"
      });
      if (!response.ok) {
        throw new Error(`Failed to fetch order: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error("Error fetching order data:", error);
      return null;
    }
  }
  function populateEditUserInfoModal(formData) {
    const modal = document.getElementById("edit-user-info-modal");
    if (!modal || !formData) return;
    modal.querySelector('input[name="first_name"]').value = formData.first_name || "";
    modal.querySelector('input[name="last_name"]').value = formData.last_name || "";
    modal.querySelector('input[name="username"]').value = formData.username || "";
    modal.querySelector('input[name="email"]').value = formData.email || "";
    modal.querySelector('input[name="phone"]').value = formData.phone || "";
    modal.showModal();
  }
  function populateCombinedOrderModal(orderData) {
    const modal = document.getElementById("order-modal");
    if (!modal || !orderData) return;
    modal.querySelector(".order-id").textContent = orderData.id;
    modal.querySelector(".order-total").textContent = orderData.total;
    modal.querySelector(".order-items").innerHTML = orderData.items.map((item) => `<li>${item.name} - ${item.quantity} x ${item.price}</li>`).join("");
    const editForm = modal.querySelector("#edit-order-form");
    if (editForm) {
      editForm.querySelector('textarea[name="edit_notes"]').value = "";
    }
  }
  function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.close();
    }
  }
  function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.showModal();
    }
  }
  function toggleEditMode() {
    const editOrderForm = document.getElementById("edit-order-form");
    const orderActions = document.getElementById("order-actions");
    if (editOrderForm && orderActions) {
      editOrderForm.classList.toggle("hidden");
      orderActions.classList.toggle("hidden");
    }
  }
  var toggleEditModeButton = document.getElementById("toggle-edit-mode");
  if (toggleEditModeButton) {
    toggleEditModeButton.addEventListener("click", toggleEditMode);
  }
  function updateQuantity(button, increment) {
    const quantityInput = button.closest(".quantity-control").querySelector(".quantity-input");
    if (!quantityInput) return;
    let currentQuantity = parseInt(quantityInput.value, 10) || 0;
    const maxQuantity = parseInt(quantityInput.getAttribute("max"), 10) || Infinity;
    const minQuantity = parseInt(quantityInput.getAttribute("min"), 10) || 0;
    if (increment) {
      currentQuantity = Math.min(currentQuantity + 1, maxQuantity);
    } else {
      currentQuantity = Math.max(currentQuantity - 1, minQuantity);
    }
    quantityInput.value = currentQuantity;
  }
  document.addEventListener("click", (event) => {
    const incrementButton = event.target.closest(".quantity-increment");
    const decrementButton = event.target.closest(".quantity-decrement");
    if (incrementButton) {
      updateQuantity(incrementButton, true);
    }
    if (decrementButton) {
      updateQuantity(decrementButton, false);
    }
  });
  function populateAddressModal(addressData) {
    const modal = document.getElementById("edit-address-modal");
    const form = modal.querySelector("form");
    if (!modal || !form) return;
    form.reset();
    form.action = addressData ? `/dashboard/edit-address/${addressData.id}/` : `/dashboard/add-address/`;
    if (addressData) {
      form.querySelector('input[name="address_id"]').value = addressData.id || "";
      form.querySelector('input[name="label"]').value = addressData.label || "";
      form.querySelector('input[name="first_name"]').value = addressData.first_name || "";
      form.querySelector('input[name="last_name"]').value = addressData.last_name || "";
      form.querySelector('input[name="address_line_1"]').value = addressData.address_line_1 || "";
      form.querySelector('input[name="address_line_2"]').value = addressData.address_line_2 || "";
      form.querySelector('input[name="city"]').value = addressData.city || "";
      form.querySelector('input[name="county"]').value = addressData.county || "";
      form.querySelector('input[name="postcode"]').value = addressData.postcode || "";
      form.querySelector('select[name="country"]').value = addressData.country || "";
    }
    modal.showModal();
  }
  document.addEventListener("click", async (event) => {
    const addAddressBtn = event.target.closest(".js-add-address-btn");
    const editAddressBtn = event.target.closest(".js-edit-address-btn");
    if (addAddressBtn) {
      populateAddressModal(null);
    }
    if (editAddressBtn) {
      const addressId = editAddressBtn.getAttribute("data-address-id");
      try {
        const response = await fetch(`/dashboard/edit-address/${addressId}/`, {
          method: "GET",
          headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCsrfToken()
          },
          credentials: "include"
        });
        if (!response.ok) {
          throw new Error(`Failed to fetch address: ${response.status}`);
        }
        const addressData = await response.json();
        populateAddressModal(addressData);
      } catch (error) {
        console.error("Error fetching address data:", error);
      }
    }
  });
  document.addEventListener("click", async (event) => {
    const changePasswordBtn = event.target.closest(".js-change-password-btn");
    const editUserInfoBtn = event.target.closest(".js-edit-user-info-btn");
    const closeModalBtn = event.target.closest(".js-close-modal-btn");
    const combinedOrderBtn = event.target.closest(".js-combined-order-btn");
    if (changePasswordBtn) {
      openModal("change-password-modal");
    }
    if (editUserInfoBtn) {
      const userId = editUserInfoBtn.getAttribute("data-user-id");
      try {
        const response = await fetch(`/users/${userId}/`, {
          method: "GET",
          headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCsrfToken()
          },
          credentials: "include"
        });
        if (!response.ok) {
          throw new Error(`Failed to fetch user info: ${response.status}`);
        }
        const userData = await response.json();
        populateEditUserInfoModal(userData);
        openModal("edit-user-info-modal");
      } catch (error) {
        console.error("Error fetching user info:", error);
      }
    }
    if (combinedOrderBtn) {
      const orderId = combinedOrderBtn.getAttribute("data-order-id");
      const orderData = await fetchOrderData(orderId);
      populateCombinedOrderModal(orderData);
      openModal("order-modal");
    }
    if (closeModalBtn) {
      const modalId = closeModalBtn.getAttribute("data-modal-id");
      closeModal(modalId);
    }
  });
})();
//# sourceMappingURL=user_profile.js.map

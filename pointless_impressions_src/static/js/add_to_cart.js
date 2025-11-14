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

  // pointless_impressions_src/theme/static_src/src/js/add_to_cart.js
  function handleQuantityButtons() {
    const decrementButton = document.getElementById("decrement-quantity");
    const incrementButton = document.getElementById("increment-quantity");
    const quantityInput = document.getElementById("id_quantity");
    const stockQuantityEl = document.getElementById("stock_quantity");
    if (!decrementButton || !incrementButton || !quantityInput || !stockQuantityEl) {
      return;
    }
    const stockQuantity = parseInt(stockQuantityEl.value, 10);
    decrementButton.addEventListener("click", () => {
      const currentValue = parseInt(quantityInput.value, 10);
      if (currentValue > 1) {
        quantityInput.value = currentValue - 1;
        incrementButton.disabled = false;
      }
    });
    incrementButton.addEventListener("click", () => {
      const currentValue = parseInt(quantityInput.value, 10);
      if (currentValue < stockQuantity) {
        quantityInput.value = currentValue + 1;
        if (currentValue + 1 === stockQuantity) {
          incrementButton.disabled = true;
        }
      }
    });
    if (parseInt(quantityInput.value, 10) >= stockQuantity) {
      incrementButton.disabled = true;
    }
  }
  async function submitAddToCartForm(form) {
    const formData = new FormData(form);
    try {
      const response = await fetch(form.action, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": getCsrfToken()
        },
        body: formData,
        credentials: "include"
      });
      const data = await response.json();
      if (data.success) {
        if (window.Toast) {
          window.Toast.show(data.message, "success");
        }
        if (window.cart) {
          await window.cart.updateCartDropdownHTML();
          window.scrollTo({ top: 0, behavior: "smooth" });
          window.cart.openCartDropdown();
        }
      } else {
        let errorMsg = "Failed to add item. Please try again.";
        if (data.errors) {
          errorMsg = Object.values(data.errors).map((e) => e[0]).join(" ");
        }
        if (window.Toast) {
          window.Toast.show(errorMsg, "error");
        }
        console.error("Failed to add item to cart:", data.errors);
      }
    } catch (error) {
      console.error("Error submitting AddToCart form:", error);
      if (window.Toast) {
        window.Toast.show("An unexpected error occurred.", "error");
      }
    }
  }
  document.addEventListener("DOMContentLoaded", () => {
    handleQuantityButtons();
    const addToCartForm = document.getElementById("add_to_cart_form");
    if (addToCartForm) {
      addToCartForm.addEventListener("submit", (event) => {
        event.preventDefault();
        submitAddToCartForm(addToCartForm);
      });
    }
  });
})();
//# sourceMappingURL=add_to_cart.js.map

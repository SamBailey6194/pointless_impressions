(() => {
  // pointless_impressions_src/theme/static_src/src/js/cart.js
  function getCsrfToken() {
    const tokenEl = document.querySelector("[name=csrfmiddlewaretoken]");
    return tokenEl ? tokenEl.value : "";
  }
  function getSessionToken() {
    try {
      const sessionid = document.cookie.split("; ").find((row) => row.startsWith("sessionid="))?.split("=")[1];
      return sessionid || null;
    } catch (error) {
      console.error("Error retrieving session ID:", error);
      return null;
    }
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
})();
//# sourceMappingURL=cart.js.map

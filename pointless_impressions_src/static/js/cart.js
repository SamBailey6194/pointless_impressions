(() => {
  // pointless_impressions_src/theme/static_src/src/js/cart.js
  function getCsrfToken() {
    const tokenEl = document.querySelector("[name=csrfmiddlewaretoken]");
    return tokenEl ? tokenEl.value : "";
  }
  async function fetchCartFromServer() {
    try {
      const response = await fetch("/checkout/", {
        method: "GET",
        headers: {
          "X-Requested-With": "XMLHttpRequest"
        },
        credentials: "include"
      });
      if (!response.ok) {
        throw new Error("Failed to fetch cart data");
      }
      return await response.json();
    } catch (error) {
      console.error("Error fetching cart:", error);
      return { items: [], total_items: 0 };
    }
  }
  async function updateCartCountBadge() {
    const cartCountEl = document.querySelector("[data-cart-count]");
    if (cartCountEl) {
      const cart = await fetchCartFromServer();
      const count = cart.total_items || 0;
      cartCountEl.textContent = count;
      cartCountEl.style.display = count > 0 ? "inline-block" : "none";
    }
  }
  async function addItemToCart(item) {
    try {
      const formData = new FormData();
      formData.append("artwork_id", item.id);
      formData.append("quantity", item.quantity);
      const response = await fetch("/checkout/", {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": getCsrfToken(),
          "X-Requested-With": "XMLHttpRequest"
        },
        credentials: "include"
      });
      if (!response.ok) {
        throw new Error("Failed to add item to cart");
      }
      await updateCartCountBadge();
    } catch (error) {
      console.error("Error adding item to cart:", error);
    }
  }
  async function removeCartItem(itemId) {
    try {
      const formData = new FormData();
      formData.append("artwork_id", itemId);
      formData.append("quantity", 0);
      const response = await fetch("/checkout/", {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": getCsrfToken(),
          "X-Requested-With": "XMLHttpRequest"
        },
        credentials: "include"
      });
      if (!response.ok) {
        throw new Error("Failed to remove item from cart");
      }
      await updateCartCountBadge();
    } catch (error) {
      console.error("Error removing item from cart:", error);
    }
  }
  async function refreshAndOpenCartDropdown() {
    const response = await fetch("/checkout/cart-dropdown/", {
      method: "GET",
      headers: {
        "X-Requested-With": "XMLHttpRequest"
      },
      credentials: "include"
    });
    if (!response.ok) {
      throw new Error("Failed to refresh cart dropdown");
    }
    const html = await response.text();
    const cartDropdown = document.getElementById("cart-dropdown");
    if (cartDropdown) {
      cartDropdown.innerHTML = html;
    }
  }
  async function submitAddToCartForm(form) {
    try {
      const formData = new FormData(form);
      const response = await fetch(form.action, {
        method: "POST",
        body: formData,
        headers: {
          "X-Requested-With": "XMLHttpRequest"
        },
        credentials: "include"
      });
      if (!response.ok) {
        throw new Error("Failed to submit AddToCart form");
      }
      const data = await response.json();
      if (data.success) {
        const artworkDetailContainer = document.getElementById("artwork-detail-container");
        if (artworkDetailContainer) {
          artworkDetailContainer.innerHTML = data.html;
        }
        await refreshAndOpenCartDropdown();
      } else {
        console.error("Form submission errors:", data.errors);
      }
    } catch (error) {
      console.error("Error submitting AddToCart form:", error);
    }
  }
  function initCart() {
    updateCartCountBadge().catch((error) => {
      console.error("Failed to initialize cart:", error);
    });
  }
  if (typeof window !== "undefined") {
    window.cart = {
      init: initCart,
      add: addItemToCart,
      remove: removeCartItem,
      updateBadge: updateCartCountBadge,
      refreshAndOpenDropdown: refreshAndOpenCartDropdown
    };
    document.addEventListener("DOMContentLoaded", () => {
      initCart();
      const addToCartForm = document.getElementById("add-to-cart-form");
      if (addToCartForm) {
        addToCartForm.addEventListener("submit", async (event) => {
          event.preventDefault();
          await submitAddToCartForm(addToCartForm);
        });
      }
    });
  }
})();
//# sourceMappingURL=cart.js.map

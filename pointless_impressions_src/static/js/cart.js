(() => {
  // pointless_impressions_src/theme/static_src/src/js/cart.js
  var CART_STORAGE_KEY = "cart";
  var API_ENDPOINTS = {
    ADD: "/checkout/api/cart/add/",
    REMOVE: "/checkout/api/cart/remove/",
    UPDATE: "/checkout/api/cart/update/",
    SYNC: "/checkout/api/cart/sync/"
  };
  function formatPrice(price) {
    if (typeof price !== "number") {
      return "\xA30.00";
    }
    return "\xA3" + price.toLocaleString("en-GB", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });
  }
  function getCart() {
    try {
      return JSON.parse(localStorage.getItem(CART_STORAGE_KEY)) || {};
    } catch (e) {
      console.error("Error parsing cart from localStorage:", e);
      return {};
    }
  }
  function saveCart(cart) {
    try {
      localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cart));
    } catch (e) {
      console.error("Error saving cart to localStorage:", e);
    }
  }
  function clearCart() {
    try {
      localStorage.removeItem(CART_STORAGE_KEY);
    } catch (e) {
      console.error("Error clearing cart:", e);
    }
  }
  function addToCart(artworkId, quantity = 1, price = 0, name = "") {
    let cart = getCart();
    if (cart[artworkId]) {
      cart[artworkId].quantity += quantity;
    } else {
      cart[artworkId] = {
        id: artworkId,
        name,
        quantity,
        price
      };
    }
    saveCart(cart);
    return cart[artworkId];
  }
  function removeFromCart(artworkId) {
    let cart = getCart();
    if (cart[artworkId]) {
      delete cart[artworkId];
      saveCart(cart);
      return true;
    }
    return false;
  }
  function updateQuantity(artworkId, newQuantity) {
    let cart = getCart();
    if (cart[artworkId]) {
      if (newQuantity <= 0) {
        return removeFromCart(artworkId) ? null : cart[artworkId];
      }
      cart[artworkId].quantity = newQuantity;
      saveCart(cart);
      return cart[artworkId];
    }
    return null;
  }
  function calculateTotal() {
    const cart = getCart();
    let total = 0;
    Object.keys(cart).forEach((artworkId) => {
      const item = cart[artworkId];
      total += item.quantity * item.price;
    });
    return Math.round(total * 100) / 100;
  }
  function getCartItemCount() {
    const cart = getCart();
    return Object.keys(cart).length;
  }
  function getTotalQuantity() {
    const cart = getCart();
    let total = 0;
    Object.keys(cart).forEach((artworkId) => {
      total += cart[artworkId].quantity;
    });
    return total;
  }
  function isCartEmpty() {
    return getCartItemCount() === 0;
  }
  function getCartItem(artworkId) {
    const cart = getCart();
    return cart[artworkId] || null;
  }
  function updateCartItem(artworkId, updates) {
    let cart = getCart();
    if (cart[artworkId]) {
      cart[artworkId] = { ...cart[artworkId], ...updates };
      saveCart(cart);
      return cart[artworkId];
    }
    return null;
  }
  async function syncCartWithBackend() {
    const cart = getCart();
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]")?.value;
    if (!csrfToken) {
      console.warn("CSRF token not found for cart sync");
      return { error: "CSRF token not found" };
    }
    try {
      const response = await fetch(API_ENDPOINTS.SYNC, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({ cart })
      });
      if (!response.ok) {
        throw new Error(`Sync failed with status ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error("Error syncing cart with backend:", error);
      throw error;
    }
  }
  async function addToCartViaAPI(artworkId, quantity = 1, options = {}) {
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]")?.value;
    if (!csrfToken) {
      console.warn("CSRF token not found for API request");
      throw new Error("CSRF token not found");
    }
    const formData = new FormData();
    formData.append("artwork_id", artworkId);
    formData.append("quantity", quantity);
    if (options.framing_option) {
      formData.append("framing_option", options.framing_option);
    }
    if (options.notes) {
      formData.append("notes", options.notes);
    }
    try {
      const response = await fetch(API_ENDPOINTS.ADD, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken
        },
        body: formData
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Failed to add item to cart");
      }
      if (data.cart) {
        saveCart(data.cart);
      }
      return data;
    } catch (error) {
      console.error("Error adding to cart via API:", error);
      throw error;
    }
  }
  async function removeFromCartViaAPI(artworkId) {
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]")?.value;
    if (!csrfToken) {
      throw new Error("CSRF token not found");
    }
    const formData = new FormData();
    formData.append("artwork_id", artworkId);
    try {
      const response = await fetch(API_ENDPOINTS.REMOVE, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken
        },
        body: formData
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Failed to remove item from cart");
      }
      removeFromCart(artworkId);
      return data;
    } catch (error) {
      console.error("Error removing from cart via API:", error);
      throw error;
    }
  }
  async function updateQuantityViaAPI(artworkId, quantity) {
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]")?.value;
    if (!csrfToken) {
      throw new Error("CSRF token not found");
    }
    const formData = new FormData();
    formData.append("artwork_id", artworkId);
    formData.append("quantity", quantity);
    try {
      const response = await fetch(API_ENDPOINTS.UPDATE, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken
        },
        body: formData
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Failed to update quantity");
      }
      if (quantity > 0) {
        updateQuantity(artworkId, quantity);
      } else {
        removeFromCart(artworkId);
      }
      return data;
    } catch (error) {
      console.error("Error updating quantity via API:", error);
      throw error;
    }
  }
  function initCartUI() {
    updateCartCountBadge();
    window.addEventListener("storage", (e) => {
      if (e.key === CART_STORAGE_KEY) {
        updateCartCountBadge();
      }
    });
  }
  function updateCartCountBadge() {
    const cartCountEl = document.querySelector("[data-cart-count]");
    if (cartCountEl) {
      const count = getTotalQuantity();
      cartCountEl.textContent = count;
      cartCountEl.style.display = count > 0 ? "block" : "none";
    }
  }
  function debugCart() {
    const cart = getCart();
    console.log("Cart Contents:", cart);
    console.log("Item Count:", getCartItemCount());
    console.log("Total Quantity:", getTotalQuantity());
    console.log("Total Price:", formatPrice(calculateTotal()));
    return cart;
  }
})();
//# sourceMappingURL=cart.js.map

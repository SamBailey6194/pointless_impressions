(() => {
  // pointless_impressions_src/theme/static_src/src/js/cart.js
  var CART_UUID_KEY = "cart_uuid";
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
  function getCartUUID() {
    return localStorage.getItem(CART_UUID_KEY) || null;
  }
  function setCartUUID(uuid) {
    if (uuid) {
      localStorage.setItem(CART_UUID_KEY, uuid);
      document.cookie = "cart_uuid=" + uuid + ";path=/;max-age=2592000";
    }
  }
  function saveCartUUID(uuid) {
    setCartUUID(uuid);
  }
  function clearCartUUID() {
    localStorage.removeItem(CART_UUID_KEY);
  }
  async function fetchCartFromBackend() {
    const cart_uuid = getCartUUID();
    if (!cart_uuid) return {};
    try {
      const response = await fetch(`/checkout/api/cart/fetch/?cart_uuid=${cart_uuid}`);
      if (!response.ok) throw new Error("Failed to fetch cart");
      return await response.json();
    } catch (e) {
      console.error("Error fetching cart from backend:", e);
      return {};
    }
  }
  async function addToCartViaAPI(artworkId, quantity = 1, options = {}) {
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]")?.value;
    const cart_uuid = getCartUUID();
    if (!csrfToken) throw new Error("CSRF token not found");
    const formData = new FormData();
    formData.append("artwork_id", artworkId);
    formData.append("quantity", quantity);
    if (options.framing_option) formData.append("framing_option", options.framing_option);
    if (options.notes) formData.append("notes", options.notes);
    let url = API_ENDPOINTS.ADD;
    if (cart_uuid) url += `?cart_uuid=${cart_uuid}`;
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
        body: formData
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Failed to add item to cart");
      if (data.cart_uuid) saveCartUUID(data.cart_uuid);
      return data;
    } catch (error) {
      console.error("Error adding to cart via API:", error);
      throw error;
    }
  }
  async function removeFromCartViaAPI(artworkId) {
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]")?.value;
    const cart_uuid = getCartUUID();
    if (!csrfToken) throw new Error("CSRF token not found");
    const formData = new FormData();
    formData.append("artwork_id", artworkId);
    let url = API_ENDPOINTS.REMOVE;
    if (cart_uuid) url += `?cart_uuid=${cart_uuid}`;
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
        body: formData
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Failed to remove item from cart");
      if (data.cart_uuid) saveCartUUID(data.cart_uuid);
      return data;
    } catch (error) {
      console.error("Error removing from cart via API:", error);
      throw error;
    }
  }
  async function updateQuantityViaAPI(artworkId, quantity) {
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]")?.value;
    const cart_uuid = getCartUUID();
    if (!csrfToken) throw new Error("CSRF token not found");
    const formData = new FormData();
    formData.append("artwork_id", artworkId);
    formData.append("quantity", quantity);
    let url = API_ENDPOINTS.UPDATE;
    if (cart_uuid) url += `?cart_uuid=${cart_uuid}`;
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
        body: formData
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Failed to update quantity");
      if (data.cart_uuid) saveCartUUID(data.cart_uuid);
      return data;
    } catch (error) {
      console.error("Error updating quantity via API:", error);
      throw error;
    }
  }
  async function syncCartWithBackend() {
    return { success: true, cart_uuid: getCartUUID() };
  }
  async function getCartItemCount() {
    const cart = await fetchCartFromBackend();
    return cart.items ? cart.items.length : 0;
  }
  async function getTotalQuantity() {
    const cart = await fetchCartFromBackend();
    let total = 0;
    if (cart.items) {
      cart.items.forEach((item) => {
        total += item.quantity;
      });
    }
    return total;
  }
  async function calculateTotal() {
    const cart = await fetchCartFromBackend();
    let total = 0;
    if (cart.items) {
      cart.items.forEach((item) => {
        total += item.total || item.price * item.quantity;
      });
    }
    return Math.round(total * 100) / 100;
  }
  function initCartUI() {
    updateCartCountBadge();
    window.addEventListener("storage", (e) => {
      if (e.key === CART_UUID_KEY) {
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
  function initCart() {
    syncCartWithBackend().then((response) => {
      if (response?.success) {
        if (window.updateCartDisplay && typeof window.updateCartDisplay === "function") {
          window.updateCartDisplay();
        }
      }
    }).catch((err) => {
      console.error("\u274C Failed to sync cart on page load:", err);
    });
  }
  if (typeof window !== "undefined") {
    window.initCart = initCart;
    window.getTotalQuantity = getTotalQuantity;
    window.calculateTotal = calculateTotal;
    window.formatPrice = formatPrice;
  }
})();
//# sourceMappingURL=cart.js.map

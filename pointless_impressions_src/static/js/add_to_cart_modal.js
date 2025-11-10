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
  function saveCartUUID(uuid) {
    if (uuid) {
      localStorage.setItem(CART_UUID_KEY, uuid);
    }
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
  async function syncCartWithBackend() {
    return { success: true, cart_uuid: getCartUUID() };
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

  // pointless_impressions_src/theme/static_src/src/js/add_to_cart_modal.js
  var Toast = window.Toast;
  var addToCartModal = {
    // Current artwork being added
    currentArtwork: null,
    /**
     * Initialize modal with artwork data
     * @param {string} artworkId - The artwork identifier
     * @param {string} artworkName - Display name of artwork
     * @param {number} artworkPrice - Price of artwork
     * @param {string} artworkImage - URL to artwork image
     * @param {number} quantity - Available quantity/stock
     * @param {array} framingOptions - Array of framing option objects [{id, name}, ...]
     */
    init(artworkId, artworkName, artworkPrice, artworkImage, quantity, framingOptions = []) {
      this.currentArtwork = {
        id: artworkId,
        name: artworkName,
        price: parseFloat(artworkPrice),
        image: artworkImage,
        quantity,
        framingOptions
      };
      document.getElementById("modal_artwork_id").value = artworkId;
      document.getElementById("modal_artwork_name").textContent = artworkName;
      document.getElementById("modal_artwork_price").textContent = formatPrice(artworkPrice);
      const imageEl = document.getElementById("modal_artwork_image");
      const placeholderEl = document.getElementById("modal_image_placeholder");
      if (artworkImage) {
        imageEl.src = artworkImage;
        placeholderEl.classList.add("hidden");
        imageEl.classList.remove("hidden");
      } else {
        imageEl.classList.add("hidden");
        placeholderEl.classList.remove("hidden", "flex");
        placeholderEl.classList.add("flex");
      }
      document.getElementById("quantity").value = 1;
      document.getElementById("quantity").max = Math.max(quantity, 1);
      document.getElementById("max_quantity_info").textContent = quantity > 0 ? `Max: ${quantity}` : "Out of stock";
      document.getElementById("modal_artwork_stock").textContent = quantity > 0 ? `${quantity} in stock` : "Out of stock";
      this.setupFramingOptions(framingOptions);
      this.resetForm();
      document.getElementById("add_to_cart_modal").showModal();
    },
    /**
     * Setup framing options in dropdown
     * @param {array} framingOptions - Array of framing option objects
     */
    setupFramingOptions(framingOptions) {
      const framingSelect = document.getElementById("framing_option");
      framingSelect.innerHTML = '<option value="" disabled selected>Select framing option...</option>';
      if (framingOptions.length > 0) {
        document.getElementById("framing_section").classList.remove("hidden");
        framingOptions.forEach((option) => {
          const opt = document.createElement("option");
          opt.value = option.id;
          opt.textContent = option.name;
          framingSelect.appendChild(opt);
        });
      } else {
        document.getElementById("framing_section").classList.add("hidden");
      }
    },
    /**
     * Reset form to default state
     */
    resetForm() {
      document.getElementById("qty_error").classList.add("hidden");
      document.getElementById("form_error").classList.add("hidden");
      document.getElementById("form_success").classList.add("hidden");
      document.getElementById("notes").value = "";
      document.getElementById("notes_count").textContent = "0/500";
      document.getElementById("framing_option").value = "";
    },
    /**
     * Increase quantity by 1
     */
    increaseQuantity() {
      const input = document.getElementById("quantity");
      const max = parseInt(input.max) || 999;
      const current = parseInt(input.value) || 1;
      if (current < max) {
        input.value = current + 1;
        this.clearQtyError();
      }
    },
    /**
     * Decrease quantity by 1
     */
    decreaseQuantity() {
      const input = document.getElementById("quantity");
      const current = parseInt(input.value) || 1;
      if (current > 1) {
        input.value = current - 1;
        this.clearQtyError();
      }
    },
    /**
     * Validate quantity input
     * @returns {boolean} True if valid, false otherwise
     */
    validateQuantity() {
      const input = document.getElementById("quantity");
      const max = this.currentArtwork?.quantity || parseInt(input.max) || 999;
      let current = parseInt(input.value) || 1;
      if (current < 1) {
        input.value = 1;
        this.showQtyError("Quantity must be at least 1");
        return false;
      }
      if (current > max) {
        input.value = max;
        this.showQtyError(`Maximum ${max} available`);
        return false;
      }
      this.clearQtyError();
      return true;
    },
    /**
     * Show quantity error message
     * @param {string} message - Error message to display
     */
    showQtyError(message) {
      const errorEl = document.getElementById("qty_error");
      errorEl.textContent = message;
      errorEl.classList.remove("hidden");
    },
    /**
     * Clear quantity error message
     */
    clearQtyError() {
      document.getElementById("qty_error").classList.add("hidden");
    },
    /**
     * Show form error message
     * @param {string} message - Error message to display
     */
    showError(message) {
      const formErrorEl = document.getElementById("form_error");
      const errorMessageEl = document.getElementById("error_message");
      if (formErrorEl && errorMessageEl) {
        errorMessageEl.textContent = message;
        formErrorEl.classList.remove("hidden");
      }
      if (Toast && typeof Toast.error === "function") {
        Toast.error(message);
      } else {
        console.error("\u274C Toast.error not available!", Toast);
      }
    },
    /** 
     * Show form success message
     * @param {string} message - Success message to display
     */
    showSuccess(message) {
      const formSuccessEl = document.getElementById("form_success");
      const successMessageEl = document.getElementById("success_message");
      if (formSuccessEl && successMessageEl) {
        successMessageEl.textContent = message;
        formSuccessEl.classList.remove("hidden");
      }
      if (Toast && typeof Toast.success === "function") {
        Toast.success(message);
      } else {
        console.error("\u274C Toast.success not available!", Toast);
      }
    },
    /**
     * Handle form submission
     * @param {Event} event - Form submit event
     */
    async handleSubmit(event) {
      event.preventDefault();
      if (!this.validateQuantity()) return;
      const quantity = parseInt(document.getElementById("quantity").value) || 1;
      const framingOption = document.getElementById("framing_option").value;
      const notes = document.getElementById("notes").value.trim();
      const framingSection = document.getElementById("framing_section");
      if (!framingSection.classList.contains("hidden") && !framingOption) {
        this.showError("Please select a framing option.");
        return;
      }
      if (quantity < 1 || quantity > this.currentArtwork.quantity) {
        this.showError("Invalid quantity.");
        return;
      }
      const submitBtn = document.getElementById("submit_btn");
      const originalText = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Adding...';
      try {
        const response = await addToCartViaAPI(
          this.currentArtwork.id,
          quantity,
          { framing_option: framingOption, notes }
        );
        if (response.success) {
          this.showSuccess(response.message || "Added to cart!");
          if (window.updateCartDisplay && typeof window.updateCartDisplay === "function") {
            window.updateCartDisplay();
          }
          setTimeout(() => {
            document.getElementById("add_to_cart_modal").close();
            setTimeout(() => {
              if (window.showCartDropdown && typeof window.showCartDropdown === "function") {
                window.showCartDropdown();
              }
            }, 250);
          }, 1200);
        } else {
          this.showError(response.message || "Failed to add to cart.");
        }
      } catch (error) {
        this.showError(error.message || "Failed to add to cart.");
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
      }
    }
  };
  function initAddToCartModal() {
    const qtyIncreaseBtn = document.getElementById("qty_increase");
    const qtyDecreaseBtn = document.getElementById("qty_decrease");
    const quantityInput = document.getElementById("quantity");
    const form = document.getElementById("add_to_cart_form");
    const notesInput = document.getElementById("notes");
    if (qtyIncreaseBtn) {
      qtyIncreaseBtn.addEventListener("click", () => addToCartModal.increaseQuantity());
    }
    if (qtyDecreaseBtn) {
      qtyDecreaseBtn.addEventListener("click", () => addToCartModal.decreaseQuantity());
    }
    if (quantityInput) {
      quantityInput.addEventListener("change", () => addToCartModal.validateQuantity());
      quantityInput.addEventListener("input", (e) => {
        let value = parseInt(e.target.value) || 0;
        if (value < 1) {
          e.target.value = 1;
          addToCartModal.showQtyError("Quantity must be at least 1");
          return;
        }
        const max = addToCartModal.currentArtwork?.quantity || 999;
        if (value > max) {
          e.target.value = max;
          addToCartModal.showQtyError(`Maximum ${max} available`);
          return;
        }
        addToCartModal.clearQtyError();
      });
      quantityInput.addEventListener("paste", (e) => {
        setTimeout(() => {
          addToCartModal.validateQuantity();
        }, 10);
      });
    }
    if (form) {
      form.addEventListener("submit", (e) => addToCartModal.handleSubmit(e));
    }
    if (notesInput) {
      notesInput.addEventListener("input", (e) => {
        document.getElementById("notes_count").textContent = `${e.target.value.length}/500`;
      });
    }
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAddToCartModal);
  } else {
    initAddToCartModal();
  }
  window.addToCartModal = addToCartModal;
})();
//# sourceMappingURL=add_to_cart_modal.js.map

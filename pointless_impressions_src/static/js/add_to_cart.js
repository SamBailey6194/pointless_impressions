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

  // pointless_impressions_src/theme/static_src/src/js/add_to_cart.js
  function handleAddToCartFormSubmission() {
    const addToCartForm = document.getElementById("add_to_cart_form");
    if (addToCartForm) {
      addToCartForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        console.log("Add to Cart form submitted");
        await refreshCartDropdown();
      });
    }
  }
  function handleQuantityButtons() {
    const decrementButton = document.getElementById("decrement-quantity");
    const incrementButton = document.getElementById("increment-quantity");
    const quantityInput = document.getElementById("id_quantity");
    const stockQuantity = parseInt(document.getElementById("stock_quantity").value, 10);
    if (decrementButton && incrementButton && quantityInput) {
      decrementButton.addEventListener("click", () => {
        const currentValue = parseInt(quantityInput.value, 10);
        console.log("Decrement button clicked, current value:", currentValue);
        if (currentValue > 1) {
          quantityInput.value = currentValue - 1;
          incrementButton.disabled = false;
        }
      });
      incrementButton.addEventListener("click", () => {
        const currentValue = parseInt(quantityInput.value, 10);
        console.log("Increment button clicked, current value:", currentValue);
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
  }
  async function submitAddToCartForm2(form) {
    const formData = new FormData(form);
    console.log("Submitting AddToCart form with data:", Object.fromEntries(formData));
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
      console.log("Response from AddToCart form submission:", data);
      if (data.success) {
        refreshAndOpenCartDropdownWithDelay();
      } else {
        console.error("Failed to add item to cart:", data.error);
      }
    } catch (error) {
      console.error("Error submitting AddToCart form:", error);
    }
  }
  async function refreshAndOpenCartDropdownWithDelay() {
    try {
      console.log("Waiting for session ID to become available...");
      await new Promise((resolve) => setTimeout(resolve, 100));
      const sessionid = getSessionToken();
      console.log("Using Session ID after delay:", sessionid);
      const response = await fetch("/checkout/cart-dropdown/", {
        method: "GET",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-Session-Token": sessionid
          // Include session ID in headers
        }
      });
      if (!response.ok) {
        console.error("Failed to refresh cart dropdown:", response.status);
        throw new Error("Failed to refresh cart dropdown");
      }
      const data = await response.json();
      console.log("Cart dropdown data:", data);
      const cartDropdown = document.getElementById("cart-dropdown");
      if (cartDropdown) {
        console.log("Updating cart dropdown HTML...");
        cartDropdown.innerHTML = data.html;
        console.log("Cart dropdown updated successfully");
        const cartItemsList = document.getElementById("cart-items-list");
        if (cartItemsList) {
          console.log("Cart items list found. Items:", cartItemsList.innerHTML);
        } else {
          console.warn("Cart items list not found in updated dropdown.");
        }
      } else {
        console.warn("Cart dropdown element not found");
      }
    } catch (error) {
      console.error("Error refreshing and opening cart dropdown:", error);
    }
  }
  function getSessionToken() {
    try {
      console.log("Attempting to retrieve session ID from cookies...");
      console.log("Document cookies:", document.cookie);
      const sessionid = document.cookie.split("; ").find((row) => row.startsWith("sessionid="))?.split("=")[1];
      if (!sessionid) {
        console.warn("Session ID not found in cookies. Ensure the sessionid cookie is set and accessible.");
      } else {
        console.log("Session ID retrieved successfully:", sessionid);
      }
      return sessionid || null;
    } catch (error) {
      console.error("Error retrieving session ID from cookies:", error);
      return null;
    }
  }
  document.addEventListener("DOMContentLoaded", () => {
    console.log("Document loaded, initializing AddToCart functionality");
    handleAddToCartFormSubmission();
    handleQuantityButtons();
    const addToCartForm = document.getElementById("add_to_cart_form");
    if (addToCartForm) {
      addToCartForm.addEventListener("submit", (event) => {
        event.preventDefault();
        console.log("AddToCart form submit event triggered");
        submitAddToCartForm2(addToCartForm);
      });
    }
  });
})();
//# sourceMappingURL=add_to_cart.js.map

(() => {
  // pointless_impressions_src/theme/static_src/src/js/checkout.js
  document.addEventListener("DOMContentLoaded", function() {
    async function refreshOrderSummary() {
      const orderSummary = document.querySelector("#order-summary-section");
      if (!orderSummary) {
        window.location.reload();
        return;
      }
      try {
        const response = await fetch(window.location.href, { headers: { "X-Requested-With": "XMLHttpRequest" } });
        if (!response.ok) throw new Error("Failed to fetch updated order summary");
        const html = await response.text();
        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = html;
        const newSummary = tempDiv.querySelector("#order-summary-section");
        if (newSummary) {
          orderSummary.replaceWith(newSummary);
        } else {
          window.location.reload();
        }
      } catch (err) {
        window.location.reload();
      }
    }
    document.body.addEventListener("click", async function(e) {
      if (e.target.classList.contains("js-qty-plus") || e.target.classList.contains("js-qty-minus")) {
        e.preventDefault();
        const form = e.target.closest(".js-cart-item-form");
        if (!form) return;
        const qtyInput = form.querySelector('input[name="quantity"]');
        if (!qtyInput) return;
        let val = parseInt(qtyInput.value, 10) || 0;
        const max = parseInt(qtyInput.getAttribute("max"), 10) || 999;
        const min = parseInt(qtyInput.getAttribute("min"), 10) || 0;
        if (e.target.classList.contains("js-qty-plus") && val < max) {
          qtyInput.value = val + 1;
        } else if (e.target.classList.contains("js-qty-minus") && val > min) {
          qtyInput.value = val - 1;
        }
        qtyInput.dispatchEvent(new Event("change", { bubbles: true }));
      }
    });
    document.body.addEventListener("submit", async function(e) {
      if (e.target.classList.contains("js-cart-item-form")) {
        e.preventDefault();
        const form = e.target;
        const artworkIdInput = form.querySelector('input[name="artwork_id"]');
        const quantityInput = form.querySelector('input[name="quantity"]');
        if (!artworkIdInput || !quantityInput) {
          console.error("Artwork ID or quantity input not found in form.");
          return;
        }
        const artworkId = artworkIdInput.value;
        const quantity = parseInt(quantityInput.value, 10);
        let result;
        if (quantity === 0) {
          result = await window.cart.removeCartItem(artworkId);
        } else {
          result = await window.cart.updateCartItem(artworkId, quantity);
        }
        if (result.success) {
          await refreshOrderSummary();
          if (window.showNotification) {
            window.showNotification(result.message, "success");
          } else {
            alert(result.message, "error");
          }
        }
      }
    });
  });
})();
//# sourceMappingURL=checkout.js.map

(() => {
  // pointless_impressions_src/theme/static_src/src/js/cart.js
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

  // pointless_impressions_src/theme/static_src/src/js/artwork_detail.js
  function displayArtworkDetail(artworkData) {
    if (!artworkData) {
      console.error("No artwork data provided to display.");
      return;
    }
    const titleElement = document.getElementById("artwork-title");
    const descriptionElement = document.getElementById("artwork-description");
    const priceElement = document.getElementById("artwork-price");
    const imageElement = document.getElementById("artwork-image");
    const statusElement = document.getElementById("availability-status");
    if (titleElement) {
      titleElement.textContent = artworkData.name || "";
    }
    if (descriptionElement) {
      descriptionElement.textContent = artworkData.description || "";
    }
    if (priceElement) {
      priceElement.textContent = artworkData.price || "";
    }
    if (imageElement) {
      imageElement.src = artworkData.image_url || "";
      imageElement.alt = artworkData.alt_text || artworkData.name || "";
    }
    if (statusElement) {
      statusElement.textContent = artworkData.availability || "Unknown";
    }
  }
  function initArtworkDetail() {
    if (window.carousel && window.carousel.initArtworkDetailCarousel) {
      window.carousel.initArtworkDetailCarousel();
    } else {
      console.error("Carousel script not loaded.");
    }
  }
  document.addEventListener("DOMContentLoaded", initArtworkDetail);
})();
//# sourceMappingURL=artwork_detail.js.map

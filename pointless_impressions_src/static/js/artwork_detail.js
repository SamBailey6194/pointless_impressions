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
      imageElement.src = artworkData.image || "";
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
    initializeReviewFunctionality();
  }
  async function submitReview() {
    const form = document.getElementById("review_form");
    const modal = document.getElementById("review_modal");
    const formData = new FormData(form);
    try {
      const response = await fetch(form.action, {
        method: "POST",
        body: formData,
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": getCCsrfToken()
        }
      });
      const data = await response.json();
      if (response.ok) {
        if (window.Toast) {
          window.Toast.show(data.message, "success");
        }
        form.reset();
        if (modal) modal.close();
        setTimeout(() => {
          window.location.reload();
        }, 1e3);
      } else {
        const errorMsg = data.error || (data.errors ? Object.values(data.errors).join(" ") : "An error occurred.");
        if (window.Toast) {
          window.Toast.show(errorMsg, "error");
        }
        console.error("Form errors:", data.errors);
      }
    } catch (error) {
      console.error("Error submitting review:", error);
      if (window.Toast) {
        window.Toast.show("Failed to submit review. Please try again.", "error");
      }
    }
  }
  function handleViewReviewsScroll() {
    const viewReviewsBtn = document.querySelector("[data-scroll-to-reviews]");
    if (viewReviewsBtn) {
      viewReviewsBtn.addEventListener("click", function() {
        const reviewsSection = document.getElementById("reviews_section");
        if (reviewsSection) {
          reviewsSection.scrollIntoView({ behavior: "smooth" });
        }
      });
    }
  }
  function initializeReviewForm() {
    const reviewForm = document.getElementById("review_form");
    if (reviewForm) {
      reviewForm.addEventListener("submit", function(e) {
        e.preventDefault();
        submitReview();
      });
    }
  }
  function initializeReviewFunctionality() {
    initializeReviewForm();
    handleViewReviewsScroll();
  }
  window.submitReview = submitReview;
  document.addEventListener("DOMContentLoaded", initArtworkDetail);
})();
//# sourceMappingURL=artwork_detail.js.map

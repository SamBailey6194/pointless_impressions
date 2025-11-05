(() => {
  // pointless_impressions_src/theme/static_src/src/js/artwork_detail.js
  function formatPrice(price) {
    if (typeof price !== "number") {
      return "\xA30.00";
    }
    return "\xA3" + price.toLocaleString("en-GB", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });
  }
  function displayArtworkDetail(artworkData) {
    if (!artworkData) {
      console.error("No artwork data provided");
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
      priceElement.textContent = formatPrice(artworkData.price);
    }
    if (imageElement) {
      imageElement.src = artworkData.image || "";
      imageElement.alt = artworkData.alt_text || artworkData.name || "";
    }
    if (statusElement) {
      statusElement.textContent = artworkData.availability || "Unknown";
    }
  }
  function addToCart(artworkId, quantity = 1, price = 0) {
    let cart = JSON.parse(localStorage.getItem("cart")) || {};
    if (cart[artworkId]) {
      cart[artworkId].quantity += quantity;
    } else {
      cart[artworkId] = {
        id: artworkId,
        quantity,
        price
      };
    }
    localStorage.setItem("cart", JSON.stringify(cart));
    return cart[artworkId];
  }
  function initArtworkDetail() {
    const addToCartBtn = document.getElementById("add-to-cart-btn");
    if (addToCartBtn) {
      addToCartBtn.addEventListener("click", () => {
        const artworkId = addToCartBtn.dataset.artworkId;
        const price = parseFloat(addToCartBtn.dataset.price);
        if (artworkId) {
          addToCart(artworkId, 1, price);
          showConfirmationMessage("Added to cart!");
        }
      });
    }
    const thumbnailContainer = document.getElementById("thumbnail-container");
    if (thumbnailContainer) {
      const thumbnails = thumbnailContainer.querySelectorAll(".thumbnail-btn");
      thumbnails.forEach((thumb) => {
        thumb.addEventListener("click", (e) => {
          e.preventDefault();
          const slideNum = parseInt(thumb.dataset.slide);
          goToSlide(slideNum);
        });
      });
    }
    document.addEventListener("keydown", (e) => {
      if (e.key === "ArrowLeft") {
        previousSlide();
      } else if (e.key === "ArrowRight") {
        nextSlide();
      }
    });
    initializeReviewFunctionality();
  }
  function showConfirmationMessage(message) {
    const confirmationDiv = document.getElementById("confirmation-message");
    if (confirmationDiv) {
      confirmationDiv.textContent = message;
      confirmationDiv.style.display = "block";
      setTimeout(() => {
        confirmationDiv.style.display = "none";
      }, 3e3);
    }
  }
  var currentSlide = 0;
  function goToSlide(n) {
    const slides = document.querySelectorAll(".carousel-item");
    const totalSlides = slides.length;
    currentSlide = n;
    if (currentSlide >= totalSlides) {
      currentSlide = 0;
    }
    if (currentSlide < 0) {
      currentSlide = totalSlides - 1;
    }
    const slideElement = document.getElementById(`slide-${currentSlide}`);
    if (slideElement) {
      slideElement.scrollIntoView({
        behavior: "smooth",
        block: "nearest",
        inline: "nearest"
      });
    }
    updateThumbnails();
  }
  function nextSlide() {
    goToSlide(currentSlide + 1);
  }
  function previousSlide() {
    goToSlide(currentSlide - 1);
  }
  function updateThumbnails() {
    const thumbnails = document.querySelectorAll(".thumbnail-btn");
    thumbnails.forEach((thumb, index) => {
      if (index === currentSlide) {
        thumb.classList.add("border-primary");
        thumb.classList.remove("border-gray-300");
      } else {
        thumb.classList.remove("border-primary");
        thumb.classList.add("border-gray-300");
      }
    });
  }
  window.goToSlide = goToSlide;
  window.nextSlide = nextSlide;
  window.previousSlide = previousSlide;
  async function submitReview() {
    const form = document.getElementById("review_form");
    const modal = document.getElementById("review_modal");
    const formData = new FormData(form);
    try {
      const response = await fetch(form.action, {
        method: "POST",
        body: formData,
        headers: {
          "X-Requested-With": "XMLHttpRequest"
        }
      });
      const data = await response.json();
      if (response.ok) {
        showNotification(data.message, "success");
        form.reset();
        modal.close();
        setTimeout(() => {
          window.location.reload();
        }, 1e3);
      } else {
        showNotification(data.error || "An error occurred", "error");
        if (data.errors) {
          console.error("Form errors:", data.errors);
        }
      }
    } catch (error) {
      console.error("Error:", error);
      showNotification("Failed to submit review. Please try again.", "error");
    }
  }
  function showNotification(message, type = "info") {
    const toast = document.createElement("div");
    const alertClass = type === "success" ? "alert-success" : "alert-error";
    toast.className = `alert ${alertClass} fixed bottom-4 right-4 shadow-lg max-w-md z-50`;
    toast.innerHTML = `
    <div>
      <svg class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="${type === "success" ? "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" : "M12 8v4m0 4v.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"}"></path>
      </svg>
      <span>${message}</span>
    </div>
  `;
    document.body.appendChild(toast);
    setTimeout(() => {
      toast.remove();
    }, 5e3);
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
  window.showNotification = showNotification;
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initArtworkDetail);
  } else {
    initArtworkDetail();
  }
})();
//# sourceMappingURL=artwork_detail.js.map

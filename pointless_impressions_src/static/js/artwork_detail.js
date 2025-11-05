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
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initArtworkDetail);
  } else {
    initArtworkDetail();
  }
})();
//# sourceMappingURL=artwork_detail.js.map

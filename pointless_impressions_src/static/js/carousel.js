(() => {
  // pointless_impressions_src/theme/static_src/src/js/carousel.js
  function scrollCarousel(carouselId, direction) {
    const carousel = document.getElementById(carouselId);
    if (!carousel) return;
    const itemElement = carousel.querySelector(".shrink-0");
    if (!itemElement) return;
    const itemWidth = itemElement.offsetWidth;
    const carouselStyle = window.getComputedStyle(carousel);
    const gap = parseFloat(carouselStyle.gap) || 24;
    const scrollAmount = itemWidth + gap;
    const currentScroll = carousel.scrollLeft;
    const maxScroll = carousel.scrollWidth - carousel.clientWidth;
    let newScroll = currentScroll + direction * scrollAmount;
    if (newScroll < 0) {
      newScroll = maxScroll;
    } else if (newScroll > maxScroll) {
      newScroll = 0;
    }
    carousel.scrollTo({
      left: newScroll,
      behavior: "smooth"
    });
  }
  function initializeCarouselNavigation() {
    const carouselNavButtons = document.querySelectorAll(".carousel-nav-btn");
    carouselNavButtons.forEach((button) => {
      button.addEventListener("click", function(e) {
        e.preventDefault();
        const carouselId = this.getAttribute("data-carousel-id");
        const direction = parseInt(this.getAttribute("data-direction"));
        scrollCarousel(carouselId, direction);
      });
    });
  }
  var currentSlide = 0;
  var totalSlides = 0;
  function goToSlide(n) {
    const slides = document.querySelectorAll(".carousel-item");
    if (slides.length === 0) return;
    totalSlides = slides.length;
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
  function initArtworkDetailCarousel() {
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
    window.goToSlide = goToSlide;
    window.nextSlide = nextSlide;
    window.previousSlide = previousSlide;
  }
  window.carousel = {
    initArtworkDetailCarousel
  };
  document.addEventListener("DOMContentLoaded", () => {
    initializeCarouselNavigation();
  });
})();
//# sourceMappingURL=carousel.js.map

(() => {
  // pointless_impressions_src/theme/static_src/src/js/general.js
  document.addEventListener("DOMContentLoaded", () => {
    function scrollCarousel(carouselId, direction, scrollMultiplier = 1) {
      const carousel = document.getElementById(carouselId);
      if (!carousel) {
        return;
      }
      const itemElement = carousel.querySelector(".shrink-0");
      if (!itemElement) {
        return;
      }
      const itemWidth = itemElement.offsetWidth;
      const carouselStyle = window.getComputedStyle(carousel);
      const gapStyle = carouselStyle.gap;
      const gap = parseFloat(gapStyle.split(" ")[0]) || 24;
      if (itemWidth === 0) {
        console.error(`Item width is zero in carousel "${carouselId}"`);
        return;
      }
      const scrollAmount = itemWidth + gap;
      const currentScroll = carousel.scrollLeft;
      const maxScroll = carousel.scrollWidth - carousel.clientWidth;
      let newScroll = currentScroll + direction * scrollAmount * scrollMultiplier;
      if (newScroll < 0) {
        newScroll = maxScroll;
      } else if (newScroll > maxScroll) {
        if (currentScroll >= maxScroll) {
          newScroll = 0;
        } else {
          newScroll = maxScroll;
        }
      }
      carousel.scrollTo({
        left: newScroll,
        behavior: "smooth"
      });
    }
    function initializeCarouselNavigation() {
      const carouselNavButtons = document.querySelectorAll(".carousel-nav-btn");
      if (carouselNavButtons.length === 0) {
        return;
      }
      carouselNavButtons.forEach((button) => {
        button.addEventListener("click", function(e) {
          e.preventDefault();
          const carouselId = this.getAttribute("data-carousel-id");
          const direction = parseInt(this.getAttribute("data-direction"));
          const scrollMultiplier = parseFloat(this.getAttribute("data-scroll-multiplier")) || 1;
          scrollCarousel(carouselId, direction, scrollMultiplier);
        });
      });
    }
    initializeCarouselNavigation();
  });
})();
//# sourceMappingURL=general.js.map

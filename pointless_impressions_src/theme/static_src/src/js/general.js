/**
 * General Utilities - Shared across all pages
 * Handles common functionality like carousel scrolling, tooltips, etc.
 */

document.addEventListener("DOMContentLoaded", () => {
    /**
     * Scroll a carousel container left or right with looping
     * @param {string} carouselId - The ID of the carousel container element
     * @param {number} direction - Direction to scroll (-1 for left, 1 for right)
     * @param {number} scrollMultiplier - Multiplier for scroll amount (default: 1)
     */
    function scrollCarousel(carouselId, direction, scrollMultiplier = 1) {
        const carousel = document.getElementById(carouselId);
        if (!carousel) {
            return;
        }

        // Get the first child element to determine item width
        const itemElement = carousel.querySelector('.shrink-0');
        if (!itemElement) {
            return;
        }

        // Calculate scroll amount: item width + gap between items
        const itemWidth = itemElement.offsetWidth;
        const carouselStyle = window.getComputedStyle(carousel);
        const gapStyle = carouselStyle.gap;
        const gap = parseFloat(gapStyle.split(' ')[0]) || 24;

        if (itemWidth === 0) {
            console.error(`Item width is zero in carousel "${carouselId}"`);
            return;
        }

        const scrollAmount = itemWidth + gap;

        // Get current scroll position and max scroll position
        const currentScroll = carousel.scrollLeft;
        const maxScroll = carousel.scrollWidth - carousel.clientWidth;
        let newScroll = currentScroll + (direction * scrollAmount * scrollMultiplier);

        // Handle looping with proper end card display
        if (newScroll < 0) {
            newScroll = maxScroll;
        } else if (newScroll > maxScroll) {
            if (currentScroll >= maxScroll) {
                newScroll = 0;
            } else {
                newScroll = maxScroll;
            }
        }

        // Scroll smoothly to the new position
        carousel.scrollTo({
            left: newScroll,
            behavior: 'smooth'
        });
    }

    /**
     * Initialize carousel navigation buttons
     * Attaches click event listeners to all carousel nav buttons
     */
    function initializeCarouselNavigation() {
        const carouselNavButtons = document.querySelectorAll('.carousel-nav-btn');

        if (carouselNavButtons.length === 0) {
            return;
        }

        carouselNavButtons.forEach(button => {
            button.addEventListener('click', function (e) {
                e.preventDefault();
                const carouselId = this.getAttribute('data-carousel-id');
                const direction = parseInt(this.getAttribute('data-direction'));
                const scrollMultiplier = parseFloat(this.getAttribute('data-scroll-multiplier')) || 1;
                scrollCarousel(carouselId, direction, scrollMultiplier);
            });
        });
    }

    // Initialize carousel navigation
    initializeCarouselNavigation();
});
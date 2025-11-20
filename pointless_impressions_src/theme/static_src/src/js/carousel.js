/**
 * Global Carousel Logic
 * Handles all carousels across the site.
 */

// -------------------------------------------------------------------
// 1. GENERAL HORIZONTAL SCROLLER (for "Similar Items", etc.)
// -------------------------------------------------------------------

/**
 * Scroll a carousel container left or right with looping
 * @param {string} carouselId - The ID of the carousel container element
 * @param {number} direction - Direction to scroll (-1 for left, 1 for right)
 */
function scrollCarousel(carouselId, direction) {
    const carousel = document.getElementById(carouselId);
    if (!carousel) return;

    const itemElement = carousel.querySelector('.shrink-0'); // Assumes flex items
    if (!itemElement) return;

    // Calculate scroll amount: item width + gap
    const itemWidth = itemElement.offsetWidth;
    const carouselStyle = window.getComputedStyle(carousel);
    const gap = parseFloat(carouselStyle.gap) || 24;
    const scrollAmount = itemWidth + gap;

    const currentScroll = carousel.scrollLeft;
    const maxScroll = carousel.scrollWidth - carousel.clientWidth;
    let newScroll = currentScroll + (direction * scrollAmount);

    // Looping logic
    if (newScroll < 0) {
        newScroll = maxScroll;
    } else if (newScroll > maxScroll) {
        newScroll = 0;
    }

    carousel.scrollTo({
        left: newScroll,
        behavior: 'smooth'
    });
}

/**
 * Initialize general-purpose carousel navigation buttons
 */
function initializeCarouselNavigation() {
    const carouselNavButtons = document.querySelectorAll('.carousel-nav-btn');
    carouselNavButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const carouselId = this.getAttribute('data-carousel-id');
            const direction = parseInt(this.getAttribute('data-direction'));
            scrollCarousel(carouselId, direction);
        });
    });
}

// -------------------------------------------------------------------
// 2. ARTWORK DETAIL PAGE CAROUSEL (Main Product Image)
// -------------------------------------------------------------------

let currentSlide = 0;
let totalSlides = 0;

/**
 * Go to a specific slide in the artwork detail carousel
 * @param {number} n - The slide number
 */
function goToSlide(n) {
    const slides = document.querySelectorAll('.carousel-item');
    if (slides.length === 0) return;
    totalSlides = slides.length;

    currentSlide = n;

    // Loop around carousel
    if (currentSlide >= totalSlides) {
        currentSlide = 0;
    }
    if (currentSlide < 0) {
        currentSlide = totalSlides - 1;
    }

    // Scroll to the slide
    const slideElement = document.getElementById(`slide-${currentSlide}`);
    if (slideElement) {
        slideElement.scrollIntoView({
            behavior: 'smooth',
            block: 'nearest',
            inline: 'nearest',
        });
    }
    updateThumbnails();
}

/** Go to next slide */
function nextSlide() {
    goToSlide(currentSlide + 1);
}

/** Go to previous slide */
function previousSlide() {
    goToSlide(currentSlide - 1);
}

/** Update thumbnail border styles to highlight current slide */
function updateThumbnails() {
    const thumbnails = document.querySelectorAll('.thumbnail-btn');
    thumbnails.forEach((thumb, index) => {
        if (index === currentSlide) {
            thumb.classList.add('border-primary');
            thumb.classList.remove('border-gray-300');
        } else {
            thumb.classList.remove('border-primary');
            thumb.classList.add('border-gray-300');
        }
    });
}

/**
 * Initialize all listeners for the artwork detail page carousel
 */
function initArtworkDetailCarousel() {
    // Initialize thumbnail listeners
    const thumbnailContainer = document.getElementById('thumbnail-container');
    if (thumbnailContainer) {
        const thumbnails = thumbnailContainer.querySelectorAll('.thumbnail-btn');
        thumbnails.forEach((thumb) => {
            thumb.addEventListener('click', (e) => {
                e.preventDefault();
                const slideNum = parseInt(thumb.dataset.slide);
                goToSlide(slideNum);
            });
        });
    }

    // Add keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
            previousSlide();
        } else if (e.key === 'ArrowRight') {
            nextSlide();
        }
    });

    window.goToSlide = goToSlide;
    window.nextSlide = nextSlide;
    window.previousSlide = previousSlide;
}

// -------------------------------------------------------------------
// INITIALIZATION
// -------------------------------------------------------------------

window.carousel = {
    initArtworkDetailCarousel: initArtworkDetailCarousel
};

// Initialize general carousels on page load
document.addEventListener("DOMContentLoaded", () => {
    initializeCarouselNavigation();
});
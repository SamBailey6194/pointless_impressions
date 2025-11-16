/**
 * Artwork Detail Page - Main Script
 * Handles displaying artwork details, initializing the carousel,
 * and review submission.
 */

import { getCsrfToken } from "./cart";

/**
 * Display artwork detail information on the page
 * @param {object} artworkData - The artwork data object
 */
export function displayArtworkDetail(artworkData) {
  if (!artworkData) {
    console.error('No artwork data provided to display.');
    return;
  }

  const titleElement = document.getElementById('artwork-title');
  const descriptionElement = document.getElementById('artwork-description');
  const priceElement = document.getElementById('artwork-price');
  const imageElement = document.getElementById('artwork-image');
  const statusElement = document.getElementById('availability-status');

  if (titleElement) {
    titleElement.textContent = artworkData.name || '';
  }

  if (descriptionElement) {
    descriptionElement.textContent = artworkData.description || '';
  }

  if (priceElement) {
    priceElement.textContent = artworkData.price || '';
  }

  if (imageElement) {
    imageElement.src = artworkData.image_url || '';
    imageElement.alt = artworkData.image_alt_text || artworkData.name || '';
  }

  if (statusElement) {
    statusElement.textContent = artworkData.availability || 'Unknown';
  }
}

/**
 * Initialize artwork detail page
 */
export function initArtworkDetail() {
  if (window.carousel && window.carousel.initArtworkDetailCarousel) {
        window.carousel.initArtworkDetailCarousel();
    } else {
        console.error('Carousel script not loaded.');
    }
  initializeReviewFunctionality();
}

/**
 * Review Submission Handling
 */

/**
 * Submit review form via fetch API
 */
async function submitReview() {
  const form = document.getElementById('review_form');
  const modal = document.getElementById('review_modal');
  const formData = new FormData(form);

  try {
    const response = await fetch(form.action, {
      method: 'POST',
      body: formData,
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': getCsrfToken()
      }
    });

    const data = await response.json();

    if (response.ok) {
      if (window.Toast) {
        window.Toast.show(data.message, 'success');
      }
      
      form.reset();
      if (modal) modal.close();
      setTimeout(() => {
        window.location.reload();
      }, 1000);

    } else {
      const errorMsg = data.error || (data.errors ? Object.values(data.errors).join(' ') : 'An error occurred.');
      if (window.Toast) {
        window.Toast.show(errorMsg, 'error');
      }
      console.error('Form errors:', data.errors);
    }
  } catch (error) {
    console.error('Error submitting review:', error);
    if (window.Toast) {
      window.Toast.show('Failed to submit review. Please try again.', 'error');
    }
  }
}

/**
 * Handle View Reviews button scroll
 */
function handleViewReviewsScroll() {
  const viewReviewsBtn = document.querySelector('[data-scroll-to-reviews]');
  if (viewReviewsBtn) {
    viewReviewsBtn.addEventListener('click', function() {
      const reviewsSection = document.getElementById('reviews_section');
      if (reviewsSection) {
        reviewsSection.scrollIntoView({ behavior: 'smooth' });
      }
    });
  }
}

/**
 * Initialize review form submission
 */
function initializeReviewForm() {
  const reviewForm = document.getElementById('review_form');

  if (reviewForm) {
    reviewForm.addEventListener('submit', function(e) {
      e.preventDefault();
      submitReview();
    });
  }
}

// Initialize review functionality on page load
function initializeReviewFunctionality() {
  initializeReviewForm();
  handleViewReviewsScroll();
}

// Make review submit function globally available
window.submitReview = submitReview;

// Initialize on page load
document.addEventListener('DOMContentLoaded', initArtworkDetail);

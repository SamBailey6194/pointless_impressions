/**
 * Artwork Detail Page - Main Script
 * Handles displaying artwork details, initializing the carousel,
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
    imageElement.alt = artworkData.alt_text || artworkData.name || '';
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
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initArtworkDetail);

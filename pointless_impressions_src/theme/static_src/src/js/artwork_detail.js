/**
 * Artwork Detail Page - Main Script
 * Handles displaying artwork details, images, and cart functionality
 */

/**
 * Format price with currency symbol and thousand separators
 * @param {number} price - The price to format
 * @returns {string} Formatted price with £ symbol
 */
export function formatPrice(price) {
  if (typeof price !== 'number') {
    return '£0.00';
  }
  return '£' + price.toLocaleString('en-GB', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

/**
 * Display artwork detail information on the page
 * @param {object} artworkData - The artwork data object
 */
export function displayArtworkDetail(artworkData) {
  if (!artworkData) {
    console.error('No artwork data provided');
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
    priceElement.textContent = formatPrice(artworkData.price);
  }

  if (imageElement) {
    imageElement.src = artworkData.image || '';
    imageElement.alt = artworkData.alt_text || artworkData.name || '';
  }

  if (statusElement) {
    statusElement.textContent = artworkData.availability || 'Unknown';
  }
}

/**
 * Add artwork to cart
 * @param {string} artworkId - The artwork identifier
 * @param {number} quantity - Quantity to add
 * @param {number} price - Price of artwork
 * @returns {object} Cart item object
 */
export function addToCart(artworkId, quantity = 1, price = 0) {
  // Get existing cart from localStorage or create new one
  let cart = JSON.parse(localStorage.getItem('cart')) || {};

  // Check if item already exists in cart
  if (cart[artworkId]) {
    // Increment quantity
    cart[artworkId].quantity += quantity;
  } else {
    // Add new item
    cart[artworkId] = {
      id: artworkId,
      quantity: quantity,
      price: price,
    };
  }

  // Save updated cart to localStorage
  localStorage.setItem('cart', JSON.stringify(cart));

  return cart[artworkId];
}

/**
 * Initialize artwork detail page
 */
export function initArtworkDetail() {
  // Add event listeners for Add to Cart button
  const addToCartBtn = document.getElementById('add-to-cart-btn');
  if (addToCartBtn) {
    addToCartBtn.addEventListener('click', () => {
      // Get artwork data from data attributes or DOM
      const artworkId = addToCartBtn.dataset.artworkId;
      const price = parseFloat(addToCartBtn.dataset.price);

      if (artworkId) {
        addToCart(artworkId, 1, price);
        showConfirmationMessage('Added to cart!');
      }
    });
  }
}

/**
 * Show confirmation message when item is added to cart
 * @param {string} message - Message to display
 */
export function showConfirmationMessage(message) {
  const confirmationDiv = document.getElementById('confirmation-message');
  if (confirmationDiv) {
    confirmationDiv.textContent = message;
    confirmationDiv.style.display = 'block';

    // Hide after 3 seconds
    setTimeout(() => {
      confirmationDiv.style.display = 'none';
    }, 3000);
  }
}

// Initialize on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initArtworkDetail);
} else {
  initArtworkDetail();
}

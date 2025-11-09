/**
 * Cart Management Module
 * Handles localStorage-based cart operations with optional backend API sync
 * Compatible with Jest and Cypress testing
 * 
 * Usage:
 *   import { addToCart, removeFromCart, getCart, calculateTotal, formatPrice } from './cart.js';
 *   
 *   addToCart('artwork-123', 1, 199.99);
 *   const total = calculateTotal();
 */

const CART_STORAGE_KEY = 'cart';
const API_ENDPOINTS = {
  ADD: '/checkout/api/cart/add/',
  REMOVE: '/checkout/api/cart/remove/',
  UPDATE: '/checkout/api/cart/update/',
  SYNC: '/checkout/api/cart/sync/',
};

/**
 * Format price with currency symbol and thousand separators
 * @param {number} price - The price to format
 * @returns {string} Formatted price with £ symbol (e.g., "£199.99")
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
 * Get entire cart from localStorage
 * @returns {object} Cart object with all items keyed by artworkId
 */
export function getCart() {
  try {
    return JSON.parse(localStorage.getItem(CART_STORAGE_KEY)) || {};
  } catch (e) {
    console.error('Error parsing cart from localStorage:', e);
    return {};
  }
}

/**
 * Save cart to localStorage
 * @param {object} cart - Cart object to save
 */
export function saveCart(cart) {
  try {
    localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cart));
  } catch (e) {
    console.error('Error saving cart to localStorage:', e);
  }
}

/**
 * Clear entire cart from localStorage
 */
export function clearCart() {
  try {
    localStorage.removeItem(CART_STORAGE_KEY);
  } catch (e) {
    console.error('Error clearing cart:', e);
  }
}

/**
 * Add artwork to cart
 * Increments quantity if already in cart
 * @param {string} artworkId - The artwork identifier (usually artwork.id or artwork.slug)
 * @param {number} quantity - Quantity to add (default: 1)
 * @param {number} price - Price of artwork (required for cart display)
 * @param {string} name - Name of artwork (optional, for cart display)
 * @returns {object} Updated cart item object
 */
export function addToCart(artworkId, quantity = 1, price = 0, name = '') {
  let cart = getCart();

  if (cart[artworkId]) {
    // Item already in cart, increment quantity
    cart[artworkId].quantity += quantity;
  } else {
    // New item
    cart[artworkId] = {
      id: artworkId,
      name: name,
      quantity: quantity,
      price: price,
    };
  }

  saveCart(cart);
  return cart[artworkId];
}

/**
 * Remove artwork from cart
 * @param {string} artworkId - The artwork identifier to remove
 * @returns {boolean} True if item was removed, false if not found
 */
export function removeFromCart(artworkId) {
  let cart = getCart();

  if (cart[artworkId]) {
    delete cart[artworkId];
    saveCart(cart);
    return true;
  }

  return false;
}

/**
 * Update quantity of artwork in cart
 * @param {string} artworkId - The artwork identifier
 * @param {number} newQuantity - The new quantity (must be > 0)
 * @returns {object|null} Updated cart item object or null if not found
 */
export function updateQuantity(artworkId, newQuantity) {
  let cart = getCart();

  if (cart[artworkId]) {
    if (newQuantity <= 0) {
      return removeFromCart(artworkId) ? null : cart[artworkId];
    }
    
    cart[artworkId].quantity = newQuantity;
    saveCart(cart);
    return cart[artworkId];
  }

  return null;
}

/**
 * Calculate total price of all items in cart
 * @returns {number} Total price (rounded to 2 decimal places)
 */
export function calculateTotal() {
  const cart = getCart();
  let total = 0;

  Object.keys(cart).forEach((artworkId) => {
    const item = cart[artworkId];
    total += item.quantity * item.price;
  });

  // Round to 2 decimal places to avoid floating point errors
  return Math.round(total * 100) / 100;
}

/**
 * Get cart item count (total number of items, not quantity)
 * @returns {number} Number of different items in cart
 */
export function getCartItemCount() {
  const cart = getCart();
  return Object.keys(cart).length;
}

/**
 * Get total quantity of all items in cart
 * @returns {number} Total quantity across all items
 */
export function getTotalQuantity() {
  const cart = getCart();
  let total = 0;

  Object.keys(cart).forEach((artworkId) => {
    total += cart[artworkId].quantity;
  });

  return total;
}

/**
 * Check if cart is empty
 * @returns {boolean} True if cart has no items
 */
export function isCartEmpty() {
  return getCartItemCount() === 0;
}

/**
 * Get specific cart item
 * @param {string} artworkId - The artwork identifier
 * @returns {object|null} Cart item object or null if not found
 */
export function getCartItem(artworkId) {
  const cart = getCart();
  return cart[artworkId] || null;
}

/**
 * Update cart item with additional data (e.g., framing options, notes)
 * @param {string} artworkId - The artwork identifier
 * @param {object} updates - Object with updates to apply
 * @returns {object|null} Updated cart item or null if not found
 */
export function updateCartItem(artworkId, updates) {
  let cart = getCart();

  if (cart[artworkId]) {
    cart[artworkId] = { ...cart[artworkId], ...updates };
    saveCart(cart);
    return cart[artworkId];
  }

  return null;
}

/**
 * Sync localStorage cart with backend
 * Sends current cart to backend API for session storage
 * @returns {Promise<object>} Response from backend
 */
export async function syncCartWithBackend() {
  const cart = getCart();
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

  if (!csrfToken) {
    console.warn('CSRF token not found for cart sync');
    return { error: 'CSRF token not found' };
  }

  try {
    const response = await fetch(API_ENDPOINTS.SYNC, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({ cart }),
    });

    if (!response.ok) {
      throw new Error(`Sync failed with status ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error syncing cart with backend:', error);
    throw error;
  }
}

/**
 * Add item to cart via backend API
 * Also updates localStorage after successful API call
 * @param {string} artworkId - The artwork identifier
 * @param {number} quantity - Quantity to add
 * @param {object} options - Additional options (framing, notes, etc.)
 * @returns {Promise<object>} API response with cart_count
 */
export async function addToCartViaAPI(artworkId, quantity = 1, options = {}) {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

  if (!csrfToken) {
    console.warn('CSRF token not found for API request');
    throw new Error('CSRF token not found');
  }

  const formData = new FormData();
  formData.append('artwork_id', artworkId);
  formData.append('quantity', quantity);

  // Add optional fields
  if (options.framing_option) {
    formData.append('framing_option', options.framing_option);
  }
  if (options.notes) {
    formData.append('notes', options.notes);
  }

  try {
    const response = await fetch(API_ENDPOINTS.ADD, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
      },
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Failed to add item to cart');
    }

    // Update localStorage with the response cart data if provided
    if (data.cart) {
      saveCart(data.cart);
    }

    return data;
  } catch (error) {
    console.error('Error adding to cart via API:', error);
    throw error;
  }
}

/**
 * Remove item from cart via backend API
 * @param {string} artworkId - The artwork identifier
 * @returns {Promise<object>} API response
 */
export async function removeFromCartViaAPI(artworkId) {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

  if (!csrfToken) {
    throw new Error('CSRF token not found');
  }

  const formData = new FormData();
  formData.append('artwork_id', artworkId);

  try {
    const response = await fetch(API_ENDPOINTS.REMOVE, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
      },
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Failed to remove item from cart');
    }

    // Update localStorage
    removeFromCart(artworkId);

    return data;
  } catch (error) {
    console.error('Error removing from cart via API:', error);
    throw error;
  }
}

/**
 * Update cart item quantity via backend API
 * @param {string} artworkId - The artwork identifier
 * @param {number} quantity - New quantity
 * @returns {Promise<object>} API response
 */
export async function updateQuantityViaAPI(artworkId, quantity) {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

  if (!csrfToken) {
    throw new Error('CSRF token not found');
  }

  const formData = new FormData();
  formData.append('artwork_id', artworkId);
  formData.append('quantity', quantity);

  try {
    const response = await fetch(API_ENDPOINTS.UPDATE, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
      },
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Failed to update quantity');
    }

    // Update localStorage
    if (quantity > 0) {
      updateQuantity(artworkId, quantity);
    } else {
      removeFromCart(artworkId);
    }

    return data;
  } catch (error) {
    console.error('Error updating quantity via API:', error);
    throw error;
  }
}

/**
 * Initialize cart UI updates
 * Updates cart count badge when cart changes
 * Can be called to set up listeners for cart changes
 */
export function initCartUI() {
  // Update cart count on page load
  updateCartCountBadge();

  // Listen for storage changes (for multi-tab sync)
  window.addEventListener('storage', (e) => {
    if (e.key === CART_STORAGE_KEY) {
      updateCartCountBadge();
    }
  });
}

/**
 * Update cart count badge in header
 * Looks for element with data-cart-count attribute
 */
export function updateCartCountBadge() {
  const cartCountEl = document.querySelector('[data-cart-count]');
  if (cartCountEl) {
    const count = getTotalQuantity();
    cartCountEl.textContent = count;
    cartCountEl.style.display = count > 0 ? 'block' : 'none';
  }
}

/**
 * Debug function to log current cart state
 * Useful for testing and debugging
 */
export function debugCart() {
  const cart = getCart();
  console.log('Cart Contents:', cart);
  console.log('Item Count:', getCartItemCount());
  console.log('Total Quantity:', getTotalQuantity());
  console.log('Total Price:', formatPrice(calculateTotal()));
  return cart;
}

// Export API endpoints for testing
export { API_ENDPOINTS, CART_STORAGE_KEY };

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

const CART_UUID_KEY = 'cart_uuid';
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
 * Get cart UUID from localStorage
 * @returns {string|null}
 */
export function getCartUUID() {
  return localStorage.getItem(CART_UUID_KEY) || null;
}

/**
 * Save cart UUID to localStorage
 * @param {string} uuid
 */
export function saveCartUUID(uuid) {
  if (uuid) {
    localStorage.setItem(CART_UUID_KEY, uuid);
  }
}

/**
 * Remove cart UUID from localStorage
 */
export function clearCartUUID() {
  localStorage.removeItem(CART_UUID_KEY);
}

/**
 * Fetch cart data from backend using UUID
 * @returns {Promise<object>} Cart data from backend
 */
export async function fetchCartFromBackend() {
  const cart_uuid = getCartUUID();
  if (!cart_uuid) return {};
  try {
    const response = await fetch(`/checkout/api/cart/fetch/?cart_uuid=${cart_uuid}`);
    if (!response.ok) throw new Error('Failed to fetch cart');
    return await response.json();
  } catch (e) {
    console.error('Error fetching cart from backend:', e);
    return {};
  }
}

/**
 * Add item to cart via backend API
 * Only stores cart_uuid in localStorage
 */
export async function addToCartViaAPI(artworkId, quantity = 1, options = {}) {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
  const cart_uuid = getCartUUID();
  if (!csrfToken) throw new Error('CSRF token not found');
  const formData = new FormData();
  formData.append('artwork_id', artworkId);
  formData.append('quantity', quantity);
  if (options.framing_option) formData.append('framing_option', options.framing_option);
  if (options.notes) formData.append('notes', options.notes);
  let url = API_ENDPOINTS.ADD;
  if (cart_uuid) url += `?cart_uuid=${cart_uuid}`;
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken },
      body: formData,
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Failed to add item to cart');
    if (data.cart_uuid) saveCartUUID(data.cart_uuid);
    return data;
  } catch (error) {
    console.error('Error adding to cart via API:', error);
    throw error;
  }
}

/**
 * Remove item from cart via backend API
 */
export async function removeFromCartViaAPI(artworkId) {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
  const cart_uuid = getCartUUID();
  if (!csrfToken) throw new Error('CSRF token not found');
  const formData = new FormData();
  formData.append('artwork_id', artworkId);
  let url = API_ENDPOINTS.REMOVE;
  if (cart_uuid) url += `?cart_uuid=${cart_uuid}`;
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken },
      body: formData,
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Failed to remove item from cart');
    if (data.cart_uuid) saveCartUUID(data.cart_uuid);
    return data;
  } catch (error) {
    console.error('Error removing from cart via API:', error);
    throw error;
  }
}

/**
 * Update cart item quantity via backend API
 */
export async function updateQuantityViaAPI(artworkId, quantity) {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
  const cart_uuid = getCartUUID();
  if (!csrfToken) throw new Error('CSRF token not found');
  const formData = new FormData();
  formData.append('artwork_id', artworkId);
  formData.append('quantity', quantity);
  let url = API_ENDPOINTS.UPDATE;
  if (cart_uuid) url += `?cart_uuid=${cart_uuid}`;
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken },
      body: formData,
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Failed to update quantity');
    if (data.cart_uuid) saveCartUUID(data.cart_uuid);
    return data;
  } catch (error) {
    console.error('Error updating quantity via API:', error);
    throw error;
  }
}

/**
 * Sync localStorage cart with backend (for legacy support)
 * Now just ensures cart_uuid is set and backend is up to date
 */
export async function syncCartWithBackend() {
  // No-op: all cart data is in backend, only cart_uuid is stored
  return { success: true, cart_uuid: getCartUUID() };
}

/**
 * Get cart item count (fetches from backend)
 */
export async function getCartItemCount() {
  const cart = await fetchCartFromBackend();
  return cart.items ? cart.items.length : 0;
}

/**
 * Get total quantity of all items in cart (fetches from backend)
 */
export async function getTotalQuantity() {
  const cart = await fetchCartFromBackend();
  let total = 0;
  if (cart.items) {
    cart.items.forEach(item => { total += item.quantity; });
  }
  return total;
}

/**
 * Calculate total price of all items in cart (fetches from backend)
 */
export async function calculateTotal() {
  const cart = await fetchCartFromBackend();
  let total = 0;
  if (cart.items) {
    cart.items.forEach(item => { total += item.total || (item.price * item.quantity); });
  }
  return Math.round(total * 100) / 100;
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
    if (e.key === CART_UUID_KEY) {
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
 * Initialize cart system
 * Syncs localStorage cart with backend session storage on page load
 * Should be called once when page loads
 */
export function initCart() {
  // Always sync cart with backend on page load
  syncCartWithBackend().then(response => {
    if (response?.success) {
      // Update header display after sync
      if (window.updateCartDisplay && typeof window.updateCartDisplay === 'function') {
        window.updateCartDisplay();
      }
    }
  }).catch(err => {
    console.error('❌ Failed to sync cart on page load:', err);
  });
}

// Export API endpoints for testing
export { API_ENDPOINTS, CART_UUID_KEY };

// Make cart functions globally available for non-module scripts
if (typeof window !== 'undefined') {
  window.initCart = initCart;
  window.getTotalQuantity = getTotalQuantity;
  window.calculateTotal = calculateTotal;
  window.formatPrice = formatPrice;
}

/**
 * Add to Cart Modal Handler
 * Manages the DaisyUI modal for adding items to cart
 * Uses cart.js for actual cart operations
 * Uses toasts.js for notifications
 * 
 * Usage:
 *   addToCartModal.init('artwork-123', 'Sunset', '199.99', '/image.jpg', 5, []);
 */

import { addToCartViaAPI, updateCartCountBadge, formatPrice } from './cart.js';

// Toast is available globally from toasts.js (loaded in base.html as non-module script)
const Toast = window.Toast;

const addToCartModal = {
  // Current artwork being added
  currentArtwork: null,

  /**
   * Initialize modal with artwork data
   * @param {string} artworkId - The artwork identifier
   * @param {string} artworkName - Display name of artwork
   * @param {number} artworkPrice - Price of artwork
   * @param {string} artworkImage - URL to artwork image
   * @param {number} quantity - Available quantity/stock
   * @param {array} framingOptions - Array of framing option objects [{id, name}, ...]
   */
  init(artworkId, artworkName, artworkPrice, artworkImage, quantity, framingOptions = []) {
    this.currentArtwork = {
      id: artworkId,
      name: artworkName,
      price: parseFloat(artworkPrice),
      image: artworkImage,
      quantity: quantity,
      framingOptions: framingOptions,
    };

    // Set artwork data in modal
    document.getElementById('modal_artwork_id').value = artworkId;
    document.getElementById('modal_artwork_name').textContent = artworkName;
    document.getElementById('modal_artwork_price').textContent = formatPrice(artworkPrice);
    
    // Set image and handle placeholder
    const imageEl = document.getElementById('modal_artwork_image');
    const placeholderEl = document.getElementById('modal_image_placeholder');
    if (artworkImage) {
      imageEl.src = artworkImage;
      placeholderEl.classList.add('hidden');
      imageEl.classList.remove('hidden');
    } else {
      imageEl.classList.add('hidden');
      placeholderEl.classList.remove('hidden', 'flex');
      placeholderEl.classList.add('flex');
    }

    // Set quantity controls
    document.getElementById('quantity').value = 1;
    document.getElementById('quantity').max = Math.max(quantity, 1);
    document.getElementById('max_quantity_info').textContent = 
      quantity > 0 ? `Max: ${quantity}` : 'Out of stock';
    document.getElementById('modal_artwork_stock').textContent = 
      quantity > 0 ? `${quantity} in stock` : 'Out of stock';

    // Set framing options
    this.setupFramingOptions(framingOptions);

    // Reset form states
    this.resetForm();

    // Open modal
    document.getElementById('add_to_cart_modal').showModal();
  },

  /**
   * Setup framing options in dropdown
   * @param {array} framingOptions - Array of framing option objects
   */
  setupFramingOptions(framingOptions) {
    const framingSelect = document.getElementById('framing_option');
    framingSelect.innerHTML = '<option value="" disabled selected>Select framing option...</option>';

    if (framingOptions.length > 0) {
      document.getElementById('framing_section').classList.remove('hidden');
      framingOptions.forEach(option => {
        const opt = document.createElement('option');
        opt.value = option.id;
        opt.textContent = option.name;
        framingSelect.appendChild(opt);
      });
    } else {
      document.getElementById('framing_section').classList.add('hidden');
    }
  },

  /**
   * Reset form to default state
   */
  resetForm() {
    document.getElementById('qty_error').classList.add('hidden');
    document.getElementById('form_error').classList.add('hidden');
    document.getElementById('form_success').classList.add('hidden');
    document.getElementById('notes').value = '';
    document.getElementById('notes_count').textContent = '0/500';
    document.getElementById('framing_option').value = '';
  },

  /**
   * Increase quantity by 1
   */
  increaseQuantity() {
    const input = document.getElementById('quantity');
    const max = parseInt(input.max) || 999;
    const current = parseInt(input.value) || 1;
    if (current < max) {
      input.value = current + 1;
      this.clearQtyError();
    }
  },

  /**
   * Decrease quantity by 1
   */
  decreaseQuantity() {
    const input = document.getElementById('quantity');
    const current = parseInt(input.value) || 1;
    if (current > 1) {
      input.value = current - 1;
      this.clearQtyError();
    }
  },

  /**
   * Validate quantity input
   * @returns {boolean} True if valid, false otherwise
   */
  validateQuantity() {
    const input = document.getElementById('quantity');
    const max = this.currentArtwork?.quantity || parseInt(input.max) || 999;
    let current = parseInt(input.value) || 1;

    // Enforce minimum quantity of 1
    if (current < 1) {
      input.value = 1;
      this.showQtyError('Quantity must be at least 1');
      return false;
    }

    // Enforce maximum quantity available
    if (current > max) {
      input.value = max;
      this.showQtyError(`Maximum ${max} available`);
      return false;
    }

    this.clearQtyError();
    return true;
  },

  /**
   * Show quantity error message
   * @param {string} message - Error message to display
   */
  showQtyError(message) {
    const errorEl = document.getElementById('qty_error');
    errorEl.textContent = message;
    errorEl.classList.remove('hidden');
  },

  /**
   * Clear quantity error message
   */
  clearQtyError() {
    document.getElementById('qty_error').classList.add('hidden');
  },

  /**
   * Show form error message
   * @param {string} message - Error message to display
   */
  showError(message) {
    console.log('❌ showError called with message:', message);
    console.log('Toast object available?', !!Toast);
    console.log('Toast.error available?', typeof Toast?.error);
    
    // Show error on the modal itself
    const formErrorEl = document.getElementById('form_error');
    const errorMessageEl = document.getElementById('error_message');
    if (formErrorEl && errorMessageEl) {
      errorMessageEl.textContent = message;
      formErrorEl.classList.remove('hidden');
      console.log('✅ Error displayed on modal');
    }
    
    // Also show toast for backup
    if (Toast && typeof Toast.error === 'function') {
      Toast.error(message);
      console.log('✅ Toast.error() called successfully');
    } else {
      console.error('❌ Toast.error not available!', Toast);
    }
  },

  /** 
   * Show form success message
   * @param {string} message - Success message to display
   */
  showSuccess(message) {
    console.log('✅ showSuccess called with message:', message);
    console.log('Toast object available?', !!Toast);
    console.log('Toast.success available?', typeof Toast?.success);
    
    // Show success on the modal itself
    const formSuccessEl = document.getElementById('form_success');
    const successMessageEl = document.getElementById('success_message');
    if (formSuccessEl && successMessageEl) {
      successMessageEl.textContent = message;
      formSuccessEl.classList.remove('hidden');
      console.log('✅ Success displayed on modal');
    }
    
    // Also show toast for backup
    if (Toast && typeof Toast.success === 'function') {
      Toast.success(message);
      console.log('✅ Toast.success() called successfully');
    } else {
      console.error('❌ Toast.success not available!', Toast);
    }
  },

  /**
   * Handle form submission
   * @param {Event} event - Form submit event
   */
  async handleSubmit(event) {
    console.log('📋 handleSubmit called');
    event.preventDefault();

    // Validate quantity
    if (!this.validateQuantity()) {
      console.log('⚠️ Quantity validation failed');
      return;
    }

    const quantity = parseInt(document.getElementById('quantity').value) || 1;
    const framingOption = document.getElementById('framing_option').value;
    const notes = document.getElementById('notes').value.trim();

    console.log('📝 Form values:', { quantity, framingOption, notes });

    // Validate framing option if section is visible (has options available)
    const framingSection = document.getElementById('framing_section');
    console.log('🎨 Framing section hidden?', framingSection.classList.contains('hidden'));
    console.log('🎨 Framing option value:', framingOption);
    
    if (!framingSection.classList.contains('hidden') && !framingOption) {
      console.log('❌ Framing validation FAILED - showing error');
      this.showError('Please select a framing option');
      return;
    }

    // Validate quantity is within range
    if (quantity < 1 || quantity > this.currentArtwork.quantity) {
      console.log('⚠️ Quantity out of range');
      this.showError(`Quantity must be between 1 and ${this.currentArtwork.quantity}`);
      return;
    }

    // Show loading state
    const submitBtn = document.getElementById('submit_btn');
    const originalText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Adding...';

    try {
      // Prepare options object
      const options = {};
      if (framingOption) {
        options.framing_option = framingOption;
      }
      if (notes) {
        options.notes = notes;
      }

      // Add to cart via API
      const response = await addToCartViaAPI(this.currentArtwork.id, quantity, options);

      // Update cart UI
      updateCartCountBadge();

      // Show success message
      this.showSuccess(`Added ${quantity} ${quantity === 1 ? 'item' : 'items'} to cart!`);

      // Close modal after 1.5 seconds
      setTimeout(() => {
        document.getElementById('add_to_cart_modal').close();
      }, 1500);
    } catch (error) {
      console.error('Error:', error);
      this.showError(error.message || 'Failed to add item to cart. Please try again.');
    } finally {
      // Restore button state
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalText;
    }
  },
};

/**
 * Initialize modal event listeners
 * Called when DOM is ready
 */
function initAddToCartModal() {
  // Quantity controls
  const qtyIncreaseBtn = document.getElementById('qty_increase');
  const qtyDecreaseBtn = document.getElementById('qty_decrease');
  const quantityInput = document.getElementById('quantity');
  const form = document.getElementById('add_to_cart_form');
  const notesInput = document.getElementById('notes');

  if (qtyIncreaseBtn) {
    qtyIncreaseBtn.addEventListener('click', () => addToCartModal.increaseQuantity());
  }

  if (qtyDecreaseBtn) {
    qtyDecreaseBtn.addEventListener('click', () => addToCartModal.decreaseQuantity());
  }

  if (quantityInput) {
    // Validate on change (when user finishes editing)
    quantityInput.addEventListener('change', () => addToCartModal.validateQuantity());
    
    // Real-time validation on input
    quantityInput.addEventListener('input', (e) => {
      // Prevent negative numbers and zero
      let value = parseInt(e.target.value) || 0;
      if (value < 1) {
        e.target.value = 1;
        addToCartModal.showQtyError('Quantity must be at least 1');
        return;
      }
      
      // Prevent exceeding stock
      const max = addToCartModal.currentArtwork?.quantity || 999;
      if (value > max) {
        e.target.value = max;
        addToCartModal.showQtyError(`Maximum ${max} available`);
        return;
      }
      
      // Clear error if valid
      addToCartModal.clearQtyError();
    });
    
    // Prevent pasting invalid values
    quantityInput.addEventListener('paste', (e) => {
      setTimeout(() => {
        addToCartModal.validateQuantity();
      }, 10);
    });
  }

  if (form) {
    form.addEventListener('submit', (e) => addToCartModal.handleSubmit(e));
  }

  if (notesInput) {
    notesInput.addEventListener('input', (e) => {
      document.getElementById('notes_count').textContent = `${e.target.value.length}/500`;
    });
  }
}

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initAddToCartModal);
} else {
  initAddToCartModal();
}

// Make modal object globally available
window.addToCartModal = addToCartModal;

// Export for ES modules
export { addToCartModal, initAddToCartModal };

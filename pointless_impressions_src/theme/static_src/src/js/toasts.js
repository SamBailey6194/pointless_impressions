/**
 * Global Toast Notification System
 * Displays dynamic toast messages for various actions:
 * - Adding to cart
 * - Writing reviews
 * - Creating comments
 * - Checkout success
 * - Login/Registration
 * - Artwork submission
 * - And more...
 */

const Toast = {
  /**
   * Toast types with their styling
   */
  types: {
    success: {
      icon: 'fa-circle-check',
      className: 'alert-success',
      duration: 3000,
    },
    error: {
      icon: 'fa-circle-exclamation',
      className: 'alert-error',
      duration: 4000,
    },
    info: {
      icon: 'fa-circle-info',
      className: 'alert-info',
      duration: 3000,
    },
    warning: {
      icon: 'fa-triangle-exclamation',
      className: 'alert-warning',
      duration: 3500,
    },
  },

  /**
   * Show a toast notification
   * @param {string} message - The message to display
   * @param {string} type - The type of toast (success, error, info, warning)
   * @param {number} duration - Optional custom duration in milliseconds
   */
  show(message, type = 'info', duration = null) {
    console.log(`🍞 Toast.show() called: type="${type}", message="${message}"`);
    const toastConfig = this.types[type] || this.types.info;
    const displayDuration = duration || toastConfig.duration;

    // Get or create container
    let container = document.getElementById('toast-container');
    if (!container) {
      console.error('🚨 Toast container NOT found in DOM! Ensure toast.html is included in base.html');
      return;
    }

    console.log('✅ Toast container found:', container);
    console.log('📏 Container classes:', container.className);
    console.log('🎨 Toast type config:', toastConfig);

    // Create toast element
    const toastEl = document.createElement('div');
    toastEl.className = `alert ${toastConfig.className} gap-2 shadow-lg pointer-events-auto animate-fade-in`;
    toastEl.innerHTML = `
      <svg class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>
      <span>${message}</span>
    `;

    console.log('🆕 Toast element created:', toastEl);
    console.log('📋 Toast element classes:', toastEl.className);

    // Add to container
    container.appendChild(toastEl);
    console.log('✅ Toast element added to container');

    // Auto-remove after duration
    setTimeout(() => {
      console.log(`⏱️ Toast auto-removing after ${displayDuration}ms`);
      toastEl.classList.add('animate-fade-out');
      setTimeout(() => {
        toastEl.remove();
        console.log('🗑️ Toast element removed from DOM');
      }, 300);
    }, displayDuration);
  },

  /**
   * Show success toast
   * @param {string} message - Success message
   * @param {number} duration - Optional custom duration
   */
  success(message, duration = null) {
    this.show(message, 'success', duration);
  },

  /**
   * Show error toast
   * @param {string} message - Error message
   * @param {number} duration - Optional custom duration
   */
  error(message, duration = null) {
    this.show(message, 'error', duration);
  },

  /**
   * Show info toast
   * @param {string} message - Info message
   * @param {number} duration - Optional custom duration
   */
  info(message, duration = null) {
    this.show(message, 'info', duration);
  },

  /**
   * Show warning toast
   * @param {string} message - Warning message
   * @param {number} duration - Optional custom duration
   */
  warning(message, duration = null) {
    this.show(message, 'warning', duration);
  },

  /**
   * Convert Django messages array to toasts
   * Called from toast.html Django template
   * @param {array} messages - Array of {text, level} objects from Django
   */
  displayDjangoMessages(messages) {
    if (!messages || !Array.isArray(messages)) return;

    messages.forEach(msg => {
      let toastType = 'info';
      switch(msg.level) {
        case 'success':
          toastType = 'success';
          break;
        case 'error':
          toastType = 'error';
          break;
        case 'warning':
          toastType = 'warning';
          break;
        case 'debug':
        case 'info':
        default:
          toastType = 'info';
      }
      this[toastType](msg.text);
    });
  },

  /**
   * Handle API response messages
   * Displays toast from API response
   * @param {object} response - API response with optional message and type
   */
  handleAPIResponse(response) {
    if (!response || !response.message) return response;

    const type = response.type || (response.success ? 'success' : 'error');
    this[type](response.message);
    return response;
  },

  /**
   * Handle API errors
   * Displays error toast from error
   * @param {Error} error - Error object
   */
  handleAPIError(error) {
    const message = error.message || 'An error occurred';
    this.error(message);
    console.error('API Error:', error);
    return Promise.reject(error);
  },
};

// Make Toast globally available
window.Toast = Toast;

// Export for ES modules
export { Toast };

/**
 * Updated Toast Notification System
 * Now styled using DaisyUI and integrates seamlessly with Django messages.
 */

const Toast = {
  /**
   * Toast types with their DaisyUI styling
   */
  types: {
    success: {
      icon: 'fa-circle-check',
      className: 'alert alert-success shadow-lg',
      duration: 3000,
    },
    error: {
      icon: 'fa-circle-exclamation',
      className: 'alert alert-error shadow-lg',
      duration: 4000,
    },
    info: {
      icon: 'fa-circle-info',
      className: 'alert alert-info shadow-lg',
      duration: 3000,
    },
    warning: {
      icon: 'fa-triangle-exclamation',
      className: 'alert alert-warning shadow-lg',
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
    const toastConfig = this.types[type] || this.types.info;
    const displayDuration = duration || toastConfig.duration;

    // Get or create container
    let container = document.getElementById('toast-container');
    if (!container) {
      console.error('🚨 Toast container NOT found in DOM! Ensure toast.html is included in base.html');
      return;
    }

    // Create toast element
    const toastEl = document.createElement('div');
    toastEl.className = `${toastConfig.className} gap-2 pointer-events-auto animate-fade-in`;
    toastEl.innerHTML = `
      <div class="flex items-center">
        <svg class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <span>${message}</span>
      </div>
    `;

    // Add to container
    container.appendChild(toastEl);

    // Auto-remove after duration
    setTimeout(() => {
      toastEl.classList.add('animate-fade-out');
      setTimeout(() => {
        toastEl.remove();
      }, 300);
    }, displayDuration);
  },

  /**
   * Convert Django messages array to toasts
   * Called from toast.html Django template
   * @param {array} messages - Array of {text, level} objects from Django
   */
  displayDjangoMessages(messages) {
    if (!messages || !Array.isArray(messages)) return;

    messages.forEach((msg) => {
      let toastType = "info";
      switch (msg.level) {
        case "success":
          toastType = "success";
          break;
        case "error":
          toastType = "error";
          break;
        case "warning":
          toastType = "warning";
          break;
        case "info":
        default:
          toastType = "info";
      }
      this.show(msg.text, toastType);
    });
  },
};

// Make Toast globally available
window.Toast = Toast;

// Export for ES modules
export { Toast };

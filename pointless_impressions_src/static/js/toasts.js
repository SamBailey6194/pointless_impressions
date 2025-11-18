(() => {
  // pointless_impressions_src/theme/static_src/src/js/toasts.js
  var Toast = {
    /**
     * Toast types with their DaisyUI styling
     */
    types: {
      success: {
        icon: "fa-circle-check",
        className: "alert alert-success shadow-lg",
        duration: 3e3
      },
      error: {
        icon: "fa-circle-exclamation",
        className: "alert alert-error shadow-lg",
        duration: 4e3
      },
      info: {
        icon: "fa-circle-info",
        className: "alert alert-info shadow-lg",
        duration: 3e3
      },
      warning: {
        icon: "fa-triangle-exclamation",
        className: "alert alert-warning shadow-lg",
        duration: 3500
      }
    },
    /**
     * Show a toast notification
     * @param {string} message - The message to display
     * @param {string} type - The type of toast (success, error, info, warning)
     * @param {number} duration - Optional custom duration in milliseconds
     */
    show(message, type = "info", duration = null) {
      const toastConfig = this.types[type] || this.types.info;
      const displayDuration = duration || toastConfig.duration;
      let container = document.getElementById("toast-container");
      if (!container) {
        console.error("\u{1F6A8} Toast container NOT found in DOM! Ensure toast.html is included in base.html");
        return;
      }
      const toastEl = document.createElement("div");
      toastEl.className = `${toastConfig.className} gap-2 pointer-events-auto animate-fade-in`;
      toastEl.innerHTML = `
      <div class="flex items-center">
        <i class="fa-solid ${toastConfig.icon} fa-lg mr-2"></i>
        <span>${message}</span>
      </div>
    `;
      container.appendChild(toastEl);
      setTimeout(() => {
        toastEl.classList.add("animate-fade-out");
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
    }
  };
  window.Toast = Toast;
})();
//# sourceMappingURL=toasts.js.map

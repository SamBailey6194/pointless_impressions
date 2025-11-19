(() => {
  // pointless_impressions_src/theme/static_src/src/js/admin_dashboard.js
  document.addEventListener("DOMContentLoaded", () => {
    const openModal = (modalId) => {
      const modal = document.getElementById(modalId);
      if (modal) {
        modal.showModal();
      }
    };
    const closeModal = (modalId) => {
      const modal = document.getElementById(modalId);
      if (modal) {
        modal.close();
      }
    };
    document.querySelectorAll("[data-modal-open]").forEach((button) => {
      button.addEventListener("click", (event) => {
        const modalId = event.target.getAttribute("data-modal-open");
        openModal(modalId);
      });
    });
    document.querySelectorAll("[data-modal-close]").forEach((button) => {
      button.addEventListener("click", (event) => {
        const modalId = event.target.getAttribute("data-modal-close");
        closeModal(modalId);
      });
    });
  });
})();
//# sourceMappingURL=admin_dashboard.js.map

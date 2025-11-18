(() => {
  // pointless_impressions_src/theme/static_src/src/js/manage_artists.js
  document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".js-approve-artist-btn").forEach((button) => {
      button.addEventListener("click", function() {
        const artistId = this.dataset.artistId;
        if (confirm("Are you sure you want to approve this artist?")) {
          fetch(`/dashboard/approve-artist/${artistId}/`, {
            method: "POST",
            headers: {
              "X-CSRFToken": getCookie("csrftoken")
            }
          }).then((response) => {
            if (response.ok) {
              location.reload();
            } else {
              alert("Failed to approve artist.");
            }
          });
        }
      });
    });
    document.querySelectorAll(".js-reject-artist-btn").forEach((button) => {
      button.addEventListener("click", function() {
        const artistId = this.dataset.artistId;
        const rejectionNotes = this.closest(".card").querySelector(".js-rejection-notes");
        rejectionNotes.classList.remove("hidden");
        rejectionNotes.focus();
        rejectionNotes.addEventListener("blur", function() {
          if (confirm("Are you sure you want to reject this artist?")) {
            fetch(`/dashboard/reject-artist/${artistId}/`, {
              method: "POST",
              headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/json"
              },
              body: JSON.stringify({ notes: rejectionNotes.value })
            }).then((response) => {
              if (response.ok) {
                location.reload();
              } else {
                alert("Failed to reject artist.");
              }
            });
          }
        }, { once: true });
      });
    });
    document.querySelectorAll(".js-remove-artist-btn").forEach((button) => {
      button.addEventListener("click", function() {
        const artistId = this.dataset.artistId;
        const removalNotes = this.closest(".card").querySelector(".js-removal-notes");
        removalNotes.classList.remove("hidden");
        removalNotes.focus();
        removalNotes.addEventListener("blur", function() {
          if (confirm("Are you sure you want to remove this artist?")) {
            fetch(`/dashboard/remove-artist/${artistId}/`, {
              method: "POST",
              headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/json"
              },
              body: JSON.stringify({ notes: removalNotes.value })
            }).then((response) => {
              if (response.ok) {
                location.reload();
              } else {
                alert("Failed to remove artist.");
              }
            });
          }
        }, { once: true });
      });
    });
  });
})();
//# sourceMappingURL=manage_artists.js.map

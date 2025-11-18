(() => {
  // pointless_impressions_src/theme/static_src/src/js/auth.js
  (function() {
    function login() {
      const loginModal = document.getElementById("login-modal");
      loginModal.showModal();
    }
    function logout() {
      const logoutModal = document.getElementById("logout-modal");
      logoutModal.showModal();
    }
    function resendCode() {
      fetch("/profiles/resend-verification-code/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken")
        }
      }).then((response) => {
        return response.json();
      });
    }
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
    const loginButton = document.getElementById("login-button");
    const logoutButton = document.getElementById("logout-button");
    if (loginButton) {
      loginButton.addEventListener("click", login);
    }
    if (logoutButton) {
      logoutButton.addEventListener("click", logout);
    }
    document.addEventListener("click", (e) => {
      if (e.target && e.target.id === "button-id-resend") {
        resendCode();
      }
    });
  })();
})();
//# sourceMappingURL=auth.js.map

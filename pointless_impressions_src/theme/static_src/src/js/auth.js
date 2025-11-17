addEventListener('DOMContentLoaded', () => {
    function login() {
        const loginModal = document.getElementById('login-modal');
        loginModal.showModal();
    }

    function logout() {
        const logoutModal = document.getElementById('logout-modal');
        logoutModal.showModal();
    }

    document.getElementById('login-button').addEventListener('click', login);
    document.getElementById('logout-button').addEventListener('click', logout);
});
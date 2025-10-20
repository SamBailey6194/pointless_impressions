document.addEventListener("DOMContentLoaded", () => {
    // Header hide on scroll
    let lastScroll = 0;
    const header = document.querySelector('header');
    window.addEventListener('scroll', () => {
    const currentScroll = window.scrollY;
    if (currentScroll > lastScroll) {
        header.style.transform = 'translateY(-100%)';
    } else {
        header.style.transform = 'translateY(0)';
    }
    lastScroll = currentScroll;
    });

    // Footer show at bottom
    const footer = document.querySelector('footer');
    window.addEventListener('scroll', () => {
    const scrollableHeight = document.documentElement.scrollHeight - window.innerHeight;
    const currentScroll = window.scrollY;
    if (currentScroll >= scrollableHeight) {
        footer.style.transform = 'translateY(0)';
    } else {
        footer.style.transform = 'translateY(100%)';
    }
    });
});
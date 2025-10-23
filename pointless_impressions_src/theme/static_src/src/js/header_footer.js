document.addEventListener("DOMContentLoaded", () => {
  // --- Elements ---
  const header = document.querySelector("header");
  const footer = document.querySelector("footer");
  const menuToggleBtn = document.getElementById("nav-toggle");
  const nav = document.getElementById("main-nav");
  const searchToggleBtn = document.getElementById("mobile-search-btn");
  const searchDropdown = document.getElementById("mobile-search-dropdown");
  const accountBtn = document.querySelector(".fa-user")?.closest("button");
  const accountMenu = accountBtn?.nextElementSibling;
  const cartBtn = document.querySelector(".fa-cart-shopping")?.closest("button");
  const cartMenu = cartBtn?.nextElementSibling;

  let lastScroll = 0;
  let ticking = false;

  // --- Helper: Close all dropdowns ---
  function closeAllDropdowns() {
    [nav, searchDropdown, accountMenu, cartMenu].forEach((el) => {
      if (el && !el.classList.contains("hidden")) el.classList.add("hidden");
    });
  }

  // --- Header hide on scroll ---
  if (header) {
    window.addEventListener("scroll", () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          const currentScroll = window.scrollY;
          const scrollingDown = currentScroll > lastScroll && currentScroll > 80;
          header.style.transform = scrollingDown ? "translateY(-100%)" : "translateY(0)";
          lastScroll = currentScroll;
          ticking = false;
        });
        ticking = true;
      }
    });
  }

  // --- Footer show at bottom ---
  if (footer) {
    window.addEventListener("scroll", () => {
      const scrollableHeight = document.documentElement.scrollHeight - window.innerHeight;
      const currentScroll = window.scrollY;
      footer.style.transform =
        currentScroll >= scrollableHeight - 5 ? "translateY(0)" : "translateY(100%)";
    });
  }

  // --- Mobile menu toggle ---
  if (menuToggleBtn && nav) {
    const icon = menuToggleBtn.querySelector("i");

    menuToggleBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      closeAllDropdowns();
      nav.classList.toggle("hidden");

      // Swap icon between bars and xmark
      if (icon) {
        icon.classList.toggle("fa-bars");
        icon.classList.toggle("fa-xmark");
      }
    });
  }

  // --- Mobile search toggle ---
  if (searchToggleBtn && searchDropdown) {
    searchToggleBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      closeAllDropdowns();
      searchDropdown.classList.toggle("hidden");
    });
  }

  // --- Account menu toggle ---
  if (accountBtn && accountMenu) {
    accountBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      closeAllDropdowns();
      accountMenu.classList.toggle("hidden");
    });
  }

  // --- Cart dropdown toggle ---
  if (cartBtn && cartMenu) {
    cartBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      closeAllDropdowns();
      cartMenu.classList.toggle("hidden");
    });
  }

  // --- Close everything when clicking outside ---
  document.addEventListener("click", (e) => {
    const clickInsideDropdown =
      [nav, searchDropdown, accountMenu, cartMenu].some((el) => el && el.contains(e.target)) ||
      [menuToggleBtn, searchToggleBtn, accountBtn, cartBtn].some((btn) => btn && btn.contains(e.target));

    if (!clickInsideDropdown) {
      closeAllDropdowns();
      const icon = menuToggleBtn?.querySelector("i");
      if (icon && icon.classList.contains("fa-xmark")) {
        icon.classList.replace("fa-xmark", "fa-bars");
      }
    }
  });
});

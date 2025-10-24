(() => {
  // pointless_impressions_src/theme/static_src/src/js/header_footer.js
  document.addEventListener("DOMContentLoaded", () => {
    const header = document.querySelector("header");
    const footer = document.querySelector("footer");
    const mobileSearchBar = document.getElementById("mobile-search-bar");
    const dropdowns = document.querySelectorAll(".dropdown");
    let lastScroll = 0;
    let ticking = false;
    window.toggleMobileSearch = function() {
      if (mobileSearchBar) {
        mobileSearchBar.classList.toggle("hidden");
        if (!mobileSearchBar.classList.contains("hidden")) {
          const searchInput = mobileSearchBar.querySelector("input");
          if (searchInput) {
            setTimeout(() => searchInput.focus(), 100);
          }
        }
      }
    };
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
    dropdowns.forEach((dropdown) => {
      const trigger = dropdown.querySelector('[tabindex="0"]');
      const menu = dropdown.querySelector(".dropdown-content");
      if (trigger && menu) {
        document.addEventListener("click", (e) => {
          if (!dropdown.contains(e.target)) {
            trigger.blur();
          }
        });
        document.addEventListener("keydown", (e) => {
          if (e.key === "Escape") {
            trigger.blur();
          }
        });
        trigger.addEventListener("click", () => {
          setTimeout(() => {
            const searchInput = menu.querySelector('input[type="text"]');
            if (searchInput) {
              searchInput.focus();
            }
          }, 100);
        });
      }
    });
    const searchInputs = document.querySelectorAll('input[type="text"][placeholder*="Search"]');
    searchInputs.forEach((input) => {
      input.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
          performSearch(input.value);
        }
      });
      const searchBtn = input.parentElement.querySelector("button");
      if (searchBtn) {
        searchBtn.addEventListener("click", () => {
          performSearch(input.value);
        });
      }
    });
    function performSearch(query) {
      if (query.trim()) {
        console.log("Searching for:", query);
      }
    }
    if (mobileSearchBar) {
      let mobileSearchTimeout;
      window.addEventListener("scroll", () => {
        clearTimeout(mobileSearchTimeout);
        mobileSearchTimeout = setTimeout(() => {
          if (!mobileSearchBar.classList.contains("hidden")) {
            mobileSearchBar.classList.add("hidden");
          }
        }, 2e3);
      });
    }
    document.addEventListener("keydown", (e) => {
      if (e.key === "Tab") {
        if (mobileSearchBar && !mobileSearchBar.classList.contains("hidden")) {
          const activeElement = document.activeElement;
          if (!mobileSearchBar.contains(activeElement)) {
            setTimeout(() => {
              if (!mobileSearchBar.contains(document.activeElement)) {
                mobileSearchBar.classList.add("hidden");
              }
            }, 100);
          }
        }
      }
    });
    const cartButtons = document.querySelectorAll('[class*="cart"]');
    cartButtons.forEach((button) => {
      button.addEventListener("click", (e) => {
        if (button.textContent.includes("View Cart")) {
          e.preventDefault();
          console.log("Navigate to cart page");
        }
      });
    });
  });
})();
//# sourceMappingURL=header_footer.js.map

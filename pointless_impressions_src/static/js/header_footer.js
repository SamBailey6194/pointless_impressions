(() => {
  // pointless_impressions_src/theme/static_src/src/js/header_footer.js
  document.addEventListener("DOMContentLoaded", () => {
    const header = document.querySelector("header");
    const footer = document.querySelector("footer");
    const mobileSearchBar = document.getElementById("mobile-search-bar");
    const dropdowns = document.querySelectorAll(".dropdown");
    let lastScroll = 0;
    let ticking = false;
    const AUTOCOMPLETE_API_URL = window.GLOBAL_URLS && window.GLOBAL_URLS.AUTOCOMPLETE_API;
    window.toggleMobileSearch = function() {
      if (mobileSearchBar) {
        mobileSearchBar.classList.toggle("hidden");
        if (!mobileSearchBar.classList.contains("hidden")) {
          const searchInput = mobileSearchBar.querySelector('input[name="q"]');
          if (searchInput) {
            setTimeout(() => searchInput.focus(), 100);
          }
        }
      }
    };
    function performSearch(query, inputElement) {
      const trimmedQuery = query.trim();
      if (trimmedQuery) {
        const form = inputElement.closest("form");
        if (form) {
          const queryInput = form.querySelector('input[name="q"]');
          if (queryInput) {
            queryInput.value = trimmedQuery;
          }
          form.submit();
        }
      }
    }
    function initAutoComplete(inputElement) {
      if (!AUTOCOMPLETE_API_URL) {
        console.warn("Autocomplete API URL is missing. Autocomplete feature disabled.");
        return;
      }
      if (typeof autoComplete === "undefined") {
        console.warn("autoComplete library is not loaded. Search will work without autocomplete suggestions.");
        return;
      }
      try {
        const inputId = inputElement.id || `search-input-${Math.random().toString(36).substr(2, 9)}`;
        if (!inputElement.id) {
          inputElement.id = inputId;
        }
        new autoComplete({
          selector: `#${inputId}`,
          placeHolder: "Search products, categories...",
          data: {
            src: async (query) => {
              try {
                const response = await fetch(`${AUTOCOMPLETE_API_URL}?term=${query}`);
                const data = await response.json();
                return data;
              } catch (error) {
                console.error("Autocomplete fetch failed:", error);
                return [];
              }
            }
          },
          resultItem: {
            highlight: true
          },
          threshold: 2,
          events: {
            input: {
              selection: (event) => {
                const inputElement2 = event.target;
                const selectedValue = event.detail.selection.value;
                inputElement2.value = selectedValue;
                performSearch(selectedValue, inputElement2);
              }
            }
          }
        });
      } catch (error) {
        console.error("Failed to initialize autoComplete:", error);
      }
    }
    const searchInputs = document.querySelectorAll('input[type="text"][name="q"]');
    searchInputs.forEach((input) => {
      initAutoComplete(input);
      input.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
          e.preventDefault();
          performSearch(input.value, input);
        }
      });
      const form = input.closest("form");
      const searchBtn = form ? form.querySelector('button[type="submit"]') : null;
      if (searchBtn) {
        searchBtn.addEventListener("click", (e) => {
          e.preventDefault();
          performSearch(input.value, input);
        });
      }
    });
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
        }
      });
    });
  });
})();
//# sourceMappingURL=header_footer.js.map

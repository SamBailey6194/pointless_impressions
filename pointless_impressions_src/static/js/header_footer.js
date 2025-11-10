(() => {
  // pointless_impressions_src/theme/static_src/src/js/cart.js
  var CART_UUID_KEY = "cart_uuid";
  function formatPrice(price) {
    if (typeof price !== "number") {
      return "\xA30.00";
    }
    return "\xA3" + price.toLocaleString("en-GB", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });
  }
  function getCartUUID() {
    return localStorage.getItem(CART_UUID_KEY) || null;
  }
  async function fetchCartFromBackend() {
    const cart_uuid = getCartUUID();
    if (!cart_uuid) return {};
    try {
      const response = await fetch(`/checkout/api/cart/fetch/?cart_uuid=${cart_uuid}`);
      if (!response.ok) throw new Error("Failed to fetch cart");
      return await response.json();
    } catch (e) {
      console.error("Error fetching cart from backend:", e);
      return {};
    }
  }
  async function syncCartWithBackend() {
    return { success: true, cart_uuid: getCartUUID() };
  }
  async function getTotalQuantity() {
    const cart = await fetchCartFromBackend();
    let total = 0;
    if (cart.items) {
      cart.items.forEach((item) => {
        total += item.quantity;
      });
    }
    return total;
  }
  async function calculateTotal() {
    const cart = await fetchCartFromBackend();
    let total = 0;
    if (cart.items) {
      cart.items.forEach((item) => {
        total += item.total || item.price * item.quantity;
      });
    }
    return Math.round(total * 100) / 100;
  }
  function initCart2() {
    syncCartWithBackend().then((response) => {
      if (response?.success) {
        if (window.updateCartDisplay && typeof window.updateCartDisplay === "function") {
          window.updateCartDisplay();
        }
      }
    }).catch((err) => {
      console.error("\u274C Failed to sync cart on page load:", err);
    });
  }
  if (typeof window !== "undefined") {
    window.initCart = initCart2;
    window.getTotalQuantity = getTotalQuantity;
    window.calculateTotal = calculateTotal;
    window.formatPrice = formatPrice;
  }

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
    window.updateCartDisplay = async function() {
      if (typeof getTotalQuantity === "function" && typeof calculateTotal === "function" && typeof formatPrice === "function") {
        let totalQuantity = 0;
        let subtotal = 0;
        let cart = {};
        try {
          totalQuantity = await getTotalQuantity();
          subtotal = await calculateTotal();
          if (typeof fetchCartFromBackend === "function") {
            cart = await fetchCartFromBackend();
          }
        } catch (e) {
          console.error("Failed to fetch cart data:", e);
        }
        const formattedPrice = formatPrice(subtotal);
        const badge = document.getElementById("cart-count-badge");
        if (badge) badge.textContent = totalQuantity;
        const itemsText = document.getElementById("cart-items-text");
        if (itemsText) itemsText.textContent = totalQuantity === 1 ? "1 Item" : `${totalQuantity} Items`;
        const subtotalEl = document.getElementById("cart-subtotal");
        if (subtotalEl) subtotalEl.textContent = formattedPrice;
        const itemsList = document.getElementById("cart-items-list");
        if (itemsList && cart.items && Array.isArray(cart.items)) {
          if (cart.items.length === 0) {
            itemsList.innerHTML = '<span class="text-sm">Your cart is empty.</span>';
          } else {
            let tableHtml = `<table class="w-full text-xs">
            <thead>
              <tr>
                <th class="w-1/4 text-left font-semibold">Image</th>
                <th class="w-1/4 text-left font-semibold">Item</th>
                <th class="w-1/4 text-center font-semibold">Qty</th>
                <th class="w-1/4 text-right font-semibold">Price</th>
              </tr>
            </thead>
            <tbody>
              ${cart.items.map((item) => `
                <tr>
                  <td class="py-1 pr-2"><img src="${item.image_url}" alt="${item.name}" class="h-10 w-10 object-cover rounded"/></td>
                  <td class="py-1 pr-2">${item.name}</td>
                  <td class="py-1 text-center">x${item.quantity}</td>
                  <td class="py-1 text-right">${formatPrice(item.total)}</td>
                </tr>
              `).join("")}
            </tbody>
          </table>`;
            itemsList.innerHTML = tableHtml;
          }
        }
      }
    };
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", () => {
        setTimeout(() => window.updateCartDisplay(), 100);
        if (typeof initCart === "function") {
          initCart();
        }
      });
    } else {
      setTimeout(() => window.updateCartDisplay(), 100);
      if (typeof initCart === "function") {
        initCart();
      }
    }
    window.addEventListener("storage", (e) => {
      if (e.key === "cart_uuid" || e.key === null) {
        window.updateCartDisplay();
      }
    });
    window.showCartDropdown = function() {
      const cartDropdown = document.getElementById("cart-dropdown");
      if (!cartDropdown) return;
      const rect = cartDropdown.getBoundingClientRect();
      if (rect.top < 0 || rect.bottom > window.innerHeight) {
        window.scrollTo({ top: 0, behavior: "smooth" });
      }
      const label = cartDropdown.querySelector('label[tabindex="0"]');
      if (label) {
        setTimeout(() => {
          label.focus();
          cartDropdown.classList.add("dropdown-open");
          setTimeout(() => {
            cartDropdown.classList.remove("dropdown-open");
          }, 2500);
        }, 400);
      }
    };
  });
})();
//# sourceMappingURL=header_footer.js.map

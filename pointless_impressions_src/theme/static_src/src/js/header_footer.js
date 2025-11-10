import { fetchCartFromBackend, formatPrice, getTotalQuantity, calculateTotal } from './cart.js';

document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const header = document.querySelector("header");
  const footer = document.querySelector("footer");
  
  // DaisyUI-specific elements
  const mobileSearchBar = document.getElementById("mobile-search-bar");
  const dropdowns = document.querySelectorAll('.dropdown');
  
  let lastScroll = 0;
  let ticking = false;

  // Global URL from window object (defined in base.html)
  const AUTOCOMPLETE_API_URL = window.GLOBAL_URLS && window.GLOBAL_URLS.AUTOCOMPLETE_API;

  // Mobile search toggle functionality
  window.toggleMobileSearch = function() {
    if (mobileSearchBar) {
      mobileSearchBar.classList.toggle('hidden');

      if (!mobileSearchBar.classList.contains('hidden')) {
        const searchInput = mobileSearchBar.querySelector('input[name="q"]');
        if (searchInput) {
          setTimeout(() => searchInput.focus(), 100);
        }
      }
    }
  };

  // Search submission function
  // This function replaces the placeholder logic and submits the actual form.
  function performSearch(query, inputElement) {
    const trimmedQuery = query.trim();
    if (trimmedQuery) {

      const form = inputElement.closest('form');
      if (form) {

        const queryInput = form.querySelector('input[name="q"]');
        if (queryInput) {
            queryInput.value = trimmedQuery;
        }
        form.submit();
      }
    }
  }

  // Autocomplete Initialization Function
  function initAutoComplete(inputElement) {
    if (!AUTOCOMPLETE_API_URL) {
      console.warn("Autocomplete API URL is missing. Autocomplete feature disabled.");
      return;
    }

    // Check if autoComplete library is available
    if (typeof autoComplete === 'undefined') {
      console.warn("autoComplete library is not loaded. Search will work without autocomplete suggestions.");
      return;
    }

    try {
      // Generate a unique selector for this input
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
              // Use the global API URL defined in base.html
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
              const inputElement = event.target;
              const selectedValue = event.detail.selection.value;
              inputElement.value = selectedValue;

              performSearch(selectedValue, inputElement);
            }
          }
        }
      });
    } catch (error) {
      console.error("Failed to initialize autoComplete:", error);
    }
  }
  
  // Initialise search inputs and Autocomplete
  const searchInputs = document.querySelectorAll('input[type="text"][name="q"]');
  searchInputs.forEach(input => {
    initAutoComplete(input);

    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        performSearch(input.value, input);
      }
    });

    const form = input.closest('form');
    const searchBtn = form ? form.querySelector('button[type="submit"]') : null;
    
    if (searchBtn) {
      searchBtn.addEventListener('click', (e) => {
        e.preventDefault();
        performSearch(input.value, input);
      });
    }
  });


  // Header hide on scroll
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

  // DaisyUI Dropdown enhancements
  dropdowns.forEach(dropdown => {
    const trigger = dropdown.querySelector('[tabindex="0"]');
    const menu = dropdown.querySelector('.dropdown-content');
    
    if (trigger && menu) {
      // Close dropdown when clicking outside
      document.addEventListener('click', (e) => {
        if (!dropdown.contains(e.target)) {
          trigger.blur();
        }
      });

      // Close dropdown when pressing Escape
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          trigger.blur();
        }
      });

      // Auto-focus search inputs in dropdowns (Currently disabled in HTML, but kept here)
      trigger.addEventListener('click', () => {
        setTimeout(() => {
          const searchInput = menu.querySelector('input[type="text"]');
          if (searchInput) {
            searchInput.focus();
          }
        }, 100);
      });
    }
  });

  // Mobile search bar auto-close on scroll
  if (mobileSearchBar) {
    let mobileSearchTimeout;
    window.addEventListener('scroll', () => {
      clearTimeout(mobileSearchTimeout);
      mobileSearchTimeout = setTimeout(() => {
        if (!mobileSearchBar.classList.contains('hidden')) {
          mobileSearchBar.classList.add('hidden');
        }
      }, 2000);
    });
  }

  // Accessibility enhancements
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      // Close mobile search when tabbing away
      if (mobileSearchBar && !mobileSearchBar.classList.contains('hidden')) {
        const activeElement = document.activeElement;
        if (!mobileSearchBar.contains(activeElement)) {
          setTimeout(() => {
            if (!mobileSearchBar.contains(document.activeElement)) {
              mobileSearchBar.classList.add('hidden');
            }
          }, 100);
        }
      }
    }
  });

  // Cart functionality placeholders
  const cartButtons = document.querySelectorAll('[class*="cart"]');
  cartButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      if (button.textContent.includes('View Cart')) {
        e.preventDefault();
        // TODO: Implement cart navigation
        // window.location.href = '/cart/';
      }
    });
  });

  // Cart UI Update Functions
  /**
   * Update cart display in header with current cart data (async)
   */
  window.updateCartDisplay = async function() {
    if (typeof getTotalQuantity === 'function' && typeof calculateTotal === 'function' && typeof formatPrice === 'function') {
      let totalQuantity = 0;
      let subtotal = 0;
      let cart = {};
      try {
        totalQuantity = await getTotalQuantity();
        subtotal = await calculateTotal();
        if (typeof fetchCartFromBackend === 'function') {
          cart = await fetchCartFromBackend();
        }
      } catch (e) {
        console.error('Failed to fetch cart data:', e);
      }
      const formattedPrice = formatPrice(subtotal);
      // Update badge
      const badge = document.getElementById('cart-count-badge');
      if (badge) badge.textContent = totalQuantity;
      // Update items text
      const itemsText = document.getElementById('cart-items-text');
      if (itemsText) itemsText.textContent = totalQuantity === 1 ? '1 Item' : `${totalQuantity} Items`;
      // Update subtotal
      const subtotalEl = document.getElementById('cart-subtotal');
      if (subtotalEl) subtotalEl.textContent = formattedPrice;
      // Render cart items in the span as a table
      const itemsList = document.getElementById('cart-items-list');
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
              ${cart.items.map(item => `
                <tr>
                  <td class="py-1 pr-2"><img src="${item.image_url}" alt="${item.name}" class="h-10 w-10 object-cover rounded"/></td>
                  <td class="py-1 pr-2">${item.name}</td>
                  <td class="py-1 text-center">x${item.quantity}</td>
                  <td class="py-1 text-right">${formatPrice(item.total)}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>`;
          itemsList.innerHTML = tableHtml;
        }
      }
    }
  };

  // Initial cart display update on page load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      setTimeout(() => window.updateCartDisplay(), 100);
      if (typeof initCart === 'function') {
        initCart();
      }
    });
  } else {
    setTimeout(() => window.updateCartDisplay(), 100);
    if (typeof initCart === 'function') {
      initCart();
    }
  }

  // Listen for cart changes (storage events from other tabs/windows)
  window.addEventListener('storage', (e) => {
    if (e.key === 'cart_uuid' || e.key === null) {
      window.updateCartDisplay();
    }
  });

  window.showCartDropdown = function() {
    // Scroll to top if needed to ensure cart is visible
    const cartDropdown = document.getElementById('cart-dropdown');
    if (!cartDropdown) return;
    const rect = cartDropdown.getBoundingClientRect();
    if (rect.top < 0 || rect.bottom > window.innerHeight) {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    const label = cartDropdown.querySelector('label[tabindex="0"]');
    if (label) {
      setTimeout(() => {
        label.focus();
        cartDropdown.classList.add('dropdown-open');
        setTimeout(() => {
          cartDropdown.classList.remove('dropdown-open');
        }, 2500);
      }, 400);
    }
  };
});

document.addEventListener("DOMContentLoaded", () => {
  // --- Elements ---
  const header = document.querySelector("header");
  const footer = document.querySelector("footer");
  
  // DaisyUI-specific elements
  const mobileSearchBar = document.getElementById("mobile-search-bar");
  const dropdowns = document.querySelectorAll('.dropdown');
  
  let lastScroll = 0;
  let ticking = false;

  // --- Mobile search toggle functionality ---
  window.toggleMobileSearch = function() {
    if (mobileSearchBar) {
      mobileSearchBar.classList.toggle('hidden');
      
      // Focus on search input when opened
      if (!mobileSearchBar.classList.contains('hidden')) {
        const searchInput = mobileSearchBar.querySelector('input');
        if (searchInput) {
          setTimeout(() => searchInput.focus(), 100);
        }
      }
    }
  };

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

  // --- DaisyUI Dropdown enhancements ---
  dropdowns.forEach(dropdown => {
    const trigger = dropdown.querySelector('[tabindex="0"]');
    const menu = dropdown.querySelector('.dropdown-content');
    
    if (trigger && menu) {
      // Close dropdown when clicking outside
      document.addEventListener('click', (e) => {
        if (!dropdown.contains(e.target)) {
          trigger.blur(); // This closes DaisyUI dropdowns
        }
      });

      // Close dropdown when pressing Escape
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          trigger.blur();
        }
      });

      // Auto-focus search inputs in dropdowns
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

  // --- Search functionality ---
  const searchInputs = document.querySelectorAll('input[type="text"][placeholder*="Search"]');
  searchInputs.forEach(input => {
    // Add search functionality
    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        performSearch(input.value);
      }
    });

    // Add search button click handlers
    const searchBtn = input.parentElement.querySelector('button');
    if (searchBtn) {
      searchBtn.addEventListener('click', () => {
        performSearch(input.value);
      });
    }
  });

  // --- Search function ---
  function performSearch(query) {
    if (query.trim()) {
      console.log('Searching for:', query);
      // TODO: Implement actual search functionality
      // window.location.href = `/search/?q=${encodeURIComponent(query)}`;
    }
  }

  // --- Mobile search bar auto-close on scroll ---
  if (mobileSearchBar) {
    let mobileSearchTimeout;
    window.addEventListener('scroll', () => {
      clearTimeout(mobileSearchTimeout);
      mobileSearchTimeout = setTimeout(() => {
        if (!mobileSearchBar.classList.contains('hidden')) {
          mobileSearchBar.classList.add('hidden');
        }
      }, 2000); // Close after 2 seconds of scroll inactivity
    });
  }

  // --- Accessibility enhancements ---
  // Add keyboard navigation for dropdowns
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

  // --- Cart functionality placeholders ---
  const cartButtons = document.querySelectorAll('[class*="cart"]');
  cartButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      // Prevent default for demo
      if (button.textContent.includes('View Cart')) {
        e.preventDefault();
        console.log('Navigate to cart page');
        // TODO: Implement cart navigation
        // window.location.href = '/cart/';
      }
    });
  });
});

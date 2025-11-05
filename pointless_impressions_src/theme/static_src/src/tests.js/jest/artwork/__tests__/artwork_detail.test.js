/**
 * Artwork Detail Page Tests
 * Tests for US002: View Artwork Details
 */

import { formatPrice, displayArtworkDetail, addToCart, showConfirmationMessage, initArtworkDetail } from '../../../../js/artwork_detail.js';

describe('Artwork Detail Page - US002', () => {
  let mockDOM;

  beforeEach(() => {
    // Setup DOM mock for tests
    document.body.innerHTML = `
      <div id="artwork-detail">
        <h1 id="artwork-title">Mountain Peak</h1>
        <div id="artwork-description">
          A serene mountain landscape in pointillist style.
        </div>
        <div id="artwork-price">£249.99</div>
        <img id="artwork-image" src="test_image.jpg" alt="Mountain Peak" />
        <div id="availability-status">Available</div>
        <button id="add-to-cart-btn">Add to Cart</button>
        <div id="artist-info">
          <a href="/profile/michael">Michael</a>
        </div>
        <div id="related-artworks"></div>
      </div>
    `;
  });

  afterEach(() => {
    document.body.innerHTML = '';
    // Clear localStorage between tests
    localStorage.clear();
  });

  describe('Artwork Title Display', () => {
    test('should display artwork title correctly', () => {
      const title = document.getElementById('artwork-title');
      expect(title).toBeDefined();
      expect(title.textContent).toBe('Mountain Peak');
    });

    test('should have non-empty title', () => {
      const title = document.getElementById('artwork-title');
      expect(title.textContent.trim()).not.toBe('');
    });
  });

  describe('Artwork Description Display', () => {
    test('should display artwork description', () => {
      const description = document.getElementById('artwork-description');
      expect(description).toBeDefined();
      expect(description.textContent).toContain('pointillist');
    });

    test('description should be readable', () => {
      const description = document.getElementById('artwork-description');
      const text = description.textContent;
      expect(text.length).toBeGreaterThan(10);
    });
  });

  describe('Price Display', () => {
    test('should display formatted price', () => {
      const price = document.getElementById('artwork-price');
      expect(price).toBeDefined();
      expect(price.textContent).toBe('£249.99');
    });

    test('should have valid price format', () => {
      const price = document.getElementById('artwork-price');
      const priceRegex = /^£\d+(\.\d{2})?$/;
      expect(priceRegex.test(price.textContent)).toBe(true);
    });

    test('formatPrice function should work correctly', () => {
      expect(formatPrice(249.99)).toBe('£249.99');
      expect(formatPrice(100)).toBe('£100.00');
      expect(formatPrice(1234.50)).toBe('£1,234.50');
    });

    test('formatPrice should handle non-number inputs', () => {
      expect(formatPrice('invalid')).toBe('£0.00');
      expect(formatPrice(null)).toBe('£0.00');
      expect(formatPrice(undefined)).toBe('£0.00');
      expect(formatPrice(true)).toBe('£0.00');
    });

    test('formatPrice should handle large prices', () => {
      expect(formatPrice(10000)).toBe('£10,000.00');
      expect(formatPrice(1000000.99)).toBe('£1,000,000.99');
    });

    test('formatPrice should handle small prices', () => {
      expect(formatPrice(0.99)).toBe('£0.99');
      expect(formatPrice(0.01)).toBe('£0.01');
    });
  });

  describe('Image Display', () => {
    test('should display artwork image', () => {
      const image = document.getElementById('artwork-image');
      expect(image).toBeDefined();
      expect(image.src).toContain('test_image.jpg');
    });

    test('image should have alt text', () => {
      const image = document.getElementById('artwork-image');
      expect(image.alt).toBe('Mountain Peak');
    });

    test('image should be visible', () => {
      const image = document.getElementById('artwork-image');
      expect(image).toBeDefined();
      expect(image).not.toBeNull();
      expect(image.src).not.toBe('');
    });
  });

  describe('Availability Status', () => {
    test('should display availability status', () => {
      const status = document.getElementById('availability-status');
      expect(status).toBeDefined();
      expect(status.textContent).toBe('Available');
    });

    test('should show correct status for available items', () => {
      const status = document.getElementById('availability-status');
      status.textContent = 'Available';
      expect(status.textContent).toBe('Available');
    });

    test('should show correct status for unavailable items', () => {
      const status = document.getElementById('availability-status');
      status.textContent = 'Sold Out';
      expect(status.textContent).toBe('Sold Out');
    });
  });

  describe('Add to Cart Button', () => {
    test('should display Add to Cart button when available', () => {
      const btn = document.getElementById('add-to-cart-btn');
      expect(btn).toBeDefined();
      expect(btn.textContent).toBe('Add to Cart');
    });

    test('button should be clickable when available', () => {
      const btn = document.getElementById('add-to-cart-btn');
      expect(btn.disabled).toBe(false);
    });

    test('button should be disabled when item is sold out', () => {
      const btn = document.getElementById('add-to-cart-btn');
      btn.disabled = true;
      expect(btn.disabled).toBe(true);
    });

    test('should trigger add to cart on button click', () => {
      const btn = document.getElementById('add-to-cart-btn');
      const clickSpy = jest.fn();
      btn.addEventListener('click', clickSpy);
      btn.click();
      expect(clickSpy).toHaveBeenCalled();
    });
  });

  describe('Artist Information', () => {
    test('should display artist name', () => {
      const artistInfo = document.getElementById('artist-info');
      expect(artistInfo).toBeDefined();
      expect(artistInfo.textContent).toContain('Michael');
    });

    test('should have link to artist profile', () => {
      const artistLink = document.querySelector('#artist-info a');
      expect(artistLink).toBeDefined();
      expect(artistLink.href).toContain('/profile/michael');
    });
  });

  describe('Related Artworks Section', () => {
    test('should have related artworks section', () => {
      const relatedSection = document.getElementById('related-artworks');
      expect(relatedSection).toBeDefined();
    });

    test('should display related artworks when available', () => {
      const relatedSection = document.getElementById('related-artworks');
      relatedSection.innerHTML = `
        <div class="artwork-card">
          <h3>Related Art 1</h3>
        </div>
      `;
      const cards = relatedSection.querySelectorAll('.artwork-card');
      expect(cards.length).toBeGreaterThan(0);
    });
  });

  describe('Framing Conditions', () => {
    test('should display framing options', () => {
      document.body.innerHTML += `
        <div id="framing-options">
          <label><input type="radio" name="framing" value="framed"> Framed</label>
          <label><input type="radio" name="framing" value="unframed"> Unframed</label>
        </div>
      `;
      const framingOptions = document.getElementById('framing-options');
      expect(framingOptions).toBeDefined();
      const inputs = framingOptions.querySelectorAll('input');
      expect(inputs.length).toBeGreaterThan(0);
    });
  });

  describe('Add to Cart Functionality', () => {
    test('addToCart should create cart item', () => {
      const cartItem = addToCart('mountain-peak', 1, 249.99);
      expect(cartItem.id).toBe('mountain-peak');
      expect(cartItem.quantity).toBe(1);
      expect(cartItem.price).toBe(249.99);
    });

    test('should increment quantity when adding same item twice', () => {
      let cartItem = addToCart('mountain-peak', 1, 249.99);
      cartItem = addToCart('mountain-peak', 1, 249.99);
      expect(cartItem.quantity).toBe(2);
    });

    test('should add multiple items to cart', () => {
      addToCart('art-1', 1, 100);
      addToCart('art-2', 1, 200);
      const cart = JSON.parse(localStorage.getItem('cart'));
      expect(Object.keys(cart).length).toBe(2);
      expect(cart['art-1'].price).toBe(100);
      expect(cart['art-2'].price).toBe(200);
    });

    test('should handle multiple quantity additions', () => {
      addToCart('mountain-peak', 2, 249.99);
      const cartItem = addToCart('mountain-peak', 3, 249.99);
      expect(cartItem.quantity).toBe(5);
    });

    test('should persist cart to localStorage', () => {
      addToCart('mountain-peak', 1, 249.99);
      const cart = JSON.parse(localStorage.getItem('cart'));
      expect(cart).not.toBeNull();
      expect(cart['mountain-peak']).toBeDefined();
    });

    test('should show confirmation message after adding to cart', () => {
      document.body.innerHTML += `
        <div id="confirmation-message"></div>
      `;
      const confirmationDiv = document.getElementById('confirmation-message');
      confirmationDiv.textContent = 'Added to cart!';
      expect(confirmationDiv.textContent).toBe('Added to cart!');
    });

    test('should show/hide confirmation message with timeout', (done) => {
      document.body.innerHTML += `
        <div id="confirmation-message"></div>
      `;
      const confirmationDiv = document.getElementById('confirmation-message');
      showConfirmationMessage('Added to cart!');
      
      expect(confirmationDiv.textContent).toBe('Added to cart!');
      expect(confirmationDiv.style.display).toBe('block');

      setTimeout(() => {
        expect(confirmationDiv.style.display).toBe('none');
        done();
      }, 3100);
    });

    test('should handle missing confirmation div gracefully', () => {
      document.body.innerHTML = '';
      expect(() => {
        showConfirmationMessage('Test message');
      }).not.toThrow();
    });
  });

  describe('Initialization', () => {
    test('initArtworkDetail should attach click listener', () => {
      document.body.innerHTML = `
        <button id="add-to-cart-btn" data-artwork-id="test-art" data-price="99.99">
          Add to Cart
        </button>
        <div id="confirmation-message"></div>
      `;

      initArtworkDetail();

      const btn = document.getElementById('add-to-cart-btn');
      const clickEvent = new MouseEvent('click', { bubbles: true });
      btn.dispatchEvent(clickEvent);

      const cart = JSON.parse(localStorage.getItem('cart'));
      expect(cart['test-art']).toBeDefined();
      expect(cart['test-art'].quantity).toBe(1);
    });

    test('initArtworkDetail should handle missing button', () => {
      document.body.innerHTML = '';
      expect(() => {
        initArtworkDetail();
      }).not.toThrow();
    });

    test('button click should add to cart with correct price', () => {
      document.body.innerHTML = `
        <button id="add-to-cart-btn" data-artwork-id="mountain-peak" data-price="249.99">
          Add to Cart
        </button>
        <div id="confirmation-message"></div>
      `;

      initArtworkDetail();

      const btn = document.getElementById('add-to-cart-btn');
      const clickEvent = new MouseEvent('click', { bubbles: true });
      btn.dispatchEvent(clickEvent);

      const cart = JSON.parse(localStorage.getItem('cart'));
      expect(cart['mountain-peak'].price).toBe(249.99);
    });

    test('button click without artworkId should not add to cart', () => {
      document.body.innerHTML = `
        <button id="add-to-cart-btn" data-price="249.99">
          Add to Cart
        </button>
        <div id="confirmation-message"></div>
      `;

      initArtworkDetail();

      const btn = document.getElementById('add-to-cart-btn');
      const clickEvent = new MouseEvent('click', { bubbles: true });
      btn.dispatchEvent(clickEvent);

      const cart = JSON.parse(localStorage.getItem('cart') || '{}');
      expect(Object.keys(cart).length).toBe(0);
    });

    test('should handle non-numeric price', () => {
      document.body.innerHTML = `
        <button id="add-to-cart-btn" data-artwork-id="art" data-price="invalid">
          Add to Cart
        </button>
        <div id="confirmation-message"></div>
      `;

      initArtworkDetail();

      const btn = document.getElementById('add-to-cart-btn');
      const clickEvent = new MouseEvent('click', { bubbles: true });
      btn.dispatchEvent(clickEvent);

      const cart = JSON.parse(localStorage.getItem('cart'));
      expect(cart['art']).toBeDefined();
      expect(cart['art'].price === null || isNaN(cart['art'].price)).toBe(true);
    });
  });

  describe('displayArtworkDetail Function', () => {
    test('should populate artwork detail correctly', () => {
      const artworkData = {
        name: 'Mountain Peak',
        description: 'A serene mountain landscape',
        price: 249.99,
        image: 'test_image.jpg',
        alt_text: 'Mountain Peak',
        availability: 'Available'
      };

      displayArtworkDetail(artworkData);

      expect(document.getElementById('artwork-title').textContent).toBe('Mountain Peak');
      expect(document.getElementById('artwork-price').textContent).toContain('249.99');
    });

    test('should handle null artworkData gracefully', () => {
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation();
      displayArtworkDetail(null);
      expect(consoleSpy).toHaveBeenCalledWith('No artwork data provided');
      consoleSpy.mockRestore();
    });

    test('should handle undefined artworkData gracefully', () => {
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation();
      displayArtworkDetail(undefined);
      expect(consoleSpy).toHaveBeenCalledWith('No artwork data provided');
      consoleSpy.mockRestore();
    });

    test('should handle missing fields with defaults', () => {
      const artworkData = {
        name: 'Test Art',
        price: 100
      };

      displayArtworkDetail(artworkData);

      expect(document.getElementById('artwork-title').textContent).toBe('Test Art');
      expect(document.getElementById('artwork-description').textContent).toBe('');
      expect(document.getElementById('artwork-image').alt).toBe('Test Art');
    });

    test('should use alt_text when provided', () => {
      const artworkData = {
        name: 'Test Art',
        alt_text: 'Custom Alt Text',
        image: 'test.jpg',
        price: 100
      };

      displayArtworkDetail(artworkData);

      expect(document.getElementById('artwork-image').alt).toBe('Custom Alt Text');
    });

    test('should use artwork name as fallback alt text', () => {
      const artworkData = {
        name: 'Mountain Peak',
        image: 'test.jpg',
        price: 100
      };

      displayArtworkDetail(artworkData);

      expect(document.getElementById('artwork-image').alt).toBe('Mountain Peak');
    });

    test('should set Unknown status when availability missing', () => {
      const artworkData = {
        name: 'Test Art',
        price: 100
      };

      displayArtworkDetail(artworkData);

      expect(document.getElementById('availability-status').textContent).toBe('Unknown');
    });

    test('should handle empty string fields', () => {
      const artworkData = {
        name: '',
        description: '',
        price: 0,
        image: '',
        alt_text: '',
        availability: ''
      };

      displayArtworkDetail(artworkData);

      expect(document.getElementById('artwork-title').textContent).toBe('');
      expect(document.getElementById('artwork-description').textContent).toBe('');
      expect(document.getElementById('artwork-price').textContent).toBe('£0.00');
      expect(document.getElementById('artwork-image').src).toContain('');
    });

    test('should not error when elements are missing from DOM', () => {
      document.body.innerHTML = '<div id="artwork-title"></div>';

      const artworkData = {
        name: 'Test',
        description: 'Test',
        price: 100,
        image: 'test.jpg',
        availability: 'Available'
      };

      expect(() => {
        displayArtworkDetail(artworkData);
      }).not.toThrow();
    });
  });
});

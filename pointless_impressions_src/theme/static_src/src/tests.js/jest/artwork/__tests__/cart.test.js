/**
 * @jest-environment jsdom
 */

/**
 * Cart functionality tests for US003
 * Tests for adding artwork to cart, updating quantities, and calculating totals
 */

import { addToCart, removeFromCart, updateQuantity, getCart, calculateTotal, formatPrice } from '../../../../js/artwork_detail';

describe('Cart Functionality - US003', () => {
  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear();
    document.body.innerHTML = '';
  });

  afterEach(() => {
    localStorage.clear();
  });

  describe('addToCart', () => {
    test('should add a new artwork to cart', () => {
      const result = addToCart('artwork-1', 1, 199.99);

      expect(result).toBeDefined();
      expect(result.quantity).toBe(1);
      expect(result.price).toBe(199.99);

      const cart = JSON.parse(localStorage.getItem('cart'));
      expect(cart['artwork-1']).toBeDefined();
      expect(cart['artwork-1'].quantity).toBe(1);
    });

    test('should increment quantity when adding same artwork twice', () => {
      addToCart('artwork-1', 1, 199.99);
      const result = addToCart('artwork-1', 1, 199.99);

      expect(result.quantity).toBe(2);

      const cart = JSON.parse(localStorage.getItem('cart'));
      expect(cart['artwork-1'].quantity).toBe(2);
    });

    test('should add multiple different artworks', () => {
      addToCart('artwork-1', 1, 199.99);
      addToCart('artwork-2', 1, 249.99);

      const cart = JSON.parse(localStorage.getItem('cart'));
      expect(Object.keys(cart).length).toBe(2);
      expect(cart['artwork-1'].quantity).toBe(1);
      expect(cart['artwork-2'].quantity).toBe(1);
    });

    test('should handle quantity parameter', () => {
      const result = addToCart('artwork-1', 3, 199.99);

      expect(result.quantity).toBe(3);

      const cart = JSON.parse(localStorage.getItem('cart'));
      expect(cart['artwork-1'].quantity).toBe(3);
    });

    test('should return cart item object with correct properties', () => {
      const result = addToCart('artwork-1', 2, 149.99);

      expect(result).toHaveProperty('id');
      expect(result).toHaveProperty('quantity');
      expect(result).toHaveProperty('price');
      expect(result.id).toBe('artwork-1');
      expect(result.quantity).toBe(2);
      expect(result.price).toBe(149.99);
    });
  });

  describe('removeFromCart', () => {
    test('should remove artwork from cart', () => {
      addToCart('artwork-1', 1, 199.99);
      removeFromCart('artwork-1');

      const cart = JSON.parse(localStorage.getItem('cart'));
      expect(cart['artwork-1']).toBeUndefined();
    });

    test('should leave other items when removing one', () => {
      addToCart('artwork-1', 1, 199.99);
      addToCart('artwork-2', 1, 249.99);

      removeFromCart('artwork-1');

      const cart = JSON.parse(localStorage.getItem('cart'));
      expect(cart['artwork-1']).toBeUndefined();
      expect(cart['artwork-2']).toBeDefined();
      expect(Object.keys(cart).length).toBe(1);
    });

    test('should handle removing non-existent item gracefully', () => {
      addToCart('artwork-1', 1, 199.99);

      // Should not throw error
      expect(() => removeFromCart('artwork-999')).not.toThrow();

      const cart = JSON.parse(localStorage.getItem('cart'));
      expect(cart['artwork-1']).toBeDefined();
    });
  });

  describe('updateQuantity', () => {
    test('should update quantity of existing item', () => {
      addToCart('artwork-1', 1, 199.99);
      updateQuantity('artwork-1', 5);

      const cart = JSON.parse(localStorage.getItem('cart'));
      expect(cart['artwork-1'].quantity).toBe(5);
    });

    test('should handle quantity of 1', () => {
      addToCart('artwork-1', 5, 199.99);
      updateQuantity('artwork-1', 1);

      const cart = JSON.parse(localStorage.getItem('cart'));
      expect(cart['artwork-1'].quantity).toBe(1);
    });

    test('should handle large quantities', () => {
      addToCart('artwork-1', 1, 199.99);
      updateQuantity('artwork-1', 999);

      const cart = JSON.parse(localStorage.getItem('cart'));
      expect(cart['artwork-1'].quantity).toBe(999);
    });

    test('should return updated item', () => {
      addToCart('artwork-1', 1, 199.99);
      const result = updateQuantity('artwork-1', 3);

      expect(result.quantity).toBe(3);
    });
  });

  describe('getCart', () => {
    test('should return empty cart when nothing added', () => {
      const cart = getCart();

      expect(cart).toEqual({});
    });

    test('should return all items in cart', () => {
      addToCart('artwork-1', 1, 199.99);
      addToCart('artwork-2', 2, 249.99);

      const cart = getCart();

      expect(Object.keys(cart).length).toBe(2);
      expect(cart['artwork-1'].quantity).toBe(1);
      expect(cart['artwork-2'].quantity).toBe(2);
    });

    test('should preserve cart data across calls', () => {
      addToCart('artwork-1', 1, 199.99);

      const cart1 = getCart();
      const cart2 = getCart();

      expect(cart1).toEqual(cart2);
    });
  });

  describe('calculateTotal', () => {
    test('should calculate total for single item', () => {
      addToCart('artwork-1', 1, 199.99);

      const total = calculateTotal();

      expect(total).toBeCloseTo(199.99, 2);
    });

    test('should calculate total for multiple items', () => {
      addToCart('artwork-1', 2, 199.99);  // 199.99 * 2 = 399.98
      addToCart('artwork-2', 1, 249.99);  // 249.99 * 1 = 249.99
      // Total = 649.97

      const total = calculateTotal();

      expect(total).toBeCloseTo(649.97, 2);
    });

    test('should return 0 for empty cart', () => {
      const total = calculateTotal();

      expect(total).toBe(0);
    });

    test('should handle decimal calculations correctly', () => {
      addToCart('artwork-1', 3, 33.33);  // 99.99

      const total = calculateTotal();

      expect(total).toBeCloseTo(99.99, 2);
    });

    test('should recalculate after quantity update', () => {
      addToCart('artwork-1', 2, 199.99);
      let total = calculateTotal();
      expect(total).toBeCloseTo(399.98, 2);

      updateQuantity('artwork-1', 3);
      total = calculateTotal();
      expect(total).toBeCloseTo(599.97, 2);
    });
  });

  describe('formatPrice', () => {
    test('should format price with £ symbol', () => {
      const formatted = formatPrice(199.99);

      expect(formatted).toBe('£199.99');
    });

    test('should format whole numbers', () => {
      const formatted = formatPrice(200);

      expect(formatted).toMatch(/£200/);
    });

    test('should handle small decimal values', () => {
      const formatted = formatPrice(0.99);

      expect(formatted).toBe('£0.99');
    });

    test('should return default for non-numeric input', () => {
      const formatted = formatPrice('not a number');

      expect(formatted).toBe('£0.00');
    });

    test('should handle very large prices', () => {
      const formatted = formatPrice(9999.99);

      expect(formatted).toContain('£');
      expect(formatted).toMatch(/9,?999\.99/);
    });
  });

  describe('Cart Integration Tests', () => {
    test('complete add-to-cart workflow', () => {
      // Add item
      addToCart('sunset-001', 1, 199.99);
      let cart = getCart();
      expect(Object.keys(cart).length).toBe(1);

      // Add same item again
      addToCart('sunset-001', 1, 199.99);
      cart = getCart();
      expect(cart['sunset-001'].quantity).toBe(2);
      expect(calculateTotal()).toBeCloseTo(399.98, 2);

      // Add different item
      addToCart('ocean-001', 1, 249.99);
      cart = getCart();
      expect(Object.keys(cart).length).toBe(2);
      expect(calculateTotal()).toBeCloseTo(649.97, 2);

      // Update quantity
      updateQuantity('ocean-001', 2);
      expect(calculateTotal()).toBeCloseTo(899.96, 2);

      // Remove item
      removeFromCart('sunset-001');
      cart = getCart();
      expect(Object.keys(cart).length).toBe(1);
      expect(calculateTotal()).toBeCloseTo(499.98, 2);
    });

    test('should persist cart in localStorage', () => {
      addToCart('artwork-1', 2, 199.99);

      // Simulate page reload by clearing in-memory state
      const storedCart = JSON.parse(localStorage.getItem('cart'));

      expect(storedCart['artwork-1'].quantity).toBe(2);
      expect(storedCart['artwork-1'].price).toBe(199.99);
    });

    test('cart with multiple items displays correct totals', () => {
      const items = [
        { id: 'art-1', qty: 1, price: 199.99 },
        { id: 'art-2', qty: 2, price: 149.99 },
        { id: 'art-3', qty: 3, price: 99.99 },
      ];

      items.forEach(item => {
        addToCart(item.id, item.qty, item.price);
      });

      const total = calculateTotal();
      // (199.99 * 1) + (149.99 * 2) + (99.99 * 3)
      // = 199.99 + 299.98 + 299.97 = 799.94
      expect(total).toBeCloseTo(799.94, 2);
    });
  });

  describe('Edge Cases', () => {
    test('should handle zero quantity gracefully', () => {
      // Depending on implementation, this might set to 0
      // or handle it differently
      addToCart('artwork-1', 1, 199.99);
      updateQuantity('artwork-1', 0);

      const cart = JSON.parse(localStorage.getItem('cart'));
      // Verify behavior (could be removal or zero quantity)
      expect(cart['artwork-1']).toBeDefined();
    });

    test('should handle negative prices gracefully', () => {
      // Should either reject or handle gracefully
      const result = addToCart('artwork-1', 1, -199.99);

      expect(result).toBeDefined();
      // Negative prices might be rejected in validation layer
    });

    test('should handle special characters in artwork IDs', () => {
      const id = 'artwork-with-special-@#$';
      const result = addToCart(id, 1, 199.99);

      expect(result).toBeDefined();

      const cart = getCart();
      expect(cart[id]).toBeDefined();
    });

    test('should handle very long artwork IDs', () => {
      const longId = 'a'.repeat(1000);
      const result = addToCart(longId, 1, 199.99);

      expect(result).toBeDefined();
    });
  });
});

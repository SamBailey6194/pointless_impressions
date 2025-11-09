/**
 * @jest-environment jsdom
 */

/**
 * Add to Cart Modal Tests
 * Tests for US003: Modal functionality for adding items to cart
 */

import { addToCartModal, initAddToCartModal } from '../../../../js/add_to_cart_modal.js';
import fs from 'fs';
import path from 'path';

describe('Add to Cart Modal - US003', () => {
  let modalHTML;

  beforeEach(() => {
    // Clear localStorage
    localStorage.clear();
    
    // Load modal fixture HTML
    const fixturePath = path.join(__dirname, 'fixtures', 'add_to_cart_modal.html');
    modalHTML = fs.readFileSync(fixturePath, 'utf-8');
    document.body.innerHTML = modalHTML;

    // Mock CSRF token
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    if (!csrfInput) {
      const input = document.createElement('input');
      input.type = 'hidden';
      input.name = 'csrfmiddlewaretoken';
      input.value = 'test-csrf-token';
      document.body.appendChild(input);
    }

    // Initialize modal event listeners
    initAddToCartModal();
  });

  afterEach(() => {
    document.body.innerHTML = '';
    localStorage.clear();
  });

  describe('Modal Initialization', () => {
    test('should have modal element in DOM', () => {
      const modal = document.getElementById('add_to_cart_modal');
      expect(modal).toBeDefined();
      expect(modal.tagName).toBe('DIALOG');
    });

    test('should have all required form elements', () => {
      expect(document.getElementById('add_to_cart_form')).toBeDefined();
      expect(document.getElementById('quantity')).toBeDefined();
      expect(document.getElementById('modal_artwork_id')).toBeDefined();
      expect(document.getElementById('modal_artwork_name')).toBeDefined();
      expect(document.getElementById('modal_artwork_price')).toBeDefined();
    });

    test('should have quantity control buttons', () => {
      expect(document.getElementById('qty_increase')).toBeDefined();
      expect(document.getElementById('qty_decrease')).toBeDefined();
    });

    test('should have error and success message elements', () => {
      expect(document.getElementById('form_error')).toBeDefined();
      expect(document.getElementById('form_success')).toBeDefined();
      expect(document.getElementById('error_message')).toBeDefined();
      expect(document.getElementById('success_message')).toBeDefined();
    });
  });

  describe('Modal Init Function', () => {
    test('should initialize modal with artwork data', () => {
      const framingOptions = [
        { id: 1, name: 'Framed' },
        { id: 2, name: 'Unframed' },
      ];

      addToCartModal.init('artwork-1', 'Sunset', 199.99, '/image.jpg', 5, framingOptions);

      expect(document.getElementById('modal_artwork_id').value).toBe('artwork-1');
      expect(document.getElementById('modal_artwork_name').textContent).toContain('Sunset');
      expect(document.getElementById('modal_artwork_price').textContent).toContain('£199.99');
      expect(document.getElementById('quantity').max).toBe('5');
    });

    test('should set quantity to 1 on init', () => {
      addToCartModal.init('artwork-1', 'Test', 100, '/img.jpg', 10, []);
      expect(document.getElementById('quantity').value).toBe('1');
    });

    test('should display stock info', () => {
      addToCartModal.init('artwork-1', 'Test', 100, '/img.jpg', 5, []);
      expect(document.getElementById('modal_artwork_stock').textContent).toContain('5 in stock');
      expect(document.getElementById('max_quantity_info').textContent).toContain('Max: 5');
    });

    test('should handle out of stock artwork', () => {
      addToCartModal.init('artwork-1', 'Sold Out', 100, '/img.jpg', 0, []);
      expect(document.getElementById('modal_artwork_stock').textContent).toContain('Out of stock');
    });
  });

  describe('Quantity Controls', () => {
    beforeEach(() => {
      addToCartModal.init('artwork-1', 'Test', 100, '/img.jpg', 10, []);
    });

    test('should increase quantity', () => {
      document.getElementById('qty_increase').click();
      expect(document.getElementById('quantity').value).toBe('2');
    });

    test('should decrease quantity', () => {
      document.getElementById('quantity').value = '3';
      document.getElementById('qty_decrease').click();
      expect(document.getElementById('quantity').value).toBe('2');
    });

    test('should not increase quantity beyond max', () => {
      document.getElementById('quantity').value = '10';
      document.getElementById('qty_increase').click();
      expect(document.getElementById('quantity').value).toBe('10');
    });

    test('should not decrease quantity below 1', () => {
      document.getElementById('quantity').value = '1';
      document.getElementById('qty_decrease').click();
      expect(document.getElementById('quantity').value).toBe('1');
    });

    test('should validate quantity on input', () => {
      const input = document.getElementById('quantity');
      input.value = '15'; // Over max of 10
      input.dispatchEvent(new Event('change'));
      
      const isValid = addToCartModal.validateQuantity();
      expect(isValid).toBe(false);
      expect(input.value).toBe('10'); // Should be capped
    });
  });

  describe('Framing Options', () => {
    test('should show framing section when options available', () => {
      const framingOptions = [
        { id: 1, name: 'Framed' },
        { id: 2, name: 'Unframed' },
      ];
      
      addToCartModal.init('artwork-1', 'Test', 100, '/img.jpg', 5, framingOptions);
      
      const framingSection = document.getElementById('framing_section');
      expect(framingSection.classList.contains('hidden')).toBe(false);
      
      const options = document.querySelectorAll('#framing_option option');
      expect(options.length).toBeGreaterThan(1);
    });

    test('should hide framing section when no options', () => {
      addToCartModal.init('artwork-1', 'Test', 100, '/img.jpg', 5, []);
      
      const framingSection = document.getElementById('framing_section');
      expect(framingSection.classList.contains('hidden')).toBe(true);
    });

    test('should populate framing select with options', () => {
      const framingOptions = [
        { id: 1, name: 'Framed' },
        { id: 2, name: 'Unframed' },
      ];
      
      addToCartModal.init('artwork-1', 'Test', 100, '/img.jpg', 5, framingOptions);
      
      const select = document.getElementById('framing_option');
      const optionTexts = Array.from(select.options).map(opt => opt.textContent);
      
      expect(optionTexts).toContain('Framed');
      expect(optionTexts).toContain('Unframed');
    });
  });

  describe('Notes Input', () => {
    beforeEach(() => {
      addToCartModal.init('artwork-1', 'Test', 100, '/img.jpg', 5, []);
    });

    test('should update character count on input', () => {
      const notes = document.getElementById('notes');
      const counter = document.getElementById('notes_count');
      
      notes.value = 'This is a test note';
      notes.dispatchEvent(new Event('input'));
      
      expect(counter.textContent).toBe('19/500');
    });

    test('should handle empty notes', () => {
      const notes = document.getElementById('notes');
      const counter = document.getElementById('notes_count');
      
      notes.value = '';
      notes.dispatchEvent(new Event('input'));
      
      expect(counter.textContent).toBe('0/500');
    });

    test('should enforce max length', () => {
      const notes = document.getElementById('notes');
      expect(notes.maxLength).toBe(500);
    });
  });

  describe('Error Handling', () => {
    beforeEach(() => {
      addToCartModal.init('artwork-1', 'Test', 100, '/img.jpg', 5, []);
    });

    test('should show quantity error when validation fails', () => {
      addToCartModal.showQtyError('Maximum 5 available');
      
      const error = document.getElementById('qty_error');
      expect(error.textContent).toBe('Maximum 5 available');
      expect(error.classList.contains('hidden')).toBe(false);
    });

    test('should clear quantity error', () => {
      addToCartModal.showQtyError('Test error');
      addToCartModal.clearQtyError();
      
      const error = document.getElementById('qty_error');
      expect(error.classList.contains('hidden')).toBe(true);
    });

    test('should show form error message', () => {
      addToCartModal.showError('Failed to add item');
      
      const error = document.getElementById('form_error');
      const message = document.getElementById('error_message');
      
      expect(error.classList.contains('hidden')).toBe(false);
      expect(message.textContent).toBe('Failed to add item');
    });

    test('should show form success message', () => {
      addToCartModal.showSuccess('Added successfully!');
      
      const success = document.getElementById('form_success');
      const message = document.getElementById('success_message');
      
      expect(success.classList.contains('hidden')).toBe(false);
      expect(message.textContent).toBe('Added successfully!');
    });
  });

  describe('Form Reset', () => {
    beforeEach(() => {
      addToCartModal.init('artwork-1', 'Test', 100, '/img.jpg', 5, []);
    });

    test('should reset quantity to 1', () => {
      document.getElementById('quantity').value = '5';
      addToCartModal.resetForm();
      expect(document.getElementById('quantity').value).toBe('1');
    });

    test('should clear notes', () => {
      document.getElementById('notes').value = 'Some note';
      addToCartModal.resetForm();
      expect(document.getElementById('notes').value).toBe('');
    });

    test('should reset notes counter', () => {
      addToCartModal.resetForm();
      expect(document.getElementById('notes_count').textContent).toBe('0/500');
    });

    test('should hide error and success messages', () => {
      addToCartModal.showError('Test');
      addToCartModal.showSuccess('Test');
      
      addToCartModal.resetForm();
      
      expect(document.getElementById('form_error').classList.contains('hidden')).toBe(true);
      expect(document.getElementById('form_success').classList.contains('hidden')).toBe(true);
    });
  });

  describe('Modal Accessibility', () => {
    test('should have form elements with proper labels', () => {
      const quantityLabel = document.querySelector('label span.label-text');
      expect(quantityLabel).toBeDefined();
      expect(quantityLabel.textContent).toContain('Quantity');
    });

    test('quantity input should have min and max attributes', () => {
      const input = document.getElementById('quantity');
      expect(input.min).toBe('1');
      expect(input.max).toBeDefined();
    });

    test('should have accessible buttons', () => {
      expect(document.getElementById('qty_increase')).toBeDefined();
      expect(document.getElementById('qty_decrease')).toBeDefined();
      expect(document.getElementById('cancel_btn')).toBeDefined();
      expect(document.getElementById('submit_btn')).toBeDefined();
    });
  });

  describe('Integration Tests', () => {
    test('complete modal workflow', () => {
      // Initialize modal
      addToCartModal.init('artwork-1', 'Sunset', 199.99, '/img.jpg', 5, []);
      
      // Increase quantity
      document.getElementById('qty_increase').click();
      expect(document.getElementById('quantity').value).toBe('2');
      
      // Add notes
      document.getElementById('notes').value = 'Frame it beautifully';
      expect(document.getElementById('notes_count').textContent).toContain('22/500');
      
      // Verify form data before submission
      const form = document.getElementById('add_to_cart_form');
      expect(form).toBeDefined();
      expect(document.getElementById('modal_artwork_id').value).toBe('artwork-1');
    });

    test('should reset form after operations', () => {
      addToCartModal.init('artwork-1', 'Test', 100, '/img.jpg', 5, []);
      
      // Modify form
      document.getElementById('quantity').value = '3';
      document.getElementById('notes').value = 'Test note';
      
      // Reset
      addToCartModal.resetForm();
      
      // Verify reset
      expect(document.getElementById('quantity').value).toBe('1');
      expect(document.getElementById('notes').value).toBe('');
    });
  });
});

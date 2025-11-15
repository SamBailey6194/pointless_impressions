/**
 * @jest-environment jsdom
 */

import {
  handleQuantityButtons,
  submitAddToCartForm,
  initAddToCartPage,
} from '../../../../js/add_to_cart';
import { getCsrfToken } from '../../../../js/cart';
import fs from 'fs';
import path from 'path';

jest.mock('../../../../js/cart.js', () => ({
  getCsrfToken: jest.fn(),
}));

describe('Add to Cart Form', () => {
  let formHTML;
  let consoleSpy;

  // --- Setup & Teardown ---

  beforeAll(() => {
    const fixturePath = path.join(__dirname, 'fixtures', 'add_to_cart_form.html');
    try {
      formHTML = fs.readFileSync(fixturePath, 'utf-8');
    } catch (err) {
      console.error("Could not read fixture file. Make sure it exists:", fixturePath);
      throw err;
    }
  });

  beforeEach(() => {
    document.body.innerHTML = formHTML;

    jest.clearAllMocks();

    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ success: true, message: 'Added to cart' }),
      })
    );

    window.Toast = {
      show: jest.fn(),
    };
    window.cart = {
      updateCartDropdownHTML: jest.fn().mockResolvedValue(),
      openCartDropdown: jest.fn(),
    };
    window.scrollTo = jest.fn();

    getCsrfToken.mockReturnValue('test-csrf-token');
    consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterEach(() => {
    consoleSpy.mockRestore();
    document.body.innerHTML = '';
  });

  // --- Test Suites ---

  describe('handleQuantityButtons', () => {
    let quantityInput, incrementButton, decrementButton, stockInput;

    beforeEach(() => {
      quantityInput = document.getElementById('id_quantity');
      incrementButton = document.getElementById('increment-quantity');
      decrementButton = document.getElementById('decrement-quantity');
      stockInput = document.getElementById('stock_quantity');
    });

    test('should increase quantity on increment click', () => {
      handleQuantityButtons();
      incrementButton.click();
      expect(quantityInput.value).toBe('2');
    });

    test('should decrease quantity on decrement click', () => {
      quantityInput.value = '3';
      handleQuantityButtons();
      decrementButton.click();
      expect(quantityInput.value).toBe('2');
    });

    test('should not decrease quantity below 1', () => {
      quantityInput.value = '1';
      decrementButton.click();
      expect(quantityInput.value).toBe('1');
    });

    test('should not increase quantity above stock (5)', () => {
      stockInput.value = '5';
      quantityInput.value = '5';

      handleQuantityButtons(); 
      
      incrementButton.click();
      expect(quantityInput.value).toBe('5');
    });

    test('should disable increment button if stock is reached', () => {
      handleQuantityButtons();
      quantityInput.value = '4';
      incrementButton.click();
      expect(quantityInput.value).toBe('5');
      expect(incrementButton.disabled).toBe(true);
    });
    
    test('should disable increment button on init if quantity >= stock', () => {
      quantityInput.value = '5';
      stockInput.value = '5';
      handleQuantityButtons();
      expect(incrementButton.disabled).toBe(true);
    });

    test('should enable increment button if quantity is lowered', () => {
      quantityInput.value = '5';
      handleQuantityButtons();
      expect(incrementButton.disabled).toBe(true);
      
      decrementButton.click();
      expect(quantityInput.value).toBe('4');
      expect(incrementButton.disabled).toBe(false);
    });
  });

  describe('submitAddToCartForm (async)', () => {
    let form;
    beforeEach(() => {
      form = document.getElementById('add_to_cart_form');
    });

    test('should handle successful submission', async () => {
      await submitAddToCartForm(form);

      expect(global.fetch).toHaveBeenCalledWith(form.action, expect.any(Object));
      const fetchOptions = global.fetch.mock.calls[0][1];
      expect(fetchOptions.method).toBe('POST');
      expect(fetchOptions.headers['X-CSRFToken']).toBe('test-csrf-token');
      expect(fetchOptions.body).toBeInstanceOf(FormData);

      expect(window.Toast.show).toHaveBeenCalledWith('Added to cart', 'success');
      expect(window.cart.updateCartDropdownHTML).toHaveBeenCalled();
      expect(window.cart.openCartDropdown).toHaveBeenCalled();
      expect(window.scrollTo).toHaveBeenCalledWith({ top: 0, behavior: 'smooth' });
    });

    test('should handle server-side error (data.success: false)', async () => {
      global.fetch.mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ success: false, errors: { quantity: ['Not enough stock'] } }),
      });

      await submitAddToCartForm(form);

      expect(window.Toast.show).toHaveBeenCalledWith('Not enough stock', 'error');
      expect(console.error).toHaveBeenCalledWith("Failed to add item to cart:", { quantity: ['Not enough stock'] });

      expect(window.cart.updateCartDropdownHTML).not.toHaveBeenCalled();
    });

    test('should handle network fetch error', async () => {
      const networkError = new Error('Network failed');
      global.fetch.mockRejectedValue(networkError);

      await submitAddToCartForm(form);

      expect(console.error).toHaveBeenCalledWith("Error submitting AddToCart form:", networkError);
      expect(window.Toast.show).toHaveBeenCalledWith('An unexpected error occurred.', 'error');

      expect(window.cart.updateCartDropdownHTML).not.toHaveBeenCalled();
    });
  });

  describe('initAddToCartPage (Integration)', () => {
    
    test('should correctly initialize quantity buttons', () => {
      initAddToCartPage();

      const quantityInput = document.getElementById('id_quantity');
      const incrementButton = document.getElementById('increment-quantity');
      
      incrementButton.click();

      expect(quantityInput.value).toBe('2'); 
    });

    test('should correctly initialize form submit listener', async () => {
      initAddToCartPage();

      const form = document.getElementById('add_to_cart_form');

      const event = new Event('submit');
      form.dispatchEvent(event);

      await new Promise(resolve => setTimeout(resolve));

      expect(global.fetch).toHaveBeenCalled(); 
      expect(window.Toast.show).toHaveBeenCalledWith('Added to cart', 'success');
    });
  });
});
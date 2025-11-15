/**
 * Cypress E2E Tests for US003: Add Artwork to Cart
 * Tests the complete user flow of adding artwork to cart with a server-side (session) cart.
 *
 * Test Data Created by: create_test_artworks.py
 * - Sunset: £199.99, Available, Quantity: 5
 * - Starry Night: £249.99, Sold Out, Quantity: 0
 */

describe('US003: Add Artwork to Cart - E2E Tests', () => {
  beforeEach(() => {
    cy.clearAllCookies();
    cy.clearAllLocalStorage();
    cy.clearAllSessionStorage();

    cy.intercept('POST', '/artworks/**').as('addToCart');
    cy.intercept('GET', '/checkout/cart-dropdown/').as('updateCartDropdown');
    cy.intercept('POST', '/checkout/update/').as('updateCartPage');
    cy.intercept('POST', '/checkout/remove/**').as('removeFromCart');

    cy.visit('/');
  });

  describe('Add to Cart Button', () => {
    it('should display Add to Cart button on available artwork detail page', () => {
      cy.visit('/artworks/sunset/');

      cy.get('#add_to_cart_form button[type="submit"]')
        .should('be.visible')
        .should('not.be.disabled');
    });

    it('should show a notice for sold-out artwork', () => {
      cy.visit('/artworks/starry-night/');

      cy.contains(/sold out|out of stock|unavailable/i).should('be.visible');
      cy.get('#add_to_cart_form').should('not.exist');
    });
  });

  describe('Adding Single Artwork', () => {
    it('should add artwork to cart and show toast notification', () => {
      cy.visit('/artworks/sunset/');
      cy.get('h1').should('contain', 'Sunset');

      cy.get('#add_to_cart_form button[type="submit"]').click();

      cy.wait('@addToCart', { timeout: 15000 });

      cy.get('#toast-container', { timeout: 10000 })
        .should('be.visible')
        .should('contain.text', 'cart');

      cy.wait('@updateCartDropdown', { timeout: 10000 });
    });
  });

  describe('Accessibility', () => {
    it('should be keyboard navigable', () => {
      cy.visit('/artworks/sunset/');

      cy.get('#add_to_cart_form button[type="submit"]')
        .focus()
        .type('{enter}');

      cy.wait('@addToCart', { timeout: 15000 });

      cy.get('#toast-container', { timeout: 10000 })
        .should('be.visible')
        .should('contain.text', 'cart');

      cy.wait('@updateCartDropdown', { timeout: 10000 });
    });
  });
});
/**
 * Cypress E2E Tests for US003: Add Artwork to Cart
 * Tests the complete user flow of adding artwork to cart and checking out
 *
 * Test Data Created by: create_test_artworks.py
 * - Sunset: £199.99, Available, Quantity: 5
 * - Starry Night: £249.99, Sold Out, Quantity: 0
 */

describe('US003: Add Artwork to Cart - E2E Tests', () => {
  beforeEach(() => {
    // Clear localStorage before each test
    cy.clearLocalStorage('cart');
    // Test data is already set up by dev.sh cypress:reset
    cy.visit('/');
  });

  describe('Add to Cart Button', () => {
    it('should display Add to Cart button on available artwork detail page', () => {
      // Navigate to Sunset artwork (available)
      cy.visit('/artworks/sunset/');
      
      // Verify Add to Cart button exists and is enabled
      cy.get('button.add-to-cart, [data-testid="add-to-cart-btn"]')
        .should('be.visible')
        .should('not.be.disabled');
    });

    it('should not display Add to Cart for sold-out artwork', () => {
      // Navigate to Starry Night artwork (sold out)
      cy.visit('/artworks/starry-night/');
      
      // Verify Add to Cart button is disabled or not visible
      cy.get('button.add-to-cart, [data-testid="add-to-cart-btn"]')
        .should('be.disabled');
    });
  });

  describe('Adding Single Artwork', () => {
    it('should add artwork to cart when clicking Add to Cart', () => {
      // Navigate to Sunset artwork detail page
      cy.visit('/artworks/sunset/');
      
      // Verify artwork data exists
      cy.get('[data-artwork-id], h1').should('be.visible');
      
      // Click Add to Cart
      cy.get('button.add-to-cart, [data-testid="add-to-cart-btn"]')
        .click();
      
      // Verify success message or confirmation
      cy.get('.success-message, .toast-message, [role="alert"]')
        .should('be.visible')
        .should('contain', 'Added to cart');
    });

    it('should update cart count after adding artwork', () => {
      // Navigate to Sunset artwork
      cy.visit('/artworks/sunset/');
      
      // Check initial cart count (should be 0 or empty)
      cy.get('[data-testid="cart-count"], .cart-count').then($count => {
        const initialCount = parseInt($count.text() || 0);
        
        // Add to cart
        cy.get('button.add-to-cart, [data-testid="add-to-cart-btn"]')
          .click();
        
        // Verify count increased
        cy.get('[data-testid="cart-count"], .cart-count')
          .should('contain', initialCount + 1);
      });
    });

    it('should persist artwork in cart after navigation', () => {
      // Add Sunset to cart
      cy.visit('/artworks/sunset/');
      cy.get('button.add-to-cart, [data-testid="add-to-cart-btn"]')
        .click();
      
      // Navigate away to home
      cy.visit('/');
      
      // Navigate back to cart
      cy.get('[href="/cart/"], .cart-link, [data-testid="cart-link"]')
        .click();
      
      // Verify Sunset artwork is still in cart
      cy.get('.cart-item').should('contain', 'Sunset');
    });
  });

  describe('Adding Multiple Artworks', () => {
    it('should increment quantity when adding same artwork twice', () => {
      // Navigate to Sunset artwork
      cy.visit('/artworks/sunset/');
      
      // Add to cart first time
      cy.get('button.add-to-cart, [data-testid="add-to-cart-btn"]')
        .click();
      
      cy.wait(500); // Wait for processing
      
      // Add to cart second time
      cy.get('button.add-to-cart, [data-testid="add-to-cart-btn"]')
        .click();
      
      // Navigate to cart
      cy.get('[href="/cart/"], .cart-link, [data-testid="cart-link"]')
        .click();
      
      // Verify quantity is 2 for Sunset
      cy.get('.cart-item').should('contain', 'Sunset');
      cy.get('.cart-item .item-quantity')
        .should('contain', 2);
    });
  });

  describe('Cart Display', () => {
    it('should display cart page with item details', () => {
      // Add Sunset artwork to cart
      cy.visit('/artworks/sunset/');
      cy.get('button.add-to-cart, [data-testid="add-to-cart-btn"]')
        .click();
      
      // Navigate to cart
      cy.get('[href="/cart/"], .cart-link, [data-testid="cart-link"]')
        .click();
      
      // Verify cart page elements
      cy.get('.cart-item')
        .should('have.length', 1)
        .should('contain', 'Sunset');
      
      // Verify item has name and price displayed
      cy.get('.cart-item .item-name').should('contain', 'Sunset');
      cy.get('.cart-item .item-price').should('contain', '199.99');
    });

    it('should display correct total price for Sunset (£199.99)', () => {
      // Add Sunset to cart
      cy.visit('/artworks/sunset/');
      cy.get('button.add-to-cart, [data-testid="add-to-cart-btn"]')
        .click();
      
      // Navigate to cart
      cy.get('[href="/cart/"], .cart-link, [data-testid="cart-link"]')
        .click();
      
      // Verify total matches Sunset's price
      cy.get('.cart-total-amount, [data-testid="cart-total"]')
        .should('contain', '199.99');
    });
  });

  describe('Cart Operations', () => {
    it('should remove artwork from cart', () => {
      // Add Sunset to cart
      cy.visit('/artworks/sunset/');
      cy.get('button.add-to-cart, [data-testid="add-to-cart-btn"]')
        .click();
      
      // Navigate to cart
      cy.get('[href="/cart/"], .cart-link, [data-testid="cart-link"]')
        .click();
      
      // Verify item in cart
      cy.get('.cart-item').should('have.length', 1);
      
      // Remove item
      cy.get('button.remove-item, [data-testid="remove-btn"]')
        .first()
        .click();
      
      // Verify item removed
      cy.get('.cart-item').should('have.length', 0);
      cy.get('.empty-cart, [class*="empty"]')
        .should('be.visible');
    });

    it('should update quantity from cart page', () => {
      // Add Sunset to cart
      cy.visit('/artworks/sunset/');
      cy.get('button.add-to-cart, [data-testid="add-to-cart-btn"]')
        .click();
      
      // Navigate to cart
      cy.get('[href="/cart/"], .cart-link, [data-testid="cart-link"]')
        .click();
      
      // Update quantity to 3
      cy.get('.item-quantity input, [data-testid="quantity-input"]')
        .first()
        .clear()
        .type('3');
      
      cy.get('button[type="submit"], [data-testid="update-cart"]')
        .click();
      
      // Verify quantity updated
      cy.get('.item-quantity input, [data-testid="quantity-input"]')
        .first()
        .should('have.value', '3');
    });

    it('should not allow quantity exceeding stock (Sunset has 5)', () => {
      // Add Sunset to cart (has 5 in stock)
      cy.visit('/artworks/sunset/');
      cy.get('button.add-to-cart, [data-testid="add-to-cart-btn"]')
        .click();
      
      // Navigate to cart
      cy.get('[href="/cart/"], .cart-link, [data-testid="cart-link"]')
        .click();
      
      // Try to set quantity above stock (e.g., 10)
      cy.get('.item-quantity input, [data-testid="quantity-input"]')
        .first()
        .clear()
        .type('10');
      
      cy.get('button[type="submit"], [data-testid="update-cart"]')
        .click();
      
      // Verify error message or quantity capped at 5
      cy.get('.error-message, [role="alert"]')
        .should('be.visible')
        .should('match', /insufficient|stock|limited/i);
    });
  });

  describe('Price Calculations', () => {
    it('should calculate correct total with Sunset (£199.99)', () => {
      // Add Sunset (£199.99) to cart
      cy.visit('/artworks/sunset/');
      cy.get('button.add-to-cart, [data-testid="add-to-cart-btn"]')
        .click();
      
      // Navigate to cart
      cy.get('[href="/cart/"], .cart-link, [data-testid="cart-link"]')
        .click();
      
      // Verify total is correct for 1 item
      cy.get('.cart-total-amount, [data-testid="cart-total"]')
        .should('contain', '199.99');
    });

    it('should update total when quantity changes (199.99 × 3 = 599.97)', () => {
      // Add Sunset (£199.99)
      cy.visit('/artworks/sunset/');
      cy.get('button.add-to-cart, [data-testid="add-to-cart-btn"]')
        .click();
      
      // Go to cart
      cy.get('[href="/cart/"], .cart-link, [data-testid="cart-link"]')
        .click();
      
      // Verify initial total
      cy.get('.cart-total-amount, [data-testid="cart-total"]')
        .should('contain', '199.99');
      
      // Update quantity to 3
      cy.get('.item-quantity input, [data-testid="quantity-input"]')
        .first()
        .clear()
        .type('3');
      
      cy.get('button[type="submit"], [data-testid="update-cart"]')
        .click();
      
      // Verify new total: 199.99 × 3 = 599.97
      cy.get('.cart-total-amount, [data-testid="cart-total"]')
        .should('contain', '599.97');
    });
  });

  describe('Cart Persistence', () => {
    it('should persist cart on page refresh', () => {
      // Add artwork
      cy.visit('/artworks/');
      cy.get('.artwork-card').first().click();
      cy.get('button.add-to-cart, [data-testid="add-to-cart-btn"]')
        .click();
      
      // Refresh page
      cy.reload();
      
      // Verify cart still has item
      cy.get('[href="/cart/"], .cart-link, [data-testid="cart-link"]')
        .click();
      
      cy.get('.cart-item').should('have.length', 1);
    });

    it('should clear cart when user clicks clear button', () => {
      // Add artwork
      cy.visit('/artworks/');
      cy.get('.artwork-card').first().click();
      cy.get('button.add-to-cart, [data-testid="add-to-cart-btn"]')
        .click();
      
      // Go to cart
      cy.get('[href="/cart/"], .cart-link, [data-testid="cart-link"]')
        .click();
      
      // Click clear cart button if it exists
      cy.get('button.clear-cart, [data-testid="clear-cart-btn"]')
        .click();
      
      // Verify cart is empty
      cy.get('.empty-cart, [class*="empty"]')
        .should('be.visible');
    });
  });

  describe('Error Handling', () => {
    it('should prevent adding sold-out artwork (Starry Night)', () => {
      // Navigate to sold-out artwork
      cy.visit('/artworks/starry-night/');
      
      // Verify Add to Cart button is disabled
      cy.get('button.add-to-cart, [data-testid="add-to-cart-btn"]')
        .should('be.disabled');
      
      // Verify error message about stock
      cy.get('.error-message, .stock-error, [data-testid="stock-error"], .sold-out-notice')
        .should('be.visible')
        .should('match', /sold.*out|out.*of.*stock|unavailable/i);
    });

    it('should prevent exceeding available stock (Sunset has max 5)', () => {
      // Add Sunset to cart
      cy.visit('/artworks/sunset/');
      cy.get('button.add-to-cart, [data-testid="add-to-cart-btn"]')
        .click();
      
      // Navigate to cart
      cy.get('[href="/cart/"], .cart-link, [data-testid="cart-link"]')
        .click();
      
      // Try to increase quantity beyond available (5)
      cy.get('.item-quantity input, [data-testid="quantity-input"]')
        .first()
        .clear()
        .type('10');
      
      cy.get('button[type="submit"], [data-testid="update-cart"]')
        .click();
      
      // Verify error displayed and quantity capped at 5
      cy.get('.error-message, [role="alert"]')
        .should('be.visible')
        .should('match', /insufficient|stock|limited|maximum/i);
    });

    it('should show validation error for invalid quantity', () => {
      // Add Sunset
      cy.visit('/artworks/sunset/');
      cy.get('button.add-to-cart, [data-testid="add-to-cart-btn"]')
        .click();
      
      // Go to cart
      cy.get('[href="/cart/"], .cart-link, [data-testid="cart-link"]')
        .click();
      
      // Enter invalid quantity (0 or negative)
      cy.get('.item-quantity input, [data-testid="quantity-input"]')
        .first()
        .clear()
        .type('0');
      
      cy.get('button[type="submit"], [data-testid="update-cart"]')
        .click();
      
      // Verify validation error
      cy.get('.error-message, [role="alert"]')
        .should('be.visible')
        .should('match', /invalid|must be|minimum|at least/i);
    });

    it('should handle network errors gracefully', () => {
      cy.intercept('POST', '/api/cart/*', {
        statusCode: 500,
        body: { error: 'Server error' }
      }).as('cartError');
      
      cy.visit('/artworks/sunset/');
      cy.get('button.add-to-cart, [data-testid="add-to-cart-btn"]')
        .click();
      
      cy.wait('@cartError', { timeout: 5000 }).then(() => {
        // Verify error message displayed
        cy.get('.error-message, [role="alert"]')
          .should('be.visible');
      });
    });
  });

  describe('Accessibility', () => {
    it('should have accessible cart button', () => {
      cy.visit('/artworks/');
      cy.get('.artwork-card').first().click();
      
      // Check if button has aria-label or title attribute
      cy.get('button.add-to-cart, [data-testid="add-to-cart-btn"]')
        .should((btn) => {
          const hasAriaLabel = btn.attr('aria-label');
          const hasTitle = btn.attr('title');
          expect(hasAriaLabel || hasTitle).to.exist;
        });
    });

    it('should be keyboard navigable', () => {
      cy.visit('/artworks/');
      cy.get('.artwork-card').first().click();
      
      // Focus the Add to Cart button using keyboard
      cy.get('button.add-to-cart, [data-testid="add-to-cart-btn"]')
        .focus()
        .type('{enter}');
      
      // Verify action executed
      cy.get('.success-message, .toast-message, [role="alert"]')
        .should('be.visible');
    });
  });
});

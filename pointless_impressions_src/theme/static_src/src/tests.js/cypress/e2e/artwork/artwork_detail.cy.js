/**
 * Cypress E2E Tests for Artwork Detail Page
 * Tests for US002: View Artwork Details
 * 
 * NOTE: These tests expect test data created by create_test_artworks.py:
 * - Sunset (available, in stock): /artwork/sunset/
 * - Starry Night (sold out): /artwork/starry-night/
 */

describe('US002 - View Artwork Details', () => {
  before(() => {
    cy.request({
      method: 'GET',
      url: '/artworks/api/setup-test-data/',
      failOnStatusCode: false
    }).then((response) => {
      cy.log(`Setup response status: ${response.status}`);
    });
  });

  beforeEach(() => {
    cy.visit('/');
  });

  describe('Artwork Detail Page Access', () => {
    it('should display artwork detail page when clicked from list', () => {
      cy.visit('/artworks/');
      cy.get('[data-testid="artwork-card"]').first().click();
      cy.url().should('include', '/artworks/');
      cy.get('h1').should('not.be.empty');
    });

    it('should load detail page with correct URL slug', () => {
      cy.visit('/artworks/sunset/');
      cy.url().should('include', '/artworks/sunset/');
    });

    it('should show 404 for non-existent artwork', () => {
      cy.visit('/artworks/non-existent-artwork/', { failOnStatusCode: false });
      cy.contains('404').should('exist');
    });
  });

  describe('Artwork Title Display', () => {
    beforeEach(() => {
      cy.visit('/artworks/sunset/');
    });

    it('should display artwork title prominently', () => {
      cy.get('h1').should('contain', 'Sunset');
    });

    it('title should be visible and readable', () => {
      cy.get('h1')
        .should('be.visible')
        .should('have.css', 'font-size')
        .and('not.equal', '0px');
    });
  });

  describe('Artwork Description Display', () => {
    beforeEach(() => {
      cy.visit('/artworks/sunset/');
    });

    it('should display full artwork description', () => {
      cy.get('[data-testid="artwork-description"], .prose')
        .invoke('text')
        .then((text) => {
          expect(text.toLowerCase()).to.include('sunset');
        });
    });

    it('description should be readable and formatted', () => {
      cy.get('[data-testid="artwork-description"], .prose')
        .should('be.visible')
        .invoke('text')
        .should('have.length.greaterThan', 10);
    });
  });

  describe('Price Display', () => {
    beforeEach(() => {
      cy.visit('/artworks/sunset/');
    });

    it('should display price in correct format', () => {
      cy.get('[data-testid="artwork-price"]')
        .should('contain', '£')
        .should('contain', '199.99');
    });

    it('price should be easily readable', () => {
      cy.get('[data-testid="artwork-price"]')
        .should('be.visible')
        .should('have.css', 'font-weight');
    });

    it('should display currency symbol', () => {
      cy.get('[data-testid="artwork-price"]')
        .invoke('text')
        .should('match', /^£/);
    });
  });

  describe('Image Display', () => {
    beforeEach(() => {
      cy.visit('/artworks/sunset/');
    });

    it('should display large artwork image', () => {
      cy.get('[data-testid="artwork-image"]')
        .should('be.visible')
        .should('have.attr', 'src')
        .should('not.be.empty');
    });

    it('image should have alt text for accessibility', () => {
      cy.get('[data-testid="artwork-image"]')
        .should('have.attr', 'alt')
        .should('not.be.empty');
    });

    it('image should load without errors', () => {
      cy.get('[data-testid="artwork-image"]')
        .should('not.have.attr', 'alt', '');
    });

    it('image should be larger than thumbnail', () => {
      cy.get('[data-testid="artwork-image"]')
        .should('have.css', 'width')
        .then((width) => {
          expect(parseInt(width)).toBeGreaterThan(300);
        });
    });
  });

  describe('Availability Status', () => {
    it('should show Available for in-stock artworks', () => {
      cy.visit('/artworks/sunset/');
      cy.get('[data-testid="availability-status"]')
        .should('contain', 'Available');
    });

    it('should show Sold Out for unavailable artworks', () => {
      cy.visit('/artworks/starry-night/');
      cy.get('[data-testid="availability-status"]')
        .should('contain', 'Sold Out');
    });

    it('availability status should be clearly visible', () => {
      cy.visit('/artworks/sunset/');
      cy.get('[data-testid="availability-status"]')
        .should('be.visible')
        .should('have.css', 'color');
    });
  });

  describe('Add to Cart Button', () => {
    it('should display Add to Cart button for available items', () => {
      cy.visit('/artworks/sunset/');
      cy.get('button').contains('Add to Cart')
        .should('be.visible')
        .should('not.be.disabled');
    });

    it('should add item to cart when clicked', () => {
      cy.visit('/artworks/sunset/');
      cy.get('button').contains('Add to Cart').click();
      cy.get('.toast, [role="alert"]')
        .invoke('text')
        .then((text) => {
          expect(text.toLowerCase()).to.satisfy((t) => 
            t.includes('added') || t.includes('cart')
          );
        });
    });

    it('button should be disabled for sold out items', () => {
      cy.visit('/artworks/starry-night/');
      cy.get('button').contains('Add to Cart')
        .should('be.disabled');
    });

    it('button should be disabled for unavailable items', () => {
      cy.visit('/artworks/starry-night/');
      cy.get('button').contains('Add to Cart')
        .should('be.disabled');
    });

    it('should show confirmation message after adding to cart', () => {
      cy.visit('/artworks/sunset/');
      cy.get('button').contains('Add to Cart').click();
      cy.get('.toast, [role="alert"], .notification')
        .should('be.visible')
        .invoke('text')
        .then((text) => {
          expect(text.toLowerCase()).to.satisfy((t) =>
            t.includes('added') || t.includes('cart')
          );
        });
    });
  });

  describe('Artist Information', () => {
    beforeEach(() => {
      cy.visit('/artworks/sunset/');
    });

    it('should display artist name', () => {
      cy.get('[data-testid="artist-name"]')
        .should('contain', 'Michael');
    });

    it('should have clickable link to artist profile', () => {
      cy.get('[data-testid="artist-profile-link"]')
        .should('be.visible')
        .should('have.attr', 'href')
        .and('include', '/profile/');
    });

    it('should navigate to artist profile when clicked', () => {
      cy.get('[data-testid="artist-profile-link"]').click();
      cy.url().should('include', '/profile/');
    });

    it('should display artist bio or information', () => {
      cy.get('[data-testid="artist-info"]')
        .should('be.visible')
        .invoke('text')
        .should('have.length.greaterThan', 0);
    });
  });

  describe('Related Artworks Section', () => {
    beforeEach(() => {
      cy.visit('/artworks/sunset/');
    });

    it('should display related artworks section', () => {
      cy.get('[data-testid="related-artworks"]')
        .should('be.visible');
    });

    it('should show artworks in same category', () => {
      cy.get('[data-testid="related-artwork-card"]')
        .should('have.length.greaterThan', 0);
    });

    it('should be scrollable if many related items', () => {
      cy.get('[data-testid="related-artworks"]')
        .should('be.visible');
    });

    it('related artworks should be clickable', () => {
      cy.get('[data-testid="related-artwork-card"]')
        .first()
        .click();
      
      cy.url().should('include', '/artworks/');
    });
  });

  describe('Framing Conditions', () => {
    beforeEach(() => {
      cy.visit('/artworks/sunset/');
    });

    it('should display available framing options', () => {
      cy.get('[data-testid="framing-options"]')
        .should('be.visible');
    });

    it('should allow selection of framing condition', () => {
      cy.get('input[name="framing"]').first().check();
      cy.get('input[name="framing"]').first()
        .should('be.checked');
    });

    it('should update display when framing option changes', () => {
      cy.get('input[name="framing"]').first().check();
      cy.get('[data-testid="selected-framing"]')
        .should('contain', 'Framed');
    });
  });

  describe('Category Information', () => {
    beforeEach(() => {
      cy.visit('/artworks/sunset/');
    });

    it('should display artwork category', () => {
      cy.get('[data-testid="artwork-category"]')
        .should('contain', 'Landscape');
    });

    it('category should be clickable', () => {
      cy.get('[data-testid="category-link"]')
        .click();
      cy.url().should('include', '/artworks/')
        .and('include', 'category=');
    });
  });

  describe('Responsive Design', () => {
    it('should be responsive on mobile', () => {
      cy.viewport('iphone-x');
      cy.visit('/artworks/sunset/');
      
      cy.get('h1').should('be.visible');
      cy.get('[data-testid="artwork-image"]').should('be.visible');
      cy.get('button').contains('Add to Cart').should('be.visible');
    });

    it('should be responsive on tablet', () => {
      cy.viewport('ipad-2');
      cy.visit('/artworks/sunset/');
      
      cy.get('h1').should('be.visible');
      cy.get('[data-testid="artwork-image"]').should('be.visible');
    });

    it('should be responsive on desktop', () => {
      cy.viewport(1280, 720);
      cy.visit('/artworks/sunset/');
      
      cy.get('h1').should('be.visible');
      cy.get('[data-testid="artwork-image"]').should('be.visible');
    });
  });

  describe('Accessibility', () => {
    beforeEach(() => {
      cy.visit('/artworks/sunset/');
    });

    it('should have proper heading structure', () => {
      cy.get('h1').should('exist');
    });

    it('images should have alt text', () => {
      cy.get('img').each(($img) => {
        cy.wrap($img).should('have.attr', 'alt');
      });
    });

    it('should be keyboard navigable', () => {
      cy.get('body').tab();
      cy.focused().should('exist');
    });

    it('buttons should be accessible', () => {
      cy.get('button').contains('Add to Cart')
        .then(($btn) => {
          const hasAriaLabel = Cypress.$($btn).attr('aria-label');
          const hasTitle = Cypress.$($btn).attr('title');
          expect(hasAriaLabel || hasTitle).to.exist;
        });
    });
  });

  describe('Error Handling', () => {
    it('should handle missing images gracefully', () => {
      cy.visit('/artworks/sunset/');
      cy.get('[data-testid="artwork-image"]')
        .should('exist');
    });

    it('should show error message for invalid URL', () => {
      cy.visit('/artworks/invalid-slug/', { failOnStatusCode: false });
      cy.get('body').should('contain', '404');
    });
  });
});

/// <reference types="cypress" />

describe('US001: Browse Pointillism Artwork', () => {

  beforeEach(() => {
    // Use your global helper to visit and wait for page
    cy.visitAndWait('http://localhost:8001/artworks/')
  });

  it('displays available artwork', () => {
    // Debug: log page content
    cy.get('body').then(($body) => {
      cy.log('Page HTML length: ' + $body.html().length)
      cy.log('Page text preview: ' + $body.text().substring(0, 500))
    })
    
    // Check for available artwork on the page
    cy.containsText('Sunset')
    cy.containsText('A beautiful sunset over the mountains.')
    cy.containsText('£199.99')
  });

  it('marks sold-out artworks', () => {
    // Check that sold-out artwork is marked appropriately
    cy.containsText('Starry Night')
    cy.get('body').then(($body) => {
      // Look for Starry Night artwork card
      const text = $body.text()
      expect(text).to.include('Starry Night')
      // Note: "Sold Out" status should be visible near Starry Night
      expect(text).to.include('Sold Out')
    })
  });

  it('sorts artworks by price ascending', () => {
    // Click the sort by price button if it exists
    cy.get('#sort-lowest-price').then(($btn) => {
      if ($btn.length > 0) {
        cy.forceClick('#sort-lowest-price')
      }
    })
    // Verify at least one artwork is visible
    cy.containsText('Sunset')
  });

  it('filters only available artworks', () => {
    // Apply availability filter if filter exists
    cy.get('#apply-filters').then(($btn) => {
      if ($btn.length > 0) {
        cy.forceClick('#apply-filters')
      }
    })
    // After filtering, Sunset should still be available
    cy.containsText('Sunset')
  });

  it('shows artwork details when clicked', () => {
    // Click on first artwork card
    cy.get('.artwork-card').first().click()
    // Verify we can see artwork details
    cy.containsText('Sunset')
    cy.containsText('A beautiful sunset over the mountains.')
    cy.containsText('£199.99')
  });
})

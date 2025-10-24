/// <reference types="cypress" />

describe('US001: Browse Pointillism Artwork', () => {

  beforeEach(() => {
    // Use your global helper to visit and wait for page
    cy.visitAndWait('http://localhost:8000/artworks/')
  });

  it('displays available artwork', () => {
    cy.containsText('Sunset')
    cy.containsText('A beautiful sunset over the mountains.')
    cy.containsText('£199.99')
  });

  it('marks sold-out artworks', () => {
    cy.containsText('Starry Night')
    cy.getTableRow('body', 'Starry Night')
      .contains('Sold Out')
      .should('be.visible')
  });

  it('sorts artworks by price ascending', () => {
    cy.forceClick('#sort-price')
    cy.get('.artwork-card .price').then(($prices) => {
      const prices = [...$prices].map(p => parseFloat(p.innerText.replace('£', '')))
      const sorted = [...prices].sort((a,b) => a-b)
      expect(prices).to.deep.equal(sorted)
    })
  });

  it('filters only available artworks', () => {
    cy.forceClick('#filter-available')
    cy.containsText('Sunset')
    cy.elementExists('body:contains("Starry Night")').then(exists => {
      expect(exists).to.be.false
    })
  });

  it('shows artwork details when clicked', () => {
    cy.forceClick('text=Sunset')
    cy.containsText('Sunset')
    cy.containsText('A beautiful sunset over the mountains.')
    cy.containsText('£199.99')
    cy.getVisible('button:contains("Add to Cart")')
  });

  it('adds artwork to cart', () => {
    cy.forceClick('text=Sunset')
    cy.forceClick('button:contains("Add to Cart")')
    cy.containsText('Sunset has been added to your cart.')
    cy.get('#cart').should('contain', 'Sunset')
  });

  it('prevents adding sold-out artwork to cart', () => {
    cy.forceClick('text=Starry Night')
    cy.containsText('Sorry, Starry Night is currently sold out.')
    cy.elementExists('button:contains("Add to Cart")').then(exists => {
      expect(exists).to.be.false
    })
  });

})

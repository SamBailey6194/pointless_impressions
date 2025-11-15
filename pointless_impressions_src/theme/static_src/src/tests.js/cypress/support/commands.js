// ***********************************************
// Custom commands for your application
// ***********************************************

/**
 * Custom Cypress commands for debugging cart tests
 * Add this to cypress/support/commands.js
 */
Cypress.Commands.add('debugCartBadge', () => {
  cy.get('#cart-count-badge', { timeout: 1000 }).then($badge => {
    cy.log('Cart Badge Text:', $badge.text());
    cy.log('Cart Badge HTML:', $badge.html());
    cy.log('Cart Badge Visible:', $badge.is(':visible'));
    cy.log('Cart Badge Classes:', $badge.attr('class'));
  }).catch(() => {
    cy.log('Cart badge not found');
  });
});

Cypress.Commands.add('clearCart', () => {
  cy.clearAllCookies();
  cy.clearAllLocalStorage();
  cy.clearAllSessionStorage();

  cy.visit('/');

  cy.get('#cart-count-badge', { timeout: 5000 }).then($badge => {
    const text = $badge.text().trim();
    if (text !== '' && text !== '0') {
      cy.log('WARNING: Cart badge not empty after clearing:', text);
    }
  });
});

Cypress.Commands.add('waitForCartUpdate', () => {
  cy.wait('@addToCart', { timeout: 15000 });
  cy.wait('@updateCartDropdown', { timeout: 10000 });
  cy.wait(500);
});

// Example: Custom command to fill out a form
Cypress.Commands.add('fillContactForm', (data) => {
  cy.get('input[name="name"]').type(data.name)
  cy.get('input[name="email"]').type(data.email)
  cy.get('textarea[name="message"]').type(data.message)
})

// Example: Check if element exists without failing
Cypress.Commands.add('elementExists', (selector) => {
  return cy.get('body').then(($body) => {
    return $body.find(selector).length > 0
  })
})

// Example: Login and preserve session
Cypress.Commands.add('login', (username, password) => {
  cy.session([username, password], () => {
    cy.visit('/login/')
    cy.get('input[name="username"]').type(username)
    cy.get('input[name="password"]').type(password)
    cy.get('button[type="submit"]').click()
    cy.url().should('not.include', '/login/')
  })
})

// Example: Wait for an element to be visible and interactable
Cypress.Commands.add('getVisible', (selector, timeout = 10000) => {
  return cy.get(selector, { timeout }).should('be.visible')
})

// Example: Click element even if covered
Cypress.Commands.add('forceClick', (selector) => {
  return cy.get(selector).click({ force: true })
})
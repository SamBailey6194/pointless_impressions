// ***********************************************************
// This support file is processed and loaded automatically before
// your test files. Use it for global configuration and behavior.
// ***********************************************************

// Import Cypress commands
import './commands'

// **********************************************
// Global Configuration
// **********************************************

// Disable uncaught exception failures (optional - be careful with this)
Cypress.on('uncaught:exception', (err, runnable) => {
  if (err.message.includes('third-party-script-error')) {
    return false
  }
  // Let other exceptions fail the test
  return true
})

// **********************************************
// Global Hooks
// **********************************************

// Run before each test
beforeEach(() => {
  // Clear cookies and local storage before each test
  cy.clearCookies()
  cy.clearLocalStorage()
  
  // Preserve session/auth cookies if needed
  // Cypress.Cookies.preserveOnce('sessionid', 'csrftoken')
})

// Run before all tests in a spec file
before(() => {
  // Setup that runs once before all tests
  // Example: seed database, setup test data
})

// Run after each test
afterEach(() => {
  // Cleanup after each test
  // Example: reset database state
})

// **********************************************
// Custom Global Behaviors
// **********************************************

// Set default viewport size
Cypress.on('window:before:load', (win) => {
  // Stub console methods if you want to reduce noise in test output
  // cy.stub(win.console, 'log')
  // cy.stub(win.console, 'warn')
})

// **********************************************
// Django-Specific Configuration
// **********************************************

// Handle Django CSRF tokens
Cypress.Commands.add('getCsrfToken', () => {
  return cy.getCookie('csrftoken').then((cookie) => {
    return cookie ? cookie.value : null
  })
})

// Login helper for Django
Cypress.Commands.add('djangoLogin', (username = 'admin', password = 'admin123') => {
  cy.visit('/admin/login/')
  cy.get('input[name="username"]').type(username)
  cy.get('input[name="password"]').type(password)
  cy.get('input[type="submit"]').click()
  cy.url().should('include', '/admin/')
})

// Logout helper for Django
Cypress.Commands.add('djangoLogout', () => {
  cy.visit('/admin/logout/')
  cy.url().should('include', '/admin/login/')
})

// **********************************************
// API Request Helpers
// **********************************************

// Make authenticated API requests with CSRF token
Cypress.Commands.add('apiRequest', (method, url, body = {}) => {
  return cy.getCsrfToken().then((csrfToken) => {
    return cy.request({
      method: method,
      url: url,
      body: body,
      headers: {
        'X-CSRFToken': csrfToken,
      },
      failOnStatusCode: false,
    })
  })
})

// **********************************************
// Wait Helpers
// **********************************************

// Wait for network to be idle
Cypress.Commands.add('waitForNetworkIdle', (timeout = 2000) => {
  let requestCount = 0
  
  cy.intercept('**', (req) => {
    requestCount++
    req.on('response', () => {
      requestCount--
    })
  })
  
  cy.wrap(null).should(() => {
    expect(requestCount).to.equal(0)
  })
})

// Wait for a specific number of milliseconds
Cypress.Commands.add('wait', (ms) => {
  return cy.wait(ms)
})

// Wait for element to be visible and interactable
Cypress.Commands.add('waitForElement', (selector, timeout = 10000) => {
  return cy.get(selector, { timeout }).should('be.visible').and('not.be.disabled')
})

// **********************************************
// Accessibility Testing (optional)
// **********************************************

// If using cypress-axe for accessibility testing
// import 'cypress-axe'

// Cypress.Commands.add('checkA11y', (context = null, options = {}) => {
//   cy.injectAxe()
//   cy.checkA11y(context, options)
// })

// **********************************************
// Visual Testing (optional)
// **********************************************

// If using Percy or another visual testing tool
// import '@percy/cypress'

// **********************************************
// Mobile/Responsive Testing Helpers
// **********************************************

Cypress.Commands.add('setMobile', () => {
  cy.viewport('iphone-x')
})

Cypress.Commands.add('setTablet', () => {
  cy.viewport('ipad-2')
})

Cypress.Commands.add('setDesktop', () => {
  cy.viewport(1920, 1080)
})

// **********************************************
// Form Helpers
// **********************************************

// Fill and submit a form
Cypress.Commands.add('submitForm', (formSelector, data) => {
  cy.get(formSelector).within(() => {
    Object.keys(data).forEach((key) => {
      cy.get(`[name="${key}"]`).clear().type(data[key])
    })
    cy.get('[type="submit"]').click()
  })
})

// Check if form has validation errors
Cypress.Commands.add('hasValidationError', (fieldName) => {
  return cy.get(`[name="${fieldName}"]`)
    .parent()
    .should('have.class', 'error')
    .or('contain', 'error')
})

// **********************************************
// Navigation Helpers
// **********************************************

// Visit page and wait for it to load
Cypress.Commands.add('visitAndWait', (url, timeout = 10000) => {
  cy.visit(url)
  cy.get('body', { timeout }).should('be.visible')
})

// Go back in browser history
Cypress.Commands.add('goBack', () => {
  cy.go('back')
})

// Reload the page
Cypress.Commands.add('reload', () => {
  cy.reload()
})

// **********************************************
// Assertion Helpers
// **********************************************

// Check if element exists without failing test
Cypress.Commands.add('elementExists', (selector) => {
  return cy.get('body').then(($body) => {
    return $body.find(selector).length > 0
  })
})

// Check if text exists on page
Cypress.Commands.add('containsText', (text) => {
  return cy.get('body').should('contain', text)
})

// Check if URL contains path
Cypress.Commands.add('urlContains', (path) => {
  return cy.url().should('include', path)
})

// **********************************************
// Interaction Helpers
// **********************************************

// Click element even if covered by another element
Cypress.Commands.add('forceClick', (selector) => {
  return cy.get(selector).click({ force: true })
})

// Type with delay between keystrokes
Cypress.Commands.add('typeSlowly', (selector, text, delay = 100) => {
  return cy.get(selector).type(text, { delay })
})

// Select option from dropdown by text
Cypress.Commands.add('selectByText', (selector, text) => {
  return cy.get(selector).select(text)
})

// **********************************************
// Debug Helpers
// **********************************************

// Log and pause for debugging
Cypress.Commands.add('debug', (message) => {
  cy.log(`🐛 DEBUG: ${message}`)
  cy.pause()
})

// Take a screenshot with a custom name
Cypress.Commands.add('screenshot', (name) => {
  const testName = Cypress.currentTest.title
  cy.screenshot(`${testName}-${name}`)
})

// Log custom message to Cypress command log
Cypress.Commands.add('logMessage', (message, type = 'info') => {
  const emoji = type === 'error' ? '❌' : type === 'success' ? '✅' : 'ℹ️'
  cy.log(`${emoji} ${message}`)
})

// **********************************************
// Storage Helpers
// **********************************************

// Set localStorage item
Cypress.Commands.add('setLocalStorage', (key, value) => {
  cy.window().then((win) => {
    win.localStorage.setItem(key, JSON.stringify(value))
  })
})

// Get localStorage item
Cypress.Commands.add('getLocalStorage', (key) => {
  return cy.window().then((win) => {
    const value = win.localStorage.getItem(key)
    return value ? JSON.parse(value) : null
  })
})

// Set sessionStorage item
Cypress.Commands.add('setSessionStorage', (key, value) => {
  cy.window().then((win) => {
    win.sessionStorage.setItem(key, JSON.stringify(value))
  })
})

// **********************************************
// File Upload Helpers
// **********************************************

// Upload file to input
Cypress.Commands.add('uploadFile', (selector, fileName, fileType = 'image/png') => {
  return cy.get(selector).attachFile({
    filePath: fileName,
    mimeType: fileType,
  })
})

// **********************************************
// Scroll Helpers
// **********************************************

// Scroll to element
Cypress.Commands.add('scrollToElement', (selector) => {
  return cy.get(selector).scrollIntoView()
})

// Scroll to top of page
Cypress.Commands.add('scrollToTop', () => {
  return cy.scrollTo('top')
})

// Scroll to bottom of page
Cypress.Commands.add('scrollToBottom', () => {
  return cy.scrollTo('bottom')
})

// **********************************************
// Table Helpers
// **********************************************

// Get table row by text content
Cypress.Commands.add('getTableRow', (tableSelector, text) => {
  return cy.get(tableSelector).contains('tr', text)
})

// Get table cell value
Cypress.Commands.add('getTableCell', (tableSelector, row, column) => {
  return cy.get(tableSelector)
    .find('tr')
    .eq(row)
    .find('td')
    .eq(column)
})

// **********************************************
// Date/Time Helpers
// **********************************************

// Get current date in specific format
Cypress.Commands.add('getCurrentDate', (format = 'YYYY-MM-DD') => {
  const now = new Date()
  // Simple date formatting - extend as needed
  return now.toISOString().split('T')[0]
})

// **********************************************
// Performance Testing
// **********************************************

// Measure page load time
Cypress.Commands.add('measureLoadTime', () => {
  cy.window().then((win) => {
    const perfData = win.performance.timing
    const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart
    cy.log(`⏱️ Page load time: ${pageLoadTime}ms`)
    return pageLoadTime
  })
})
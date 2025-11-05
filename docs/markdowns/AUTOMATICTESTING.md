# Automated Tests

This document outlines the automated tests ran for Django and JavaScript

Please copy the example to the relevant part for your tests.

---

## Table of Contents

- [Automated Tests](#automated-tests)
  - [Table of Contents](#table-of-contents)
  - [Writing the Tests](#writing-the-tests)
    - [Django Tests (Backend)](#django-tests-backend)
    - [Behave (BDD) Tests](#behave-bdd-tests)
    - [Frontend Tests (Jest \& Cypress)](#frontend-tests-jest--cypress)
      - [Jest (Unit Tests)](#jest-unit-tests)
      - [Cypress (End-to-End Tests)](#cypress-end-to-end-tests)
  - [Running The Tests](#running-the-tests)
    - [Commands](#commands)
    - [Optional Commands](#optional-commands)
  - [Documenting The Automated Tests](#documenting-the-automated-tests)
    - [Example](#example)
      - [Type of Testing (TDD or BDD)](#type-of-testing-tdd-or-bdd)
        - [App-Name](#app-name)
          - [What is it testing](#what-is-it-testing)
    - [Python Tests](#python-tests)
      - [TDD Testing via TestCase](#tdd-testing-via-testcase)
        - [US001: Browse Available Artworks - In Artwork App](#us001-browse-available-artworks---in-artwork-app)
          - [Artwork Model Tests](#artwork-model-tests)
        - [Artwork Views Tests](#artwork-views-tests)
    - [BDD Testing via Behave](#bdd-testing-via-behave)
      - [US001: Browse Available Artworks - In Artwork App](#us001-browse-available-artworks---in-artwork-app-1)
        - [Artwork Browsing Features](#artwork-browsing-features)
          - [Viewing Available Artwork](#viewing-available-artwork)
          - [Sold Out Artworks Are Clearly Marked](#sold-out-artworks-are-clearly-marked)
          - [Sort Artworks by Price](#sort-artworks-by-price)
          - [Filter Artworks by Availability](#filter-artworks-by-availability)
          - [View Artwork Details](#view-artwork-details)
          - [Add Artwork to Cart](#add-artwork-to-cart)
          - [Attempt to Add Sold Out Artwork to Cart](#attempt-to-add-sold-out-artwork-to-cart)
    - [JavaScript Tests](#javascript-tests)
      - [TDD Testing via Jest](#tdd-testing-via-jest)
        - [US001: Browse Available Artworks - In Artwork App](#us001-browse-available-artworks---in-artwork-app-2)
          - [Artwork Listing Component Tests](#artwork-listing-component-tests)
      - [BDD Testing via Cypress](#bdd-testing-via-cypress)
        - [US001: Browse Available Artworks - In Artwork App](#us001-browse-available-artworks---in-artwork-app-3)
          - [Artwork Browsing Features](#artwork-browsing-features-1)

---

## Writing the Tests

---

When writing tests for **Pointless Impressions**, it’s important to keep test frameworks organised by type and location to maintain clarity and consistency.

### Django Tests (Backend)

**Location:** Each app should have its own a `tests/tests.py` folder.  
Example: pointless_impressions_src/home/tests/tests.py

**Structure:**  
- Use `django.test.TestCase` for model, view, and form tests.  
- Keep tests small and focused (one assertion per behavior).  
- Name test methods descriptively:  
  
  ```python
  class HomeModelTest(TestCase):
      def test_home_str_method_returns_title(self):
          home = Home.objects.create(title="Sunset")
          self.assertEqual(str(home), "Sunset")
  ```

**Best Practices:**  
- Use `setUpTestData()` for creating objects once per class if multiple tests share them.  
- Mock external calls where needed (e.g., APIs, email sending).

### Behave (BDD) Tests

**Location:** All tests should be located in the `features/` folder in `pointless_impressions_src/`.  
Example: pointless_impressions_src/features/

- **Structure:**  
- `.feature` files describe behavior in **Given/When/Then** format.  
- Step definitions go in `steps/` within the same `features/` folder.

- **Naming:** Feature file names should be descriptive, e.g., `browse_home.feature`.

**Example:**
```gherkin
Feature: Browse available Home
  As a customer
  I want to see the homepage display current artwork for sale
  So that I can decide what to purchase

  Scenario: Viewing artwork list
    Given the following artwork exists:
      | title       | price |
      | Sunset      | 100   |
      | Mountains   | 200   |
    When I visit the homepage I want to see a section for latest artwork
    Then I should see "Sunset" and "Mountains"
```

### Frontend Tests (Jest & Cypress)

#### Jest (Unit Tests)

- **Location** all frontend tests live in `pointless_impressions_src/theme/static_src/src/tests.js/jest/app_name/*.test.js`
- Test JavaScript functions, components, or utilities
- **File Naming:** Use `NAME.test.js` suffix, e.g., `artwork.test.js`
- **HTML Fixture:**
  - Store mock HTML pages or snippets in `pointless_impressions_src/theme/static_src/src/tests.js/jest/app_name/fixtures/*.html`
  - Load fixtures in Jest tests

**Example**

```javascript
import { formatPrice } from '../utils/format';

test('formats price correctly', () => {
  expect(formatPrice(100)).toBe('£100.00');
});
```

#### Cypress (End-to-End Tests)

- **Location** all frontend tests live in `pointless_impressions_src/theme/static_src/src/tests.js/cypress/e2e/app_name/*.cy.js`
- Test full user flows in the browser
- **File Naming:** Use `NAME.cy.js` suffix, e.g., `browse_artwork.cy.js`
    
    ```javascript
    cy.fixture('artwork_list.html').then((html) => {
        document.body.innerHTML = html;
        cy.get('.artwork-title').should('contain', 'Sunset');
    });
    ```

---

## Running The Tests

---

To run the tests please use:

### Commands

In the `dev.sh` script there are easy commands to run each type of test.

1. For Django TestCase

  ```bash
  ./dev.sh test
  ```

2. For Django Behave

  ```bash
  ./dev.sh behave
  ```

3. For JavaScript Jest

  ```bash
  ./dev.sh jest
  ```

4. For JavaScript Cypress

  ```bash
  ./dev.sh cypress
  ```

  or to open the Cypress UI and see tests running visually:

  ```bash
  ./dev.sh cypress-open
  ```

  **Important** Cypress tests will reset the development database. After running Cypress tests, the `Photo` and `Artwork` fixtures will be reloaded automatically to restore the data.

### Optional Commands

Running specific tests can be done following the below:

1. To run app specific Django TestCase:

  ```bash
  ./dev.sh test app_name
  
  # Example:
  ./dev.sh test artwork
  ```

2. To run specific Behave feature tests:

  For Behave tests, you need to be in the Docker container shell first:

  ```bash
  ./dev.sh bash
  ```

  Then run the specific feature file (all feature files are located in `pointless_impressions_src/features/`):

  ```bash
  behave feature_file.feature

  # Example:
  behave artwork_browse.feature
  ```

  Behave will automatically locate and use the corresponding step definitions in the `steps/` folder.

3. To run app specific Jest tests:

  In the `package.json`, ensure you have the following script defined:

  ```json
  "scripts": {
    "test:app_name": "jest --config=jest.config.js pointless_impressions_src/theme/static_src/src/tests.js/jest/app_name/__tests__/"
  }
  ```

  As an example, for the `artwork` app, you would add:

  ```json
  "scripts": {
    "test:artwork": "jest --config=jest.config.js pointless_impressions_src/theme/static_src/src/tests.js/jest/artwork/__tests__/"
  }
  ```

  Then access the Docker container shell:

  ```bash
  ./dev.sh bash
  ```

  Then run the app specific Jest tests by executing:

  ```bash
  npm run test:app_name
  ```

  So for artwork app tests, you would run:

  ```bash
  npm run test:artwork
  ```

4. To run app specific Cypress tests:

  In the `package.json`, ensure you have the following script defined:

  ```json
  "scripts": {
    "cypress:app_name": "cross-env NODE_ENV=development cypress run --spec 'pointless_impressions_src/theme/static_src/cypress/e2e/app_name/**/*'"
  }
  ```

  As an example, for the `artwork` app, you would add:

  ```json
  "scripts": {
    "cypress:artwork": "cross-env NODE_ENV=development cypress run --spec 'pointless_impressions_src/theme/static_src/cypress/e2e/artwork/**/*'"
  }
  ```

  You will need to clear the Dev DB and load the Test Port and Fixtures again before running Cypress tests to ensure a clean state:

  ```bash
  ./dev.sh cypress:reset
  ```

  Then access the Docker container shell by running in a terminal not already in the container:

  ```bash
  ./dev.sh bash
  ```

  Then run the app specific Cypress tests by executing:

  ```bash
  npm run cypress:app_name
  ```

  So for artwork app tests, you would run:

  ```bash
  npm run cypress:artwork
  ```

  Make sure you then start the dev server again by running in a terminal not already in the container:

  ```bash
  ./dev.sh start
  ```

  And load the fixtures again if needed by running in a terminal not already in the container:

  ```bash
  ./dev.sh loadfixtures
  ```

  This will restore the development database to the with the required data.

---

## Documenting The Automated Tests

---

### Example

#### Type of Testing (TDD or BDD)

##### App-Name

###### What is it testing

| Step | Action          | Outcome                 | Pass / Fail                |
| ---- | --------------- | ----------------------- | -------------------------- |
| 1    | Action by User  | Expected Outcome        | Did it Pass or Fail        |

---

### Python Tests

#### TDD Testing via TestCase

##### US001: Browse Available Artworks - In Artwork App

###### Artwork Model Tests

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Create new Artwork and check initial state | Verifies all initial fields and Foreign Key relationships are correctly set. | Pass |
| 2 | Verify Artwork's selected conditions relationship  | Confirms the ManyToMany relationship for `selected_conditions` is correctly established. | Pass |
| 3 | Check string representation of the Artwork | Confirms the `Artwork.__str__` method returns the correct name string. | Pass |
| 4 | Update the Artwork's price | Confirms updates to the `price` field are correctly saved. | Pass |
| 5 | Update the Artwork's description | Confirms updates to the `description` field are correctly saved. | Pass |
| 6 | Change Artwork availability status | Confirms the boolean flag `is_available` can be toggled and persists. | Pass |
| 7 | Change Artwork stock status | Confirms the boolean flag `is_in_stock` can be toggled and persists. | Pass |
| 8 | Change Artwork featured status | Confirms the boolean flag `is_featured` can be toggled and persists. | Pass |
| 9 | Update the Artwork's Category | Confirms assigning and updating the `category` foreign key works correctly. | Pass |
| 10 | Update the Artwork's Framing Condition | Confirms assigning and updating the `selected_conditions` relationship works correctly. | Pass |
| 11 | Check string representation of a Category | Verifies the `ArtworkCategory.__str__` method returns the correct string. | Pass |
| 12 | Check string representation of a Condition | Verifies the `ArtworkFramingCondition.__str__` returns the correct formatted string. | Pass |
| 13 | Modify the Artwork's name and save | Verifies `created_at` remains fixed and `updated_at` changes. | Pass |
| 14 | Attempt to create item with a duplicate SKU | Verifies the unique constraint is enforced by asserting an exception is raised. | Pass |
| 15 | Create a new Artwork without providing a slug | Verifies automatic slug generation from the name is successful. | Pass |
| 16 | Create a new Artwork without providing an SKU | Verifies automatic SKU generation is successful and starts with `"SKU-"`. | Pass |
| 17 | Access Artwork image and alt text properties | Verifies computed image properties retrieve data correctly from the linked photo. | Pass |
| 18 | Remove all photos and access alt text | Verifies the deepest fallback logic: defaults to Artwork name when no related photo exists. | Pass |
| 19 | Create a second, independent Artwork | Confirms integrity when creating a new, distinct artwork instance. | Pass |

##### Artwork Views Tests

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Load the general **Shop** (Artworks List) page. | **Response 200**, displays both available artworks. | Pass |
| 2 | Load the list after marking an artwork as unavailable. | **Response 200**, when available only filter is set, only available photos are shown. | Pass |
| 3 | Test list navigation across multiple pages (17 items). | Page 1 displays 12 artworks, and Page 2 displays the remaining 5 artworks. | Pass |
| 4 | Filter the list by category **"Nature"**. | **Response 200**, only `Sunset` (Nature) is displayed. | Pass |
| 5 | Filter the list by category **"Seascape"**. | **Response 200**, only `Ocean` (Seascape) is displayed. | Pass |
| 6 | Filter the list by price range **£150-£200**. | **Response 200**, only `Sunset` (price 199.99) is displayed. | Pass |
| 7 | Filter the list by price range **£300-£400**. | **Response 200**, JSON is empty so **"No artworks found."** is displayed. | Pass |

---

### BDD Testing via Behave

#### US001: Browse Available Artworks - In Artwork App

##### Artwork Browsing Features

###### Viewing Available Artwork

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | Visit the artwork listing page | See "Sunset" | Pass |
| 2 | See artwork description | "A beautiful sunset over the mountains." | Pass |
| 3 | See artwork price | "£199.99" | Pass |

###### Sold Out Artworks Are Clearly Marked

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | Visit the artwork listing page | See "Starry Night" | Pass |
| 2 | Check sold out badge | "Sold Out" next to "Starry Night" | Pass |

###### Sort Artworks by Price

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | Visit the artwork listing page sorted by "price" | Artworks displayed in ascending price order | Pass |

###### Filter Artworks by Availability

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | Visit the artwork listing page with filter "available" | See "Sunset" | Pass |
| 2 | Check filtered out items | Do not see "Starry Night" | Pass |

###### View Artwork Details

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | Visit artwork listing page | Page loads successfully | Pass |
| 2 | Click on "Sunset" | See artwork detail page | Pass |
| 3 | Check artwork info | See "Sunset" | Pass |
| 4 | Check artwork description | See "A beautiful sunset over the mountains." | Pass |
| 5 | Check artwork price | See "£199.99" | Pass |
| 6 | Check "Add to Cart" button | Button visible | Pass |

###### Add Artwork to Cart

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | On detail page for "Sunset" | Page loads successfully | Pass |
| 2 | Click "Add to Cart" button | "Sunset" added to shopping cart | Pass |
| 3 | Check confirmation message | "Sunset has been added to your cart." | Pass |

###### Attempt to Add Sold Out Artwork to Cart

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | On detail page for "Starry Night" | Page loads successfully | Pass |
| 2 | Click "Add to Cart" button | See error message: "Sorry, Starry Night is currently sold out." | Pass |
| 3 | Check button visibility | "Add to Cart" button not visible | Pass |

---

### JavaScript Tests

#### TDD Testing via Jest

##### US001: Browse Available Artworks - In Artwork App

###### Artwork Listing Component Tests

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | Render artwork list | Available artwork `Sunset` is displayed with description `A beautiful sunset over the mountains.` and price `£199.99` | Pass |
| 2 | Render artwork list | Sold-out artwork `Starry Night` is displayed and clearly marked as `Sold Out` | Pass |
| 3 | Sort artworks by price ascending | Artworks are sorted with lowest price first (`Sunset` before `Starry Night`) | Pass |
| 4 | Sort artworks by price descending | Artworks are sorted with highest price first (`Starry Night` before `Sunset`) | Pass |
| 5 | Sort artworks alphabetically | Artworks are sorted alphabetically by name (`Starry Night` before `Sunset`) | Pass |
| 6 | Sort artworks by artist | Artworks are sorted alphabetically by artist username (`blake` before `chris`) | Pass |
| 7 | Filter available artworks | Only available artworks are returned (`Sunset`) | Pass |
| 8 | Click on artwork | Artwork detail shows name, description, price, and `Add to Cart` button | Pass |

#### BDD Testing via Cypress

##### US001: Browse Available Artworks - In Artwork App

###### Artwork Browsing Features

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | Visit `/artworks/` page | Available artwork `Sunset` is displayed with description `A beautiful sunset over the mountains.` and price `£199.99` | Pass |
| 2 | Check sold-out artworks | Artwork `Starry Night` is displayed and marked `Sold Out` | Pass |
| 3 | Click `#sort-price` | Artworks are sorted by price ascending (`Sunset` before `Starry Night`) | Pass |
| 4 | Click `#filter-available` | Only available artworks (`Sunset`) are displayed; `Starry Night` is hidden | Pass |
| 5 | Click `Sunset` artwork | Artwork detail shows name, description, price, and `Add to Cart` button | Pass |
| 6 | Add `Sunset` to cart | Confirmation message appears; cart updates to include `Sunset` | Pass |
| 7 | Attempt to add sold-out `Starry Night` | Shows sold-out message; `Add to Cart` button does not appear | Pass |

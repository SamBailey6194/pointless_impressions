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
        - [US002: View Artwork Details - In Artwork App](#us002-view-artwork-details---in-artwork-app)
          - [Artwork Detail View Tests](#artwork-detail-view-tests)
        - [US008: Admin Upload and Manage Artwork - In Artwork App](#us008-admin-upload-and-manage-artwork---in-artwork-app)
          - [Artwork Admin CRUD Tests](#artwork-admin-crud-tests)
          - [Artwork Admin Permissions Tests](#artwork-admin-permissions-tests)
          - [Artwork Validation Tests](#artwork-validation-tests)
          - [Artwork Form Tests](#artwork-form-tests)
        - [US003: Add Artwork to Cart - In Artwork App](#us003-add-artwork-to-cart---in-artwork-app)
          - [Cart Session Management Tests](#cart-session-management-tests)
    - [Photo Form Tests (DRY Approach)](#photo-form-tests-dry-approach)
      - [Photo Form Field Conditioning Tests](#photo-form-field-conditioning-tests)
    - [BDD Testing via Behave](#bdd-testing-via-behave)
      - [US001: Browse Available Artworks - In Artwork App](#us001-browse-available-artworks---in-artwork-app-1)
        - [Artwork Browsing Features](#artwork-browsing-features)
          - [Viewing Available Artwork](#viewing-available-artwork)
          - [Sold Out Artworks Are Clearly Marked](#sold-out-artworks-are-clearly-marked)
          - [Sort Artworks by Price](#sort-artworks-by-price)
          - [Filter Artworks by Availability](#filter-artworks-by-availability)
          - [View Artwork Details](#view-artwork-details)
      - [US002: View Artwork Details - In Artwork App](#us002-view-artwork-details---in-artwork-app-1)
        - [Availability Status](#availability-status)
        - [Artist Information](#artist-information)
        - [Related Artworks Display](#related-artworks-display)
        - [Framing Conditions Display](#framing-conditions-display)
      - [US003: Add Artwork to Cart - In Artwork App](#us003-add-artwork-to-cart---in-artwork-app-1)
        - [Add to Cart Features](#add-to-cart-features)
          - [Add Available Artwork to Cart](#add-available-artwork-to-cart)
          - [Prevent Adding Sold-Out Artwork](#prevent-adding-sold-out-artwork)
          - [Add Multiple Different Artworks](#add-multiple-different-artworks)
          - [Increment Quantity When Adding Same Artwork Twice](#increment-quantity-when-adding-same-artwork-twice)
          - [Cart Display Information](#cart-display-information)
          - [Remove Artwork from Cart](#remove-artwork-from-cart)
          - [Update Cart Quantity](#update-cart-quantity)
          - [Prevent Quantity Exceeding Available Stock](#prevent-quantity-exceeding-available-stock)
          - [Scenario 9: Session-Based Cart Persistence (Implementation Detail)](#scenario-9-session-based-cart-persistence-implementation-detail)
    - [JavaScript Tests](#javascript-tests)
      - [TDD Testing via Jest](#tdd-testing-via-jest)
        - [US001: Browse Available Artworks - In Artwork App](#us001-browse-available-artworks---in-artwork-app-2)
          - [Artwork Listing Component Tests](#artwork-listing-component-tests)
        - [US002: View Artwork Details - In Artwork App](#us002-view-artwork-details---in-artwork-app-2)
          - [Artwork Detail Display Functions](#artwork-detail-display-functions)
          - [Carousel Navigation Functions](#carousel-navigation-functions)
          - [Review Submission Functions](#review-submission-functions)
        - [US003: Add Artwork to Cart - In Artwork App](#us003-add-artwork-to-cart---in-artwork-app-2)
          - [Add to Cart Function Tests](#add-to-cart-function-tests)
          - [Remove from Cart Function Tests](#remove-from-cart-function-tests)
          - [Update Quantity Function Tests](#update-quantity-function-tests)
          - [Get Cart Function Tests](#get-cart-function-tests)
          - [Calculate Total Function Tests](#calculate-total-function-tests)
          - [Format Price Function Tests](#format-price-function-tests)
          - [localStorage Integration Tests](#localstorage-integration-tests)
          - [Edge Cases Tests](#edge-cases-tests)
      - [BDD Testing via Cypress](#bdd-testing-via-cypress)
        - [US001: Browse Available Artworks - In Artwork App](#us001-browse-available-artworks---in-artwork-app-3)
          - [Artwork Browsing Features](#artwork-browsing-features-1)
        - [US002: View Artwork Details - In Artwork App](#us002-view-artwork-details---in-artwork-app-3)
          - [Artwork Detail Page Access](#artwork-detail-page-access)
          - [Artwork Title Display](#artwork-title-display)
          - [Artwork Description Display](#artwork-description-display)
          - [Price Display](#price-display)
          - [Image Display](#image-display)
          - [Availability Status](#availability-status-1)
          - [Related Artworks Section](#related-artworks-section)
          - [Framing Conditions](#framing-conditions)
          - [Category Information](#category-information)
          - [Responsive Design](#responsive-design)
          - [Accessibility](#accessibility)
          - [Error Handling](#error-handling)
        - [US003: Add Artwork to Cart - In Artwork App](#us003-add-artwork-to-cart---in-artwork-app-3)
          - [Add to Cart Button](#add-to-cart-button)
          - [Adding Single Artwork](#adding-single-artwork)
          - [Adding Multiple Artworks](#adding-multiple-artworks)
          - [Quantity Increment](#quantity-increment)
          - [Cart Page Display](#cart-page-display)
          - [Remove from Cart](#remove-from-cart)
          - [Update Quantity](#update-quantity)
          - [Stock Limit Validation](#stock-limit-validation)
          - [Price Calculations](#price-calculations)
          - [Cart Persistence](#cart-persistence)
          - [Error Handling](#error-handling-1)
          - [Accessibility](#accessibility-1)

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

##### US002: View Artwork Details - In Artwork App

###### Artwork Detail View Tests

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Load artwork detail page with valid slug | HTTP 200 response returned | Pass |
| 2 | Load artwork detail page | Correct template `artwork/artwork_detail.html` is rendered | Pass |
| 3 | Load artwork detail page | Context contains `artwork` object | Pass |
| 4 | Load detail page for "Mountain Peak" | Artwork title "Mountain Peak" displays on page | Pass |
| 5 | Load detail page for "Mountain Peak" | Full description "A serene mountain landscape in pointillist style." displays | Pass |
| 6 | Load detail page for "Mountain Peak" | Price "£249.99" is displayed | Pass |
| 7 | Load detail page for available artwork | Availability status shows as available | Pass |
| 8 | Load detail page for artwork with zero quantity | Stock status shows as "Out of Stock" or "Sold Out" | Pass |
| 9 | Load detail page for "Mountain Peak" | Artwork image displays correctly | Pass |
| 10 | Load detail page for "Mountain Peak" | Artist name "michael" is displayed | Pass |
| 11 | Load detail page for "Mountain Peak" | Category "Landscape Art" is displayed | Pass |
| 12 | Request detail page with non-existent slug | HTTP 404 response returned | Pass |
| 13 | Load detail page with related artworks in same category | Related artwork "Valley View" is available in context or displayed | Pass |
| 14 | Load detail page for artwork | Framing conditions (e.g., "framed") are displayed as options | Pass |
| 15 | Load detail page for artwork | Average rating annotation is calculated (0 for new artwork) | Pass |
| 16 | Load detail page for artwork with reviews | Review count annotation is calculated correctly | Pass |
| 17 | Load detail page for artwork | Review form is available in context | Pass |
| 18 | Load detail page for artwork | All reviews ordered by newest first are in context | Pass |

---

##### US008: Admin Upload and Manage Artwork - In Artwork App

###### Artwork Admin CRUD Tests

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Create artwork with all required fields | Artwork created with name, artist, description, price, category; SKU and slug auto-generated | Pass |
| 2 | Create multiple artworks | Each artwork receives unique auto-generated SKU starting with "SKU-" | Pass |
| 3 | Create artwork and verify slug generation | Artwork name "The Starry Night" generates slug "the-starry-night" | Pass |
| 4 | Create artwork with framing conditions | Artwork created and framing conditions successfully added via ManyToMany relation | Pass |
| 5 | Read artwork by ID | Admin can retrieve artwork by primary key with all fields intact | Pass |
| 6 | Read artwork by slug | Admin can retrieve artwork using slug field for direct access | Pass |
| 7 | Update artwork name | Admin can change artwork name and save; updated name persists | Pass |
| 8 | Update artwork price | Admin can change artwork price; updated price persists | Pass |
| 9 | Update artwork description | Admin can change artwork description; updated description persists | Pass |
| 10 | Update artwork category | Admin can reassign artwork to different category; change persists | Pass |
| 11 | Update artwork artist | Admin can reassign artwork to different artist; change persists | Pass |
| 12 | Delete artwork | Admin can delete artwork; artwork no longer exists in database | Pass |
| 13 | Mark artwork as sold out | Admin can set `is_available=False`; status persists | Pass |
| 14 | Mark artwork as available | Admin can set `is_available=True` on unavailable artwork; status persists | Pass |
| 15 | Mark artwork out of stock | Admin can set `quantity=0`; `is_in_stock` automatically becomes False | Pass |
| 16 | Update artwork quantity | Admin can increase quantity; `is_in_stock` automatically becomes True | Pass |
| 17 | Mark artwork as featured | Admin can set `is_featured=True`; status persists | Pass |
| 18 | CRUD sequence: Create-Read-Update-Delete | Artwork progresses through full lifecycle correctly | Pass |

###### Artwork Admin Permissions Tests

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Check add_artwork permission exists | Permission `add_artwork` created for Artwork model | Pass |
| 2 | Check change_artwork permission exists | Permission `change_artwork` created for Artwork model | Pass |
| 3 | Check delete_artwork permission exists | Permission `delete_artwork` created for Artwork model | Pass |
| 4 | Check view_artwork permission exists | Permission `view_artwork` created for Artwork model | Pass |
| 5 | Superuser has all artwork permissions | Superuser can execute add, change, delete, view operations | Pass |
| 6 | Staff user can be assigned artwork permissions | Staff user without permissions; after granting `add_artwork`, user has permission | Pass |
| 7 | Regular user lacks artwork permissions | Regular (non-staff) user lacks all artwork admin permissions by default | Pass |

###### Artwork Validation Tests

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Create artwork with duplicate name | IntegrityError raised; unique constraint on `name` enforced | Pass |
| 2 | Create artwork with duplicate SKU | IntegrityError raised; unique constraint on `sku` enforced | Pass |
| 3 | Create artwork without description | Artwork created with empty description (TextField allows empty strings) | Pass |
| 4 | Create artwork without price | IntegrityError raised; database NOT NULL constraint on `price` enforced | Pass |
| 5 | Create artwork with decimal price | Artwork saves with precise decimal format (e.g., 99.99) | Pass |
| 6 | Create artwork with two-decimal price | Price retrieved as string maintains precision (e.g., "199.99") | Pass |
| 7 | Create artwork with default quantity | New artwork has quantity=0 by default | Pass |
| 8 | Create artwork with default availability | New artwork has is_available=True by default | Pass |
| 9 | Create artwork with default featured status | New artwork has is_featured=False by default | Pass |
| 10 | Attempt duplicate slug assignment | IntegrityError raised; unique constraint on `slug` enforced | Pass |

###### Artwork Form Tests

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Submit ArtworkForm with all required fields | Form validates successfully and artwork can be created | Pass |
| 2 | Submit ArtworkForm without name field | Form validation fails with error in `name` field | Pass |
| 3 | Submit ArtworkForm without price field | Form validation fails with error in `price` field | Pass |
| 4 | Submit ArtworkForm without description field | Form validation fails with error in `description` field | Pass |
| 5 | Submit ArtworkForm with non-numeric price | Form validation fails with error in `price` field | Pass |
| 6 | Submit ArtworkForm with negative price | Form validation fails; negative prices rejected | Pass |
| 7 | Save valid ArtworkForm | New artwork object created with all form data | Pass |
| 8 | Submit ArtworkSubmissionForm with limited fields | Form validates with name, description, price, category only | Pass |
| 9 | Check ArtworkSubmissionForm excludes admin fields | Form does not include `is_featured`, `sku`, `is_available` fields | Pass |
| 10 | Save ArtworkSubmissionForm with artist parameter | Artwork saves with artist set from parameter; is_available defaults to False | Pass |
| 11 | Submit ArtworkApprovalForm with valid data | Form validates successfully with is_available field | Pass |
| 12 | Check ArtworkApprovalForm field count | Form contains exactly 1 field: `is_available` | Pass |
| 13 | Save ArtworkApprovalForm with instance | Artwork instance updated with approval status | Pass |
| 14 | Submit ArtworkForm with framing conditions | Form validates and saves with ManyToMany framing conditions attached | Pass |
| 15 | Submit ArtworkForm with decimal price | Form preserves decimal precision (e.g., 99.99) when saved | Pass |

---

##### US003: Add Artwork to Cart - In Artwork App

###### Cart Session Management Tests

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Add available artwork to session cart | Artwork successfully added with id, name, price, quantity, and sku | Pass |
| 2 | Add multiple different artworks to cart | Both artworks present in session with correct data | Pass |
| 3 | Add same artwork to cart twice | Quantity increments from 1 to 2 for existing item | Pass |
| 4 | Prevent adding sold-out artwork | Sold-out artwork not added; is_available=False and quantity=0 verified | Pass |
| 5 | Calculate cart total with single item | Total = item price × quantity (e.g., 199.99 × 1 = 199.99) | Pass |
| 6 | Calculate cart total with multiple items | Total = sum of (price × quantity) for all items (e.g., 649.97 for mixed items) | Pass |
| 7 | Remove artwork from cart | Item deleted from session; other items remain | Pass |
| 8 | Update quantity in cart | Item quantity updated to new value and persists | Pass |
| 9 | Verify empty cart | Cart session exists but contains no items | Pass |
| 10 | Cart persistence across requests | Item added in first request still present in second request | Pass |

---

### Photo Form Tests (DRY Approach)

#### Photo Form Field Conditioning Tests

Photo forms use a DRY (Don't Repeat Yourself) approach with conditional field inclusion based on `photo_type` parameter. A single `PhotoForm` base class handles artwork, profile, and site asset photos.

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Submit PhotoForm with photo_type='artwork' and valid artwork image | Form validates successfully with artwork, title, description, image, alt_text fields | Pass |
| 2 | Submit PhotoForm with photo_type='profile' and valid profile image | Form validates successfully with title, description, image, alt_text fields (no artwork/asset fields) | Pass |
| 3 | Submit PhotoForm with photo_type='site_asset' and valid asset image | Form validates successfully with asset_identifier, title, description, image, alt_text fields | Pass |
| 4 | Submit PhotoForm artwork type without artwork field | Form validation fails with error in `artwork` field | Pass |
| 5 | Submit PhotoForm site_asset type without asset_identifier | Form validation fails with error in `asset_identifier` field | Pass |
| 6 | Initialize PhotoForm with photo_type='artwork' | Form field 'asset_identifier' is excluded from form.fields | Pass |
| 7 | Initialize PhotoForm with photo_type='site_asset' | Form field 'artwork' is excluded from form.fields | Pass |
| 8 | Initialize PhotoForm with photo_type='profile' | Form fields 'artwork' and 'asset_identifier' are both excluded from form.fields | Pass |
| 9 | Submit PhotoForm without title field | Form validation fails with error in `title` field | Pass |
| 10 | Submit PhotoForm without description field | Form validation fails with error in `description` field | Pass |
| 11 | Submit PhotoForm with title less than 3 characters | Form validation fails; title must be minimum 3 characters | Pass |
| 12 | Submit PhotoForm with description less than 5 characters | Form validation fails; description must be minimum 5 characters | Pass |
| 13 | Submit PhotoForm with alt_text exceeding 255 characters | Form validation fails; alt_text must be 255 characters or less | Pass |
| 14 | Save valid PhotoForm with user parameter | Photo object saved with uploaded_by field set to provided user | Pass |

---

### BDD Testing via Behave

**Important Note** Due to behave auto setting Debug to false during tests all image related tests have been omitted as images do not render in this mode.

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

---

#### US002: View Artwork Details - In Artwork App

##### Availability Status

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Create artworks: "Mountain Peak" (Available, 2 stock) and "Sold Out Art" (Unavailable, 0 stock) | Artworks created successfully in test database | Pass |
| 2 | View detail page for "Mountain Peak" | "Available" status displays on page | Pass |
| 3 | View detail page for "Mountain Peak" | "Add to Cart" button is visible | Pass |
| 4 | View detail page for "Sold Out Art" | "Sold Out" status displays on page | Pass |
| 5 | View detail page for "Sold Out Art" | "Add to Cart" button is NOT visible | Pass |

##### Artist Information

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Create artwork "Mountain Peak" by artist "Michael" | Artwork created with artist relationship | Pass |
| 2 | View detail page for "Mountain Peak" | Artist name "Michael" is displayed on page | Pass |
| 3 | View detail page for "Mountain Peak" | Artist name is displayed as a clickable profile link (href attribute exists) | Pass |

##### Related Artworks Display

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Create three artworks: "Mountain Peak" (Landscape), "Ocean Breeze" (Seascape), "Sold Out Art" (Portrait) - all by Michael | Artworks created with category and artist relationships | Pass |
| 2 | View detail page for "Mountain Peak" | "related" or "category" text appears in page content (indicating related artworks section) | Pass |
| 3 | View detail page for "Mountain Peak" | Related artworks in the same category are available in the page | Pass |

##### Framing Conditions Display

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Create artwork with "framed" framing condition option | Artwork linked to framing condition successfully | Pass |
| 2 | View detail page for artwork | Text containing "framed" or "framing" appears on page | Pass |
| 3 | View detail page for artwork | Artwork dimensions information is available (page loads with 200 OK status) | Pass |

---

#### US003: Add Artwork to Cart - In Artwork App

**Important Note** Image-related steps are omitted as images do not render in Behave test mode. Cart is implemented as session-based (backend) with frontend localStorage integration planned for checkout app.

##### Add to Cart Features

###### Add Available Artwork to Cart

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Create test artwork "Sunset Pointilism" (£199.99, qty 5, available) | Artwork created successfully | Pass |
| 2 | Navigate to artwork detail page | Detail page loads successfully | Pass |
| 3 | Click "Add to Cart" button | Artwork added to session cart | Pass |
| 4 | Verify artwork in cart | Cart session contains 1 item | Pass |
| 5 | Verify cart total | Cart total calculation shows "£199.99" | Pass |

###### Prevent Adding Sold-Out Artwork

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Create sold-out artwork "Sold Out Artwork" (£299.99, qty 0, unavailable) | Artwork created with is_available=False | Pass |
| 2 | Navigate to artwork detail page | Detail page loads successfully | Pass |
| 3 | Check "Add to Cart" button visibility | Button is not visible or disabled (is_available=False check) | Pass |

###### Add Multiple Different Artworks

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Create "Sunset Pointilism" (£199.99, qty 5) and "Ocean Waves" (£249.99, qty 3) | Both artworks created successfully | Pass |
| 2 | Navigate to "Sunset Pointilism" and click "Add to Cart" | First artwork added to session cart | Pass |
| 3 | Navigate to "Ocean Waves" and click "Add to Cart" | Second artwork added to session cart | Pass |
| 4 | Verify cart item count | Session cart contains 2 items | Pass |
| 5 | Verify cart total | Total calculation shows "£449.98" (199.99 + 249.99) | Pass |

###### Increment Quantity When Adding Same Artwork Twice

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Create "Sunset Pointilism" (£199.99, qty 5) | Artwork created successfully | Pass |
| 2 | Navigate to artwork and click "Add to Cart" | Artwork added with quantity 1 | Pass |
| 3 | Click "Add to Cart" button again | Quantity incremented to 2 | Pass |
| 4 | Verify cart item count | Cart shows 1 item with quantity=2 | Pass |
| 5 | Verify cart total | Total shows "£399.98" (199.99 × 2) | Pass |

###### Cart Display Information

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Create "Mountain Peak" artwork (£179.99, qty 4, available) | Artwork created successfully | Pass |
| 2 | Navigate to detail page and add to cart | Item added to session cart | Pass |
| 3 | Verify item name in session | Session cart contains item with name "Mountain Peak" | Pass |
| 4 | Verify item price in session | Item stored with price £179.99 | Pass |
| 5 | Verify cart total calculated | Session total shows "£179.99" | Pass |

###### Remove Artwork from Cart

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Create "Sunset Pointilism" (£199.99) and "Ocean Waves" (£249.99) | Both artworks created successfully | Pass |
| 2 | Add both artworks to cart | Session cart contains 2 items | Pass |
| 3 | Remove "Ocean Waves" from cart | Item removed from session | Pass |
| 4 | Verify remaining item | Only "Sunset Pointilism" remains (£199.99) | Pass |
| 5 | Verify removed item gone | "Ocean Waves" not in session cart | Pass |
| 6 | Verify updated total | Total recalculates to "£199.99" | Pass |

###### Update Cart Quantity

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Create "Sunset Pointilism" (£199.99, qty 5, available) | Artwork created successfully | Pass |
| 2 | Add artwork to cart | Item added with quantity 1 | Pass |
| 3 | Update quantity to 3 (no stock capping) | Quantity updated to 3 in session | Pass |
| 4 | Verify quantity updated | Item quantity shows 3 | Pass |
| 5 | Verify total recalculated | Total shows "£599.97" (199.99 × 3) | Pass |

###### Prevent Quantity Exceeding Available Stock

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Create "Limited Artwork" (£149.99, qty 2, available) | Artwork created with only 2 in stock | Pass |
| 2 | Add artwork to cart | Item added with quantity 1 | Pass |
| 3 | Try to update quantity to 5 (with stock capping) | Quantity update attempted with max stock validation | Pass |
| 4 | Verify quantity capped at stock limit | Quantity remains at 1 (or max allowed ≤ 2) | Pass |
| 5 | Verify error message | Error message shown about insufficient stock | Pass |

###### Scenario 9: Session-Based Cart Persistence (Implementation Detail)

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Add artwork to session cart | Item stored in Django session dict | Pass |
| 2 | Verify session key structure | Session cart contains entries keyed by artwork id | Pass |
| 3 | Verify session item structure | Each item contains: id, name, price, quantity, sku | Pass |
| 4 | Verify calculation logic | Total = sum(item['price'] × item['quantity']) for all items | Pass |

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
| 4 | Sort artworks by artist | Artworks are sorted alphabetically by artist username (`blake` before `chris`) | Pass |
| 5 | Filter available artworks | Only available artworks are returned (`Sunset`) | Pass |

---

##### US002: View Artwork Details - In Artwork App

###### Artwork Detail Display Functions

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Call `formatPrice(249.99)` | Returns "£249.99" | Pass |
| 2 | Call `formatPrice(100)` | Returns "£100.00" | Pass |
| 3 | Call `formatPrice(1234.50)` | Returns "£1,234.50" with thousand separator | Pass |
| 4 | Call `formatPrice('invalid')` | Returns "£0.00" safely | Pass |
| 5 | Call `displayArtworkDetail({name: 'Mountain Peak', price: 249.99})` | Title element updates to "Mountain Peak" | Pass |
| 6 | Call `displayArtworkDetail()` with null | Handles gracefully without error | Pass |

###### Carousel Navigation Functions

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Call `goToSlide(0)` | Carousel moves to first slide | Pass |
| 2 | Call `nextSlide()` | Carousel moves to next slide, loops at end | Pass |
| 3 | Call `previousSlide()` | Carousel moves to previous slide, loops at start | Pass |
| 4 | Keyboard arrow right pressed | Calls `nextSlide()` automatically | Pass |
| 5 | Keyboard arrow left pressed | Calls `previousSlide()` automatically | Pass |
| 6 | Click thumbnail button | `goToSlide()` called with correct index | Pass |
| 7 | Thumbnail styling updates | Active slide thumbnail highlighted with border | Pass |

###### Review Submission Functions

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Call `submitReview()` with valid form data | Fetch POST sent to `/artworks/reviews/submit/` | Pass |
| 2 | Review submission succeeds (200 OK) | Success notification shows "Review submitted successfully!" | Pass |
| 3 | Review submission fails (400 validation error) | Error notification shows validation message | Pass |
| 4 | Review submission fails (401 unauthorized) | Error notification shows login required message | Pass |
| 5 | Review submission fails (404 artwork not found) | Error notification shows artwork not found message | Pass |
| 6 | After successful submission | Modal closes and page reloads to show new review | Pass |
| 7 | Call `showNotification('Test', 'success')` | Toast appears with success styling and disappears after 5s | Pass |
| 8 | Call `showNotification('Error', 'error')` | Toast appears with error styling and disappears after 5s | Pass |
| 9 | Click "View Reviews" button | Smooth scrolls to reviews section | Pass |

---

##### US003: Add Artwork to Cart - In Artwork App

###### Add to Cart Function Tests

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Call `addToCart('artwork-1', 1, 199.99)` | Returns cart item with id, quantity=1, price=199.99 | Pass |
| 2 | Call `addToCart('artwork-1', 1, 199.99)` twice | Second call increments quantity to 2 | Pass |
| 3 | Call `addToCart('artwork-2', 1, 249.99)` | Adds new item; cart now contains 2 items | Pass |
| 4 | Call `addToCart()` with quantity 0 | Item added with quantity=0 | Pass |
| 5 | Call `addToCart()` with negative price | Item added with price stored as-is | Pass |

###### Remove from Cart Function Tests

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Call `removeFromCart('artwork-1')` with item in cart | Item removed from cart | Pass |
| 2 | Call `removeFromCart('artwork-1')` for non-existent item | Handles gracefully without error | Pass |
| 3 | Call `removeFromCart()` then verify other items persist | Other items remain in cart unchanged | Pass |

###### Update Quantity Function Tests

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Call `updateQuantity('artwork-1', 3)` on existing item | Item quantity updated to 3 | Pass |
| 2 | Call `updateQuantity('artwork-1', 1)` | Quantity updated to 1 | Pass |
| 3 | Call `updateQuantity('artwork-1', 0)` | Quantity set to 0 | Pass |
| 4 | Call `updateQuantity()` for non-existent item | Handles gracefully without error | Pass |

###### Get Cart Function Tests

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Call `getCart()` with empty cart | Returns empty object or array | Pass |
| 2 | Add item and call `getCart()` | Returns cart with added item | Pass |
| 3 | Call `getCart()` multiple times | Returns same data consistently | Pass |

###### Calculate Total Function Tests

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Call `calculateTotal()` with empty cart | Returns 0 | Pass |
| 2 | Call `calculateTotal()` with single item (199.99 × 1) | Returns 199.99 | Pass |
| 3 | Call `calculateTotal()` with multiple items | Returns sum of (price × quantity) for all items | Pass |
| 4 | Call `calculateTotal()` with item quantity 3, price 100 | Returns 300 | Pass |
| 5 | Call `calculateTotal()` with decimal calculations | Returns accurate decimal value (e.g., 399.98 not 399.99) | Pass |

###### Format Price Function Tests

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Call `formatPrice(199.99)` | Returns "£199.99" | Pass |
| 2 | Call `formatPrice(100)` | Returns "£100.00" | Pass |
| 3 | Call `formatPrice(1234.56)` | Returns "£1,234.56" with thousand separator | Pass |
| 4 | Call `formatPrice('invalid')` | Returns "£0.00" safely | Pass |
| 5 | Call `formatPrice(0)` | Returns "£0.00" | Pass |

###### localStorage Integration Tests

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Add item to cart | Item persists in localStorage | Pass |
| 2 | Retrieve cart after page reload simulation | Cart data restored from localStorage | Pass |
| 3 | Clear localStorage and check cart | Cart becomes empty | Pass |
| 4 | Add items, close page, reopen | Cart items still present (via localStorage) | Pass |

###### Edge Cases Tests

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Add item with very long ID | Item added and retrieved correctly | Pass |
| 2 | Add item with special characters in ID | Item handled without errors | Pass |
| 3 | Add item with extremely large price (999999.99) | Price stored and calculated correctly | Pass |
| 4 | Calculate total with many items (20+) | Accurate total calculated | Pass |

---

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
| 6 | Attempt to add sold-out `Starry Night` | Shows sold-out message; `Add to Cart` button does not appear | Pass |

---

##### US002: View Artwork Details - In Artwork App

###### Artwork Detail Page Access

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Visit `/artworks/` browse page and click first artwork card | Navigate to artwork detail page with title displayed | Pass |
| 2 | Visit `/artworks/sunset/` directly | Page loads with correct URL slug `/artworks/sunset/` | Pass |
| 3 | Visit `/artworks/non-existent-artwork/` | 404 error page displays | Pass |

###### Artwork Title Display

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Load detail page for "Sunset" | `<h1>` displays "Sunset" prominently | Pass |
| 2 | Load detail page | Title is visible with appropriate font-size | Pass |

###### Artwork Description Display

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Load detail page for "Sunset" | Description contains text about "sunset" | Pass |
| 2 | Load detail page | Description text is visible and formatted | Pass |

###### Price Display

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Load detail page for "Sunset" | Price "£199.99" displays in correct format | Pass |
| 2 | Load detail page | Price is visible and readable with appropriate font-weight | Pass |
| 3 | Load detail page | Currency symbol "£" is displayed before price | Pass |

###### Image Display

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Load detail page for "Sunset" | Large artwork image is visible with src attribute | Pass |
| 2 | Load detail page | Image has descriptive alt text | Pass |
| 3 | Load detail page | Image element exists and displays without errors | Pass |

###### Availability Status

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | View detail page for "Sunset" (available, in stock) | "Available" badge displays | Pass |
| 2 | View detail page for "Starry Night" (sold out) | "Sold Out" badge displays | Pass |
| 3 | View detail page for available artwork | Availability status is visible with color styling | Pass |

###### Related Artworks Section

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Load detail page for "Sunset" | Related artworks section displays with [data-testid="related-artworks"] | Pass |
| 2 | Load detail page | Related artwork cards are visible with count > 0 | Pass |
| 3 | Load detail page | Related artworks section is scrollable | Pass |
| 4 | Click on first related artwork card | Navigate to that artwork's detail page with URL including `/artworks/` | Pass |

###### Framing Conditions

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Load detail page for "Sunset" | Framing options section displays with [data-testid="framing-options"] | Pass |

###### Category Information

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Load detail page for "Sunset" | Category "Pointillism" badge displays with [data-testid="artwork-category"] | Pass |
| 2 | Click category link with [data-testid="category-link"] | Navigate to artwork list filtered by category with URL including `/artworks/` and `category=` parameter | Pass |

###### Responsive Design

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | View detail page on mobile (iPhone X) | Title (h1), image, and Add to Cart button all visible | Pass |
| 2 | View detail page on tablet (iPad 2) | Title (h1) and image are visible and readable | Pass |
| 3 | View detail page on desktop (1280x720) | Title (h1) and image are visible and readable | Pass |

###### Accessibility

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Load detail page | `<h1>` heading element exists | Pass |
| 2 | Load detail page | All `<img>` elements have alt text attribute | Pass |
| 3 | Load detail page | Add to Cart button has class attribute and is accessible | Pass |

###### Error Handling

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Load detail page for "Sunset" | Image element exists and handles missing images gracefully | Pass |
| 2 | Visit `/artworks/invalid-slug/` | 404 error page displays with "404" text | Pass |

---

##### US003: Add Artwork to Cart - In Artwork App

###### Add to Cart Button

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Visit `/artworks/` and click first artwork | Detail page loads with Add to Cart button visible | Pass |
| 2 | Verify Add to Cart button is not disabled | Button is clickable and functional | Pass |
| 3 | Visit sold-out artwork detail page | Add to Cart button is disabled or not visible | Pass |

###### Adding Single Artwork

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Click Add to Cart button on artwork detail | Success message "Added to cart" displays | Pass |
| 2 | Check cart count badge | Cart count increases by 1 | Pass |
| 3 | Add artwork and navigate away, then back to cart | Artwork persists in cart | Pass |

###### Adding Multiple Artworks

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Add first artwork to cart | First artwork added | Pass |
| 2 | Add second artwork to cart | Second artwork added | Pass |
| 3 | Check cart count | Cart count shows 2 items | Pass |

###### Quantity Increment

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Add artwork to cart | Quantity is 1 | Pass |
| 2 | Click Add to Cart button again on same artwork | Quantity increments to 2 | Pass |
| 3 | Navigate to cart | Item shows quantity 2 | Pass |

###### Cart Page Display

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Add artwork and navigate to `/cart/` | Cart page displays successfully | Pass |
| 2 | Verify artwork name displays | Item name visible in cart | Pass |
| 3 | Verify artwork price displays | Item price visible and formatted with £ | Pass |
| 4 | Verify total price displays | Cart total section visible | Pass |

###### Remove from Cart

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Add two artworks to cart | Both items in cart | Pass |
| 2 | Navigate to cart page | Cart displays both items | Pass |
| 3 | Click remove button for first item | First item removed | Pass |
| 4 | Verify second item remains | Second item still in cart | Pass |
| 5 | Verify empty state if all removed | Empty cart message displays when no items | Pass |

###### Update Quantity

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Add artwork to cart | Quantity is 1 | Pass |
| 2 | Navigate to cart page | Cart displays with update form | Pass |
| 3 | Change quantity to 3 | Quantity input updates | Pass |
| 4 | Submit update | Quantity updated to 3 | Pass |
| 5 | Verify total recalculated | Cart total updates based on new quantity | Pass |

###### Stock Limit Validation

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Add limited stock artwork (e.g., 2 available) | Artwork added | Pass |
| 2 | Navigate to cart page | Cart displays item | Pass |
| 3 | Try to update quantity to 5 | Quantity capped at available stock (1-2) | Pass |
| 4 | Verify error message | Error message about insufficient stock displays | Pass |

###### Price Calculations

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Add item with price £199.99 | Cart total shows £199.99 | Pass |
| 2 | Add second item with price £249.99 | Cart total shows £449.98 | Pass |
| 3 | Update first item quantity to 3 | Total recalculates to £849.97 (199.99×3 + 249.99) | Pass |
| 4 | Remove one item | Total updates to £199.99 | Pass |

###### Cart Persistence

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Add artwork to cart | Item in cart | Pass |
| 2 | Refresh page | Item still in cart after page reload | Pass |
| 3 | Navigate to different page and back | Cart items persist | Pass |
| 4 | Click clear cart button if available | Cart becomes empty | Pass |

###### Error Handling

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Add artwork to cart | Success confirmation shown | Pass |
| 2 | Simulate network error on add | Error message displays | Pass |
| 3 | Invalid artwork ID submitted | Handles gracefully without breaking | Pass |

###### Accessibility

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Add to Cart button has accessible label | Button has aria-label or title attribute | Pass |
| 2 | Cart page is keyboard navigable | Tab through elements and update quantity with Enter | Pass |
| 3 | Quantity input is accessible | Input field is accessible and can be modified | Pass |

```
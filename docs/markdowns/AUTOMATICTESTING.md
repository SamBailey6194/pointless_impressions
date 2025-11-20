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
        - [US003: Add Artwork to Cart \& US004: Checkout with Address Form - In Artwork App](#us003-add-artwork-to-cart--us004-checkout-with-address-form---in-artwork-app)
          - [Cart Session Management Tests](#cart-session-management-tests)
    - [Photo Form Tests (DRY Approach)](#photo-form-tests-dry-approach)
      - [Photo Form Field Conditioning Tests](#photo-form-field-conditioning-tests)
    - [JavaScript Tests](#javascript-tests)
      - [TDD Testing via Jest](#tdd-testing-via-jest)
        - [US001: Browse Available Artworks - In Artwork App](#us001-browse-available-artworks---in-artwork-app-1)
          - [Artwork Listing Component Tests](#artwork-listing-component-tests)
        - [US002: View Artwork Details - In Artwork App](#us002-view-artwork-details---in-artwork-app-1)
          - [Artwork Detail Display Functions](#artwork-detail-display-functions)
          - [Carousel Navigation Functions](#carousel-navigation-functions)
          - [Review Submission Functions](#review-submission-functions)
        - [US003: Add Artwork to Cart \& US004: Checkout with Address Form - In Artwork App](#us003-add-artwork-to-cart--us004-checkout-with-address-form---in-artwork-app-1)
    - [Quantity Button Behaviour Tests](#quantity-button-behaviour-tests)
    - [Network \& Server Error Handling Tests](#network--server-error-handling-tests)
    - [Add To Cart Page Initialisation Tests](#add-to-cart-page-initialisation-tests)

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

##### US003: Add Artwork to Cart & US004: Checkout with Address Form - In Artwork App

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
| 11 | Submit PhotoForm with title less than 3 characters | Form validation fails with error in `title` field | Pass |
| 12 | Submit PhotoForm with description less than 5 characters | Form validation fails with error in `description` field | Pass |
| 13 | Submit PhotoForm with alt_text exceeding 255 characters | Form validation fails with error in `alt_text` field | Pass |
| 14 | Save valid PhotoForm with user parameter | Photo object is saved with `uploaded_by` field set to the user | Pass |

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

##### US003: Add Artwork to Cart & US004: Checkout with Address Form - In Artwork App

### Quantity Button Behaviour Tests

| Step | Action | Outcome | Pass / Fail |
|------|--------|----------|--------------|
| 1 | Click increment button | Quantity increases from 1 → 2 | Pass |
| 2 | Click decrement button | Quantity decreases from 3 → 2 | Pass |
| 3 | Click decrement at minimum | Quantity stays at 1 (no negative values) | Pass |
| 4 | Increase quantity at max stock (5) | Quantity remains 5 (cannot exceed stock) | Pass |
| 5 | Increment reaches stock | Increment button becomes disabled | Pass |
| 6 | Init with quantity = stock | Increment button disabled on page load | Pass |
| 7 | Decrease below stock | Increment button becomes enabled again | Pass |

### Network & Server Error Handling Tests

| Step | Action | Outcome | Pass / Fail |
|------|--------|----------|--------------|
| 1 | Server returns `{ success: false, errors }` | Error toast displayed with message | Pass |
| 2 | Server returns `{ success: false }` | Error logged to console | Pass |
| 3 | Server error response | Cart does NOT update | Pass |
| 4 | Network `fetch` failure | Error logged: "Error submitting AddToCart form:" | Pass |
| 5 | Network `fetch` failure | Toast shows: "An unexpected error occurred." | Pass |
| 6 | Network failure | Cart dropdown NOT updated | Pass |

### Add To Cart Page Initialisation Tests

| Step | Action | Outcome | Pass / Fail |
|------|--------|----------|--------------|
| 1 | Call `initAddToCartPage()` | Quantity button handlers registered | Pass |
| 2 | Init then click increment | Quantity increases from 1 → 2 | Pass |
| 3 | Init event listeners | Form submit listener attached | Pass |
| 4 | Submit form after init | Performs POST and shows success toast | Pass |

---
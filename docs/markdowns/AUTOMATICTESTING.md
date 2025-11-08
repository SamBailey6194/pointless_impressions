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
    - [BDD Testing via Behave](#bdd-testing-via-behave)
      - [US001: Browse Available Artworks - In Artwork App](#us001-browse-available-artworks---in-artwork-app-1)
        - [Artwork Browsing Features](#artwork-browsing-features)
          - [Viewing Available Artwork](#viewing-available-artwork)
          - [Sold Out Artworks Are Clearly Marked](#sold-out-artworks-are-clearly-marked)
          - [Sort Artworks by Price](#sort-artworks-by-price)
          - [Filter Artworks by Availability](#filter-artworks-by-availability)
          - [View Artwork Details](#view-artwork-details)
      - [US002: View Artwork Details - In Artwork App](#us002-view-artwork-details---in-artwork-app-1)
        - [Artwork Detail Display](#artwork-detail-display)
        - [Availability Status](#availability-status)
        - [Artist and Category Information](#artist-and-category-information)
        - [Framing Conditions Display](#framing-conditions-display)
        - [Related Artworks Display](#related-artworks-display)
        - [Reviews Section Display](#reviews-section-display)
    - [JavaScript Tests](#javascript-tests)
      - [TDD Testing via Jest](#tdd-testing-via-jest)
        - [US001: Browse Available Artworks - In Artwork App](#us001-browse-available-artworks---in-artwork-app-2)
          - [Artwork Listing Component Tests](#artwork-listing-component-tests)
        - [US002: View Artwork Details - In Artwork App](#us002-view-artwork-details---in-artwork-app-2)
          - [Artwork Detail Display Functions](#artwork-detail-display-functions)
          - [Carousel Navigation Functions](#carousel-navigation-functions)
          - [Review Submission Functions](#review-submission-functions)
      - [BDD Testing via Cypress](#bdd-testing-via-cypress)
        - [US001: Browse Available Artworks - In Artwork App](#us001-browse-available-artworks---in-artwork-app-3)
          - [Artwork Browsing Features](#artwork-browsing-features-1)
        - [US002: View Artwork Details - In Artwork App](#us002-view-artwork-details---in-artwork-app-3)
          - [Artwork Detail Page Access](#artwork-detail-page-access)
          - [Artwork Information Display](#artwork-information-display)
        - [Availability Status](#availability-status-1)
          - [Artist Information](#artist-information)
          - [Category Information](#category-information)
          - [Framing Conditions](#framing-conditions)
          - [Carousel Navigation](#carousel-navigation)
          - [Similar Artworks Display](#similar-artworks-display)
          - [Reviews Section](#reviews-section)
          - [Responsive Design](#responsive-design)
          - [Accessibility](#accessibility)
          - [Error Handling](#error-handling)

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

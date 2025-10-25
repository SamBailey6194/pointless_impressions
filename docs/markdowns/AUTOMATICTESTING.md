# Automated Tests

This document outlines the automated tests ran for Django and JavaScript

Please copy the example to the relevant part for your tests.

---

## Table of Contents

- [Automated Tests](#automated-tests)
  - [Table of Contents](#table-of-contents)
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

## Example

### Type of Testing (TDD or BDD)

#### App-Name

##### What is it testing

| Step | Action          | Outcome                 | Pass / Fail                |
| ---- | --------------- | ----------------------- | -------------------------- |
| 1    | Action by User  | Expected Outcome        | Did it Pass or Fail        |

---

## Python Tests

### TDD Testing via TestCase

#### US001: Browse Available Artworks - In Artwork App

##### Artwork Model Tests

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | Create an `Artwork` instance with name "Sunset" | `Artwork` is created with all fields correctly set | Pass |
| 2 | Check `selected_condition` initially | `selected_condition` is `None` | Pass |
| 3 | Assign a `FramingCondition` to artwork | `selected_condition` is set and persists | Pass |
| 4 | Assign a `Category` to artwork | `category` is set and persists | Pass |
| 5 | Check `__str__` method of artwork | Returns `"Sunset"` | Pass |
| 6 | Toggle `is_available` from `True` to `False` | Field updates and persists | Pass |
| 7 | Toggle `is_in_stock` from `True` to `False` | Field updates and persists | Pass |
| 8 | Toggle `is_featured` from `False` to `True` | Field updates and persists | Pass |
| 9 | Update artwork price from 199.99 to 249.99 | Price updates correctly | Pass |
| 10 | Update artwork description | Description updates correctly | Pass |
| 11 | Attempt to create artwork with duplicate SKU "SUNSET1234" | Raises an exception (unique constraint) | Pass |
| 12 | Check timestamps after updating artwork name | `created_at` remains, `updated_at` changes | Pass |
| 13 | Create a second artwork instance | Two artworks exist with different IDs and fields set correctly | Pass |

#### Artwork Views Tests

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | Visit artwork list view | Returns 200 OK and contains artwork names | Pass/Fail |
| 2 | Visit artwork detail view | Returns 200 OK and contains description and price | Pass/Fail |
| 3 | Visit featured artwork view | Only featured artwork appears | Pass/Fail |
| 4 | Mark artwork unavailable and check list view | Unavailable artwork does not appear | Pass/Fail |
| 5 | Mark artwork out of stock and check detail view | Shows "Out of Stock" | Pass/Fail |
| 6 | Populate 15 extra artworks and test pagination | First page shows 10, second page shows remaining | Pass/Fail |
| 7 | Search artwork by name "Sunset" | Returns only matching artwork | Pass/Fail |
| 8 | Search artwork with non-existent term | Returns "No artworks found" | Pass/Fail |
| 9 | Filter artwork by category "Nature" | Returns only artworks in that category | Pass/Fail |
| 10 | Filter artwork by price range 150–200 | Returns only artworks in that range | Pass/Fail |
| 11 | Filter artwork by price range 300–400 | Returns "No artworks found" | Pass/Fail |

---

### BDD Testing via Behave

#### US001: Browse Available Artworks - In Artwork App

##### Artwork Browsing Features

###### Viewing Available Artwork

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | Visit the artwork listing page | See "Sunset" | |
| 2 | See artwork description | "A beautiful sunset over the mountains." | |
| 3 | See artwork price | "£199.99" | |

###### Sold Out Artworks Are Clearly Marked

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | Visit the artwork listing page | See "Starry Night" | |
| 2 | Check sold out badge | "Sold Out" next to "Starry Night" | |

###### Sort Artworks by Price

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | Visit the artwork listing page sorted by "price" | Artworks displayed in ascending price order | |

###### Filter Artworks by Availability

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | Visit the artwork listing page with filter "available" | See "Sunset" | |
| 2 | Check filtered out items | Do not see "Starry Night" | |

###### View Artwork Details

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | Visit artwork listing page | Page loads successfully | |
| 2 | Click on "Sunset" | See artwork detail page | |
| 3 | Check artwork info | See "Sunset" | |
| 4 | Check artwork description | See "A beautiful sunset over the mountains." | |
| 5 | Check artwork price | See "£199.99" | |
| 6 | Check "Add to Cart" button | Button visible | |

###### Add Artwork to Cart

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | On detail page for "Sunset" | Page loads successfully | |
| 2 | Click "Add to Cart" button | "Sunset" added to shopping cart | |
| 3 | Check confirmation message | "Sunset has been added to your cart." | |

###### Attempt to Add Sold Out Artwork to Cart

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | On detail page for "Starry Night" | Page loads successfully | |
| 2 | Click "Add to Cart" button | See error message: "Sorry, Starry Night is currently sold out." | |
| 3 | Check button visibility | "Add to Cart" button not visible | |

---

## JavaScript Tests

### TDD Testing via Jest

#### US001: Browse Available Artworks - In Artwork App

##### Artwork Listing Component Tests

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | Render artwork list | Available artwork `Sunset` is displayed with description `A beautiful sunset over the mountains.` and price `£199.99` | Pass |
| 2 | Render artwork list | Sold-out artwork `Starry Night` is displayed and clearly marked as `Sold Out` | Pass |
| 3 | Sort artworks by price ascending | Artworks are sorted with lowest price first (`Sunset` before `Starry Night`) | Pass |
| 4 | Filter available artworks | Only available artworks are returned (`Sunset`) | Pass |
| 5 | Click on artwork | Artwork detail shows name, description, price, and `Add to Cart` button | Pass |

### BDD Testing via Cypress

#### US001: Browse Available Artworks - In Artwork App

##### Artwork Browsing Features

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | Visit `/artworks/` page | Available artwork `Sunset` is displayed with description `A beautiful sunset over the mountains.` and price `£199.99` | Fail |
| 2 | Check sold-out artworks | Artwork `Starry Night` is displayed and marked `Sold Out` | Fail |
| 3 | Click `#sort-price` | Artworks are sorted by price ascending (`Sunset` before `Starry Night`) | Fail |
| 4 | Click `#filter-available` | Only available artworks (`Sunset`) are displayed; `Starry Night` is hidden | Fail |
| 5 | Click `Sunset` artwork | Artwork detail shows name, description, price, and `Add to Cart` button | Fail |
| 6 | Add `Sunset` to cart | Confirmation message appears; cart updates to include `Sunset` | Fail |
| 7 | Attempt to add sold-out `Starry Night` | Shows sold-out message; `Add to Cart` button does not appear | Fail |

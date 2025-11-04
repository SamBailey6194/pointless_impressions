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

#### Artwork Views Tests

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

## BDD Testing via Behave

### US001: Browse Available Artworks - In Artwork App

#### Artwork Browsing Features

##### Viewing Available Artwork

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | Visit the artwork listing page | See "Sunset" | Pass |
| 2 | See artwork description | "A beautiful sunset over the mountains." | Pass |
| 3 | See artwork price | "£199.99" | Pass |

##### Sold Out Artworks Are Clearly Marked

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | Visit the artwork listing page | See "Starry Night" | Pass |
| 2 | Check sold out badge | "Sold Out" next to "Starry Night" | Pass |

##### Sort Artworks by Price

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | Visit the artwork listing page sorted by "price" | Artworks displayed in ascending price order | Pass |

##### Filter Artworks by Availability

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | Visit the artwork listing page with filter "available" | See "Sunset" | Pass |
| 2 | Check filtered out items | Do not see "Starry Night" | Pass |

##### View Artwork Details

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | Visit artwork listing page | Page loads successfully | Pass |
| 2 | Click on "Sunset" | See artwork detail page | Pass |
| 3 | Check artwork info | See "Sunset" | Pass |
| 4 | Check artwork description | See "A beautiful sunset over the mountains." | Pass |
| 5 | Check artwork price | See "£199.99" | Pass |
| 6 | Check "Add to Cart" button | Button visible | Pass |

##### Add Artwork to Cart

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | On detail page for "Sunset" | Page loads successfully | Pass |
| 2 | Click "Add to Cart" button | "Sunset" added to shopping cart | Pass |
| 3 | Check confirmation message | "Sunset has been added to your cart." | Pass |

##### Attempt to Add Sold Out Artwork to Cart

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | On detail page for "Starry Night" | Page loads successfully | Pass |
| 2 | Click "Add to Cart" button | See error message: "Sorry, Starry Night is currently sold out." | Pass |
| 3 | Check button visibility | "Add to Cart" button not visible | Pass |

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
| 4 | Sort artworks by price descending | Artworks are sorted with highest price first (`Starry Night` before `Sunset`) | Pass |
| 5 | Sort artworks alphabetically | Artworks are sorted alphabetically by name (`Starry Night` before `Sunset`) | Pass |
| 6 | Sort artworks by artist | Artworks are sorted alphabetically by artist username (`blake` before `chris`) | Pass |
| 7 | Filter available artworks | Only available artworks are returned (`Sunset`) | Pass |
| 8 | Click on artwork | Artwork detail shows name, description, price, and `Add to Cart` button | Pass |

### BDD Testing via Cypress

#### US001: Browse Available Artworks - In Artwork App

##### Artwork Browsing Features

| Step | Action | Outcome | Pass / Fail |
| ---- | ------ | ------- | ----------- |
| 1 | Visit `/artworks/` page | Available artwork `Sunset` is displayed with description `A beautiful sunset over the mountains.` and price `£199.99` | Pass |
| 2 | Check sold-out artworks | Artwork `Starry Night` is displayed and marked `Sold Out` | Pass |
| 3 | Click `#sort-price` | Artworks are sorted by price ascending (`Sunset` before `Starry Night`) | Pass |
| 4 | Click `#filter-available` | Only available artworks (`Sunset`) are displayed; `Starry Night` is hidden | Pass |
| 5 | Click `Sunset` artwork | Artwork detail shows name, description, price, and `Add to Cart` button | Pass |
| 6 | Add `Sunset` to cart | Confirmation message appears; cart updates to include `Sunset` | Pass |
| 7 | Attempt to add sold-out `Starry Night` | Shows sold-out message; `Add to Cart` button does not appear | Pass |

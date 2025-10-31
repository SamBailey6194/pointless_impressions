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
| 2 | Check string representation of the Artwork | Confirms the `Artwork.__str__` method returns the correct name string. | Pass |
| 3 | Update the Artwork's price | Confirms updates to the `price` field are correctly saved. | Pass |
| 4 | Update the Artwork's description | Confirms updates to the `description` field are correctly saved. | Pass |
| 5 | Change Artwork availability status | Confirms the boolean flag `is_available` can be toggled and persists. | Pass |
| 6 | Change Artwork stock status | Confirms the boolean flag `is_in_stock` can be toggled and persists. | Pass |
| 7 | Change Artwork featured status | Confirms the boolean flag `is_featured` can be toggled and persists. | Pass |
| 8 | Update the Artwork's Category | Confirms assigning and updating the `category` foreign key works correctly. | Pass |
| 9 | Update the Artwork's Framing Condition | Confirms assigning and updating the `selected_condition` foreign key works correctly. | Pass |
| 10 | Check string representation of a Category | Verifies the `ArtworkCategory.__str__` method returns the correct string. | Pass |
| 11 | Check string representation of a Condition | Verifies the `ArtworkFramingCondition.__str__` returns the correct formatted string. | Pass |
| 12 | Modify the Artwork's name and save | Verifies `created_at` remains fixed and `updated_at` changes. | Pass |
| 13 | Attempt to create item with a duplicate SKU | Verifies the unique constraint is enforced by asserting an exception is raised. | Pass |
| 14 | Create a new Artwork without providing a slug | Verifies automatic slug generation from the name is successful. | Pass |
| 15 | Create a new Artwork without providing an SKU | Verifies automatic SKU generation is successful and starts with `"SKU-"`. | Pass |
| 16 | Access Artwork image and alt text properties | Verifies computed image properties retrieve data correctly from the linked photo. | Pass |
| 17 | Remove all photos and access alt text | Verifies the deepest fallback logic: defaults to Artwork name when no related photo exists. | Pass |
| 18 | Create a second, independent Artwork | Confirms integrity when creating a new, distinct artwork instance. | Pass |

#### Artwork Views Tests

| Step | Action | Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Load the general **Shop** (Artworks List) page. | **Response 200**, displays both available artworks. | Pass |
| 2 | Load the list after marking an artwork as unavailable. | **Response 200**, unavailable artwork not displayed, available artwork displayed. | Pass |
| 3 | Test list navigation across multiple pages (17 items). | Page 1 displays 10 artworks, and Page 2 displays the remaining 7 artworks. | Pass |
| 4 | Search the list using the existing term **"Sunset"**. | **Response 200**, only `Sunset` is displayed. | Pass |
| 5 | Search the list using a non-existent term. | **Response 200**, displays the message **"No artworks found."**. | Pass |
| 6 | Filter the list by category **"Nature"**. | **Response 200**, only `Sunset` (Nature) is displayed. | Pass |
| 7 | Filter the list by category **"Seascape"**. | **Response 200**, only `Ocean` (Seascape) is displayed. | Pass |
| 8 | Filter the list by price range **£150-£200**. | **Response 200**, only `Sunset` (price 199.99) is displayed. | Pass |
| 9 | Filter the list by price range **£300-£400**. | **Response 200**, displays the message **"No artworks found."**. | Pass |

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

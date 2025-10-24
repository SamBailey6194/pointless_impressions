# Automated Tests

This document outlines the manual tests carried out for each feature.

Please copy the example to the relevant part for your tests.

---

## Table of Contents

- [Automated Tests](#automated-tests)
  - [Table of Contents](#table-of-contents)
  - [Example](#example)
    - [Section](#section)
      - [Area](#area)
  - [Backend Testing](#backend-testing)
    - [US001: Browse Available Artworks - In Artwork App](#us001-browse-available-artworks---in-artwork-app)
  - [Frontend Testing](#frontend-testing)
    - [US001: Browse Available Artworks - In Artwork App](#us001-browse-available-artworks---in-artwork-app-1)

---

## Example

### Section

#### Area

| Step | Action          | Outcome                 | Pass / Fail                |
| ---- | --------------- | ----------------------- | -------------------------- |
| 1    | Action by User  | Expected Outcome        | Did it Pass or Fail        |

---

## Backend Testing

### US001: Browse Available Artworks - In Artwork App

| Step | Action | Expected Outcome | Pass / Fail |
| ---- | ------ | ---------------- | ----------- |
| 1 | Query artwork model for all artworks | Returns all artworks in the database | Fail |
| 2 | Query artwork model for available artworks only | Returns only artworks with `is_available=True` and/or `is_in_stock=True` | Fail |
| 3 | Sort artworks by price ascending | Artworks returned are sorted correctly by `price` | Fail |
| 4 | Sort artworks by price descending | Artworks returned are sorted correctly by `price` descending | Fail |
| 5 | Retrieve artwork details by SKU or ID | Returns the correct `name`, `description`, `price`, and `availability` | Fail |
| 6 | Attempt to retrieve a non-existent artwork | Returns 404 or raises appropriate exception | Fail |
| 7 | Add available artwork to cart | Cart database or session updates correctly | Fail |
| 8 | Attempt to add sold-out artwork to cart | Operation is rejected, cart does not update | Fail |

---

## Frontend Testing

### US001: Browse Available Artworks - In Artwork App

| Step | Action | Expected Outcome | Pass / Fail |
| ---- | ------ | ---------------- | ----------- |
| 1 | Navigate to `/artworks/` page | Page loads successfully | Fail |
| 2 | Observe available artworks | `Sunset` is displayed with description and price | Fail |
| 3 | Observe sold-out artworks | `Starry Night` is displayed and marked as `Sold Out` | Fail |
| 4 | Click "Sort by Price" button | Artworks are sorted ascending | Fail |
| 5 | Click "Filter Available" button | Only available artworks are visible | Fail |
| 6 | Click on `Sunset` artwork | Artwork detail appears with name, description, price, and `Add to Cart` button | Fail |
| 7 | Add `Sunset` to cart | Cart updates and confirmation message appears | Fail |
| 8 | Attempt to add `Starry Night` | Sold-out message appears; `Add to Cart` button is not visible | Fail |
| 9 | Verify cart updates | Cart displays correct items after adding artwork | Fail |

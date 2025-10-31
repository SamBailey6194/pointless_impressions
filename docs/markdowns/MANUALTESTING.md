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
| :--- | :--- | :--- | :--- |
| 1 | Query artwork model for all items (without filters) | Returns all artwork records (e.g., 2 records) in the database. | Fail |
| 2 | Query artwork model for **available only** (`is_available=True` and `is_in_stock=True`) | Returns only artwork records marked as available and in stock. | Fail |
| 3 | Query artworks filtered by **Category Name** (`Nature`) | Returns only artworks linked to the `Nature` category. | Fail |
| 4 | Query artworks filtered by **Framing Condition** (`Framed`) | Returns only artworks linked to the `Framed` condition. | Fail |
| 5 | Query artworks filtered by **Price Range** (e.g., £150-£200) | Returns only artworks whose price falls within the specified range. | Fail |
| 6 | Retrieve artwork details by **Slug** (e.g., `sunset-painting`) | Returns the correct single `Artwork` object with the matching name, description, and price. | Fail |
| 7 | Attempt to retrieve a non-existent artwork (by non-existent slug) | Returns 404 or raises appropriate `DoesNotExist` exception. | Fail |

---

## Frontend Testing

### US001: Browse Available Artworks - In Artwork App

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Navigate to `/artworks/` page | Page loads successfully, and all available/in-stock artworks are displayed. | Fail |
| 2 | Search with existing term (`Sunset`) | Only the `Sunset` artwork is displayed; the other items are filtered out. | Fail |
| 3 | Search with non-existent term | Page loads, displays a "No artworks found." message. | Fail |
| 4 | Apply **Category** filter (e.g., select "Nature") | Only artworks matching the selected category are displayed. | Fail |
| 5 | Apply **Price** filter (e.g., Min 150, Max 200) | Only artworks within the price range are displayed. | Fail |
| 6 | Test **Pagination** (must have > 10 items) | Only 10 items are shown initially; navigation controls lead to remaining items on the next page. | Fail |
| 7 | Observe an **Out of Stock** artwork's display | The item is visible (if not filtered out by availability) but marked with a clear "Sold Out" status. | Fail |
| 8 | Click on an available artwork's image or title from the list | Loads the Detail Page with the artwork's full name, description, price, and an **Add to Cart** button. | Fail |
| 9 | Attempt to add a **Sold Out** artwork to cart (if button is visible) | Operation is blocked or button is visibly disabled/missing. | Fail |

# Manual Testing Guide

This document outlines the manual tests to be carried out for each feature. Use this to verify functionality that automated tests may not catch.

---

## Table of Contents

- [Manual Testing Guide](#manual-testing-guide)
  - [Table of Contents](#table-of-contents)
  - [Example](#example)
    - [Section](#section)
      - [Area](#area)
  - [Backend Testing](#backend-testing)
    - [US001: Browse Available Artworks - In Artwork App](#us001-browse-available-artworks---in-artwork-app)
      - [Test the Artwork Model and Database Queries](#test-the-artwork-model-and-database-queries)
  - [Frontend Testing](#frontend-testing)
    - [US001: Browse Available Artworks - In Artwork App](#us001-browse-available-artworks---in-artwork-app-1)
      - [Test the Artwork Listing Page](#test-the-artwork-listing-page)
      - [Test Artwork Detail Page](#test-artwork-detail-page)
      - [Test Pagination (if applicable)](#test-pagination-if-applicable)
      - [Test Responsive Design](#test-responsive-design)
      - [Test Error Handling](#test-error-handling)

---

## Example

### Section

#### Area

| Step | Action | Expected Outcome | Pass / Fail |
| ---- | --------------- | ----------------------- | ----------- |
| 1 | Action by User | Expected Outcome | Pass/Fail |

---

## Backend Testing

### US001: Browse Available Artworks - In Artwork App

#### Test the Artwork Model and Database Queries

Use `./dev.sh shell` to access the Django shell for executing the queries 2 to 10.

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Start dev server with `./dev.sh start` | Server starts at http://localhost:8000 without errors | Pass |
| 2 | Query artwork model for all items (no filters): `Artwork.objects.all().count()` | Returns all artwork records from database (e.g., if 2 artworks exist, returns 2) | Pass |
| 3 | Query artworks for available only: `Artwork.objects.filter(is_available=True).count()` | Returns only records marked as available (e.g., returns 1 if "Sunset" is available) | Pass |
| 4 | Query artworks filtered by category: `Artwork.objects.filter(category__name="paintings")` | Returns only artworks linked to the selected category (e.g., returns "Autumn Reflections" for Paintings) | Pass |
| 5 | Query artworks filtered by price range: `Artwork.objects.filter(price__gte=150, price__lte=200)` | Returns only artworks whose price falls within specified range (e.g., returns "City The Buzz" for 150-200) | Pass |
| 6 | Query artworks filtered by framing condition: `Artwork.objects.filter(selected_conditions__condition_name="original framed")` | Returns only artworks linked to the selected framing condition | Pass |
| 7 | Retrieve artwork details by slug: `artwork = Artwork.objects.get(slug="city-icons-01")` then `print(artwork.name, artwork.description, artwork.price, artwork.artist)` | Returns the correct single Artwork object with matching name, description, price, and artist | Pass |
| 8 | Attempt to retrieve non-existent artwork by slug: `Artwork.objects.get(slug="nonexistent")` | Raises `Artwork.DoesNotExist` exception (proper error handling) | Pass |
| 9 | Check artwork relationships: verify `artwork.artist` exists | Artwork has valid Artist foreign key relationship | Pass |
| 10 | Check artwork photos: verify `artwork.main_photo` exists | Artwork has valid Photo relationship for main image | Pass |

---

## Frontend Testing

### US001: Browse Available Artworks - In Artwork App

#### Test the Artwork Listing Page

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Navigate to http://localhost:8000/artworks/ | Page loads successfully with artwork list and all elements visible (filters, sorting, pagination) | Pass |
| 2 | Verify page title and heading | Page displays "Browse Artworks" or similar heading | Pass |
| 3 | Verify available artworks display | "Pointillism The Dog 02" artwork card is visible with image, title, artist, price, and availability status | Pass |
| 4 | Verify sold-out artwork display | "Seascape Tides Out" artwork card is visible and clearly marked as "Sold Out" | Pass |
| 5 | Verify artwork card elements | Each artwork card shows: thumbnail image, title, artist name, price in GBP (e.g., £199.99), availability badge | Pass |
| 6 | Apply category filter (select "Pointillism") | Only artworks in "Pointillism" category display; other categories filter out | Pass |
| 7 | Apply price range filter (Min 150, Max 200) | Only artworks with price between £150-£200 display (e.g., "Sunset" shows) | Pass |
| 8 | Apply availability filter (Available Only) | Only available artworks display; "Starry Night" (sold out) is hidden | Pass |
| 9 | Clear all filters | All artworks return to display; filters reset to default state | Pass |
| 10 | Sort by price ascending | Artworks display with lowest price first (cheaper artwork appears before expensive ones) | Pass |
| 11 | Sort by price descending | Artworks display with highest price first (expensive artwork appears before cheaper ones) | Pass |
| 12 | Sort alphabetically (A-Z) | Artworks display in alphabetical order by title | Pass |
| 13 | Sort by artist name | Artworks display in alphabetical order by artist username | Pass |

#### Test Artwork Detail Page

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Click on available artwork ("Sunset") from list | Detail page loads showing full artwork information (image, description, price, artist) | Pass |
| 2 | Verify detail page layout | Page displays: large artwork image, title, artist link, full description, price, quantity info, "Add to Cart" button | Pass |
| 3 | Verify artwork information accuracy | All details match listing (title, price, artist, description are correct) | Pass |
| 4 | Check artist link | Click artist name links to artist profile or artist's artworks filtered view | Pass |
| 5 | Verify "Add to Cart" button | Button is visible, enabled, and clearly clickable for available artwork | Pass |
| 6 | Click "Add to Cart" for available artwork | Cart updates, confirmation message displays (e.g., "Sunset added to cart"), button may change state | Pass |
| 7 | Navigate back to artwork list | Browser back button or breadcrumb navigation returns to list view | Pass |
| 8 | Click on sold-out artwork ("Starry Night") | Detail page loads with "Sold Out" status clearly displayed | Pass |
| 9 | Verify sold-out state | "Add to Cart" button is either hidden, disabled, or shows "Out of Stock" message | Pass |
| 10 | Attempt to add sold-out artwork to cart | Operation is blocked; error message displays (e.g., "Item is sold out") | Pass |

#### Test Pagination (if applicable)

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Create/verify 15+ artworks in database | Pagination controls appear on page | Pass |
| 2 | Verify first page displays | Shows first 12 artworks (or configured page size), pagination controls visible | Pass |
| 3 | Navigate to page 2 | Displays next set of artworks (remaining 3+ artworks), URL updates (e.g., ?page=2) | Pass |
| 4 | Verify page numbers or next/previous buttons | Navigation controls work correctly to move between pages | Pass |
| 5 | Return to first page | Previous/first page button works, returns to page 1 | Pass |

#### Test Responsive Design

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | View artwork list on desktop (1920px width) | Layout displays full grid of artwork cards, all elements visible | Pass |
| 2 | View artwork list on tablet (768px width) | Layout adapts gracefully, artwork cards stack appropriately, filters/sorting remain accessible | Pass |
| 3 | View artwork list on mobile (375px width) | Layout stacks vertically, single column, filters/sorting accessible via menu or scroll | Pass |
| 4 | Test filter/sort controls on mobile | Dropdowns/buttons are touch-friendly and clickable, no layout breaks | Pass |

#### Test Error Handling

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Search with non-existent term (if search exists) | No results found message displays or empty list shows | Pass |
| 2 | Apply filters that return no results | "No artworks found" message displays clearly | Pass |
| 3 | Refresh page during cart operation | Page reloads gracefully without errors | Pass |
| 4 | Check browser console for errors | No JavaScript errors or warnings in browser developer tools console | Pass |
| 5 | Verify images load correctly | No broken image icons, all artwork images display properly | Pass |

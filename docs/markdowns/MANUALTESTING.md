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
    - [US002: View Artwork Details - In Artwork App](#us002-view-artwork-details---in-artwork-app)
      - [Test the Artwork Model and Detail Retrieval](#test-the-artwork-model-and-detail-retrieval)
  - [Frontend Testing](#frontend-testing)
    - [US001: Browse Available Artworks - In Artwork App](#us001-browse-available-artworks---in-artwork-app-1)
      - [Test the Artwork Listing Page](#test-the-artwork-listing-page)
      - [Test Artwork Detail Page](#test-artwork-detail-page)
      - [Test Pagination (if applicable)](#test-pagination-if-applicable)
      - [Test Responsive Design](#test-responsive-design)
      - [Test Error Handling](#test-error-handling)
    - [US002: View Artwork Details - In Artwork App](#us002-view-artwork-details---in-artwork-app-1)
      - [Test Artwork Detail Page Access](#test-artwork-detail-page-access)
      - [Test Artwork Title Display](#test-artwork-title-display)
      - [Test Artwork Description Display](#test-artwork-description-display)
      - [Test Price Display](#test-price-display)
      - [Test Image Display](#test-image-display)
      - [Test Availability Status](#test-availability-status)
      - [Test Related Artworks Section](#test-related-artworks-section)
      - [Test Framing Conditions](#test-framing-conditions)
      - [Test Category Information](#test-category-information)
      - [Test Responsive Design](#test-responsive-design-1)
      - [Test Accessibility](#test-accessibility)
      - [Test Error Handling](#test-error-handling-1)

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

### US002: View Artwork Details - In Artwork App

#### Test the Artwork Model and Detail Retrieval

Use `./dev.sh shell` to access the Django shell for executing the queries 2 to 12.

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Start dev server with `./dev.sh start` | Server starts at http://localhost:8000 without errors | Pass |
| 2 | Retrieve artwork by slug: `artwork = Artwork.objects.get(slug="city-icons-01")` and `print(artwork.slug)` | Returns correct Artwork object for "City Icons 01" with name, price, description, and is_available=True | Pass |
| 3 | Check artwork title: `print(artwork.name)` | Returns "City Icons 01" | Pass |
| 4 | Check artwork price: `print(artwork.price)` | Returns Decimal value 150.00 (or similar decimal format) | Pass |
| 5 | Check artwork description: `print(artwork.description)` | Returns full description text for the artwork | Pass |
| 6 | Check availability status: `print(artwork.is_available)` | Returns True for "City Icons 01" | Pass |
| 7 | Retrieve artwork image: `print(artwork.main_photo)` | Returns Photo object associated with artwork | Pass |
| 8 | Check artist relationship: `print(artwork.artist.user.username)` | Returns artist username; verifies ForeignKey relationship is intact | Pass |
| 9 | Check category relationship: `print(artwork.category.name)` | Returns "Photography" for "City Icons 01"; verifies ForeignKey relationship is intact | Pass |
| 10 | Check framing conditions: `print(list(artwork.selected_conditions.all()))` | Returns list of FramingCondition objects associated with artwork | Pass |
| 11 | Attempt to retrieve non-existent artwork: `Artwork.objects.get(slug="fake-artwork")` | Raises `Artwork.DoesNotExist` exception (proper error handling) | Pass |

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

---

### US002: View Artwork Details - In Artwork App

#### Test Artwork Detail Page Access

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Navigate to http://localhost:8000/artworks/ and click on "City Icons 01" artwork card | Detail page loads and displays full artwork information (image, title, description, price) | Pass |
| 2 | Navigate directly to http://localhost:8000/artworks/city-icons-01/ | Page loads successfully with URL slug `/artworks/city-icons-01/` visible in address bar | Pass |
| 3 | Navigate to http://localhost:8000/artworks/non-existent-artwork/ | 404 error page displays with "404" message | Pass |

#### Test Artwork Title Display

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Load detail page for "City Icons 01" | Artwork title "City Icons 01" displays prominently as main heading (h1 element) | Pass |
| 2 | Load detail page for any artwork | Title text is visible, clearly readable, and uses larger font-size than body text | Pass |

#### Test Artwork Description Display

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Load detail page for "City Icons 01" | Full artwork description is visible below the title | Pass |
| 2 | Load detail page for any artwork | Description text is formatted and readable, with appropriate line spacing | Pass |

#### Test Price Display

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Load detail page for "City Icons 01" | Price displays in correct format: "£150.00" with currency symbol and decimal places | Pass |
| 3 | Load detail page for any artwork | Currency symbol "£" is visible before the numeric price | Pass |

#### Test Image Display

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Load detail page for "City Icons 01" | Large artwork image is visible and loads completely | Pass |
| 2 | Load detail page for any artwork | Image element displays with descriptive alt text (not empty or generic) | Pass |
| 3 | Load detail page for any artwork | Image loads without 404 errors; broken image icon not displayed | Pass |

#### Test Availability Status

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | View detail page for "City Icons 01" (available, in stock) | "Available" badge or status indicator is clearly visible and labeled | Pass |

#### Test Related Artworks Section

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Load detail page for "City Icons 01" | "Related Artworks" or similar section displays below main content with multiple artwork cards | Pass |
| 2 | Load detail page for any artwork | Related artwork cards are visible and show thumbnail images, titles, and prices | Pass |
| 3 | Load detail page for any artwork | Related artworks section is horizontally scrollable or displays as grid without overflow issues | Pass |
| 4 | Click on a related artwork card | Navigate to that artwork's detail page; URL changes to reflect selected artwork (e.g., `/artworks/city-modernity/`) | Pass |

#### Test Framing Conditions

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Load detail page for "City Icons 01" | Framing options or conditions section displays with text or list of available framing choices | Pass |

#### Test Category Information

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Load detail page for "City Icons 01" | Category badge displays "Photography" | Pass |
| 2 | Click on the category badge or link | Browser navigates to artwork list page filtered by category with URL containing category filter parameter | Pass |

#### Test Responsive Design

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | View detail page on mobile (iPhone X, 375px width) | All key elements visible without horizontal scroll: title, image, price, and Add to Cart button | Pass |
| 2 | View detail page on tablet (iPad, 768px width) | Title and image are prominently displayed and readable; layout adapts gracefully to wider screen | Pass |
| 3 | View detail page on desktop (1280x720 or larger) | Title, image, and all details are visible with optimal spacing and readability | Pass |

#### Test Accessibility

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Load detail page and inspect page structure | Main heading (h1 element) is present at top of page | Pass |
| 2 | Load detail page and open browser developer tools | All images have alt text attributes (not empty, contain descriptive text) | Pass |
| 3 | Load detail page and test keyboard navigation | Add to Cart button (or equivalent CTA) is accessible and has appropriate HTML class attributes | Pass |

#### Test Error Handling

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Load detail page for "City Icons 01" | Even if image fails to load from server, page displays gracefully with no JavaScript console errors | Pass |
| 2 | Navigate to `/artworks/invalid-slug-12345/` | 404 error page displays with "404" or "Not Found" message; no blank page or server error | Pass |

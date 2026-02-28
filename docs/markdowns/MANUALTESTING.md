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
    - [US008: Admin Upload and Manage Artwork - In Artwork App](#us008-admin-upload-and-manage-artwork---in-artwork-app)
      - [Test Artwork Admin CRUD Operations](#test-artwork-admin-crud-operations)
      - [Test Artwork Form Submissions](#test-artwork-form-submissions)
    - [Photo Form Tests](#photo-form-tests)
      - [Test Photo Form DRY Approach](#test-photo-form-dry-approach)
    - [US003: Add Artwork to Cart - Backend](#us003-add-artwork-to-cart---backend)
      - [Test Add to Cart Functionality (Backend)](#test-add-to-cart-functionality-backend)
    - [US004: Checkout with Address Form](#us004-checkout-with-address-form)
      - [Test Checkout Functionality](#test-checkout-functionality)
    - [User Registration Fix (4.1, 4.4) - Backend](#user-registration-fix-41-44---backend)
      - [Test Registration Atomicity and Email Dispatch](#test-registration-atomicity-and-email-dispatch)
    - [Cart Interactivity Fix (1.1) - Backend](#cart-interactivity-fix-11---backend)
      - [Test Cart Update and Remove Endpoints](#test-cart-update-and-remove-endpoints)
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
    - [US003: Add Artwork to Cart](#us003-add-artwork-to-cart)
      - [Test Add to Cart Functionality](#test-add-to-cart-functionality)
    - [US004: Checkout with Address Form](#us004-checkout-with-address-form-1)
      - [Test Checkout Functionality](#test-checkout-functionality-1)
    - [User Registration Fix (4.1, 4.4) - Frontend](#user-registration-fix-41-44---frontend)
      - [Test Registration and Email Verification Flow](#test-registration-and-email-verification-flow)
    - [Cart Interactivity Fix (1.1) - Frontend](#cart-interactivity-fix-11---frontend)
      - [Test Cart Quantity Controls and Remove Item](#test-cart-quantity-controls-and-remove-item)

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

### US008: Admin Upload and Manage Artwork - In Artwork App

#### Test Artwork Admin CRUD Operations

Use `./dev.sh shell` to access the Django shell for executing these tests.

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Access Django admin at http://localhost:8000/admin/ | Admin login page displays | Pass |
| 2 | Log in with superuser credentials (username: admin) | Admin dashboard loads successfully | Pass |
| 3 | Navigate to Artwork section in admin | Artwork list displays all existing artworks with columns: Name, Artist, Price, Category, Available, Stock, Featured | Pass |
| 4 | Click "Add Artwork" button | Artwork creation form loads with fields: name, artist, description, price, category, framing conditions, main_photo, quantity, is_available, is_featured | Pass |
| 5 | Fill all required fields and click "Save" | New artwork is created; admin displays success message and returns to artwork list showing new artwork | Pass |
| 6 | Verify auto-generated SKU | New artwork has auto-generated SKU starting with "SKU-" (e.g., "SKU-12345") | Pass |
| 7 | Verify auto-generated slug | New artwork slug is generated from name and URL-safe (e.g., "test-artwork" from "Test Artwork") | Pass |
| 8 | Click on existing artwork to edit | Artwork edit form loads with all current values populated | Pass |
| 9 | Modify artwork fields (name, price, category) and click "Save" | Artwork updates; success message displays; changes persist in artwork list | Pass |
| 10 | Use admin action "Mark as available" | Select artwork and execute action; artwork is_available flag sets to True; list refreshes showing updated status | Pass |
| 11 | Use admin action "Mark as sold out" | Select artwork and execute action; artwork is_available flag sets to False; list refreshes showing updated status | Pass |
| 12 | Use admin action "Mark as featured" | Select artwork and execute action; artwork is_featured flag sets to True; list refreshes showing updated status | Pass |
| 13 | Filter artwork list by category | Click category filter; list displays only artworks matching selected category | Pass |
| 14 | Filter artwork list by availability | Click availability filter; list displays only available or unavailable artworks as selected | Pass |
| 15 | Search artwork by name or SKU | Use search box; list filters to show only matching artworks | Pass |
| 16 | Delete artwork | Click delete button or action; confirmation prompt appears; after confirming, artwork is removed from list and database | Pass |

#### Test Artwork Form Submissions

Use `./dev.sh shell` to test form validation in Django shell.

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Submit ArtworkForm with all required fields | Form validates without errors; artwork saves to database | Pass |
| 2 | Submit ArtworkForm without name field | Form shows validation error on name field (e.g., "This field is required") | Pass |
| 3 | Submit ArtworkForm without price field | Form shows validation error on price field (e.g., "This field is required") | Pass |
| 4 | Submit ArtworkForm without description field | Form shows validation error on description field | Pass |
| 5 | Submit ArtworkForm with non-numeric price (e.g., "abc") | Form shows validation error: "Price must be a valid decimal number" | Pass |
| 6 | Submit ArtworkForm with negative price (e.g., -50.00) | Form shows validation error: "Price must be greater than 0" | Pass |
| 7 | Submit ArtworkForm with decimal price (e.g., 99.99) | Form accepts decimal format; saves with proper decimal precision | Pass |
| 8 | Submit ArtworkSubmissionForm (artist workflow) | Form validates with limited fields: name, description, price, category (no is_featured, sku, is_available) | Pass |
| 9 | Submit ArtworkSubmissionForm without artist pre-selection | Form saves with artist set from parameter; is_available defaults to False (pending approval) | Pass |
| 10 | Submit ArtworkApprovalForm (admin approval) | Form validates with only is_available field; admin can approve artwork for sale | Pass |
| 11 | Save ArtworkForm with framing conditions | Form accepts multiple framing conditions; saves ManyToMany relationships correctly | Pass |
| 12 | Retrieve saved artwork and verify precision | Artwork price stored and retrieved as Decimal with 2 decimal places (e.g., "99.99") | Pass |

---

### Photo Form Tests

#### Test Photo Form DRY Approach

Use `./dev.sh shell` to test photo form behavior with conditional fields.

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Initialize PhotoForm with photo_type='artwork' | Form includes fields: photo_type, title, description, image, alt_text, artwork; excludes asset_identifier | Pass |
| 2 | Initialize PhotoForm with photo_type='profile' | Form includes base fields: photo_type, title, description, image, alt_text; excludes artwork and asset_identifier | Pass |
| 3 | Initialize PhotoForm with photo_type='site_asset' | Form includes fields: photo_type, title, description, image, alt_text, asset_identifier; excludes artwork | Pass |
| 4 | Submit PhotoForm artwork type with all fields including valid artwork | Form validates successfully; photo saves with artwork relationship | Pass |
| 5 | Submit PhotoForm artwork type without artwork field | Form validation fails with error: "Artwork must be selected for artwork photos" | Pass |
| 6 | Submit PhotoForm site_asset type with asset_identifier | Form validates successfully; photo saves with asset_identifier | Pass |
| 7 | Submit PhotoForm site_asset type without asset_identifier | Form validation fails with error: "Asset identifier is required for site assets" | Pass |
| 8 | Submit PhotoForm without title field | Form validation fails; title is required | Pass |
| 9 | Submit PhotoForm without description field | Form validation fails; description is required | Pass |
| 10 | Submit PhotoForm with title less than 3 characters (e.g., "ab") | Form validation fails: "Title must be at least 3 characters long" | Pass |
| 11 | Submit PhotoForm with description less than 5 characters (e.g., "test") | Form validation fails: "Description must be at least 5 characters long" | Pass |
| 12 | Submit PhotoForm with alt_text exceeding 255 characters | Form validation fails: "Alt text must be 255 characters or less" | Pass |
| 13 | Save valid PhotoForm with user parameter | Photo saves with uploaded_by field set to provided user; user relationship persists | Pass |
| 14 | Verify field exclusion logic at form level | Accessing form.fields['artwork'] raises KeyError for profile/site_asset types; no field pollution | Pass |

---

### US003: Add Artwork to Cart - Backend

#### Test Add to Cart Functionality (Backend)

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Add an artwork to the cart via API | API returns success response, and cart updates in the database | Pass |
| 2 | Add the same artwork again via API | API increments the quantity in the database | Pass |
| 3 | Remove an artwork from the cart via API | API returns success response, and the item is removed from the database | Pass |
| 4 | Update the quantity of an artwork via API | API updates the quantity in the database | Pass |
| 5 | Attempt to add more than available stock via API | API returns error response, and quantity does not exceed stock | Pass |

---

### US004: Checkout with Address Form

#### Test Checkout Functionality

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Submit checkout form via API with valid data | API returns success response, and order is created in the database | Pass |
| 2 | Submit checkout form via API with missing fields | API returns error response with validation messages | Pass |
| 3 | Submit checkout form via API with invalid address | API returns error response with validation messages | Pass |
| 4 | Submit checkout form via API with valid address | API returns success response, and address is saved in the database | Pass |

---

### User Registration Fix (4.1, 4.4) - Backend

#### Test Registration Atomicity and Email Dispatch

Requires the dev environment running (`./dev.sh start`) with MailDev accessible at http://localhost:1080.

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Navigate to http://localhost:8000/profiles/signup/ | Signup page loads with signup, profile photo, and address forms | Pass |
| 2 | Fill all required signup fields (username, email, password, first name, last name) and submit without a profile photo | Registration completes successfully — photo is optional and must not block submission | Pass |
| 3 | After successful submission, open MailDev at http://localhost:1080 | A "Your Email Verification Code" email is present for the registered email address, confirming `send_verification_email()` was called | Pass |
| 4 | Note the 6-digit verification code from the email | Code is a zero-padded 6-digit number (e.g., 047821) | Pass |
| 5 | Open the Django shell and run: `from pointless_impressions_src.account.models import CustomUser; u = CustomUser.objects.latest('date_joined'); print(u.is_active)` | Returns `False` — the user is inactive until email is verified | Pass |
| 6 | Check that related records exist: `from pointless_impressions_src.profiles.models import UserProfile, Customer; print(UserProfile.objects.filter(user=u).exists(), Customer.objects.filter(user_profile__user=u).exists())` | Returns `True True` — UserProfile and Customer records were created atomically alongside the user | Pass |
| 7 | Simulate a failed signup by temporarily disconnecting the database mid-transaction (or by checking that no orphan `CustomUser` record exists after a validation error on a later form field) | If any form fails validation, no user, profile, customer, or address record is created — the transaction rolls back completely | Pass |
| 8 | With email sending configured, verify `EmailVerificationCode` record was created: `from pointless_impressions_src.account.models import EmailVerificationCode; print(EmailVerificationCode.objects.filter(user=u).count())` | Returns `1` — exactly one unused verification code exists for the new user | Pass |

---

### Cart Interactivity Fix (1.1) - Backend

#### Test Cart Update and Remove Endpoints

Use `./dev.sh shell` or a REST client (e.g. curl/Postman) to call the endpoints directly. Requires at least one item already in the cart session.

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | POST to `/checkout/update/` with `X-Requested-With: XMLHttpRequest`, valid CSRF token, and FormData containing `artwork_id`, `quantity=2`, `framing_option` | Returns `{"success": true, "message": "..."}` and the cart session is updated with the new quantity | Pass |
| 2 | POST to `/checkout/update/` with a quantity exceeding available stock | Returns `{"success": false, "error": "..."}` — cart quantity is not changed | Pass |
| 3 | POST to `/checkout/update/` with a missing `artwork_id` | Returns an error response — no change to cart | Pass |
| 4 | POST to `/checkout/remove-item/` with `X-Requested-With: XMLHttpRequest`, valid CSRF token, and JSON body `{"artwork_id": <id>}` | Returns `{"success": true}` and the item is removed from the cart session | Pass |
| 5 | POST to `/checkout/remove-item/` with an `artwork_id` not in the cart | Returns an error or success response gracefully — no server 500 | Pass |

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

---

### US003: Add Artwork to Cart

#### Test Add to Cart Functionality

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Open the cart page | Cart page loads successfully with all elements visible | Pass |
| 2 | Add an artwork to the cart | Artwork is added to the cart, and the cart updates correctly | Pass |
| 3 | Add the same artwork again | Quantity of the artwork in the cart increments | Pass |
| 4 | Add multiple different artworks | All artworks are added to the cart with correct quantities | Pass |
| 5 | Remove an artwork from the cart | Artwork is removed, and the cart updates correctly | Pass |
| 6 | Update the quantity of an artwork | Quantity updates correctly, and total price recalculates | Pass |
| 7 | Attempt to add more than available stock | Error message displays, and quantity does not exceed stock | Pass |
| 8 | Verify cart persistence after page reload | Cart retains all items and quantities after reload | Pass |

---

### US004: Checkout with Address Form

#### Test Checkout Functionality

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Open the checkout page | Checkout page loads successfully with all elements visible | Pass |
| 2 | Fill in the address form with valid data | Form validates successfully, and the next step is enabled | Pass |
| 3 | Submit the form with missing fields | Form displays validation errors for required fields | Pass |
| 4 | Submit the form with invalid address | Form displays validation errors for address fields | Pass |
| 5 | Submit the form with valid address | Form submits successfully, and confirmation page is displayed | Pass |

---

### User Registration Fix (4.1, 4.4) - Frontend

#### Test Registration and Email Verification Flow

Requires the dev environment running (`./dev.sh start`) with MailDev accessible at http://localhost:1080.

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Navigate to http://localhost:8000/profiles/signup/ as an unauthenticated user | Signup page loads with three form sections: account details, profile photo (optional), and address | Pass |
| 2 | Submit the form with all required fields filled and no profile photo | Registration succeeds — page redirects to the email verification page at `/profiles/verify-email/` with a success message | Pass |
| 3 | Open MailDev at http://localhost:1080 and check inbox | A "Your Email Verification Code" email is present for the registered address within a few seconds of submission | Pass |
| 4 | On the email verification page, enter the correct 6-digit code from the MailDev email | Page redirects to the dashboard; success message "Your email has been verified!" displays | Pass |
| 5 | Open MailDev again after successful verification | A "Your Email Has Been Verified!" confirmation email is present in the inbox | Pass |
| 6 | Return to the verification page after already verifying (`/profiles/verify-email/`) | Redirect or error message displays — the user cannot re-verify an already verified account | Pass |
| 7 | On the email verification page, enter an incorrect or expired code | Error message displays (e.g., "Invalid verification code.") — the user remains on the verify email page | Pass |
| 8 | Click "Resend code" on the verification page | A new code email arrives in MailDev; the previous code is invalidated | Pass |
| 9 | Submit the signup form with a required field missing (e.g., no email address) | Form re-renders with field-level validation error; no user is created; no verification email is sent | Pass |
| 10 | Submit the signup form with a duplicate username or email already in the database | Form re-renders with a validation error on the relevant field; no duplicate user is created | Pass |

---

### Cart Interactivity Fix (1.1) - Frontend

#### Test Cart Quantity Controls and Remove Item

Requires the dev environment running (`./dev.sh start`) with at least one artwork in the cart. Navigate to http://localhost:8000/checkout/ to see the cart summary with forms.

| Step | Action | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| 1 | Navigate to http://localhost:8000/checkout/ with one or more items in the cart | Checkout page loads showing cart summary with quantity controls (– and + buttons), an Update button, and a Remove button for each item | Pass |
| 2 | Click the **–** button on a cart item that has quantity 2 | Quantity input decrements to 1 | Pass |
| 3 | Click the **–** button on a cart item that already shows quantity 1 | Quantity input stays at 1 — it cannot go below 1 | Pass |
| 4 | Click the **+** button on a cart item | Quantity input increments by 1 | Pass |
| 5 | Click **Update** on a cart item after changing the quantity | Page reloads; cart summary reflects the new quantity and updated subtotal/grand total | Pass |
| 6 | Change the framing option dropdown on a cart item and click **Update** | Page reloads; cart summary reflects the new framing selection | Pass |
| 7 | Click **Remove** on a cart item | Page reloads; the item is no longer shown in the cart summary; totals update accordingly | Pass |
| 8 | Remove the last item in the cart | Page reloads showing an empty cart message | Pass |
| 9 | Open the browser developer tools console before clicking **Update** or **Remove** | No JavaScript errors appear in the console during or after the operation | Pass |
| 10 | Click **Update** with no changes to quantity or framing | Page reloads without error — a no-op update is handled gracefully | Pass |

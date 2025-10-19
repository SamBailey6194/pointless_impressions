# Pointless Impressions User Stories Backlog

---

## Table of Contents

- [Pointless Impressions User Stories Backlog](#pointless-impressions-user-stories-backlog)
  - [Table of Contents](#table-of-contents)
  - [US001: Browse Available Artwork](#us001-browse-available-artwork)
  - [US002: View Artwork Details](#us002-view-artwork-details)
  - [US003: Add Artwork to Cart](#us003-add-artwork-to-cart)
  - [US004: Checkout with Address Form](#us004-checkout-with-address-form)
  - [US005: Pay Securely with Stripe](#us005-pay-securely-with-stripe)
  - [US006: Track Order via Unique Link](#us006-track-order-via-unique-link)
  - [US007: Register and Manage Account](#us007-register-and-manage-account)
  - [US008: Admin Upload and Manage Artwork](#us008-admin-upload-and-manage-artwork)
  - [US009: Edit About Page Content](#us009-edit-about-page-content)
  - [US010: Write and Publish Blog Posts](#us010-write-and-publish-blog-posts)
  - [US011: Integrate Facebook Marketing](#us011-integrate-facebook-marketing)
  - [US012: Mailchimp Newsletter Signup](#us012-mailchimp-newsletter-signup)
  - [US013: Order Confirmation and Email Notifications](#us013-order-confirmation-and-email-notifications)
  - [US014: Responsive and Accessible Design](#us014-responsive-and-accessible-design)

---

## US001: Browse Available Artwork
**Description:**  
As a customer,  
I want to browse available pointillism artwork,  
so that I can view what is currently for sale.  

**Acceptance Criteria:**  
- Display artwork with title, image, price, and short description.  
- Option to sort artwork by price, artist, or date added.  
- Works marked as "sold out" are clearly displayed as unavailable.  

**Tasks:**  
- Create Artwork model in Django.  
- Build view and template for artwork listing page.  
- Apply TailwindCSS styling for responsive grid layout.  
- Add filtering and sorting using JavaScript.  

**MoSCoW:** Must Have  
**Story Points:** 5  

---

## US002: View Artwork Details
**Description:**  
As a customer,  
I want to view detailed information about an artwork,  
so that I can decide whether to purchase it.  

**Acceptance Criteria:**  
- Clicking an artwork shows full details: larger image, title, description, size, price, and availability.  
- Display “Add to Cart” button if available.  
- Include related artworks section.  

**Tasks:**  
- Create artwork detail view and template.  
- Implement URL routing for artwork detail pages.  
- Add TailwindCSS styling and image zoom/expand.  

**MoSCoW:** Must Have  
**Story Points:** 3  

---

## US003: Add Artwork to Cart
**Description:**  
As a customer,  
I want to add artwork to a shopping cart,  
so that I can review and purchase it later.  

**Acceptance Criteria:**  
- “Add to Cart” button adds selected artwork to session/cart.  
- Cart shows item name, price, and total.  
- Prevent adding sold-out items.  

**Tasks:**  
- Implement cart functionality using Django sessions.  
- Build cart page with update/remove options.  
- Use JavaScript for real-time cart updates.  

**MoSCoW:** Must Have  
**Story Points:** 5  

---

## US004: Checkout with Address Form
**Description:**  
As a customer,  
I want to enter my shipping address during checkout,  
so that I can receive my physical artwork.  

**Acceptance Criteria:**  
- Checkout form includes name, email, address, and phone number.  
- Validation for required fields.  
- Saved addresses for logged-in users.  

**Tasks:**  
- Create Django form for shipping details.  
- Connect address form to order model.  
- Apply TailwindCSS form styling.  

**MoSCoW:** Must Have  
**Story Points:** 5  

---

## US005: Pay Securely with Stripe
**Description:**  
As a customer,  
I want to pay securely online using Stripe,  
so that my payment details are protected.  

**Acceptance Criteria:**  
- Stripe integrated at checkout.  
- Display payment success or failure message.  
- Orders marked as “paid” once successful.  

**Tasks:**  
- Integrate Stripe payment API in Django.  
- Add webhook to update order status.  
- Create confirmation page and email receipt.  

**MoSCoW:** Must Have  
**Story Points:** 8  

---

## US006: Track Order via Unique Link
**Description:**  
As an unregistered customer,  
I want to receive a unique order tracking link,  
so that I can monitor my order’s progress without logging in.  

**Acceptance Criteria:**  
- Generate unique tracking URL per order.  
- Show order status and estimated delivery.  
- Only accessible to customer who placed the order.  

**Tasks:**  
- Create token-based tracking system.  
- Add email confirmation with tracking link.  
- Build order tracking page.  

**MoSCoW:** Must Have  
**Story Points:** 8  

---

## US007: Register and Manage Account
**Description:**  
As a customer,  
I want to register for an account,  
so that I can view my order history and manage my information.  

**Acceptance Criteria:**  
- Registration, login, and logout functionality.  
- Profile page to edit personal info.  
- View order history for past purchases.  

**Tasks:**  
- Use Django’s built-in authentication system.  
- Create profile model and views.  
- Add TailwindCSS UI for account pages.  

**MoSCoW:** Must Have  
**Story Points:** 8  

---

## US008: Admin Upload and Manage Artwork
**Description:**  
As an admin,  
I want to upload, edit, or remove artwork,  
so that I can manage the store’s inventory.  

**Acceptance Criteria:**  
- Admin dashboard with CRUD functionality for artwork.  
- Option to mark artwork as “sold out”.  
- Only accessible to admin users.  

**Tasks:**  
- Create admin views or extend Django Admin.  
- Build upload form for images and details.  
- Apply permissions and access control.  

**MoSCoW:** Must Have  
**Story Points:** 8  

---

## US009: Edit About Page Content
**Description:**  
As an admin,  
I want to edit the About page,  
so that I can update information about the artist and process.  

**Acceptance Criteria:**  
- WYSIWYG editor for text and image content.  
- Changes reflect immediately on front-end.  
- Only admin users can access this feature.  

**Tasks:**  
- Create About model and editable view.  
- Integrate a rich text editor (e.g., TinyMCE).  
- Restrict access to superusers/admins.  

**MoSCoW:** Should Have  
**Story Points:** 5  

---

## US010: Write and Publish Blog Posts
**Description:**  
As an admin,  
I want to write and publish blog posts,  
so that I can share insights and inspirations behind my art.  

**Acceptance Criteria:**  
- Blog section visible to all users.  
- Ability to create, edit, and delete posts.  
- Blog posts sorted by date published.  

**Tasks:**  
- Create Blog model and CRUD admin views.  
- Display blog feed and detail pages.  
- Add TailwindCSS layout for posts.  

**MoSCoW:** Should Have  
**Story Points:** 8  

---

## US011: Integrate Facebook Marketing
**Description:**  
As an admin,  
I want to integrate Facebook tracking,  
so that I can monitor conversions and reach.  

**Acceptance Criteria:**  
- Facebook Pixel integrated into site.  
- Track key events (view, add to cart, purchase).  

**Tasks:**  
- Add Facebook Pixel to base template.  
- Test event tracking in sandbox.  

**MoSCoW:** Should Have  
**Story Points:** 3  

---

## US012: Mailchimp Newsletter Signup
**Description:**  
As a customer,  
I want to sign up for a newsletter,  
so that I can receive updates and promotions.  

**Acceptance Criteria:**  
- Mailchimp form embedded or API-integrated.  
- Confirmation message after signup.  
- Data securely stored in Mailchimp list.  

**Tasks:**  
- Embed Mailchimp signup form on site.  
- Style form with TailwindCSS.  
- Test integration and GDPR compliance.  

**MoSCoW:** Should Have  
**Story Points:** 3  

---

## US013: Order Confirmation and Email Notifications
**Description:**  
As a customer,  
I want to receive order confirmation and updates via email,  
so that I know my purchase is being processed.  

**Acceptance Criteria:**  
- Email sent on order confirmation, payment success, and dispatch.  
- Email includes artwork details and tracking link.  

**Tasks:**  
- Configure Django email backend.  
- Design HTML email templates.  
- Trigger email notifications on order status changes.  

**MoSCoW:** Must Have  
**Story Points:** 5  

---

## US014: Responsive and Accessible Design
**Description:**  
As a customer,  
I want the website to be mobile-friendly and accessible,  
so that I can browse and purchase on any device.  

**Acceptance Criteria:**  
- Fully responsive across devices.  
- Meets WCAG AA accessibility standards.  

**Tasks:**  
- Test responsiveness using TailwindCSS utilities.  
- Run accessibility audit.  

**MoSCoW:** Must Have  
**Story Points:** 5  

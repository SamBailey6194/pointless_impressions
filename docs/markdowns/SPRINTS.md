# Pointless Impressions Sprints

---

## Table of Contents

- [Pointless Impressions Sprints](#pointless-impressions-sprints)
  - [Table of Contents](#table-of-contents)
  - [Sprint 1: Core Setup \& Artwork Display (11 points)](#sprint-1-core-setup--artwork-display-11-points)
  - [Sprint 2: Cart \& Checkout (11 points)](#sprint-2-cart--checkout-11-points)
  - [Sprint 3: Stripe Payments \& Order Confirmation (11 points)](#sprint-3-stripe-payments--order-confirmation-11-points)
  - [Sprint 4: User Accounts \& Order Tracking (11 points)](#sprint-4-user-accounts--order-tracking-11-points)
  - [Sprint 5: Full Order Tracking \& Admin Content Management (11 points)](#sprint-5-full-order-tracking--admin-content-management-11-points)
  - [Sprint 6: Blog \& Marketing Integrations (11 points)](#sprint-6-blog--marketing-integrations-11-points)
  - [Sprint 7: Newsletter \& Accessibility Polish (11 points)](#sprint-7-newsletter--accessibility-polish-11-points)

---

## Sprint 1: Core Setup & Artwork Display (11 points)
**Goal:** Set up the project foundation and let users browse and view artwork.  

**Included User Stories:**  
- US001: Browse Available Artwork — 5 pts  
- US002: View Artwork Details — 3 pts  
- US008 (partial): Admin Upload (Backend only) — 3 pts  

**Total:** 11 pts  

**Focus:**  
- Initialise Django project and PostgreSQL database.  
- Create Artwork model and admin panel for uploads.  
- Implement artwork list and detail pages with TailwindCSS styling.  

---

## Sprint 2: Cart & Checkout (11 points)
**Goal:** Enable customers to select artwork, view cart contents, and enter address details for checkout.  

**Included User Stories:**  
- US003: Add Artwork to Cart — 5 pts  
- US004: Checkout with Address Form — 5 pts  
- 1 pt buffer for bug fixes and validation logic.  

**Total:** 11 pts  

**Focus:**  
- Implement session-based cart logic.  
- Build checkout form for name, address, and contact details.  
- Validate fields and apply responsive Tailwind styling.  

---

## Sprint 3: Stripe Payments & Order Confirmation (11 points)
**Goal:** Process secure payments and send confirmation emails after successful orders.  

**Included User Stories:**  
- US005: Pay Securely with Stripe — 8 pts  
- US013 (partial): Order Confirmation (Email only) — 3 pts  

**Total:** 11 pts  

**Focus:**  
- Integrate Stripe for payment processing and webhooks.  
- Update order status upon successful payment.  
- Send confirmation email with basic details and receipt.  

---

## Sprint 4: User Accounts & Order Tracking (11 points)
**Goal:** Add account management for registered users and order tracking for guests.  

**Included User Stories:**  
- US007: Register and Manage Account — 8 pts  
- US006 (partial): Track Order via Unique Link (Backend) — 3 pts  

**Total:** 11 pts  

**Focus:**  
- Set up user registration, login, logout, and profile editing.  
- Build backend logic for unique tracking links.  
- Secure all user data and restrict access appropriately.  

---

## Sprint 5: Full Order Tracking & Admin Content Management (11 points)
**Goal:** Complete guest order tracking and give admins control over the About page.  

**Included User Stories:**  
- US006 (remaining): Track Order Frontend Integration — 5 pts  
- US009: Edit About Page Content — 5 pts  
- 1 pt buffer for QA and testing.  

**Total:** 11 pts  

**Focus:**  
- Create frontend interface for order tracking via unique URLs.  
- Implement editable About page with WYSIWYG text editor.  
- Test admin permissions and edit workflows.  

---

## Sprint 6: Blog & Marketing Integrations (11 points)
**Goal:** Add blog publishing and marketing tools.  

**Included User Stories:**  
- US010: Write and Publish Blog Posts — 8 pts  
- US011: Integrate Facebook Marketing — 3 pts  

**Total:** 11 pts  

**Focus:**  
- Create blog model, list view, and detail view.  
- Add CRUD capabilities for admin blog posts.  
- Integrate Facebook Pixel for analytics.  

---

## Sprint 7: Newsletter & Accessibility Polish (11 points)
**Goal:** Complete marketing integration and ensure accessibility compliance.  

**Included User Stories:**  
- US012: Mailchimp Newsletter Signup — 3 pts  
- US014: Responsive and Accessible Design — 5 pts  
- US013 (remaining): Enhanced HTML Email Templates — 3 pts  

**Total:** 11 pts  

**Focus:**  
- Embed Mailchimp form and confirm GDPR compliance.  
- Finalise email templates for order updates.  
- Audit and fix responsiveness and accessibility issues.  

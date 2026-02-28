## Features 

Due to time constraints I haven't been able to post the screenshots for the features implemented.

Below are the features for the website and at the end is listed any features that weren't able to be implemented but would be with more time. Please note as this is a resubmission I have not changed the screenshots of the features as they are essentially the same with minor differences.

### SEO Features

I implemented a comprehensive SEO strategy directly within the Django `base.html` template to ensure every page is optimised for search engines and social media sharing. The following features have been implemented:

1. **Dynamic Meta Description**
   - Each page automatically generates a unique meta description based on the page type. Each description is truncated to **155 characters** for SEO best practices and uses `striptags` to remove HTML tags:
     - **Product pages:** Uses the product’s description.  
     - **Categories:** Uses the category description.  
     - **About Page:** Uses a custom description highlighting the company’s mission and values.  
     - **Other pages:** Uses a default description promoting the platform and its Pointillism art focus.  
   - Ensures search engines display accurate and relevant snippets in search results.

2. **Dynamic Page Titles**
   - Each page dynamically sets its `<title>` tag and uses `striptags` to remove HTML tags:
     - Product name for product pages.  
     - Category name for category pages.  
     - Custom titles for the About page and fallback for other pages.  
   - Improves SEO relevance and user click-through rates.

3. **Robots Control**
   - Public pages use `<meta name="robots" content="index, follow" />`.  
   - Private or sensitive pages (login, signup, checkout, account, admin) use `<meta name="robots" content="noindex, nofollow" />` to prevent indexing.  
   - Complemented with a `robots.txt` that references a `sitemap.xml` generated via [Sitemap Generator](https://www.xml-sitemaps.com/).

4. **Open Graph (OG) Tags**
   - OG tags are dynamically generated to optimise social media sharing:
     - **og:title:** Matches the page title dynamically.  
     - **og:description:** Matches the page description dynamically, truncated to **200 characters**, with `striptags` applied.  
     - **og:image:** Uses Cloudinary in production with auto-formatting (`f_webp`) for optimized WebP images; local media is used in development.  
     - **og:url:** Automatically set to the page’s absolute URL.  
     - **og:type:** Set as `website`.  
     - **og:site_name:** Set as `Pointless Impressions`.

5. **Canonical URLs**
   - Each page includes a `<link rel="canonical">` pointing to the current absolute URL.  
   - Prevents duplicate content issues by signalling the preferred URL to search engines.

6. **Responsive Meta Tags**
   - `<meta charset="UTF-8" />` ensures proper character encoding.  
   - `<meta name="viewport" content="width=device-width, initial-scale=1.0" />` ensures mobile-friendly, responsive design.

7. **Centralised Management**
   - All SEO-related tags are defined in `base.html` with blocks for overriding if needed:
     - `meta` block for all meta tags.
     - `meta_description` for dynamic descriptions.
     - `meta_robots` for dynamic robots control. 
     - `meta_og_tags` block for Open Graph tags.  
     - `extra_meta` block for page-specific tags like noindex or canonical overrides.

8. **Sitemap and Robot.txt**:
    - A `robots.txt` file is included to guide search engine crawlers.  
    - Using `django.contrib.sitemaps`, a dynamic `sitemap.xml` is generated to list all public URLs for better indexing. It can be accessed at `/sitemap.xml`.

**Result:** Every page of Pointless Impressions is optimised for search engines, social media sharing, and user experience, while sensitive pages are protected from indexing. This setup reduces maintenance overhead by centralising SEO logic in a single template.

### Payments Feature

Due to the client having an existing Square account with a subscription already set up, I integrated Square payments into the checkout process. This allows users to securely complete their purchases using Square's payment gateway, ensuring compliance with payment regulations and providing a seamless checkout experience. The features are listed in the next section.

### Existing Features

#### Header & Navigation (Responsive Navbar)

**Desktop View:**
- **Logo**: Clickable Pointless Impressions logo (top-left) with fallback text branding
- **Primary Navigation Menu** (visible on md+ screens):
  - Home, Shop (with dropdown: Categories, Framing Options, Artists)
  - Each link styled with hover states (yellow background, black text)
- **Search Button**: Top-right icon button with "Search" label (visible on desktop)
- **Account Dropdown**: Profile picture if authenticated, user icon if guest; expandable menu showing profile options
- **Cart Dropdown**: Shows item count badge and subtotal (expandable)
- **Responsive Grid Layout**: Items evenly distributed with navbar-start/center/end sections

**Mobile View:**
- **Hamburger Menu**: Collapsible navigation drawer revealing Shop
- **Logo**: Scaled appropriately for smaller screens
- **Search Icon**: Visible in mobile menu, integrated with search functionality
- **Account/Cart Buttons**: Positioned in navbar-end, accessible without hamburger
- **Touch-Friendly**: Larger tap targets, stacked layout for readability

**Authentication States:**
- **Logged In**: Shows user profile picture, username in dropdown, "Profile" and "Logout" options
- **Guest**: Shows generic user icon, "Login" and "Signup" options in dropdown
- **Authenticated Features Unlock**: Account menu expands with profile dashboard links

**User Interactions:**
- Hover effects on navigation items (yellow highlight with smooth transitions)
- Dropdown menus expand/collapse on click
- Search button triggers search modal/page
- Cart button shows mini-cart preview with quick access to checkout
- Account menu shows recent orders and quick links

**Cart Dropdown in Header:**
- The cart icon in the header displays a badge with the current item count and subtotal.
- Clicking the cart icon reveals a dropdown showing all cart items in a table with image, name, quantity, and price.
- Users can quickly review their cart contents and subtotal without leaving the current page.
- The dropdown updates instantly after any cart change (add, update, remove) via AJAX.
- Clicking "View Cart" in the dropdown takes the user directly to the checkout page.

---

#### Footer

**Content Sections (Responsive Grid):**
- **Newsletter Signup**: Email subscription form with validation, success confirmation via toast
- **Company Info**: Logo, brand description ("Discover unique Pointillism artwork..."), social links placeholder
- **Quick Links**: Home and Shop links
- **Branding**: Uses --pointless-blue, --pointless-yellow brand colors

**Features:**
- **Responsive Layout**: Stacks vertically on mobile (md:grid-cols-3 on tablet+)
- **Dark Mode Support**: Adapts colors for light/dark themes
- **Newsletter Integration**: Email validation, success toasts on subscription
- **Social Media Icons**: Facebook link sends user to Pointless Impressions Facebook page
- **Accessibility**: Semantic HTML, proper link structure

---

#### Homepage

**Hero Section:**
- **Headline**: "Welcome to Pointless Impressions" (responsive font sizes: md:text-5xl)
- **Subheading**: "Discover unique Pointillism artwork from talented artists..."
- **CTA Button**: "Browse Art" linking to artwork list page
- **Background**: Section-alt styling with custom brand colors

**Featured Artwork Carousel:**
- **Horizontal Scrolling**: Snap-scroll carousel with 6-8 featured artworks
- **Card Design**: 
  - Artwork image (400x300px with Cloudinary optimization for production)
  - Title, artist name, category, description (truncated)
  - Price displayed prominently
  - Action buttons: "View More Category", "View More by Artist", "Details"
- **Navigation**: Previous/Next buttons (❮ ❯) for manual carousel control
- **Responsive Sizing**: w-72 (mobile), md:w-80, lg:w-96 for adaptive card widths
- **Hover Effects**: Shadow transitions on card hover

**Interaction Features:**
- Carousel auto-scrolls smoothly
- Click artwork card → Details page
- Click "View More Category" → Artwork list pre-filtered by category
- Click "View More by Artist" → Artwork list pre-filtered by artist
- Mobile: Swipe/scroll to navigate carousel
- Desktop: Use arrow buttons or scroll with mouse

---

#### Artwork List Page

**Filter Panel (Collapsible on Mobile):**
- **Category Filter**: Dropdown with all artwork categories
- **Framing Condition Filter**: Dropdown for framing options
- **Artist Filter**: Dropdown listing all artists
- **Price Range**: Min and Max price number inputs with validation
- **Availability**: "Available Only" checkbox to filter out sold-out items
- **Apply/Clear Buttons**: Submit filters or reset to defaults
- **Active Indicators**: Selected filters highlight for visibility

**Sort Controls:**
- **Sort by Lowest Price**: Ascending price order
- **Sort by Highest Price**: Descending price order
- **Sort Alphabetically by Name**: A-Z artwork names
- **Sort by Artist**: A-Z artist names
- **Active Sort Display**: Current sort button highlighted in primary color

**Artwork Grid:**
- **Layout**: 1 column (mobile), 2 columns (md), 3 columns (lg)
- **Cards Display**: 
  - Artwork image (optimized, lazy-loaded)
  - Title, artist link, description (15-word truncation)
  - Price in bold
  - "Add to Cart" button (if in stock)
  - "Details" link
  - Stock status (green "Available" or red "Sold Out" badge)
- **Hover Effects**: Shadow lift, slight scale on card hover
- **Click Handlers**: Add to cart triggers modal, details opens artwork detail page

**Pagination:**
- Page numbers with current page highlighted
- Previous/Next navigation
- Responsive pagination controls (stacked on mobile)

**Empty State:**
- Large icon, "No artworks found" message
- Helper text: "Try adjusting your filters..."
- "Clear Filters" button for quick reset

**SSR + AJAX Integration:**
- Initial page load uses server-side rendering (full HTML)
- Filters/sorts trigger AJAX requests to API endpoint
- JavaScript dynamically updates artwork grid without page reload
- Maintains URL query parameters for bookmarking

---

#### Artwork Detail Page

**Breadcrumb Navigation:**
- Home > Artworks > [Artwork Name]
- Helps users understand page hierarchy and navigate back

**Image Carousel:**
- **Main Display**: Large image (400px+ height) with Cloudinary optimization
- **Thumbnail Navigation**: Row of small preview images (w-16 h-16)
- **Navigation Controls**: Previous/Next arrow buttons on carousel
- **Click Thumbnail**: Jumps to that image in main carousel
- **Arrow Navigation**: Cycle through images sequentially
- **Mobile Responsive**: Maintains aspect ratio, scrollable thumbnails

**Product Information Section:**
- **Title & Category**: Large heading with category badge (linked to filtered list)
- **Stock Status**: 
  - Green alert: "Available" with check icon
  - Red alert: "Sold Out" with warning icon
- **Price Display**: Large bold £ amount
- **Description Card**: Full product description in prose format
- **Details Card**:
  - Artist name (clickable link to artist's other artworks)
  - Artist info snippet
  - Category (clickable filter link)
  - Framing options (linked to pre-filtered list)
  - Rating display (star visualization, average rating, review count)
- **Review Section**:
  - "Write Review" button (if authenticated) → opens review modal
  - "Login to Review" link (if guest)
  - "View Reviews" button (if reviews exist) → scrolls to reviews section
  - Reviews list below with rating, title, author, date, comment

**Action Buttons:**
- **Add to Cart** (if in stock): Primary button, opens add-to-cart modal
- **Out of Stock**: Disabled button (if sold out)
- **Back to Browse**: Secondary button returning to artwork list with previous filters

**Related Artworks Section:**
- **Title**: "Other Artwork by [Artist Name]"
- **Carousel**: Same structure as homepage carousel
- Shows 4-6 similar artworks from same artist
- Clickable cards linking to their detail pages
- Button that links to full artist's artwork list
- **Title**: "Other [Category Name] Artwork"
- **Carousel**: Same structure as above
- Shows 4-6 similar artworks from same category
- Clickable cards linking to their detail pages
- Button that links to full category artwork list

**Desktop View:**
- Two-column layout: Images (left 50%), Details (right 50%)
- Sticky details sidebar (doesn't scroll out of view)
- All sections visible without scrolling

**Mobile View:**
- Single-column stack: Images (top), then details (bottom)
- Details scroll naturally
- Buttons full-width for easy tapping

**Add To Cart Form**
- Form is on the page with quantity, framing options and notes
- "Add to Cart" button triggers adding to cart and scrolling to top with toast notification and cart dropdown update

---

#### Checkout Page

**Order Summary Panel:**
- Displays all cart items in a table with image, name, quantity, framing option, and price.
- Subtotal, delivery info, and total are clearly shown and update dynamically.
- Delivery information is stacked vertically and offset to the right for clarity.

**Editable Cart Items:**
- Users can update quantity and framing option directly in the order summary.
- Quantity input is validated: cannot exceed available stock, cannot go below 1, and setting to 0 removes the item.
- Framing option is a dropdown populated with available choices for each artwork.
- "Update" button triggers AJAX update; changes are reflected immediately without page reload.
- "Remove" button allows users to delete items from the cart instantly.

**Cart Synchronization:**
- Cart is stored in cookies session id
- It updates via AJAX to keep backend and frontend in sync.

**AJAX Integration:**
- All cart updates (quantity, framing, removal) use AJAX for a seamless user experience.
- Order summary and cart dropdown update in real time after any change.

**Validation & Error Handling:**
- Quantity and framing option are validated both client-side and server-side.
- Error messages are displayed via toast notifications for invalid actions (e.g., exceeding stock).

**Checkout Actions:**
- Checkout form is displayed below order summary.
- Guest and Authentiticated users need to fill in necessary details.
- When they click to pay it opens a confirm order modal to finalise the order.
- If they confirm it scrolls to top of the modal and shows a spinner while processing the order.
- Once processed, user is redirected to order confirmation page.
- If they are in a region that requires SCA compliance the modal closes and the button on the checkout form has a spinning shield icon then the SCA confirmation appears for the user to complete, the checkout form button then becomes a spinner.
- If all is a success they are redirected to the order confirmation page.
- If an error occurs during order processing, an error toast notification is displayed and the user remains on the checkout page to correct any issues.
- If the payment goes through the order gets stored on the PaymentRecovery model.

**Security & SEO:**
- Checkout page uses `<meta name="robots" content="noindex, nofollow" />` to prevent indexing.
- All sensitive actions are protected by CSRF tokens and session validation.

**Accessibility & Responsiveness:**
- Fully responsive layout for mobile and desktop.
- All form controls are accessible via keyboard and screen readers.
- Clear focus states and error indicators for all inputs.

---

### Additional Features

#### Email Templates
- **Order Confirmation for Guests**: Sends an email confirmation for guest orders. This grants them access to track their order.
- **Email Verified Confirmation**: Notifies users when their email is successfully verified.
- **Verification Email**: Sends a verification email to users upon registration.
- **Order Confirmation for Authenticated Users**: Sends an email confirmation for orders placed by logged-in users. Has a button that takes them to their user profile dashboard to track their order.

#### Error Templates
- Custom error pages for various HTTP status codes:
  - `400.html`: Bad Request
  - `401.html`: Unauthorized
  - `403.html`: Forbidden
  - `404.html`: Not Found
  - `408.html`: Request Timeout
  - `500.html`: Internal Server Error
  - `502.html`: Bad Gateway
  - `503.html`: Service Unavailable

#### Dashboard App
- **Admin Dashboard**: Provides an interface for managing artworks, orders, and users.
- **User Profile Dashboard**: Allows users to view and manage their profile details. They can manage their orders and see order history, all cancelled orders are hidden.
- **Guest Order Dashboard**: Enables guests to track their orders.
- **Modals for Admin Actions**:
  - Edit Artwork
  - Add Artwork
  - Delete Artwork
  - Edit Order
  - Delete Order
  - Update Order

#### Profiles App
- **User Profiles**: Stores user-specific information, including addresses and preferences.
- **Admin Features**: Allows management of user roles and approvals for artists.
- **Signals**: Handles events like profile creation upon user registration.
- **Fixtures**: Predefined data for testing profiles and addresses.
- **Authentication** Features: Login, logout, signup, and email verification.

#### Square Integration with SCA
- **Secure Payments**: Integrated Square API for processing payments with Strong Customer Authentication (SCA).
- **Order Confirmation**: Ensures payment details are securely handled and confirmed.
- **Error Handling**: Custom logic to manage Square API errors, ensuring a seamless user experience.
- **Testing**: Comprehensive tests to validate payment workflows and error scenarios.

---

#### Toast Notification System

**Architecture:**
- **Frontend Module**: `toasts.js` - Unified Toast class with all display logic
- **Backend Integration**: `toast.html` - Pure Django template passing SSR messages to Toast module
- **Load Order**: toasts.js loads first in `<head>` (defer), then toast.html included in body
- **Global Access**: `window.Toast` object provides methods for any JavaScript to trigger notifications

**Toast Methods:**

```javascript
// Basic display (type: 'success', 'error', 'info', 'warning')
Toast.show(message, type, duration)

// Convenience methods
Toast.success(message, duration = 3000)    // Green toast
Toast.error(message, duration = 4000)      // Red toast
Toast.info(message, duration = 3000)       // Blue toast
Toast.warning(message, duration = 3500)    // Yellow toast

// Framework integration
Toast.displayDjangoMessages(messages)      // Auto-converts SSR messages
Toast.handleAPIResponse(response)          // Extracts message from JSON
Toast.handleAPIError(error)                // Displays API error messages
```

**Toast Display Characteristics:**
- **Position**: Fixed top-right corner (top-4 right-4 z-50)
- **Stack**: Multiple toasts stack vertically with gap-2 spacing
- **Auto-Remove**: Toasts auto-dismiss after duration (success: 3s, error: 4s, info: 3s, warning: 3.5s)
- **Pointer Events**: Container has pointer-events-none, individual toasts pointer-events-auto for clickability
- **Styling**: DaisyUI alert components with Pointless brand colors

**Integration Points:**

1. **Django Messages (SSR):**
   ```python
   messages.success(request, 'Item added to cart!')
   # Auto-converts to Toast.success() on page load
   ```

2. **API Responses:**
   ```javascript
   fetch('/api/add-to-cart', {method: 'POST', body: formData})
     .then(response => Toast.handleAPIResponse(response))
   ```

3. **Manual Triggers:**
   ```javascript
   Toast.warning('This is a warning!');
   Toast.error('Something went wrong!');
   ```

**Message Types & Styling:**
- **Success** (Green): "Item added to cart!", "Order placed!", confirmations
- **Error** (Red): "Validation failed!", "Out of stock!", errors
- **Info** (Blue): "Loading...", informational messages
- **Warning** (Yellow): "Low stock available!", cautions

---

#### Integration Features

**SSR + API Hybrid Approach:**
- **Server-Side Rendering**: Initial page load renders full HTML for SEO and performance
- **AJAX Enhancements**: Filtering, sorting, pagination via API without full page reloads
- **Progressive Enhancement**: Works with JavaScript disabled (SSR fallback) or fully enhanced (API)

**Image Optimization:**
- **Development**: Local image URLs via Django media storage
- **Production**: Cloudinary with auto-formatting (format="auto"), quality optimization (quality="auto")
- **Responsive Images**: Width/height specifications for each context
- **Fallback Handling**: Placeholder icons for missing images

**Cart Persistence:**
- **Session/LocalStorage**: Cart persists across page navigations
- **Server Sync**: AJAX requests sync cart with server session
- **Real-time Updates**: Quantity changes reflected immediately in dropdown

**Search Functionality:**
- **Global Search**: Unified search across artworks categories
- **Autocomplete**: Tarekraafat autocomplete library provides suggestions as user types

---

### Example of Social Media Marketing

I used Facebook to make a page. Below are examples of the page.

![Facebook Page Screenshot](/docs/images/facebook_page.png)

![Facebook Posts Screenshot](/docs/images/facebook_posts.png)

### Features Left to Implement

Some of the features listed below have the backend structure in place but need frontend implementation or further refinement:

- Blog App with full CRUD functionality for posts and comments
- Adding and editing Addresses in User Profile
- Adding and editing profile picture in User Profile
- Adding and editing payment methods in User Profile
- Enabling people to sign up as Artists and sell their artwork on the platform
- Admin Dashboard Analytics with charts and graphs showing sales data, user registrations, and other key metrics
- About page content and styling
- Contact page with contact form and map integration
- When editing an artwork in the Admin Dashboard, the admin can see the images currently uploaded for that artwork and can delete them individually while also adding new images.
- Implementing unit and integration tests for critical components and features of the application to ensure reliability and maintainability.
- Some of the modals styling could be improved further to make them more visually appealing and user-friendly.
- Review system for Artwork to be reviewed by verified purchasers.
- Link the DB newsletter subscriptions to an actual email marketing service like Mailchimp. For now we are using the newsletter subscription in the footer to send to MailChimp.
- Enhancing accessibility features across the site to ensure compliance with WCAG standards, for example ensuring everything has a aria-label when required.
- Change size of PNGs to be smaller for faster loading times.

---
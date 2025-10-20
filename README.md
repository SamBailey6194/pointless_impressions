# Pointless Impressions

---

## Table of Contents

- [Pointless Impressions](#pointless-impressions)
  - [Table of Contents](#table-of-contents)
  - [Development Guide](#development-guide)
  - [Pointless Impressions](#pointless-impressions-1)
    - [Planning Process](#planning-process)
      - [Business Plan and User Stories](#business-plan-and-user-stories)
      - [Database Plan](#database-plan)
      - [Wireframes](#wireframes)
      - [Font and Colours](#font-and-colours)
        - [Colours](#colours)
      - [Fonts](#fonts)
  - [Features](#features)
    - [SEO Features](#seo-features)
    - [Existing Features](#existing-features)
      - [Navbar](#navbar)
    - [Features Left to Implement](#features-left-to-implement)
  - [Lessons Learnt](#lessons-learnt)
  - [Testing](#testing)
    - [Fixed Bugs](#fixed-bugs)
    - [Unfixed Bugs](#unfixed-bugs)
    - [Validator Testing](#validator-testing)
      - [Page Speed Insights](#page-speed-insights)
      - [HTML](#html)
      - [CSS](#css)
      - [JS](#js)
  - [Deployment](#deployment)
    - [Production Files](#production-files)
    - [Staging Files](#staging-files)
  - [Cloning](#cloning)
  - [Credits](#credits)

---

## Development Guide

Please read [Development Markdown](docs/markdowns/DEVELOPMENT.md) before developing.

---

## Pointless Impressions

### Planning Process

#### Business Plan and User Stories

The decision to make this website is due to the [B2C Business Plan](docs/markdowns/BUSINESSPLAN.md). Please note this has teh keywords for SEO in it as well.

This led to this [User Stories Backlog](docs/markdowns/USERSTORYBACKLOG.md) being made and agreed with the client.

You can also see how the user stories were made into [Sprints](docs/markdowns/SPRINTS.md).

As we progressed in the project some of the sprints were skipped due to time. You can see more in [Features](#features) section, especially [Features Left to Implement](#features-left-to-implement).

#### Database Plan

Following on from the Sprints the [Database Tables](docs/markdowns/DATABASEPLAN.md) were made, which then had the ERDs visually made.

![Visual ERDs](docs/images/pointless_impressions_visual_erds.png)

Then the flows of different users were generated.

**General Flow**

![General Flow](docs/images/pointless_impressions_general_flow.drawio.png)

**Signup Flow**

![Signup Flow](docs/images/pointless_impressions_signup_flow.drawio.png)

**Registered Customer Flow**

![Registered Customer Flow](docs/images/pointless_impressions_registered_customer_flow.drawio.png)

**Admin Flow**

![Admin Flow](docs/images/pointless_impressions_admin_flow.png)

#### Wireframes

Next the below wireframes were generated:

**Homepage**

![Homepage](docs/images/homepage.png)

**About**

![About](docs/images/about.png)

**Shop**

![Shop](docs/images/product_listing.png)

**Product Details**

![Product Details](docs/images/product_detail.png)

**Checkout**

![Checkout](docs/images/checkout.png)

**Account Profile**

![Account Profile](docs/images/account_profile.png)

**Blog Index**

![Blog Index](docs/images/blog_index.png)

**Blog Page**

![Blog Page](docs/images/blog_page.png)

There are other pages planned to do, but time was running out in the planning phase.

Other pages not done include:

1. Signup Form
2. Login Form
3. Logout Success
4. Order Change Request Form
5. Address Add Form
6. Admin Dashboard
7. Admin Add Art Form
8. Admin Update Art Form
9. Delete Art Success

Some of these will be models rather than full pages.

#### Font and Colours

##### Colours

- Logo Colours:
  - Bakground = #fbfcfc (Off-White)
  - Yellow = #fba419
  - Blue = #055187
  - Red = #ec381c
  - Black = #000301
- Header and Footer BG = #055187 (Blue)
- Header and Footer Text = #fbfcfc (Off-White)
- Background = #fbfcfc (Off-White)
- Headings = #000301 (Black)
- Body = #055187 (Blue) or #000301 (Black)
- Form Input BG = #fbfcfc (Off-White)
- Form Input Outline = #055187 (Blue)
- Form Input Placeholder = #05518780 (Blue 50% Opacity)
- Form Input Text = #000301 (Black)
- Buttons = #fba419 (Yellow)
- Buttons on Hover = #ec381c (Red)
- Button Outlines = #055187 (Blue)   
- Button Outlines Hover = #fba419 (Yellow)
- Modals BG = #000301 (Black)
- Modals Outline = #055187 (Blue)
- Modals Header = #fba419 (Yellow)
- Modals Body = #fbfcfc (Off-White)
- Modals Input BG = #fbfcfc (Off-White) 
- Modals input Outline = #055187 (Blue) 
- Modals Input Text = #000301 (Black)
- Modals Buttons = #fba419 (Yellow)
- Modals Buttons on Hover = #ec381c (Red)
- Modals Button Outlines = #055187 (Blue)
- Modals Button Outlines Hover = #fba419 (Yellow)

#### Fonts

- Header and Footer = Poppins
- Headings = Montserrat
- Body = Inter

As you venture to look at the [Features](#features) you will notice some design choices, flow and relationships between the database tables were changed while the project was being made.

![Responsive Image]()

---

## Features 

Below are the features for the website and at the end is listed any features that weren't able to be implemented but would be with more time. Please note as this is a resubmission I have not changed the screenshots of the features as they are essentially the same with minor differences.

### SEO Features

I implemented a comprehensive SEO strategy directly within the Django `base.html` template to ensure every page is optimised for search engines and social media sharing. The following features have been implemented:

1. **Dynamic Meta Description**
   - Each page automatically generates a unique meta description based on the page type. Each description is truncated to **155 characters** for SEO best practices and uses `striptags` to remove HTML tags:
     - **Product pages:** Uses the product’s description.  
     - **Blog posts:** Uses the post’s meta description.  
     - **Categories:** Uses the category description.  
     - **About Page:** Uses a custom description highlighting the company’s mission and values.  
     - **Other pages:** Uses a default description promoting the platform and its Pointillism art focus.  
   - Ensures search engines display accurate and relevant snippets in search results.

2. **Dynamic Page Titles**
   - Each page dynamically sets its `<title>` tag and uses `striptags` to remove HTML tags:
     - Product name for product pages.  
     - Post title for blog posts.  
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
     - **og:image:** Uses Cloudinary in production with auto-formatting (`f_auto`) for optimized WebP/AVIF images; local media is used in development.  
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

**Result:** Every page of Pointless Impressions is optimised for search engines, social media sharing, and user experience, while sensitive pages are protected from indexing. This setup reduces maintenance overhead by centralising SEO logic in a single template.

### Existing Features

#### Navbar

  - The navbar is dynamic for mobile and non mobile views.
  - The navbar is also dynamic depending on if a user is authenticated or not.


### Features Left to Implement

- Create

---

## Lessons Learnt

- For 

---

## Testing 

The website has been manually and automatically tested.

You can see the manual testing table [here](docs/markdowns/MANUALTESTING.md).

You can see the automatic testing table [here](docs/markdowns/AUTOMATICTESTING.md).

For TDD I used TestCase for Django and Jest for JavaScript

For BDD I used Behave for Django and Cypress for JavaScript

Please note for the Jest and Cypress testing there was a need to create html fixture files as Jest and Cypress don't always read the Django dynamic structure.

### Fixed Bugs

- **Tailwind build failure**: The `npm run dev` and `npm run build` commands were failing because the PostCSS scripts pointed to a non-existent `./src/style.css` file. Updated paths to the correct `src/css/styles.css` file.
- **Clean script issue**: The `rimraf` command in `package.json` was originally wiping folders instead of just their contents. Adjusted it to remove only files inside `static/css` and `static/js`, preserving the directories.
- **Development watcher errors**: Running `python manage.py tailwind start` previously threw `Input Error: You must pass a valid list of files to parse` because PostCSS couldn’t locate the source CSS file. This is now fixed with the correct path.
- **Environment isolation**: Development MailDev emails and Redis data were previously accessible from staging or production, which could interfere with live data. This is now fixed by ensuring MailDev only runs in development and each environment has its own Redis instance.

### Unfixed Bugs

- None

### Validator Testing 

#### Page Speed Insights

- You can click the link to see the results from 27th August in the evening.
- You can switch between the mobile and desktop results as well.
- The tests were only run for the unauthenticated users.

  - [Homepage results]()

#### HTML

- Homepage
  
![W3C validator - Homepage]()

#### CSS

- Due to using Django-Tailwind the Jigsaw validator had errors. 
- All errors were to do with the @layer, @property and so forth. Therefore, I deemed it was all valid.

 ![(Jigsaw) validator 1](docs/images/jigsaw_css_1.png)

#### JS

No errors were returned when passing through the official JS Hint, see images below for each page.

  - Alert JS
    
  ![JS Hint - Alert]()

---

## Deployment

The app deployed via Heroku [here]() following the steps documented in [Production Deployment using Docker Container](docs/markdowns/PRODUCTION.md).

It is important to note to simulate a real world environment I also deployed a staging version of the web app via Heroku [here]() and I followed the steps outlined in [Staging Deploymennt using Docker Container](docs/markdowns/STAGING.md)

As I used a Docker Contianer I set the Python Version and gunicorn in my relevant Docker related files:

### Production Files

1. [Dockerfile](Dockerfile.production)
2. [Dcoker Compose](docker-compose.production.yml)
3. [Entrypoint](pointless_impressions_src/production-entrypoint.sh)
4. [Env Example](.env.production.example)
5. [Production Settings](pointless_impressions_src/pointless_impressions/settings/production.py)

### Staging Files

1. [Dockerfile](Dockerfile.staging)
2. [Dcoker Compose](docker-compose.staging.yml)
3. [Entrypoint](pointless_impressions_src/staging-entrypoint.sh)
4. [Env Example](.env.staging.example)
5. [Production Settings](pointless_impressions_src/pointless_impressions/settings/staging.py)

---

## Cloning

At the top of this document is a link to the guide to clone to help with development.

Please follow this [Cloning and Development](docs/markdowns/DEVELOPMENT.md)

 
## Credits 

Below are my credits for where I got inspiration for some of the code and content

- To help me understand how to implement Docker with Django I used [Docker - Django and PostgreSQL setup (with uv) from scratch! by BugBytes](https://www.youtube.com/watch?v=37aNpE-9dD4&t=524s)
- To help improve my understanding of meta tage I looked at [Meta Tags Google Support](https://www.semrush.com/blog/meta-tag/?g_acctid=152-012-3634&g_adid=767193674768&g_adgroupid=149553965890&g_network=g&g_adtype=search&g_keyword=&g_keywordid=dsa-2185834090056&g_campaignid=18352326857&g_campaign=UK_SRCH_DSA_Blog_EN&kw=&cmp=UK_SRCH_DSA_Blog_EN&label=dsa_pagefeed&Network=g&Device=c&utm_content=767193674768&kwid=dsa-2185834090056&cmpid=18352326857&agpid=149553965890&BU=Core&extid=279889846583&adpos=&matchtype=&gad_source=1&gad_campaignid=18352326857&gclid=CjwKCAjwu9fHBhAWEiwAzGRC_-teJyIG_ANaSCkqwUocd1HZOJeb2tReI3nyEP6C-cOVMI71hg0U6BoCHtYQAvD_BwE)
- Keywords meta tag is no longer supported or encouraged for SEO, hence why they are minimally used. My source was [Semrush Article](https://www.semrush.com/blog/meta-keywords/?g_acctid=152-012-3634&g_adid=767053397457&g_adgroupid=149553965890&g_network=g&g_adtype=search&g_keyword=&g_keywordid=dsa-2185834090056&g_campaignid=18352326857&g_campaign=UK_SRCH_DSA_Blog_EN&kw=&cmp=UK_SRCH_DSA_Blog_EN&label=dsa_pagefeed&Network=g&Device=c&utm_content=767053397457&kwid=dsa-2185834090056&cmpid=18352326857&agpid=149553965890&BU=Core&extid=279966777342&adpos=&matchtype=&gad_source=1&gad_campaignid=18352326857&gclid=CjwKCAjwu9fHBhAWEiwAzGRC_24eTlVF0HbH8ahzdYsMy02RFznsJt5_Bkz_fcM2fByAM7rYrErlgBoC8bYQAvD_BwE)
- To underrstand striptags I used [Django Striptags Docs](https://docs.djangoproject.com/en/5.2/ref/templates/builtins/#striptags)

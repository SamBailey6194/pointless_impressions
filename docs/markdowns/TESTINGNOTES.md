## Testing 

The website has been manually and automatically tested.

You can see the manual testing table [here](docs/markdowns/MANUALTESTING.md).

You can see the automatic testing table [here](docs/markdowns/AUTOMATICTESTING.md).

**Important**: Due to time constraints only US001, US002, US003 and US008 Backend TDD and BDD tests were implemented. I also only noted down the manual tests for the same user stories. The importance of completing the project to a high standard was prioritised over completing all tests.

For TDD I used TestCase for Django and Jest for JavaScript

For BDD I used Behave for Python and Cypress for JavaScript.

Please note for the Jest testing there was a need to create html fixture files as Jest doesn't always read the Django dynamic structure.

**Important 2.0**: I did have Behave tests working previously. But after removing the local image calls to Cloudinary tags they were no longer working as the images were not being found. Due to time constraints I could not fix this issue. Therefore, I have removed the all the Behave tests. I also have removed cypress tests for the same reason.

### Fixed Bugs

- **Tailwind build failure**: The `npm run dev` and `npm run build` commands were failing because the PostCSS scripts pointed to a non-existent `./src/style.css` file. Updated paths to the correct `src/css/styles.css` file.
- **Clean script issue**: The `rimraf` command in `package.json` was originally wiping folders instead of just their contents. Adjusted it to remove only files inside `static/css` and `static/js`, preserving the directories.
- **Development watcher errors**: Running `python manage.py tailwind start` previously threw `Input Error: You must pass a valid list of files to parse` because PostCSS couldn't locate the source CSS file. This is now fixed with the correct path.
- **Environment isolation**: Development MailDev emails and Redis data were previously accessible from staging or production, which could interfere with live data. This is now fixed by ensuring MailDev only runs in development and each environment has its own Redis instance.
- **Complex CSS override battles**: Removed extensive DaisyUI override CSS (~400+ lines) that were fighting framework defaults with `!important` declarations and complex selectors. Simplified to use clean DaisyUI patterns with custom theming.
- **Navbar structure conflicts**: Fixed duplicate navbar classes where `base.html` had `<header class="navbar">` and `header.html` had redundant `<div class="navbar">` wrapper, causing layout conflicts and CSS selector mismatches.
- **CSS specificity wars**: Eliminated complex selector battles like `header.navbar .navbar-center` vs `.navbar .navbar-center` by restructuring HTML to align with DaisyUI's expected component hierarchy.
- **Mobile layout regressions**: After CSS refactoring, fixed mobile burger menu positioning, search button background, and account/cart buttons being pushed off-screen due to flexbox conflicts.
- **Indentation and structure hierarchy**: Corrected HTML indentation in `header.html` to properly reflect navbar-start/center/end relationship as direct children of navbar container.
- **Brand color inheritance**: Ensured Pointless Impressions brand colors (--pointless-yellow, --pointless-blue, --pointless-red) are properly applied to header, footer, buttons, and navigation elements instead of default DaisyUI colors.
- **Navigation hover states missing**: Added proper hover and active states for navigation menu items to display yellow background (`var(--pointless-yellow)`) with black text on hover, maintaining brand consistency.
- **Header syntax error**: Fixed missing quote in `header.html` (`<div class="w-full>`) that was causing template parsing issues.
- **Button styling inconsistency**: Standardized all buttons to use Pointless branding with yellow background, blue borders, and red hover states while maintaining DaisyUI component structure.
- **Search bar positioning**: Maintained desktop search bar on second level below main navigation while ensuring mobile search toggle functionality works correctly.
- **CSS compilation workflow**: Established proper workflow between source CSS (`theme/static_src/src/css/styles.css`) and compiled output (`static/css/styles.css`) to ensure changes are properly built and deployed.
- **Verbose Quoting**: Made sure all routes were more verbose for deployment purposes. E.g. in `base.py` I added `pointless_impressions_src` to `ROOT_URLCONF = "pointless_impressions_src.pointless_impressions.urls"`.
- **Add __init__.py files**: Added missing `__init__.py` files to ensure proper package structure and module imports.
- **Add Pointless_Impressions_src to INSTALLED_APPS**: Added `pointless_impressions_src` before each of the apps in the `INSTALLED_APPS` list in `base.py` to more more verbose and help with Heroku finding the apps.
- **Remove Some Allowed Hosts**: Removed staging.example.com from the allowed hosts in `staging.py` as it was not needed.
- **Removed Django from ALLOWED_HOSTS**: Removed DJANGO from ALLOWED_HOSTS in `staging.py` as it was not needed.
- **Static and Media files blocked**: Blocked static and media files being served from cloudinary and S3 due to lack of CSP settings. Installed Django-CSP. Added `csp.middleware.CSPMiddleware` to the MIDDLEWARE list in `base.py`. Added CSP settings to staging and production files.
- **Media Storage**: Django-Cloudinary-Storages is an old community packege that I was having issues with and is no longer maintained. Therefore, I used the official Cloudinary package to configure the media storage instead.
- **Heroku Deployment Issues**: Fixed various Heroku deployment issues by ensuring proper Procfile, .slugignore, and environment variable configurations.
- **Testing Configuration**: Updated Jest configuration to properly handle ES6 modules and added Babel support for JavaScript files.
- **Models and Views for Artwork**: Views didn't properly filter artworks by category. Fixed the views to correctly filter artworks based on the selected category slug.
- **Search Functionality**: To make search global across all relevant apps and a fail safe for if a search result isn't in an app it searches all apps. Created a search app to ensure it is global across all apps.
- **CustomUser Model**: Restrictive management across the web app, instead used Groups for Owner, Manager and Employee roles and linked it to the CustomUser model. Added a profile app to manage Customer profiles separately along with Artists and linked it to the CustomUser model and Artists to the Artwork.
- **Photo Fetching**: Implemented proper fetching of photos for all apps by ensuring related objects are selected in queries to avoid N+1 query problems and ensure images display correctly.
- **Sort Functions**: Positioning of sort buttons were not centered and the message for no artworks found was not displaying correctly. Fixed the sort button positioning and message display by updating the artwork.js file and artwork.html template to have col-span-full to take up the space. While also applying JS and dataset attributes to ensure the correct sort button remains highlighted after sorting.
- **GET for Filter**: GET request was not being used for the available only filter button in artwork.js. Therefore, the filter button was not working correctly. Fixed the issue by moving available only to a checkbox management system inside the filter form.
- **Artwork CBV**: Fixed the Artwork CBV to properly filter artworks based on availability and sort order. Updated the get_queryset method to handle filtering and sorting logic correctly. While also ensuring the JSON response for AJAX requests is properly formatted.
- **Sort Buttons Only Working on Artwork on the Page**: The sort buttons were only sorting the artworks that were currently displayed on the page rather than all artworks. Fixed this by updating the Django templates to use SSR and JavaScript to fetch and render sorted artworks from the server.
- **Search Views had Wrong Names**: The search queries were not named after the correct models properly leading to type and attribute errors. Fixed this by renaming the queries to match the correct models and ensuring proper imports.
- **Use Behave-Django instead of Django-Behave**: Django-Behave is no longer maintained and was causing issues with the latest Django versions. Therefore, I switched to Behave-Django which is actively maintained and works better with Django and created a `environment.py` and `settings/test.py` file for the testing environment as the actual database being populated was causing issues when running behave.
- **Syntax issues with Behave-Django**: Behave tests were failing due to mismatches between feature file steps and step definitions. Fixed this by ensuring exact matches in wording and punctuation between feature files and step implementations. Behave-Django also can't use background features therefore each scenario feature had the database information added to it.
- **Cypress test port on same port as dev**: Cypress was trying to run on the same port as the development server causing port conflicts. Along with that, Cypress was not receiving the data properly. Fixed this by creating a separate `docker-compose.test.yml` and adjusted the `dev.sh` entrypoint script to run the test server on port 8001. Updated Cypress configuration to point to the correct test server URL.
- **Images not showing**: Due to the different way images are served on dev v staging and production the artworks page was not showing the iamges when applying filtering and sorting. Fixed this to enable ArtworkListView CBV JSON data to have both image_url for dev and image_public_id for staging and production and updated the artwork.js file to handle both cases when rendering images.
- **Search Autocomplete not showing**: The search autocomplete was not showing the results when typing so used tarekraafat /autocomplete.js library to implement the autocomplete functionality properly.
- **Carousel Navigation Issues**: Initial carousel navigation wasn't showing the final card fully, just partially. Fixed this by adding an if/else condition to check if it's the last card and adjusting the scroll position accordingly.
- **Carousel Accessibility**: Added ARIA labels and keyboard navigation support to the carousel for better accessibility.
- **Behave Tests Not Passing Images**: Behave tests automatically set Debug to false which caused issues with image fetching due to using cloudinary tags. Therefore, removed image checks from behave tests to avoid failures.
- **Cypress Tests not running due to lack of data-testids**: Cypress tests were not able to find elements due to missing data-testids. Added data-testids to relevant elements in the artwork detail template.
- **Framing Option Selection in Cart**: The add to cart modal was not showing a dropdown selection for the framing options due to lack of JSON being passed to the template. Added a function to the Artwork model to return framing options as a list of tuples for the template to render the dropdown. Added the JSON dump to ArtworkListView and ArtworkDetailView CBVs. Then ensured the data was being fetched properly in the relevant html and js files.
- **Add to Cart Submission**: The add to cart modal was not submitting the form properly due to handling of JSON responses for framing conditions. Updated the `artwork_detail.html` to have the postloadjs hold the framing conditions JSON data for the modal to fetch and render the dropdown properly.
- **Toasts Were Displayed Outside the Header Container**: The toasts were being displayed outside the header container due to styling issues. Added a custom `#toast-container` styling to the source CSS file to ensure proper positioning.
- **Local Storage and SSR**: The cookie and local storage uuid's for the cart were not syncing, meaning the django session was not receiving the cart data properly and the order summary on the checkout page was not receiving the information. Fixed by sending the cart uuid from local storage to the server via a cookie on each request.
- **Network Error when updating order in checkout**: The checkout page was throwing a network error when trying to update the order summary due to the `header_footer.js` sending too many requests for the cart uuid. Added a debounce wrapper which fixed the network errors by ensuring only one cart fetch runs within a short time window, preventing multiple overlapping requests that the browser would otherwise abort.
- **SSR Incorrect Implementation and Frontend not receiving Session ID**: Using local storage for cart and uuid is not a robust solution to use SSR properly. Fixed by using Django Sessions to store cart in session id and synced that with the frontend via AJAX requests to ensure proper cart functionality across SSR. Needed to set `SESSION_COOKIE_SECURE = False` to enable frontend in development to access the session cookie.
- **Toast Notifications Not Displaying on API Responses**: The toast notifications were not displaying properly due to lack of integration and having multiple toast systems. Therefore, created a unified toast notification system that works using Django messages with AJAX requests.
- **Circular Imports between utils and models**: Fixed circular imports by having the utils functions imported within the functions that need them rather than at the top of the file and the same for models imported within the utils functions that need them. 
- **Cloudinary Images Not Working**: Fixed various issues with Cloudinary image fetching by ensuring proper configuration of Cloudinary settings, using correct tags in templates, and handling both development and production image URLs in views. Used a context processor to handle placeholder image and the image to render function as well. Ensured the DB image path matched the public id as well. Once set up use Cloudinary in local development as well to avoid issues.
- **400 and 500 Requests to Square**: Payment was throwing 400 and 500 errors firstly the order was not creating a payment_id in the Order model. Fixed this by adding payment_id being created when the order is created and sent to the DB and Square. Secondly, Sqaure was not updating the payment due to incorrect headers and body being sent. Fixed this by ensuring the correct headers and body were being sent to Square API by including them in OrderCOnfirmationView CBV.
- **Confirm Order Modal Not Scrolling**: Confirm order modal was not scrolling to the top when opened, causing users to miss important information at the top of the modal. Fixed this by adding `modalContent.scrollTop = 0;` when the modal is opened to ensure it starts at the top and when the Yes, Confirm Order button is clicked it scrolls to the top to show the spinner.
- **Deletion of Orders**: If a user deleted an order it changed to cancelled but was still showing in the user profile orders list. Fixed this by excluding cancelled orders from the orders list in the UserProfileView CBV.
- **Cloudianry Images Being Blocked and Returning 404**: Cloudinary images were being blocked due to lack of CORS, so added `crossorigin='anonymous'` to the image tags to fix this issue. It then returned 404 error due to a wrong path being stored in the DB. Fixed this by ensuring the correct public id was stored in the DB.
- **Cloudinary not serialisable into JSON**: Cloudinary image objects were not serialisable into JSON when sending data via AJAX for filtering and sorting. Fixed this by adding fallbacks in the `-serialize_artwork_data` function to extract the image URL from the Cloudinary object or use the image field directly if necessary.
- **User Registration 500 Error (Criteria 4.1, 4.4)**: Registration was throwing a 500 error because `generate_verification_code()` and `send_verification_email()` were never called in `SignupView.post()`, leaving users redirected to the email verification page with no code in their inbox. Additionally, the signup flow had no `transaction.atomic()` wrapper, so any mid-registration failure (e.g., after `user.save()`) left orphan user records in the database. Unhandled exceptions from `send_mail()` also propagated and crashed registration when the email server was unavailable. Fixed by: wrapping all DB writes in `transaction.atomic()`; calling `generate_verification_code(user)` inside the atomic block after `Customer` creation; calling `send_verification_email(user)` outside the atomic block with a `try/except` so an email failure shows a warning message rather than a 500; and adding `try/except` guards to both `send_verification_email()` and `send_email_verified_confirmation()` in `account/utils.py`.

### Unfixed Bugs

- **Square payment styling**: I could not figure out how to style the input background colour to match the rest of the site. It was stuck as white despite trying multiple methods. However, this does not affect functionality. 
- **Using Authenticated Users Info for Checkout**: When an authenticated user goes to checkout the form does not prefill with their information from their profile. I could not figure out how to do this with the current setup. However, this does not affect functionality as the user can still input their information manually.
- **Image Sizes**: Images were provided by artists in various sizes and resolutions. Even with Cloudinary optimisations some images load slower than others. I could not fix this as I do not have access to the original image files to resize them. However, this does not affect functionality.

### Validator Testing

Due to time constraints I could not run the validators on the entire site. However, I did run the validators on key pages to ensure there were no major issues.

- **HTML Validator**: Used the W3C Markup Validation Service to check key pages like the homepage, artwork listing, and checkout page. Fixed minor issues like missing alt attributes and unclosed tags.
- **CSS Validator**: Used the W3C CSS Validation Service to validate the main stylesheet. Addressed warnings related to vendor prefixes and deprecated properties.
  
---
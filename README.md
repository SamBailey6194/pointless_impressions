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
  - [Lessons Learnt](#lessons-learnt)
  - [Testing](#testing)
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

Due to the length of the features section please see [Features Markdown](docs/markdowns/FEATURES.md).

---

## Lessons Learnt

- Always use cookies sessionid for cart persistence rather than localStorage only to avoid sync issues between backend and frontend.
- For seamless user experience use AJAX for all cart updates on checkout page rather than full page reloads.
- JS files can be modularised and used as modules with import/export to keep code organised.
- SSR is always safer and more consistent to start with before adding AJAX enhancements.
- Circular imports can be avoided by importing inside functions rather than at the top of the file.
- For anything you may use across multiple apps create a `utils.py` or `context_processors.py` file to hold the functions depending on the use case. Alongside this create a template that is reuseable either as a includes or template tag. If needed create a core or common app to hold these files. For example, the featured artworks section is across multiple pages and multiple CBVs so next time I would create a core app to hold the logic and template tag for this.

---

## Testing 

Due to the length of the testing section please see [Testing Markdown](docs/markdowns/TESTING.md).

---

## Deployment

The app deployed via Heroku [here](https://pointless-impressions-c0e03a9cdc86.herokuapp.com/) following the steps below:

1. **Ensure you run commands before committing**

   1. Build the requirements files

      1. Navigate to your `.venv` or virtual environment or create one if you haven't already.

        ```bash
        python -m venv .venv
        source .venv/bin/activate  # Linux/Mac
        .venv\Scripts\activate     # Windows
        ```

        If python or pip don't work ensure you can run this as:

        ```bash
        python3 -m venv .venv
        source .venv/bin/activate  # Linux/Mac
        .venv\Scripts\activate     # Windows
        ```
      2. Run the command below to build the `requirements.txt` file

        ```bash
        pip freeze > requirements.txt
        ```

        If python or pip don't work ensure you can run this as:

        ```bash
        pip3 freeze > requirements.txt
        ```

  2. **Update Packages**

      1. In the `.venv` or virtual environment navigate to the `theme/static_src` folder and run the command below to update the npm packages

        1. Install to update the `package-lock.json` file

        ```bash
        npm install
        ```

        2. Run the command below to update the `package.json` file

        ```bash
        npm update
        ```
        3. Build the Tailwind CSS and JS files

        ```bash
        npm run build
        ```

        **IMPORTANT** As we are also using Django-Tailwind you can run from the root `python manage.py tailwind build` or `python3 manage.py tailwind build` command to build the Tailwind CSS files as well.

        Either way ensures the `static/css/styles.css` and `static/js/scripts.js` files are updated and hashed for caching purposes on deployment.

        If python or pip don't work ensure you can run this as:

        ```bash
        pip3 install --upgrade pip setuptools wheel
        ```
2. **Create your Procfile file**

   1. In the root of your project create a `Procfile` file with the following content:

      ```
      web: gunicorn pathtosettings.wsgi:application
      ```

   2. In the root of your project create a `.python-version` file with the following content:

      ```
      3.13
      ```

3. **Create your .slugignore file**
   
   1. In the root of your project create a `.slugignore` file with the following content:

      ```
      # -----------------------------
      # Markdown
      # -----------------------------
      *.md
      docs/

      # -----------------------------
      # Environment Example files 
      # -----------------------------
      .env.dev.example
      .env.staging.example
      .env.production.example

      # -----------------------------
      # Docker Files
      # -----------------------------
      /**/*-entrypoint.sh
      .dockerignore
      Dockerfile.*
      docker-compose.*.yml
      *.sh
      redis.conf

      # -----------------------------
      # Tests
      # -----------------------------
      **/static_src/cypress.config.js
      **/static_src/jest.config.js
      **/static_src/src/tests.js

      # -----------------------------
      # Generated / local CSS (will be hashed in build)
      # -----------------------------
      **/static/css/styles.css
      ```

      **IMPORTANT** This will stop the files being uploaded to Heroku which are not needed for production or staging deployment. As we aren't able to use the Docker images due to having a student Heroku account. We also don't need the tests or markdown files on the live server. We are also hashing the CSS and JS files during the build process so the un-hashed built CSS files are not needed.

4. **Git Commit**

   1. Run the command below to check which branch you are on

      ```bash
      git branch
      ```

   2. If you are not on the `staging` branch for staging deployment or the `main` branch for production deployment, run the command below to switch to it

      For Staging:
      ```bash
      git checkout staging
      ```

      For Production:
      ```bash
      git checkout main
      ```
    3. Run the commands below to add, commit and push the changes to the relevant branch

        For Staging:
        ```bash
        git add .
        git commit -m "Your commit message"
        git push origin staging
        ```

        For Production:
        ```bash
        git add .
        git commit -m "Your commit message"
        git push origin main
        ```

5. **Set up Cloudinary for Staging Media Storage**

    1. Log into your [Cloudinary Dashboard](https://cloudinary.com/console)
    
    2. Create a new folder for staging environment:
       - Navigate to Media Library
       - Click "Create Folder" 
       - Name it something relevant if for staging include staging, if for production just the name of the project
       - Note down your Cloud Name, API Key, and API Secret from the dashboard

6. **Set up Email for Correct Deployment**

   1. **Staging Environment - Ethereal Email**
      1. Go to [Ethereal Email](https://ethereal.email/)
      2. Click "Create Ethereal Account" to generate test credentials
      3. Note down the SMTP settings:
       - Host: 
       - Port: 
       - Username: [generated username]
       - Password: [generated password]
       - Use TLS: 
      4. Save the web interface URL to view sent emails during testing
  
   2. **Production Environment - Gmail**
      1. Go to your [Google Account Security Settings](https://myaccount.google.com/security)
      2. Under "Signing in to Google," enable 2-Step Verification
      3. After enabling 2-Step Verification, go to "App Passwords"
      4. Create an app password for "Mail" on "Other (Custom name)" and name it "Django App"
      5. Note down the generated app password for SMTP use
      6. Use the following SMTP settings in your production environment:
       - Host: 
       - Port: 
       - Username: your full Gmail address
       - Password: the generated app password
       - Use TLS: 

7. **Set up AWS S3 Bucket and IAM for Staging**

   1. **Create AWS Account (if not already done):**
       - Go to [AWS Signup](https://aws.amazon.com/)
       - Follow the steps to create a new account

   2. **Create S3 Bucket:**
       - Log into AWS Console
       - Navigate to S3 service
       - Click "Create bucket"
       - Bucket name: choose a name that is globally unique.
       - Region: Choose closest to your users (e.g., eu-west-2 for UK)
       - Uncheck "Block all public access" for media files
       - Enable versioning (optional but recommended)
       - Click "Create bucket"

   3. **Configure Bucket Policy:**
       - Go to bucket → Permissions → Bucket Policy
       - Add policy for public read access to static files:
       ```json
       {
         "Version": "2012-10-17",
         "Statement": [
           {
             "Sid": "PublicReadGetObject",
             "Effect": "Allow",
             "Principal": "*",
             "Action": "s3:GetObject",
             "Resource": "arn"
           }
         ]
       }
       ```

   4. **Configure CORS:**
       - Go to bucket → Permissions → Cross-origin resource sharing (CORS)
       - Add CORS configuration:
       ```json
       [
         {
           "AllowedHeaders": ["*"],
           "AllowedMethods": ["GET", "POST", "PUT", "DELETE"],
           "AllowedOrigins": ["*"],
           "ExposeHeaders": ["ETag"],
           "MaxAgeSeconds": 3000
         }
       ]
       ```

    5. **Create IAM Policy:**
       - Navigate to IAM → Policies
       - Click "Create policy"
       - Select "JSON" tab and add the following policy (replace `your-bucket-name`):
       ```json
       {
         "Version": "2012-10-17",
         "Statement": [
           {
             "Effect": "Allow",
             "Action": [
               "s3:PutObject",
               "s3:GetObject",
               "s3:DeleteObject",
               "s3:ListBucket"
             ],
             "Resource": [
               "arn",
               "arn/*"
             ]
           }
         ]
       }
       ```
       - Click "Next: Tags" → "Next: Review"
       - Name: Global Name
       - Description (optional): Describe whether it is for staging or production
       - Click "Create policy"

    6. **Create IAM User Groups:**

       **Service Group (for applications):**
       - Navigate to IAM → User groups
       - Click "Create group"
       - Group name: global name
       - Description: Descriube whether it is for staging or production
       - Attach the policy: policy name
       - Click "Create group"

       **Developer Group (for human users):**
       - Click "Create group"
       - Group name: global name 
       - Description: Descriube whether it is for staging or production
       - Attach policies:
         - Policy Name (custom policy created above)
         - `CloudWatchLogsReadOnlyAccess` (AWS managed - for debugging)
         - `IAMReadOnlyAccess` (AWS managed - to view their own permissions)
       - Click "Create group"

    7. **Create IAM User:**
       - Navigate to IAM → Users
       - Click "Create user"
       - Username: Global Name
       - Select "Programmatic access"
       - Click "Next"

    8. **Add User to Service Group:**
       - On the permissions page, select "Add user to group"
       - Select User Groups Global Name you created earlier
       - Click "Next" → "Create user"
       - **Important:** Download the Access Key ID and Secret Access Key
       - Store these securely - they won't be shown again

8. **Square Setup:**
   1. Log into your [Square Developer Dashboard](https://developer.squareup.com/apps)
   2. Create a new application for staging or production
   3. Note down the Application ID, Access Token, and Application Secret
   4. Set up Webhooks:
      - Navigate to "Webhooks" tab in your application
      - Add a new subscription with the following details:
        - Event Types: Select relevant events (e.g., payment updates)
        - Notification URL: Your webhook endpoint (e.g., `https://your-domain.com/order/webhooks/square`)
      - Note down the Webhook Subscription ID and Signature Key

9.  **Create Heroku App:**
   1. Navigate to Heroku Dashboard
   2. Click "New" → "Create new app"
   3. App name: Global Name
   4. Choose region: EU
   5. Click "Create app"

10. **Create Config Vars:**
   1. In the Heroku app dashboard, navigate to "Settings" → "Config Vars"
   2. Add all necessary environment variables as per your `.env.production.example` or `.env.staging.example` files.
   3. Ensure to include AWS, Cloudinary, Email, and Django secret key settings.
   4. Save each variable after adding.

    As an example make sure you have the following variables set:

    ```plaintext
    ALLOWED_HOSTS=
    DEBUG=FALSE
    DJANGO_SECRET_KEY= 
    DEBUG=False 
    DOMAIN=
    DJANGO_SETTINGS_MODULE= 
    DISABLE_COLLECTSTATIC=0
    STAGING/PRODUCTION_DB_URL= 
    EMAIL_BACKEND= 
    EMAIL_HOST= 
    EMAIL_PORT= 
    EMAIL_USE_TLS= 
    EMAIL_HOST_USER= 
    EMAIL_HOST_PASSWORD= 
    DEFAULT_FROM_EMAIL= 
    CLOUDINARY_CLOUD_NAME= 
    CLOUDINARY_API_KEY= 
    CLOUDINARY_API_SECRET= 
    AWS_STORAGE_BUCKET_NAME= 
    AWS_S3_REGION_NAME= 
    AWS_ACCESS_KEY_ID= 
    AWS_SECRET_ACCESS_KEY= 
    SQUARE_APP_ID=
    SQUARE_ACCESS_TOKEN=
    SQUARE_APP_SECRET=
    SQUARE_LOCATION_ID=
    SQUARE_WEBHOOK_SUBSCRIPTION_ID=
    SQUARE_WEBHOOK_URL=
    SQUARE_WEBHOOK_SIGNATURE_KEY=
    ```

11. **Deploy the App:**
    1. In the Heroku app dashboard, navigate to "Deploy" tab
    2. Under "Deployment method," select "GitHub"
    3. Connect to your GitHub account and select the repository
    4. Set up automatic deploys if desired using the correct branch (`staging` for staging deployment or `main` for production deployment)
    5. Choose the branch (`staging` for staging deployment or `main` for production deployment)
    6. Click "Deploy Branch"
    7. Monitor the build logs for any errors
    8. Once deployed, click "View" to see your live application

Due to having a student Heroku account the Docker container deployment option is not available, due to file size limitations.

I have also written how to deploy using the Docker files for [Production Deployment using Docker Container](docs/markdowns/PRODUCTION.md).

It is important to note to simulate a real world environment I also deployed a staging version of the web app via Heroku [here]() and I followed the steps outlined in [Staging Deploymennt using Docker Container](docs/markdowns/STAGING.md)

As I used a Docker Container I set the Python Version and gunicorn in my relevant Docker related files:

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

---
 
## Credits 

Due to the length of the credits section please see [Credits Markdown](docs/markdowns/CREDITS.md).
# Production Environment Guide

This document explains how to work with the **production environment** for the Pointless Impressions project. 

Production is the live environment where the application is accessible to end users. All production work should branch off `main` and be approved by the lead developer.

---

## Table of Contents
    
- [Production Environment Guide](#production-environment-guide)
  - [Table of Contents](#table-of-contents)
  - [Purpose](#purpose)
  - [Docker Files](#docker-files)
  - [Prerequisites](#prerequisites)
  - [Variables for Heroku Config Vars and .env.staging](#variables-for-heroku-config-vars-and-envstaging)
  - [Heroku Setup](#heroku-setup)
  - [Github Actions Deployment](#github-actions-deployment)

---

## Purpose

Production is the live environment for customers to access the application. It is used to:

- Serve the live web application to end users
- Handle real user data and transactions
- Ensure high availability and performance
- Monitor for issues and maintain security

---

## Docker Files

- `docker-compose.production.yml`
- `Dockerfile.production`
- `production-entrypoint.sh`
- `.env.production` (contains production secrets)

---

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads)
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- [AWS account with S3 and IAM access](https://aws.amazon.com/)
- [Cloudinary account](https://cloudinary.com/users/register)
- [Ethereal Email account](https://ethereal.email/)

---

## Variables for Heroku Config Vars and .env.staging

1. In the Dev Docker container we can generate the Secret Key by running

  ```bash
  ./dev.sh bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```

  If python doesn't work, use python3:

  ```bash
  ./dev.sh bash
  python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```

  You should get a long string in your terminal. You can then copy it and paste it into the `.env.production` and this is your production secret key for **Pointless Impressions**. Which will also need to go into the Heroku Config Vars.

2. **Set up Cloudinary for Production Media Storage**

    1. Log into your [Cloudinary Dashboard](https://cloudinary.com/console)

    2. Create a new folder for production environment:
       - Navigate to Media Library
       - Click "Create Folder" 
       - Name it `pointless-impressions`
       - Note down your Cloud Name, API Key, and API Secret from the dashboard

3. **Set up Email Provider for Production**

    1. I chose to use Google's SMTP service for sending emails in production. Follow these steps to set it up:

    2. Go to your [Google Account Security Settings](https://myaccount.google.com/security)
      1. Under "Signing in to Google," enable 2-Step Verification
      2. After enabling 2-Step Verification, go to "App Passwords"
      3. Create an app password for "Mail" on "Other (Custom name)" and name it "Django App"
      4. Note down the generated app password for SMTP use
      5. Use the following SMTP settings in your production environment:
       - Host: 
       - Port: 
       - Username: your full Gmail address
       - Password: the generated app password
       - Use TLS: 

4. **Set up AWS S3 Bucket and IAM for Production**

    1. **Create S3 Bucket:**
       - Log into AWS Console
       - Navigate to S3 service
       - Click "Create bucket"
       - Bucket name: `pointless-impressions-static`
       - Region: Choose closest to your users (e.g., eu-west-2 for UK)
       - Uncheck "Block all public access" for media files
       - Enable versioning (optional but recommended)
       - Click "Create bucket"

    2. **Configure Bucket Policy:**
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

    3. **Configure CORS:**
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

    4. **Create IAM Policy:**
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

    5. **Create IAM User Groups:**

       **Service Group (for applications):**
       - Navigate to IAM → User groups
       - Click "Create group"
       - Group name: global name
       - Description: Describe whether it is for staging or production
       - Attach the policy: policy name
       - Click "Create group"

    6. **Create IAM User:**
       - Navigate to IAM → Users
       - Click "Create user"
       - Username: Global Name
       - Select "Programmatic access"
       - Click "Next"

    7. **Add User to Service Group:**
       - On the permissions page, select "Add user to group"
       - Select User Groups Global Name you created earlier
       - Click "Next" → "Create user"
       - **Important:** Download the Access Key ID and Secret Access Key
       - Store these securely - they won't be shown again

5. **Create a DB**
   - Create a new database using Code Institutes DB Maker
   - Note the Database URL and name it PRODUCTION_DB_URL in the `/env.production`

**Important** Note all of these in the `.env.production` as we will need them for the Heroku Config Vars.

**Important** All the relevant data for production will be loaded in from the fixtures during deployment via the `production-entrypoint.sh` including a superuser, artwork, photos and more.

## Heroku Setup

1. **Create Heroku Staging App:**
   - Log into [Heroku Dashboard](https://dashboard.heroku.com/)
   - Click "New" → "Create new app"
   - App name: `pointless-impressions` (or similar)
   - Region: Choose closest to your users (e.g., Europe)
   - Click "Create app"

2. **Set Up Heroku Config Vars:**
   - Go to the "Settings" tab of your new app
   - Click "Reveal Config Vars"
   - Add the following config vars (replace placeholders with actual values):

     ```plaintext
    ALLOWED_HOSTS=
    DEBUG=FALSE
    DJANGO_SECRET_KEY= 
    DEBUG=False 
    ALLOWED_HOSTS= 
    DJANGO_SETTINGS_MODULE= 
    DJANGO_ENVIRONMENT=production
    ENV=production
    PRODUCTION_DB_URL= 
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
    CLOUDINARY_UPLOAD_PREFIX=pointless-impressions
    AWS_STORAGE_BUCKET_NAME= 
    AWS_S3_REGION_NAME= 
    AWS_ACCESS_KEY_ID= 
    AWS_SECRET_ACCESS_KEY= 
    STRIPE_PUBLIC_KEY= 
    STRIPE_SECRET_KEY= 
    STRIPE_WH_SECRET= 
    ```

## Github Actions Deployment

1. Create a `.github/workflows/deploy-production.yml` file in your repository with the following content:

  ```yaml
  name: Production Deploy

  on:
    push:
      branches:
        - main

  jobs:
    deploy_production:
      runs-on: ubuntu-latest
      steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Install Heroku CLI
        run: curl https://cli-assets.heroku.com/install.sh | sh

      - name: Procfile Setup for Production
        run: cp Procfile.production Procfile

      - name: Login to Heroku Container Registry
        run: echo ${{ secrets.HEROKU_API_KEY }} | docker login --username=_ --password-stdin registry.heroku.com

      - name: Build, Push and Release to Heroku (Production App)
        run: |
          heroku container:push web --dockerfile Dockerfile.production -a ${{ secrets.HEROKU_PRODUCTION_APP_NAME }}
          heroku container:release web -a ${{ secrets.HEROKU_PRODUCTION_APP_NAME }}
  ```

2. Set the following secrets in your GitHub repository settings:

   - `HEROKU_API_KEY`: Your Heroku API key (found in Heroku account settings)
   - `HEROKU_PRODUCTION_APP_NAME`: The name of your Heroku production app

3. Create a PR to merge changes into the `main` branch. Upon merging, the GitHub Actions workflow will automatically deploy the changes to the production environment on Heroku.
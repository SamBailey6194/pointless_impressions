# Staging Environment Guide

This document explains how to work with the **staging environment** for the Pointless Impressions project. 

Staging is used for QA and client review before deployment to production. All staging work should branch off `staging` and be approved by the lead developer.

---

## Table of Contents

- [Staging Environment Guide](#staging-environment-guide)
  - [Table of Contents](#table-of-contents)
  - [Purpose](#purpose)
  - [Project Structure](#project-structure)
  - [Prerequisites](#prerequisites)
  - [Environment Setup](#environment-setup)
    - [Environment Variables](#environment-variables)
  - [Docker Setup](#docker-setup)
  - [Deploying the Staging App](#deploying-the-staging-app)

---

## Purpose

Staging is a near-production environment used to:

- Allow the client to see the web app after each sprint
- Test database migrations and integrations
- Ensure email and cache functionality works correctly
- Catch any issues before production deployment

---

## Project Structure

Staging uses the same project structure as development. Relevant Docker files:

- `docker-compose.staging.yml`
- `Dockerfile.staging`
- `staging-entrypoint.sh`
- `.env.staging` (contains staging secrets)

---

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Git
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

---

## Environment Setup

1. Copy the staging environment template:

```bash
cp .env.staging.example .env.staging
```

2. Update the .env.staging with the credentials, secret key and database settings

    ### Example
    DJANGO_SECRET_KEY="staging_secret_key"
    STAGING_DB_HOST=db_staging
    STAGING_DB_PORT=5432
    STAGING_DB_NAME=staging_db
    STAGING_DB_USER=staging_user
    STAGING_DB_PASS=staging_pass
    CACHE_URL=redis://redis_staging:6379/0
    EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    EMAIL_HOST=maildev_staging
    EMAIL_PORT=1025
    EMAIL_USE_TLS=False
    DEFAULT_FROM_EMAIL=staging@example.com

    On Heroku for staging you will need to put these in as config vars, along with AWS S3, Cloudinary and .env.staging variables.

    For emails on Heroku look to use [ethereal](https://ethereal.email/), follow their docs on how to set it up.

3. For the Heroku staging we will need to have a postgres created from Code Institutes Database maker and we will need to create a superuser for the staging Django Web App as well. We will do this later.

4. We will also need to generate a secret key for the staging

    In the venv in VS Code you can enter:

    ```bash
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    ```

    You should get a long string in your terminal. You can then copy it and paste it into the .env.staging and this is your staging secret key for **Pointless Impressions**. Which will also need to go into the Heroku Config Vars.

### Environment Variables

| Variable           | Purpose                       | Example                                           |
| ------------------ | ----------------------------- | ------------------------------------------------- |
| DJANGO_SECRET_KEY  | Django secret key for staging | "staging_secret_key"                              |
| STAGING_DB_HOST    | Database host                 | db_staging                                        |
| STAGING_DB_PORT    | Database port                 | 5432                                              |
| STAGING_DB_NAME    | Database name                 | staging_db                                        |
| STAGING_DB_USER    | Database username             | staging_user                                      |
| STAGING_DB_PASS    | Database password             | staging_pass                                      |
| CACHE_URL          | Redis cache URL               | redis://redis_staging:6379/0                      |
| EMAIL_BACKEND      | Email backend                 | django.core.mail.backends.smtp.EmailBackend       |
| EMAIL_HOST         | Email server host             | maildev_staging                                   |
| EMAIL_PORT         | Email server port             | 1025                                              |
| EMAIL_USE_TLS      | Enable TLS for email          | False                                             |
| DEFAULT_FROM_EMAIL | Default sender email          | [staging@example.com](mailto:staging@example.com) |

---

## Docker Setup

For development you only need to worry about the Dockerfile.staging, docker-compose.staging.yml and staging-entrypoint.sh

Ensure AWS S3, Cloudinary, PostgreSQL, and Stripe are reachable from the staging container.

---

## Deploying the Staging App

**Important**: Never change or upgrade dependencies or packages, leave this to the lead dev. If there are any warnings at install please contact the lead dev.

1. Ensure env.staging is set up and has the relevant variables

3. Ensure your Dockerfile.staging and staging-entrypoint.sh are correctly configured.

2. Build and start staging the containers

    ```bash
    docker compose -f docker-compose.staging.yml up --build -d
    ```

3. Verify they are running

    ```bash
    docker ps
    ```

4. Ensure you have Heroku CLI installed, you can check by typing.

    ```bash
    heroku --version
    ```

    You should have Heroku return what version you have

    If you do not have a version appear then install Heroku CLI from [here](https://devcenter.heroku.com/articles/heroku-cli)

5. Log into Heroku and Heroku Container Registry

    ```bash
    heroku login
    heroku container:login
    ```

6. Create your app in Heroku

    ```bash
    heroku create pointless-impressions-staging
    ```

7. Push the docker image to Heroku

    ```bash
    heroku container:push web --app pointless-impressions-staging --context-dir .
    ```

8. Create the config vars in Heroku CLI

    ```bash
    heroku config:set \
    ALLOWED_HOSTS= \
    DJANGO_SECRET_KEY= \
    DJANGO_DEBUG=False \
    DJANGO_ALLOWED_HOSTS= \
    DJANGO_SETTINGS_MODULE= \
    STAGING_DB_NAME= \
    STAGING_DB_USER= \
    STAGING_DB_PASSWORD= \
    STAGING_DB_HOST= \
    STAGING_DB_PORT= \
    EMAIL_BACKEND= \
    EMAIL_HOST= \
    EMAIL_PORT= \
    EMAIL_USE_TLS= \
    EMAIL_HOST_USER= \
    EMAIL_HOST_PASSWORD= \
    DEFAULT_FROM_EMAIL= \
    CLOUDINARY_CLOUD_NAME= \
    CLOUDINARY_API_KEY= \
    CLOUDINARY_API_SECRET= \
    AWS_STORAGE_BUCKET_NAME= \
    AWS_S3_REGION_NAME= \
    AWS_ACCESS_KEY_ID= \
    AWS_SECRET_ACCESS_KEY= \
    STRIPE_PUBLIC_KEY= \
    STRIPE_SECRET_KEY= \
    STRIPE_WH_SECRET= \
    --app pointless-impressions-staging
    ```

9. Release the container

    ```bash
    heroku container:release web --app pointless-impressions
    ```

10. Access the app

    ```bash
    heroku open --app pointless-impressions-staging
    ```
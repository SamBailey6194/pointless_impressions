# Staging Environment Guide

This document explains how to work with the production environment for the Pointless Impressions project.

Production is the live environment used by clients and end-users. All production deployments should be approved by the lead developer. It all comes from `main` branch.

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

Production is the live environment used to:

- Serve the public-facing application
- Ensure all features are stable and performant
- Integrate with real payment, email, and cloud services
- Serve static files and media via AWS S3 / Cloudinary
- Maintain logs and monitor uptime

---

## Project Structure

Production uses the same project structure as development and staging. Relevant Docker files:

- `docker-compose.production.yml`
- `Dockerfile.production`
- `production-entrypoint.sh`
- `.env.production` (contains production secrets)

---

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Git
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

---

## Environment Setup

1. Copy the production environment template:

```bash
cp .env.production.example .env.production
```

2. Update the .env.dev with the credentials, secret key and database settings

    ### Example
    DJANGO_SECRET_KEY="production_secret_key"
    PROD_DB_HOST=your_production_db_host
    PROD_DB_PORT=5432
    PROD_DB_NAME=prod_db
    PROD_DB_USER=prod_user
    PROD_DB_PASS=prod_pass
    CACHE_URL=redis://redis_production:6379/0
    EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    EMAIL_HOST=your_email_provider
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    DEFAULT_FROM_EMAIL=production@example.com


    On Heroku for production you will need to put these in as config vars, along with AWS S3, Cloudinary and .env.production variables.

    For emails on Heroku look to use Gmail, to do this follow the video [SMTP Setup](https://www.youtube.com/watch?v=ZfEK3WP73eY), you don't need to use SMTP Test tool. The video just shows you how to get the password for the config vars.

3. For the Heroku staging we will need to have a postgres created from Code Institutes Database maker and we will need to create a superuser for the staging Django Web App as well. We will do this later.

4. We will also need to generate a secret key for the production

    In the venv in VS Code you can enter:

    ```bash
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    ```

    You should get a long string in your terminal. You can then copy it and paste it into the .env.staging and this is your staging secret key for **Pointless Impressions**. Which will also need to go into the Heroku Config Vars.

### Environment Variables

| Variable           | Purpose                          | Example                                                 |
| ------------------ | -------------------------------- | ------------------------------------------------------- |
| DJANGO_SECRET_KEY  | Django secret key for production | "production_secret_key"                                 |
| PROD_DB_HOST       | Database host                    | your_production_db_host                                 |
| PROD_DB_PORT       | Database port                    | 5432                                                    |
| PROD_DB_NAME       | Database name                    | prod_db                                                 |
| PROD_DB_USER       | Database username                | prod_user                                               |
| PROD_DB_PASS       | Database password                | prod_pass                                               |
| CACHE_URL          | Redis cache URL                  | redis://redis_production:6379/0                         |
| EMAIL_BACKEND      | Email backend                    | django.core.mail.backends.smtp.EmailBackend             |
| EMAIL_HOST         | Email server host                | smtp.yourprovider.com                                   |
| EMAIL_PORT         | Email server port                | 587                                                     |
| EMAIL_USE_TLS      | Enable TLS for email             | True                                                    |
| DEFAULT_FROM_EMAIL | Default sender email             | [production@example.com](mailto:production@example.com) |


---

## Docker Setup

For development you only need to worry about the Dockerfile.production, docker-compose.production.yml and production-entrypoint.sh

Ensure AWS S3, Cloudinary, PostgreSQL, and Stripe are reachable from the production container.

---

## Deploying the Staging App

**Important**: Never change or upgrade dependencies or packages, leave this to the lead dev. If there are any warnings at install please contact the lead dev.

1. Ensure env.production is set up and has the relevant variables

3. Ensure your Dockerfile.production and production-entrypoint.sh are correctly configured.

2. Build and start staging the containers

    ```bash
    docker compose -f docker-compose.production.yml up --build -d
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
    heroku create pointless-impressions
    ```

7. Push the docker image to Heroku

    ```bash
    heroku container:push web --app pointless-impressions --context-dir .
    ```

8. Create the config vars in Heroku CLI

    ```bash
    heroku config:set \
    ALLOWED_HOSTS= \
    DJANGO_SECRET_KEY= \
    DJANGO_DEBUG=False \
    DJANGO_ALLOWED_HOSTS= \
    DJANGO_SETTINGS_MODULE= \
    PRODUCTION_DB_NAME= \
    PRODUCTION_DB_USER= \
    PRODUCTION_DB_PASSWORD= \
    PRODUCTION_DB_HOST= \
    PRODUCTION_DB_PORT= \
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
    heroku open --app pointless-impressions
    ```
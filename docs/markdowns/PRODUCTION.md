# Production Environment Guide

This document explains how to work with the production environment for the Pointless Impressions project.

Production is the live environment used by clients and end-users. All production deployments should be approved by the lead developer. It all comes from `main` branch.

---

## Table of Contents

- [Production Environment Guide](#production-environment-guide)
  - [Table of Contents](#table-of-contents)
  - [Purpose](#purpose)
  - [Project Structure](#project-structure)
  - [Prerequisites](#prerequisites)
  - [Environment Setup](#environment-setup)
    - [Environment Variables](#environment-variables)
  - [Docker Setup](#docker-setup)
    - [Using the Production Helper Script](#using-the-production-helper-script)
  - [Deploying the Production App](#deploying-the-production-app)

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

1. Ensure you create a local venv to be able to manage the requirements.txt and install the requirements.txt into your venv.

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/Mac
    .venv\Scripts\activate     # Windows
    pip install -r requirements.txt
    ```

    If python or pip don't work ensure you can run this as:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # Linux/Mac
    .venv\Scripts\activate     # Windows
    pip3 install -r requirements.txt
    ```

2. Copy the production environment template:

```bash
cp .env.production.example .env.production
```

3. Update the .env.production with the credentials, secret key and database settings

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

4. For the Heroku production we will need to have a postgres created from Code Institutes Database maker and we will need to create a superuser for the production Django Web App as well. We will do this later.

5. We will also need to generate a secret key for the production

    In the venv in VS Code you can enter:

    ```bash
    source .venv/bin/activate  # Linux/Mac
    .venv\Scripts\activate     # Windows
    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    ```

    If python doesn't work ensure you can run this as:

    ```bash
    source .venv/bin/activate  # Linux/Mac
    .venv\Scripts\activate     # Windows
    python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    ```

    You should get a long string in your terminal. You can then copy it and paste it into the .env.production and this is your production secret key for **Pointless Impressions**. Which will also need to go into the Heroku Config Vars.

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

### Using the Production Helper Script

A helper script `production.sh` is provided to simplify production environment management with built-in safety warnings:

```bash
# Make the script executable (one time setup)
chmod +x production.sh

# Start production services (with confirmation prompt)
./production.sh start

# Stop production services
./production.sh stop

# Build production images
./production.sh build

# Rebuild and restart everything (with confirmation prompt)
./production.sh rebuild

# View logs (all services or specific service)
./production.sh logs
./production.sh logs web_prod

# Open shell in Django container (with production warning)
./production.sh shell

# Run Django migrations (with confirmation prompt)
./production.sh migrate

# Run Django tests
./production.sh test

# Create database backup
./production.sh backup

# Check service health
./production.sh health

# Clean up containers and volumes (requires typing "DELETE" to confirm)
./production.sh clean

# Show service status
./production.sh status

# Show service URLs
./production.sh urls

# Show help
./production.sh help
```

**⚠️ IMPORTANT:** The production script includes safety prompts and warnings since this affects live users. Always double-check before confirming destructive operations.

---

## Deploying the Production App

**Important**: Never change or upgrade dependencies or packages, leave this to the lead dev. If there are any warnings at install please contact the lead dev.

1. Ensure env.production is set up and has the relevant variables

2. In the venv ensure you run `pip freeze > requirements.txt` or `pip3 freeze > requirements.txt` this will ensure the requirements.txt is up to date.


3. Ensure your Dockerfile.production and production-entrypoint.sh are correctly configured.

4. Build and start production the containers

    **Option A: Using the helper script (recommended)**
    ```bash
    ./production.sh start
    ```
    *Note: This will prompt for confirmation since it's production*

    **Option B: Using docker-compose directly**
    ```bash
    docker compose -f docker-compose.production.yml up --build -d
    ```

5. Verify they are running

    **Option A: Using the helper script**
    ```bash
    ./production.sh status
    ```

    **Option B: Check health of all services**
    ```bash
    ./production.sh health
    ```

    **Option C: Using docker directly**
    ```bash
    docker ps
    ```

6. Create a superuser for the Django Admin by:

    **Option A: Using the helper script (recommended)**
    ```bash
    ./production.sh shell
    # Then inside the container:
    python manage.py createsuperuser
    ```
    *Note: This will show a production warning before opening the shell*

    **Option B: Direct docker-compose command**
    ```bash
    docker-compose -f docker-compose.production.yml exec web_prod python manage.py createsuperuser
    ```

    **Option C: Using local venv (if you prefer)**
    1. Ensure you are in your venv

        ```bash
        source .venv/bin/activate  # Linux/Mac
        .venv\Scripts\activate     # Windows
        ```

    2. Typing:

        ```bash
        python manage.py createsuperuser
        ```

        If python doesn't work ensure you can run this as:

        ```bash
        python3 manage.py createsuperuser
        ```

    3. Enter the username, email, and password when prompted

7. Ensure you have Heroku CLI installed, you can check by typing.

    ```bash
    heroku --version
    ```

    You should have Heroku return what version you have

    If you do not have a version appear then install Heroku CLI from [here](https://devcenter.heroku.com/articles/heroku-cli)

8. Log into Heroku and Heroku Container Registry

    ```bash
    heroku login
    heroku container:login
    ```

9. Create your app in Heroku

    ```bash
    heroku create pointless-impressions
    ```

10. Push the docker image to Heroku

    ```bash
    heroku container:push web --app pointless-impressions --context-dir .
    ```

11.  Create the config vars in Heroku CLI

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
    --app pointless-impressions
    ```

12. Release the container

    ```bash
    heroku container:release web --app pointless-impressions
    ```

13. Access the app

    ```bash
    heroku open --app pointless-impressions
    ```
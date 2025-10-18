# Development Guide

This document explains how to set up and contribute to the **Pointless Impressions** project in a development environment. All development work should branch off `dev`.

In the guide there is mention of venv and Docker. You won't need to run ```python manage.py runserver``` as the local host will be run via the Docker Container we build later.

Venv is only for managing the `requirements.txt` and the `package.json` so other devs get your updated packages and dependencies.

---

## Table of Contents

- [Development Guide](#development-guide)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Prerequisites](#prerequisites)
  - [Cloning the Repository](#cloning-the-repository)
  - [Environment Setup](#environment-setup)
    - [Environment Variables](#environment-variables)
  - [Docker Setup](#docker-setup)
  - [Running the Development Environment](#running-the-development-environment)
  - [Git Workflow](#git-workflow)
    - [Testing Guides](#testing-guides)
      - [For Django TestCase](#for-django-testcase)
      - [For Django Behave](#for-django-behave)
      - [For JavaScript Jest](#for-javascript-jest)
      - [For JavaScript Cypress](#for-javascript-cypress)
    - [Commit Message Guide](#commit-message-guide)
      - [Git Commit Template](#git-commit-template)
        - [Definitions](#definitions)
    - [Pull Request Flow](#pull-request-flow)
      - [PR Template](#pr-template)

---

## Project Structure

    POINTLESS_IMPRESSIONS
    ├── DEVELOPMENT.md
    ├── docker-compose.dev.yml
    ├── docker-compose.production.yml
    ├── docker-compose.staging.yml
    ├── Dockerfile.dev
    ├── Dockerfile.production
    ├── Dockerfile.staging
    ├── docs
    │   └── markdowns
    │       ├── AUTOMATICTESTING.md
    │       ├── DEVELOPMENT.md
    │       └── MANUALTESTING.md
    ├── manage.py
    ├── pointless_impressions_src
    │   ├── dev-entrypoint.sh
    │   ├── home
    │   │   ├── __init__.py
    │   │   ├── apps.py
    │   │   ├── admin.py
    │   │   ├── migrations
    │   │   ├── models.py
    │   │   ├── tests.py
    │   │   └── views.py
    │   ├── pointless_impressions
    │   │   ├── __init__.py
    │   │   ├── settings
    │   │   │   ├── __init__.py
    │   │   │   ├── base.py
    │   │   │   ├── dev.py
    │   │   │   ├── production.py
    │   │   │   └── staging.py
    │   │   ├── asgi.py
    │   │   ├── urls.py
    │   │   └── wsgi.py
    │   ├── production-entrypoint.sh
    │   ├── staging-entrypoint.sh
    │   ├── static
    │   │   ├── css
    │   │   └── js
    │   └── theme
    │       ├── __init__.py
    │       ├── apps.py
    │       ├── static
    │       │   └── css
    │       │       └── dist
    │       │           └── style.css
    │       ├── static_src
    │       │   ├── src
    │       │   │   ├── build.js
    │       │   │   │   └── hash-js.js
    │       │   │   ├── css
    │       │   │   │   └── style.css (TAILWIND FILE)
    │       │   │   └── js
    │       │   │       └── 
    │       │   ├── cypress.config.js 
    │       │   ├── jest.config.js
    │       │   ├── package.json 
    │       │   └── postcss.config.js      
    │       └── templates
    │           └── base.html (TAILWIND BASE.HTML)
    ├── README.md
    └── requirements.txt

---

## Prerequisites

Make sure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Git
- Python 3.13 (optional, if you want to run Django outside Docker)
- Node.js and npm (optional, if you want to run Tailwind outside Docker)

---

## Cloning the Repository

```bash
git clone git@github.com:YOUR_USERNAME/pointless_impressions.git
cd pointless_impressions
git checkout dev
```

**IMPORTANT NOTE**: I would advise you have your git account as a ssh on your local device and then you can change 

```bash
git clone git@ssh-label:YOUR_USERNAME/pointless_impressions.git
```

To generate your ssh please follow this guide [Git SSH Key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent?platform=linux)

Ensure you pick the correct guide for your OS.

---

## Environment Setup

1. Copy the environment template

    ```bash
    cp .env.example .env.dev
    ```

2. Update the .env.dev with the credentials, secret key and database settings

    ### Example
    DJANGO_SECRET_KEY="your_generated_secret_key"
    DEV_DB_HOST=db_dev
    DEV_DB_PORT=5432
    DEV_DB_NAME=dev_db
    DEV_DB_USER=dev_user
    DEV_DB_PASS=dev_pass
    CACHE_URL=redis://redis_dev:6379/0
    EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    EMAIL_HOST=maildev_dev
    EMAIL_PORT=1025
    EMAIL_USE_TLS=False
    DEFAULT_FROM_EMAIL=dev@example.com

3. We will create a superuser later.

### Environment Variables

| Variable           | Purpose                                      | Example                  |
|-------------------|----------------------------------------------|-------------------------|
| DJANGO_SECRET_KEY  | Django secret key for local development      | "your_generated_secret_key" |
| DEV_DB_HOST        | Database host for dev environment            | db_dev                  |
| DEV_DB_PORT        | Database port                                | 5432                    |
| DEV_DB_NAME        | Database name                                | dev_db                  |
| DEV_DB_USER        | Database username                             | dev_user                |
| DEV_DB_PASS        | Database password                             | dev_pass                |
| CACHE_URL          | Redis cache URL                               | redis://redis_dev:6379/0 |
| EMAIL_BACKEND      | Email backend for dev                         | django.core.mail.backends.smtp.EmailBackend |
| EMAIL_HOST         | Email server host                             | maildev_dev             |
| EMAIL_PORT         | Email server port                             | 1025                    |
| EMAIL_USE_TLS      | Enable TLS for email                          | False                   |
| DEFAULT_FROM_EMAIL | Default from email address                    | dev@example.com         |

---

## Docker Setup

For development you only need to worry about the Dockerfile.dev, docker-compose.dev.yml and dev-entrypoint.sh

The staging and production versions are for the lead developer to maintain and adjust.

Only with permission can you adjust those files.

---

## Running the Development Environment

**Important**: Never change or upgrade dependencies or packages, leave this to the lead dev. If there are any warnings at install please contact the lead dev. 

1. Ensure you create a local venv to be able to manage the requirements.txt and install the requirements.txt into your venv.

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    pip install -r requirements.txt
    ```

2. Now let us create a secret key for local .env.dev:

    ```bash
    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    ```

    You should get a long string in your terminal. You can then copy it and paste it into the .env.dev and this is your local secret key for **Pointless Impressions**

3. Ensure you have a terminal pointing to pointless_impressions/pointless_impressions_src/theme/static_src and install npm into the venv

    ```bash
    cd pointless_impressions_src/theme/static_src
    npm install
    ```

4. Now we have things set up locally you can build and start all Docker containers

    ```bash
    docker compose -f docker-compose.dev.yml up --build
    ```

    It should build in the order of

    1. db_dev = PostgreSQL
   
    2. redis_dev = Redis Cache

    3. maildev_dev = Email testing
   
    4. web = Django development server

    Important notes: 
    5. Tailwind and JS files will automatically run in watch mode
    6. The database will automatically migrate

5. Create a superuser for the Django Admin by:

    1. Ensure you are in your venv

        ```bash
        source venv/bin/activate  # Linux/Mac
        venv\Scripts\activate     # Windows
        ```

    2. Typing:

        ```bash
        python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
        ```

    3. Enter the username

    4. Enter an email

    5. Enter a password

    This now gives you access to [Django Admin](http://localhost:8000/admin)

6. Access the local development by going to [Local Development](http://localhost:8000/)

7. Access the maildev development:

    1. For seeing the listening server that sends emails use [Maildev Listening](http://localhost:1025/)

    2. For seeing the web interface inbox, where you can also see the sent emails use [Maildev Interface](http://localhost:1080/)

---

## Git Workflow

There are four core branches

1. Main - used only for production

2. Staging - used for staging to show the client

3. Dev - used to have the latest approved development, everything will get checked by the lead dev and then sent to staging for the client to review

4. Testing - used to send PRs so they can be tested and approved for development

To develop a feature you have been assigned always branch off dev, you can do this by following:

```bash
git checkout dev
git checkout -b user-story-number/your-feature-name
```

### Testing Guides

Ensure you build your tests for **TDD** and **BDD** first.

In this project we are using **Django's** **TestCase** and **Behave** and for **JavaScript** we are using **Jest** and **Cypress**.

We want to always build tests and get them failing first before we start to build the actual feature to the point where they pass.

Please ensure you update the **Testing Markdowns** with your **automatic tests** and **manual tests**, at the top of both is an example table layout to use:

[Automatic Tests](docs/markdowns/AUTOMATICTESTING.md)

[Manual Tests](docs/markdowns/MANUALTESTING.md)

To run the tests please use:

#### For Django TestCase

1. For all tests run in your venv:
    
    ```bash
    python manage.py test
    ```

2. For app specific tests run in your venv:

    ```bash
    python manage.py test app_name
    ```

#### For Django Behave

1. For tests run in your venv:

    ```bash
    python manage.py behave
    ```
2. For specific feature file tests run in your venv:

    ```bash
    python manage.py behave pointless_impressions_src/app_name/features/my_feature.feature
    ```    

#### For JavaScript Jest

1. You will need to make dummy HTML files for the Jest tests

2. You will also need to be in pointless_impressions/pointless_impressions_src/theme/static_src you can do this by:

    ```bash
    cd pointless_impressions_src/theme/static_src
    ```

3. For tests run:

    ```bash
    npm run test
    ```

4. For app specific tests run:

    1. Ensure you add the line below to package.json:

        ```bash
        "test:app_name": "jest ../../js/app_name/__tests__/",
        ```

    2. Then you can run the below command for app specific tests:

        ```bash
        npm run test:app_name
        ```

#### For JavaScript Cypress

1. You will need to have dummy HTML files for the Cypress tests

2. You will also need to be in pointless_impressions/pointless_impressions_src/theme/static_src you can do this by:

    ```bash
    cd pointless_impressions_src/theme/static_src
    ```

3. For tests run

    ```bash
    npm run cypress:run
    ```

4. For app specific tests run:

    1. Ensure you add the line below to package.json:

        ```bash
        "cypress:app_name": "cypress run --spec 'cypress/e2e/app_name/**/*'",
        ```

    2. Then you can run the below command for app specific tests:

        ```bash
        npm run cypress:app_name
        ```

### Commit Message Guide

#### Git Commit Template 

```bash
type(scope): Description - Summarise

Body - What did you do?

Files Changed:
- List the files you generated or edited
- For created apps just list app-name created
- For files use app-name/folder/file OR app-name/file

Still to do:
- For this user story what is there still to do
```

##### Definitions

- **Types**:
  - feat: A new feature
  - fix: A bug fix
  - docs: Documentation changes
  - style: Formatting, missing semicolons, etc.; no code change
  - refactor: A code change that neither fixes a bug nor adds a feature
  - perf: A code change that improves performance
  - test: Adding missing tests or correcting existing tests
  - build: Changes that affect the build system or external dependencies
  - ci: Changes to CI configuration files and scripts
  - chore: Other changes that don't modify src or test files
  - revert: Reverts a previous commit
- **Scope** A small scope indicating the part of the codebase affected
- **Description** Summarise what you did for this commit
- **Body** Explain what you did for this commit
  
### Pull Request Flow

1. Once you have got the feature made and passed all automatic and manual tests you need to create a PR to the `testing` branch. Before you send the PR to `testing` ensure you check [PR Template](#pr-template)

2. The testing team/QA will then run the tests and manually and ensure it passes it all.

3. They will then either send it back to you as there are bugs to fix OR they will create a PR to the `dev` branch for the lead dev to approve.

4. Lead dev will then either send it back to you to improve OR create a PR to `staging` and deploy to the staging environment

5. The client will then have a chance to test it and look at it, they will either approve it or send it back for some changes, which you will need to implement.

#### PR Template

```bash
TITLE = user-story-number/your-feature-name

Body - List all the bodies of your commit messages

Files Changed:
- List the files you generated or edited
- For created apps just list app-name created
- For files use app-name/folder/file OR app-name/file

Still to do:
- For this sprint what is there still to do
```
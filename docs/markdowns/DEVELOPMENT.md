# Development Guide

This document explains how to set up and contribute to the **Pointless Impressions** project in a development environment. All development work should branch off `dev`.

As we are running Docker, you won't need to run ```python manage.py runserver``` as the local host will be run via the Docker Container we build later.

You will need to manage `requirements.txt` and the `package.json` in the Docker console, this will be explained later.

---

## Table of Contents

- [Development Guide](#development-guide)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Cloning the Repository](#cloning-the-repository)
  - [Environment Setup](#environment-setup)
    - [Environment Variables](#environment-variables)
  - [Docker Setup](#docker-setup)
  - [Running the Development Environment](#running-the-development-environment)
    - [Using the Development Helper Script (Recommended)](#using-the-development-helper-script-recommended)
      - [Quick Start with dev.sh](#quick-start-with-devsh)
      - [Available dev.sh Commands](#available-devsh-commands)
    - [Manual Docker Setup (Alternative Method)](#manual-docker-setup-alternative-method)
    - [Creating Additional Superusers](#creating-additional-superusers)
    - [Accessing the Development Environment](#accessing-the-development-environment)
    - [Troubleshooting Development Environment](#troubleshooting-development-environment)
      - [Common Issues and Solutions](#common-issues-and-solutions)
      - [Useful Development Commands](#useful-development-commands)
  - [Git Workflow](#git-workflow)
    - [Testing Guides](#testing-guides)
    - [Installing Packages and Dependencies](#installing-packages-and-dependencies)
      - [Django Packages and Dependencies](#django-packages-and-dependencies)
      - [Django-Tailwind / Tailwind Plugins](#django-tailwind--tailwind-plugins)
      - [Node Packages and Dependencies for JavaScript](#node-packages-and-dependencies-for-javascript)
    - [Commit Guide](#commit-guide)
      - [In the Docker Container Bash](#in-the-docker-container-bash)
      - [Git Commit Template](#git-commit-template)
        - [Definitions](#definitions)
      - [Git Commit Commands](#git-commit-commands)
    - [Pull Request Flow](#pull-request-flow)
      - [PR Template](#pr-template)

---

## Prerequisites

Make sure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads)

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
    - DJANGO_SECRET_KEY="your_generated_secret_key"
    - DEV_DB_HOST=db_dev
    - DEV_DB_PORT=5432
    - DEV_DB_NAME=dev_db
    - DEV_DB_USER=dev_user
    - DEV_DB_PASS=dev_pass
    - CACHE_URL=redis://redis_dev:6379/0
    - EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    - EMAIL_HOST=maildev_dev
    - EMAIL_PORT=1025
    - EMAIL_USE_TLS=False
    - DEFAULT_FROM_EMAIL=dev@example.com

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

### Using the Development Helper Script (Recommended)

We've created a `dev.sh` script to simplify common development tasks. This script provides easy commands for managing your development environment.

#### Quick Start with dev.sh

1. Make sure the script is executable (already done):

   ```bash
   chmod +x dev.sh
   ```

2. Start the development environment:

   ```bash
   ./dev.sh start
   ```
   
   This command will:
   - Check if Docker and Docker Compose are installed
   - Create `.env.dev` from example if it doesn't exist
   - Build and start all Docker containers
   - Show you the access URLs

  It should build in the order of:
  1. db_dev = PostgreSQL
  2. redis_dev = Redis Cache
  3. maildev_dev = Email testing
  4. web = Django development server

  Important notes: 
  - Tailwind and JS files will automatically run in watch mode
  - The database will automatically migrate
  - All data will be created automatically from the fixture files

3. View all available commands:
   ```bash
   ./dev.sh help
   ```

#### Available dev.sh Commands

| Command | Description | Example |
|---------|-------------|---------|
| `start` | Start all development services | `./dev.sh start` |
| `stop` | Stop all development services | `./dev.sh stop` |
| `restart` | Restart all development services | `./dev.sh restart` |
| `build` | Build the development containers | `./dev.sh build` |
| `logs` | Show logs from all services | `./dev.sh logs` or `./dev.sh logs web` |
| `shell` | Access Django shell | `./dev.sh shell` |
| `bash` | Access bash shell in container | `./dev.sh bash` |
| `migrate` | Run Django migrations | `./dev.sh migrate` |
| `makemigrations` | Create Django migrations | `./dev.sh makemigrations` |
| `createsuperuser` | Create Django superuser | `./dev.sh createsuperuser` |
| `test` | Run Django tests | `./dev.sh test` |
| `collectstatic` | Collect static files | `./dev.sh collectstatic` |
| `clean` | Clean up containers and volumes | `./dev.sh clean` |
| `status` | Show status of all services | `./dev.sh status` |

### Manual Docker Setup (Alternative Method)

If you prefer to run Docker commands manually instead of using the `dev.sh` script:

1. Build and start all Docker containers:

    ```bash
    docker compose -f docker-compose.dev.yml up --build
    ```

    It should build in the order of:

    1. db_dev = PostgreSQL
    2. redis_dev = Redis Cache
    3. maildev_dev = Email testing
    4. web = Django development server

    Important notes: 
    - Tailwind and JS files will automatically run in watch mode
    - The database will automatically migrate
    - A superuser (admin/admin123) will be created automatically

### Creating Additional Superusers

If you need to create additional superusers:

1. Using the dev.sh script (recommended):

   ```bash
   ./dev.sh createsuperuser
   ```

2. Once in the Docker container we can generate the Secret Key by running

  ```bash
  ./dev.sh bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```

  If python doesn't work, use python3:

  ```bash
  ./dev.sh bash
  python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```

  You should then get a string output which you can then copy and paste into your `.env.dev` file for the `DJANGO_SECRET_KEY` variable.

### Accessing the Development Environment

After starting the development environment, you can access:

- **Web application**: [http://localhost:8000](http://localhost:8000/)
- **Django Admin**: [http://localhost:8000/admin](http://localhost:8000/admin) (admin/admin123)
- **MailDev Interface**: [http://localhost:1080](http://localhost:1080/) (for viewing sent emails)
- **Database**: localhost:5433 (PostgreSQL)
- **Redis**: localhost:6379 (Redis Cache)

### Troubleshooting Development Environment

#### Common Issues and Solutions

1. **Port conflicts**: If you get port binding errors, make sure no other services are running on ports 8000, 5433, 6379, 1025, or 1080.

2. **Permission errors with dev.sh**: Make sure the script is executable:
   ```bash
   chmod +x dev.sh
   ```

3. **Docker not found**: Ensure Docker and Docker Compose are installed and running.

4. **Environment variables not loaded**: The `./dev.sh start` command automatically creates `.env.dev` from the example file if it doesn't exist.

5. **Containers not starting**: Check the logs:
   ```bash
   ./dev.sh logs
   ```

6. **Clean restart**: If you're having persistent issues, clean everything and start fresh:
   ```bash
   ./dev.sh clean
   ./dev.sh start
   ```

#### Useful Development Commands

- **View running containers**: `./dev.sh status`
- **Access Django shell**: `./dev.sh shell`
- **View logs**: `./dev.sh logs` or `./dev.sh logs web`
- **Run tests**: `./dev.sh test`
- **Access container bash**: `./dev.sh bash`

---

## Git Workflow

**Important Notes** To run git commands you will need to use a terminal that is outside of the Docker container, as git isn't installed in the container for security reasons.

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

### Installing Packages and Dependencies

This app is using Django which requires a `requirements.txt`, Django-Tailwind and JavaScript testing frameworks that both require a `package.json`.
To get certain aspects working you may need to install dependencies and packages yourself. Ensure you do this locally in your venv following the steps below.

#### Django Packages and Dependencies

**Important Note**: Ensure you are in the Docker container bash when you run your development server so the packages are installed in the correct environment. Run `./dev.sh bash` to get into the container bash.

1. You can then type `pip install package-name` or `pip3 install package-name`
2. This should then install the package and you can then run `pip freeze > requirements.txt` or `pip3 freeze > requirements.txt` and the Docker Dev Container should be able to read the updated `requirements.txt` due to the settings in the `dev.entrypoint.sh`

#### Django-Tailwind / Tailwind Plugins

1. You can then type `python manage.py tailwind plugin_install TAILWIND-PLUGIN` or `python3 manage.py tailwind plugin_install TAILWIND-PLUGIN` or `npm install TAILWIND-PLUGIN` or `yarn add TAILWIND-PLUGIN`.
2. This should automatically update your `package.json` and the Docker Dev Container should be able to read the updated `package.json` due to the settings in the `dev.entrypoint.sh`

#### Node Packages and Dependencies for JavaScript

1. You can type `npm install PACKAGE-NAME`
2. This should automatically update your `package.json` and the Docker Dev Container should be able to read the updated `package.json` due to the settings in the `dev.entrypoint.sh`

If you follow the above you should then be able to access and see changes at [Local Development](http://localhost:8000/). If they aren't taking place you may need to run exit the container and rebuild it by following the below

1. In the terminal with the container open press `Ctrl + C` or `Cmd + C`, this will exit the container
2. Then run `./dev.sh build` or `docker compose -f docker-compose.dev.yml build` this will build the container.
3. Then run `./dev.sh start` or `docker compose -f docker-compose.dev.yml up` to start the container again.
  Alternatively you can just run `./dev.sh restart` to do both steps 2 and 3 in one command.

### Commit Guide

#### In the Docker Container Bash

```bash
./dev.sh bash
```

Before you commit always run `pip freeze > requirements.txt` or `pip3 freeze > requirements.txt` and `npm install` or `yarn install` to ensure all dependencies are up to date along with `npm run update` to ensure packages are updated fully.

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

#### Git Commit Commands

1. In your terminal run

```bash
git add .
```

2. Then you can write out the commit message by using

```bash
git commit -m "feat(dev-container): update dev entrypoint and Dockerfile - ensure Node 24 and NPM 11.6.2 are installed globally for dev workflow" \
-m "Body - Modified dev.entrypoint.sh to install Node dependencies if missing and start Tailwind in watch mode. Updated Dockerfile.dev to install Node 24.10 and NPM 11.6.2 globally, avoiding version mismatch warnings." \
-m "Files Changed:
- dev.entrypoint.sh
- Dockerfile.dev" \
-m "Still to do:
- Add optional watcher for requirements.txt and package.json updates
- Test Tailwind hot reload inside dev container"
```

The \ and -m allows you to type out the full commit. Alternatively you can enter after running `git add .` an editor using:


1. Running the below

```bash
git commit
```

2. Then in the editor write out the git commit message using the template above

    Then depending on your editor depends how you confirm the message two examples are below.

       1. Vim:
          1. Press `Esc`
          2. Type: `:wq` (write+quite)
          3. Press `Enter`

           If you just want to abort type `:q!` then press `enter`

       2. Nano:
          1. Press `Ctrl + O` or `Cmd + O` (write out)
          2. Press `Enter` (confirm filename)
          3. Press `Ctrl + X` or `Cmd + x` (exit)

           If you just want to abort you can press `Ctrl + X` or `Cmd + x` and then `N` when prompted

       3. VS Code:
          1. Press `Ctrl + S` or `Cmd + S` to save the message
          2. Close the VS Code tab/window and Git will detect the file is saved and then create the commit message

       4. If you are unsure which editor Git is using type `git var GIT_EDITOR` and it will return which one you are using
          1. `editor` or `vim` is most likely Vim
          2. `nano` is nano
          3. `code` is VS Code
          4. If you want to set the Git editor to your preference enter `git config --global core.editor "name-editor"`:
             1. `"vim"` = Vim
             2. `"nano"` = nano
             3. `"code --wait"` = VS Code and instructs Git to wait until you close it.
  
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
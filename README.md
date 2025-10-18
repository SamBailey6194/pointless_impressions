# Pointless Impressions

---

## Table of Contents

- [Pointless Impressions](#pointless-impressions)
  - [Table of Contents](#table-of-contents)
  - [Development Guide](#development-guide)
  - [Pointless Impressions](#pointless-impressions-1)
  - [Features](#features)
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

The decision to make this website is due to the user stories found [here]().

You can also see how the user stories were made into sprints [here]().

As we progressed in the project some of the sprints were skipped due to time. You can see more in [Features](#features) section, especially [Features Left to Implement](#features-left-to-implement).

The design and layout is due to the wireframes shown below:

![Wireframe]()

Alongside the user stories, sprints and wireframes ERDs were made and a logic flow chart.

![ERDs]()

![User Flow Chart]()

As you venture to look at the [Features](#features) you will notice some design choices, flow and relationships between the database tables were changed while the project was being made.

![Responsive Image]()

---

## Features 

Below are the features for the website and at the end is listed any features that weren't able to be implemented but would be with more time. Please note as this is a resubmission I have not changed the screenshots of the features as they are essentially the same with minor differences.

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

 **Tailwind build failure**: The `npm run dev` and `npm run build` commands were failing because the PostCSS scripts pointed to a non-existent `./src/style.css` file. Updated paths to the correct `src/css/styles.css` file.
- **Clean script issue**: The `rimraf` command in `package.json` was originally wiping folders instead of just their contents. Adjusted it to remove only files inside `static/css` and `static/js`, preserving the directories.
- **Development watcher errors**: Running `python manage.py tailwind start` previously threw `Input Error: You must pass a valid list of files to parse` because PostCSS couldn’t locate the source CSS file. This is now fixed with the correct path.

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

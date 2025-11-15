import { defineConfig } from "cypress";

if (process.env.NODE_ENV !== "development") {
  console.warn("Cypress should only be run in development mode!");
  process.exit(1);
}

export default defineConfig({
  e2e: {
    baseUrl: "http://localhost:8001",
    specPattern: "pointless_impressions_src/theme/static_src/src/tests.js/cypress/e2e/**/*.cy.js",
    supportFile: "pointless_impressions_src/theme/static_src/src/tests.js/cypress/support/e2e.js",
    video: false,
    screenshotOnRunFailure: true,
    defaultCommandTimeout: 10000,
    screenshotsFolder: "pointless_impressions_src/theme/static_src/src/tests.js/cypress/screenshots",
    videosFolder: "pointless_impressions_src/theme/static_src/src/tests.js/cypress/videos",
    
    setupNodeEvents(on, config) {
      on('task', {
        log(message) {
          console.log(message);
          return null;
        },
      });

      return config;
    },
  },
  env: {
    JS_SRC_DIR: "pointless_impressions_src/theme/static_src/src/js",
    JS_BUILD_DIR: "pointless_impressions_src/static/js",
  },
});
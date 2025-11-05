import { defineConfig } from "cypress";

if (process.env.NODE_ENV !== "development") {
  console.warn("Cypress should only be run in development mode!");
  process.exit(1);
}

export default defineConfig({
  e2e: {
    baseUrl: "http://localhost:8000",
    // Now relative to project root
    specPattern: "pointless_impressions_src/theme/static_src/src/tests.js/cypress/e2e/**/*.cy.js",
    supportFile: "pointless_impressions_src/theme/static_src/src/tests.js/cypress/support/e2e.js",
    video: false,
    screenshotOnRunFailure: true,
    defaultCommandTimeout: 10000,
    // Where to store screenshots/videos if needed
    screenshotsFolder: "pointless_impressions_src/theme/static_src/src/tests.js/cypress/screenshots",
    videosFolder: "pointless_impressions_src/theme/static_src/src/tests.js/cypress/videos",
  },
  env: {
    JS_SRC_DIR: "pointless_impressions_src/theme/static_src/src/js",
    JS_BUILD_DIR: "pointless_impressions_src/static/js",
  },
});
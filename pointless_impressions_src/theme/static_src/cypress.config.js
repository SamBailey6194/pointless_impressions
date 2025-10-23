import { defineConfig } from "cypress";

if (process.env.NODE_ENV !== "development") {
  console.warn("Cypress should only be run in development mode!");
  process.exit(1);
}

export default defineConfig({
  e2e: {
    baseUrl: "http://localhost:8000",
    specPattern: "cypress/e2e/**/*.cy.js",
    supportFile: "cypress/support/e2e.js",
    video: false,
    screenshotOnRunFailure: true,
    defaultCommandTimeout: 10000,
  },
  env: {
    JS_SRC_DIR: "src/js",
    JS_BUILD_DIR: "../../static/js",
  },
});

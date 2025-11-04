/** @type {import('@jest/types').Config.InitialOptions} */
const config = {
  clearMocks: true,
  collectCoverage: true,
  coverageDirectory: "coverage",
  
  rootDir: ".",
  
  roots: [
    "<rootDir>/pointless_impressions_src/theme/static_src/src/js",
    "<rootDir>/pointless_impressions_src/theme/static_src/src/tests.js/jest"
  ],
  
  testEnvironment: "jsdom",
  
  testMatch: [
    "**/__tests__/**/*.?([mc])[jt]s?(x)",
    "**/?(*.)+(spec|test).?([mc])[jt]s?(x)"
  ],
  
  // Now we can properly exclude .venv from root
  modulePathIgnorePatterns: [
    "<rootDir>/.venv/",
    "\\.venv"
  ],
  
  testPathIgnorePatterns: [
    "/node_modules/",
    "/.venv/",
    "/\\.venv/",
    "site-packages"
  ],
  
  watchPathIgnorePatterns: [
    "/.venv/",
    "/\\.venv/"
  ],

  transform: {
    '^.+\\.js$': 'babel-jest',
  },
};

export default config;
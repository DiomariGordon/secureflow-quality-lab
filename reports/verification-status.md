# Verification Status - v0.3.0

## Verified baseline

- Python source and tests compile successfully.
- 14 non-browser unit, API, database-integrity, configuration, security-regression, and crypto-inventory tests pass in the managed build environment.
- Measured non-browser application coverage is 81% for the public v0.3.0 baseline.
- The crypto-agility inventory CLI executes and produces a Markdown report.
- The repository excludes local databases, virtual environments, test artifacts, `.env`, and editor state.

## Playwright evidence

- The project owner executed the Windows E2E runner against the v0.2 baseline.
- Pytest selected the single test marked `e2e` and the Playwright analyst create-and-submit workflow passed.
- The v0.3.0 public suite contains 15 tests: 14 non-browser plus 1 browser E2E test.
- This managed container blocks browser navigation to local services with `ERR_BLOCKED_BY_ADMINISTRATOR`; GitHub Actions independently executed the updated browser workflow successfully.
- GitHub Actions run 1 passed both the non-browser and Playwright jobs and retained separate evidence artifacts.

## Public-hardening changes in v0.3.0

- Replaced stored local signing secrets with a process-generated development secret.
- Added strict production configuration checks.
- Disabled demo-user seeding by default in production and rejected unsafe production overrides.
- Switched Uvicorn and the container entry point to an application factory.
- Added a non-root container health check and an explicit production-readiness document.
- Added malformed Base64 handling to signed-session verification.

## GitHub verification

The public `quality-gate` workflow passed on the published `main` branch. The non-browser job enforced the 80% coverage threshold, and the Playwright job installed Chromium and passed the end-to-end analyst workflow. Both jobs uploaded machine-readable evidence artifacts.

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
- This managed container blocks browser navigation to local services with `ERR_BLOCKED_BY_ADMINISTRATOR`, so the updated browser test must be repeated through GitHub Actions after publication.
- GitHub Actions is configured to run non-browser and browser suites independently and retain JUnit/test evidence.

## Public-hardening changes in v0.3.0

- Replaced stored local signing secrets with a process-generated development secret.
- Added strict production configuration checks.
- Disabled demo-user seeding by default in production and rejected unsafe production overrides.
- Switched Uvicorn and the container entry point to an application factory.
- Added a non-root container health check and an explicit production-readiness document.
- Added malformed Base64 handling to signed-session verification.

## Remaining verification gate

The public GitHub workflow must pass after the repository is published. Until that run succeeds, CI is accurately described as configured rather than independently verified on GitHub.

# File-by-File Guide

Use this reading order. Do not begin with the largest file.

## 1. The business rule

### `src/secureflow/repository.py`

Start with `classify_risk`.

Why first: it is a pure function. The same input always produces the same output, so it is easy to reason about and test at boundaries.

Then read:

- `create_record`: applies the rule and persists state.
- `transition_record`: changes status only when the current status matches the expected state.
- `log_audit`: stores evidence about actions and denials.

## 2. The data model

### `src/secureflow/db.py`

Creates SQLite tables, demo users, password hashes, and connections.

Questions to answer:

- Which columns represent identity, ownership, workflow state, and evidence?
- Why are SQL values passed as parameters instead of interpolated into strings?
- Which data is regenerated for tests?

### `src/secureflow/models.py`

Pydantic request and response contracts.

Question: what invalid input is rejected before the route reaches repository logic?

## 3. Authentication and session security

### `src/secureflow/auth.py`

Key concepts:

- Password verification
- HMAC-signed session identifier
- Server-side session state
- Expiration
- CSRF token validation

Important distinction: signing protects integrity; it does not encrypt the value.

## 4. Application routes and authorization

### `src/secureflow/app.py`

This is the composition root and HTTP boundary.

Read routes in this order:

1. `/health`
2. `/api/auth/login`
3. `/api/auth/me`
4. `POST /api/records`
5. `GET /api/records/{record_id}`
6. submit and approve transitions
7. audit endpoint

For every route, identify:

- Authentication requirement
- Authorization rule
- Input contract
- State change
- Audit evidence
- Expected error responses

## 5. Test fixtures

### `tests/conftest.py`

Builds a fresh application and database for tests, then provides logged-in clients.

Why it matters: deterministic setup separates product failures from stale-data failures.

### `tests/e2e/conftest.py`

Starts a live local server for Playwright.

## 6. Tests, from narrowest to broadest

### `tests/unit/test_crypto_inventory.py`

Pure rule tests.

### `tests/api/test_api_workflow.py`

Business workflow and boundary behavior.

### `tests/api/test_data_integrity.py`

Cross-layer oracle: compares public API output to independent database state.

### `tests/api/test_security_regression.py`

Negative testing for CSRF, role restrictions, horizontal access, session invalidation, and response controls.

### `tests/e2e/test_ui_workflow.py`

One browser journey proving that the UI, HTTP routes, business logic, and persistence are wired together.

A browser test is intentionally not used for every rule. Lower layers are faster and more diagnostic.

## 7. Delivery automation

### `.github/workflows/ci.yml`

Installs dependencies, installs Chromium, runs lower-layer tests, runs Playwright, and uploads evidence.

Question: what should block a pull request, and what should merely create a warning?

## 8. Crypto-agility bridge

### `config/crypto_inventory.json`

Synthetic declared dependencies.

### `src/secureflow/crypto_inventory.py`

Classifies algorithms and renders a readiness report.

Limitation: it does not inspect certificates, binaries, TLS handshakes, key stores, or source code. That is a later milestone.

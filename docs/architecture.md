# Architecture

## Purpose

SecureFlow is deliberately small enough to understand end to end while still demonstrating the layers expected of an automation-first quality engineer.

## Delivery spine

```text
Requirement
   ↓
FastAPI route / browser workflow
   ↓
Authentication + CSRF + authorization policy
   ↓
Repository logic + parameterized SQL
   ↓
SQLite state + audit event
   ↓
API tests + browser tests + data checks + security regression
   ↓
GitHub Actions quality gate + evidence artifacts
```

## Test layers

1. **Unit:** deterministic risk classification and crypto-inventory rules.
2. **API:** workflow transitions, boundary values, response contracts, and authorization.
3. **Data:** compare the public API result to the persisted SQLite state.
4. **Security regression:** CSRF, horizontal access, least privilege, session invalidation, headers, and cookie settings.
5. **E2E:** a user completes the workflow through the browser with Playwright.

## Important limitations

- This is a portfolio lab, not a production clinical system.
- Demo credentials are intentionally visible for local use.
- The content security policy permits inline script/style to keep the first milestone self-contained; a later milestone should remove those exceptions.
- SQLite is suitable for the lab, not a claim of enterprise scalability.
- The crypto inventory does not inspect binaries, TLS handshakes, source code, key stores, or certificates. It only evaluates declared synthetic inventory data.

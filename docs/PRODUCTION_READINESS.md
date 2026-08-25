# Production-Readiness Boundary

SecureFlow is a synthetic portfolio and learning system. It demonstrates security-aware quality engineering, but it is **not represented as a production-ready financial, healthcare, identity, penetration-testing, or compliance product**.

## Controls intentionally demonstrated

- Parameterized SQL and database constraints
- Scrypt password hashing with per-user random salts
- Opaque, HMAC-signed session references
- Server-side session state and logout invalidation
- `HttpOnly` and `SameSite=Strict` session cookies
- CSRF validation on state-changing requests
- Server-side role and ownership authorization
- Security headers and audit events
- Synthetic accounts and data only
- Non-root container execution and a container health check
- Environment-based secrets and configuration
- Production mode rejects missing/short secrets, insecure cookies, and demo-user seeding

## Development-only choices

The local PowerShell launcher generates a fresh process-scoped signing secret and uses HTTP on `127.0.0.1`. Fixed credentials in the repository belong only to synthetic `example.test` accounts and exist to make repeatable testing possible.

Docker Compose requires `SECUREFLOW_SECRET` through an ignored `.env` file. `.env.example` contains placeholders, not credentials.

## Important gaps before real deployment

- TLS termination and trusted-proxy configuration
- External identity provider, MFA, password reset, and account lifecycle
- Login throttling and abuse detection
- Managed secret storage and key rotation
- Database migrations, backups, concurrency planning, and a production database
- Centralized observability and alerting
- Session cleanup, administrative revocation, and session-rotation policies
- CSP nonces or external scripts instead of the current inline-script exception
- Dependency, SAST, secret, container, and DAST scanning with reviewed findings
- Formal threat modeling, privacy review, accessibility review, and security testing by qualified reviewers

## Portfolio claim

The accurate claim is:

> SecureFlow demonstrates layered functional, API, data-integrity, authorization, session, security-regression, browser, CI, and crypto-inventory testing in a synthetic environment.

It does not claim production certification, penetration-test coverage, or cryptographic assurance.

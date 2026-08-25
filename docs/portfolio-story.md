# Portfolio Story

## One-line description

Built a learner-documented, automation-first quality lab that validates a regulated-style workflow across browser, API, database, authorization, audit, CI, and crypto-agility layers.

## Interview narrative

**Problem:** A browser-only regression suite can show that screens work while missing authorization failures, incorrect backend state, broken transitions, unreliable evidence, and security regressions. AI can generate more test code quickly, but volume does not guarantee that the tests ask the right questions or fail for the right reasons.

**Design:** I built a synthetic FastAPI application with role-based workflows, server-side sessions, CSRF protection, SQLite persistence, and audit logging. I created layered tests: Playwright for the user journey, direct API tests for state transitions and boundary values, independent SQL checks for data integrity, and negative security regression for access-control and session behavior.

**Operationalization:** The local non-browser suite passes with a coverage gate, and a GitHub Actions workflow is configured to run fast and Playwright suites separately while retaining machine-readable evidence. The first public workflow run remains a verification gate. The project includes a repeatable learning log: for AI-assisted changes I record the requirement, predicted files, reviewed diff, targeted test, intentional failure, manual modification, and remaining risk.

**Security extension:** The framework treats authentication, authorization, session controls, configuration safety, evidence, and secure release criteria as part of quality engineering rather than an afterthought. Public hardening added environment-based secrets, production guardrails, disabled demo seeding in production, and an explicit gap analysis. It does not claim to replace penetration testing.

**Quantum-security extension:** I added an educational crypto-inventory module that distinguishes public-key migration targets from symmetric-review items and NIST post-quantum algorithm families. This connects quantum exploration to real inventory, crypto-agility, and migration-readiness work rather than forcing Qiskit into browser automation.

## Resume bullet draft

- Built a Python/Playwright quality-engineering lab spanning UI, REST APIs, SQLite data verification, role-based authorization, CSRF/session controls, configuration guardrails, audit evidence, and CI/CD; documented AI-assisted changes through independent execution, failure analysis, and human review.

## Claims not yet earned

Do not claim these until the corresponding milestone is completed and demonstrated:

- Enterprise automation-framework ownership
- Production application security engineering
- Penetration testing
- Production cryptographic auditing
- Post-quantum migration implementation
- Quantum software engineering

The portfolio becomes stronger by stating limitations accurately and then showing how each limitation is addressed.

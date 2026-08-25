# SecureFlow Quality Lab

[![Quality gate](https://github.com/DiomariGordon/secureflow-quality-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/DiomariGordon/secureflow-quality-lab/actions/workflows/ci.yml)

SecureFlow is a **learner-documented quality-engineering portfolio project** that connects Python, Playwright, API testing, SQL/data verification, security regression, CI/CD, and an educational crypto-agility module.

The project asks five engineering questions:

1. What should the system do?
2. What could go wrong?
3. How do we create trustworthy evidence?
4. How do we distinguish product, test, data, and environment failures?
5. What risk remains after the tests pass?

## Verified baseline

- 14 non-browser tests cover business rules, API workflows, persistence, security requirements, crypto inventory, and environment safety.
- One Playwright end-to-end test exercises login, record creation, classification, and workflow submission through the browser; the project owner verified the workflow locally on the v0.2 learner baseline, and the current public revision is independently gated in CI.
- Non-browser coverage is gated at a minimum of 80%; the v0.3 baseline measures above that threshold.
- GitHub Actions verified the non-browser and Playwright suites as independent passing jobs and retained JUnit/coverage evidence.

## System mental model

```text
User or test
    ↓
FastAPI route
    ↓
Authentication + CSRF + authorization decision
    ↓
Repository/business rule
    ↓
SQLite state + audit event
    ↓
API/UI response
    ↓
Unit + API + data + security + browser evidence
    ↓
GitHub Actions quality gate
```

## Start here

1. [`docs/START_HERE.md`](docs/START_HERE.md) — first guided session with commands and explanations.
2. [`docs/FILE_BY_FILE_GUIDE.md`](docs/FILE_BY_FILE_GUIDE.md) — purpose of every major file.
3. [`docs/architecture.md`](docs/architecture.md) — system boundaries and request flow.
4. [`docs/AI_ASSISTED_DEVELOPMENT.md`](docs/AI_ASSISTED_DEVELOPMENT.md) — human-governed AI workflow.
5. [`docs/roadmap.md`](docs/roadmap.md) — milestones and definitions of done.
6. [`docs/PRODUCTION_READINESS.md`](docs/PRODUCTION_READINESS.md) — explicit deployment limits and safer defaults.

## Windows setup and run

Open PowerShell in the repository:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\check_environment.ps1
.\scripts\setup_windows.ps1
```

Start the application in **Terminal 1**:

```powershell
.\scripts\run_windows.ps1
```

Open `http://127.0.0.1:8000`.

Run the test layers in **Terminal 2**:

```powershell
.\scripts\run_fast_tests.ps1
.\scripts\run_e2e_tests.ps1
```

## Focused command menu

```powershell
.\scripts\run_fast_tests.ps1       # Unit, API, data, security, and settings tests
.\scripts\run_api_tests.ps1        # API workflow and data-integrity tests
.\scripts\run_security_tests.ps1   # Security-requirement regression tests
.\scripts\run_e2e_tests.ps1        # Playwright browser workflow
.\scripts\run_crypto_report.ps1    # Generate the crypto-agility report
.\scripts\test_windows.ps1         # Entire test suite
```

## Demo accounts

| Role | Email | Password |
|---|---|---|
| Analyst | `analyst.one@example.test` | `AnalystPass!1` |
| Second analyst | `analyst.two@example.test` | `AnalystPass!2` |
| Viewer | `viewer@example.test` | `ViewerPass!1` |
| Approver | `approver@example.test` | `ApproverPass!1` |

These credentials are public by design, use the reserved `.test` domain, and are seeded only in development/test by default. Never substitute employer, customer, or personal data.

## AI-assisted engineering discipline

AI tools may accelerate scaffolding, test ideation, and refactoring, but they do not define correctness. For meaningful AI-assisted changes, the project records:

1. The requirement in human-readable language.
2. The expected files and behavior before the change.
3. The reviewed diff and rejected assumptions.
4. The narrow test and broader regression evidence.
5. An intentional challenge or failure case.
6. The final human decision and remaining risk.

See [`docs/AI_ASSISTED_DEVELOPMENT.md`](docs/AI_ASSISTED_DEVELOPMENT.md).

## Repository map

```text
src/secureflow/          application, authentication, authorization, persistence, crypto inventory
tests/unit/              business-rule, settings, and inventory tests
tests/api/               workflow, data-integrity, and security regression
tests/e2e/               Playwright browser workflow
.github/workflows/       independent CI quality gates
docs/                    architecture, guided learning, AI review, production boundary
exercises/               safe break/fix and feature exercises
config/                  synthetic crypto inventory
scripts/                 Windows setup, run, targeted-test, and reporting commands
```

## Security and production boundary

This is a synthetic portfolio lab, not a production clinical or financial system, penetration-testing product, or cryptographic implementation. It intentionally documents what would be required before real deployment. Test only systems you own or have explicit authorization to assess.

See [`SECURITY.md`](SECURITY.md) and [`docs/PRODUCTION_READINESS.md`](docs/PRODUCTION_READINESS.md).

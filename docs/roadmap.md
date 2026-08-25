# SecureFlow Build Roadmap

This roadmap separates **tool use** from **engineering ownership**. Each milestone includes what to learn, what to build, the main commands, and a definition of done.

## Working method for every milestone

```text
Requirement → prediction → baseline test → small change → targeted test → adversarial test → full suite → explanation → commit
```

Use `LEARNING_LOG.md` for every meaningful change.

---

# Milestone 0 — Own the baseline

## Goal

Understand the existing request path before adding features.

## Learn

- Virtual environments
- FastAPI routes
- Pydantic input/output contracts
- Authentication versus authorization
- CSRF
- Repository and SQL boundaries
- Unit, API, data, security, and browser test roles

## Commands

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\check_environment.ps1
.\scripts\setup_windows.ps1
```

Terminal 1:

```powershell
.\scripts\run_windows.ps1
```

Terminal 2:

```powershell
.\scripts\run_fast_tests.ps1
```

Target one cross-layer test:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\api\test_data_integrity.py -vv -s
```

Target one security test:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\api\test_security_regression.py::test_horizontal_access_is_blocked -vv -s
```

## Practice

Complete the intentional risk-boundary failure in `docs/START_HERE.md`.

## Done when

- The app runs locally.
- Non-browser tests pass.
- Playwright runs locally or the exact environment limitation is documented.
- You can trace one request from input to database and back.
- You can explain one authorization denial.
- `LEARNING_LOG.md` contains your own explanation and one intentional failure.

---

# Milestone 1 — Framework engineering

## Goal

Move from individual tests to reusable quality infrastructure.

## 1.1 Reusable API client

### Learn

- Why test code needs its own abstractions
- Authentication setup
- Request helpers
- Error visibility

### Build

Create a small client under `tests/support/` that owns login, CSRF headers, record creation, submission, and approval.

### Baseline command

```powershell
.\scripts\run_api_tests.ps1
```

### Done when

- Tests no longer duplicate login/request setup unnecessarily.
- Failed requests still display useful response details.
- The abstraction does not hide important assertions.

## 1.2 Deterministic test-data factory

### Learn

- Fixtures and fixture scope
- Unique test data
- Isolation and cleanup
- Why test order must not matter

### Build

Add factory helpers for users and records. Prove tests pass in random or reversed order where practical.

### Commands

```powershell
.\.venv\Scripts\python.exe -m pytest tests\api -vv
.\.venv\Scripts\python.exe -m pytest tests\api\test_api_workflow.py -vv
```

### Done when

- Every test gets known initial state.
- Re-running the suite produces the same result.
- One test cannot make another test pass or fail.

## 1.3 Failure evidence

### Learn

- Screenshots
- Playwright traces
- Logs
- JUnit reports
- Evidence retention

### Build

Configure browser screenshots and traces on failure and upload them from CI.

### Command

```powershell
.\scripts\run_e2e_tests.ps1
```

### Practice

Complete `exercises/04-ci-evidence.md`.

### Done when

A reviewer can diagnose a failed browser step from CI evidence without using your local machine.

## 1.4 Contract validation

### Learn

- Response models
- JSON Schema
- Semantic assertions versus structural assertions

### Build

Validate API structure while retaining meaningful business assertions.

### Command

```powershell
.\scripts\run_api_tests.ps1
```

### Done when

A breaking field or type change fails clearly, but tests are not tied to irrelevant implementation details.

## 1.5 Reliability metrics

### Learn

- Product defect versus test defect
- Data/environment/infrastructure failure categories
- Retry risks
- Flaky-test rate

### Build

Record test duration and failure category. Do not add retries until a failure mechanism is understood.

### Done when

You can explain why each retry exists and show that retries are not concealing product defects.

## 1.6 Docker test environment

### Learn

- Image versus container
- Build context
- Environment variables
- Reproducibility

### Commands

```powershell
docker compose build
docker compose up
```

### Done when

A clean machine can run the same application and tests with documented commands.

---

# Milestone 2 — Secure release readiness

## Goal

Turn security requirements into repeatable evidence without pretending automated regression is a full penetration test.

## 2.1 Authorization matrix

### Build

Create a role/action matrix and implement the auditor-role exercise.

### Commands

```powershell
.\scripts\run_security_tests.ps1
```

### Practice

Complete `exercises/02-auditor-role.md`.

### Done when

Every allowed action has a positive test and every forbidden action has a negative server-side test.

## 2.2 Authentication abuse controls

### Build

Add an educational failed-login rate limit and audit evidence.

### Practice

Complete `exercises/03-login-rate-limit.md`.

### Done when

The behavior is tested without leaking account existence or creating an unexplained lockout risk.

## 2.3 Automated security tooling

### Learn

- SAST
- Dependency scanning
- Secret scanning
- DAST
- False positives and false negatives

### Build

Add dependency and secret scanning to CI, then an OWASP ZAP baseline scan against the local lab.

### Typical local commands

Exact commands will be selected when the tools are added. The evidence must be integrated into `.github/workflows/ci.yml` rather than run only on a developer laptop.

### Done when

- Findings are reviewed, not blindly accepted.
- Suppressions have written justification.
- The pipeline separates informational findings from release blockers.

## 2.4 Audit-log integrity

### Build

Test required audit fields, denied actions, timestamps, actor/target linkage, and tamper-evident design options.

### Done when

A release report can show what was tested, who acted, which access was denied, and what evidence remains incomplete.

## 2.5 Performance baseline

### Learn

- Response-time percentiles
- Concurrency
- Throughput
- Error rate
- Warm-up and environment realism

### Build

Use k6 or JMeter/Taurus for a small controlled workload.

### Done when

Thresholds have a documented business reason and failures produce actionable evidence.

## 2.6 Release gate

### Build

Define criteria for:

- Functional correctness
- Authorization and session controls
- Dependency/secret findings
- Performance
- Evidence completeness
- Known residual risk

### Done when

The pipeline supports a defensible release decision rather than merely reporting test counts.

---

# Milestone 3 — AI-system assurance

## Goal

Extend the same quality and security method to AI-enabled features.

## Learn

- Evaluation datasets
- Test-oracle limits
- Prompt and model versioning
- Hallucination and unsafe-output categories
- Adversarial testing
- Human review thresholds
- Drift and monitoring
- NIST AI RMF testing, evaluation, verification, and validation concepts

## Build

Add a synthetic AI-assisted decision feature only after the conventional system baseline is stable. Test:

- Input validation
- Output schema
- Known-answer cases
- Refusal or escalation cases
- Role and data boundaries
- Prompt/model configuration traceability
- Human approval for high-impact outcomes

## Done when

You can show what the automated evaluation proves, what it does not prove, and where human judgment remains mandatory.

---

# Milestone 4 — Crypto agility and quantum bridge

## Goal

Build a credible post-quantum migration-readiness capability without inventing production cryptography.

## 4.1 Controlled inventory

### Current command

```powershell
.\scripts\run_crypto_report.ps1
```

### Build

Replace declared sample inventory with controlled certificate/TLS inspection in a lab environment.

### Learn

- Cryptographic use versus algorithm name
- Certificates, key exchange, signatures, and data-at-rest controls
- System owner and dependency mapping
- Data lifetime and harvest-now-decrypt-later risk

### Done when

Every finding identifies a system, component, use, owner, algorithm, data lifetime, dependency, and migration priority.

## 4.2 Algorithm-change regression

### Build

Using supported libraries and test environments, measure:

- Compatibility
- Handshake or operation success
- Latency
- Payload/key/signature size
- Failure behavior
- Rollback and coexistence behavior

### Done when

The report distinguishes implementation evidence from theoretical quantum risk.

## 4.3 Qiskit learning notebook

### Build

Create a separate notebook explaining:

- Qubits and statevectors
- Bra-ket notation
- Gates and measurement
- Why Shor's algorithm threatens common public-key assumptions
- Why post-quantum cryptography normally runs on classical systems

### Done when

The notebook supports the threat-model explanation but is not falsely presented as the production migration scanner.

## Safety rule

Never implement a novel cryptographic algorithm for production use. Use reviewed standards and supported libraries, and involve qualified security/cryptography review for real deployments.

# Changelog

## v0.3.0 — Public portfolio baseline

### Security and configuration

- Generate a process-scoped signing secret for local Windows development instead of storing a reusable local secret.
- Require explicit, sufficiently long production secrets.
- Require secure cookies and disabled demo-user seeding in production mode.
- Add strict boolean and session-TTL environment parsing.
- Use a FastAPI application factory for Uvicorn and container startup.
- Add a non-root container health check and malformed-session-token handling.

### Quality engineering and evidence

- Add environment-safety tests for development and production configuration.
- Separate non-browser and Playwright tests into independent GitHub Actions jobs.
- Retain JUnit and coverage evidence and enforce an 80% non-browser coverage gate.
- Record the owner-verified local Playwright pass on the v0.2 learner baseline and the 15-test public suite.
- Verify the public GitHub quality gate: both non-browser and Playwright jobs pass and retain evidence artifacts.

### Documentation and curation

- Add an explicit production-readiness boundary and recruiter-focused README.
- Convert the spoken architecture/test review into a concise human-verification learning log.
- Remove personal scheduling, event-planning, and career-planning documents from the public project surface.

## v0.2.0 — Learner Edition

This release keeps the tested application behavior from v0.1 and adds a structured human-learning and portfolio workflow.

### Added

- Guided first session with exact Windows commands and a deliberate break/fix exercise.
- File-by-file architecture guide and Windows command reference.
- Learning workbook and AI-assisted-development review protocol.
- Personal `LEARNING_LOG.md` template.
- Career leverage map covering domain quality, SDET/framework work, secure systems assurance, AI TEVV, and the post-quantum/quantum bridge.
- Expanded milestone roadmap with learning objectives, build tasks, commands, and definitions of done.
- Four practical exercises: risk boundary, auditor role, login rate limiting, and CI failure evidence.
- Focused PowerShell scripts for API, security, E2E, fast, and crypto-inventory testing.
- GitHub publication checklist and CI verification guide.

### Improved

- Windows setup now detects Python 3.12 or 3.11 and includes a no-build-isolation installation fallback.
- Source and test comments now emphasize requirements, invariants, trust boundaries, and test-oracle reasoning rather than narrating syntax.
- Portfolio story now distinguishes verified evidence from future or unearned claims.

### Verified

- 11 non-browser unit, API, data-integrity, and security-regression tests pass.
- Non-browser application coverage is 84% in the build environment.
- The crypto-agility CLI generates the included Markdown report.
- The Playwright test is collected and launches Chromium, but local navigation is blocked by the managed build container; it must be verified on Windows or GitHub Actions.

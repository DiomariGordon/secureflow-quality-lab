# GitHub Publishing Checklist

Intended repository: `DiomariGordon/secureflow-quality-lab`

## Before publishing

```powershell
.\scripts\run_fast_tests.ps1
.\scripts\run_e2e_tests.ps1
```

Then confirm:

- No employer code, screenshots, data, requirements, or credentials are present.
- `.env`, `.venv`, `*.db`, Playwright artifacts, coverage output, and editor state are ignored.
- `.env.example` contains placeholders only.
- The public README and production-readiness limitations are accurate.
- The GitHub and LinkedIn contact links on the application resume are correct.

## Suggested repository settings

- Visibility: public
- Default branch: `main`
- Description: `Synthetic Python/Playwright quality-engineering lab for API, data-integrity, authorization, browser, CI, and crypto-agility testing.`
- Topics: `playwright`, `pytest`, `fastapi`, `quality-engineering`, `api-testing`, `security-testing`, `github-actions`, `python`

## First public verification

After the initial commit:

1. Open the `quality-gate` workflow.
2. Confirm the non-browser and Playwright steps both pass.
3. Download the `quality-evidence` artifact.
4. Compare the GitHub result with the local baseline.
5. Update `reports/verification-status.md` if the results differ.

Do not describe GitHub CI as verified until that workflow has completed successfully.

# Exercise 4 — CI Failure Evidence

## Objective

Make failures diagnosable without rerunning them locally first.

## Tasks

1. Configure Playwright screenshots and traces on failure.
2. Generate a machine-readable JUnit report.
3. Upload reports and traces in GitHub Actions even when tests fail.
4. Intentionally fail one browser assertion on a branch.
5. Download the CI artifact and identify the failure from evidence.
6. Restore the test and document the difference between product evidence and test-runner output.

## Commands

Local browser test:

```powershell
.\scripts\run_e2e_tests.ps1
```

Git review:

```powershell
git diff
git status
```

## Definition of done

A reviewer can determine what failed, where it failed, and what the browser displayed without access to your local machine.

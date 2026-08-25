# Windows Command Guide

Run commands from the project root in PowerShell.

## Environment and setup

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

Allows local PowerShell scripts only for the current terminal session. It does not permanently change machine policy.

```powershell
.\scripts\check_environment.ps1
```

Read-only environment check.

```powershell
.\scripts\setup_windows.ps1
```

Creates `.venv`, installs the project, and installs Playwright Chromium.

## Run the application

```powershell
.\scripts\run_windows.ps1
```

Starts the local FastAPI server at `http://127.0.0.1:8000`.

Stop it with `Ctrl+C`.

## Targeted tests

```powershell
.\scripts\run_fast_tests.ps1
```

Runs all non-browser tests with coverage. Use this after most code changes.

```powershell
.\scripts\run_api_tests.ps1
```

Runs API workflow and database-integrity tests.

```powershell
.\scripts\run_security_tests.ps1
```

Runs tests marked `security`.

```powershell
.\scripts\run_e2e_tests.ps1
```

Runs the Playwright browser workflow. The script starts the application fixture automatically.

```powershell
.\scripts\test_windows.ps1
```

Runs the entire suite.

## Run one test

```powershell
.\.venv\Scripts\python.exe -m pytest tests\api\test_security_regression.py::test_horizontal_access_is_blocked -vv -s
```

Anatomy:

- `python.exe -m pytest` runs pytest inside the project environment.
- The path selects one file.
- `::test_name` selects one test function.
- `-vv` increases detail.
- `-s` shows printed output instead of capturing it.

## Generate the crypto-agility report

```powershell
.\scripts\run_crypto_report.ps1
```

Reads `config/crypto_inventory.json` and writes `reports/crypto-readiness.md`.

This is an inventory and migration-readiness exercise, not a cryptographic audit.

## Git status

```powershell
git status
```

Shows modified, staged, and untracked files.

```powershell
git diff
```

Shows unstaged code changes. Read this before accepting AI-generated work.

```powershell
git diff --staged
```

Shows exactly what will be committed.

## Common troubleshooting

### `py` or `python` is not recognized

Install Python 3.11 or 3.12 and enable the Python launcher during installation. Then open a new PowerShell window.

### Script execution is disabled

Run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

### Playwright says the browser is missing

Run:

```powershell
.\.venv\Scripts\python.exe -m playwright install chromium
```

### Port 8000 is already in use

Find and stop the other local process, or run Uvicorn on another port:

```powershell
.\.venv\Scripts\python.exe -m uvicorn secureflow.app:app --reload --host 127.0.0.1 --port 8001
```

### Tests have stale local data

The tests use isolated temporary databases. The local application uses `secureflow.db`. Stop the server, delete only the local synthetic database, and restart:

```powershell
Remove-Item .\secureflow.db
.\scripts\run_windows.ps1
```

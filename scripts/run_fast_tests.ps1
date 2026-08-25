$ErrorActionPreference = "Stop"

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    throw "Virtual environment not found. Run .\scripts\setup_windows.ps1 first."
}

.\.venv\Scripts\python.exe -m pytest -m "not e2e" --cov=secureflow --cov-report=term-missing

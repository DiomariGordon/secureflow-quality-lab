$ErrorActionPreference = "Stop"

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    throw "Virtual environment not found. Run .\scripts\setup_windows.ps1 first."
}

.\.venv\Scripts\python.exe -m pytest tests\api\test_api_workflow.py tests\api\test_data_integrity.py -vv

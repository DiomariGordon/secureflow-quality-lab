$ErrorActionPreference = "Stop"

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    throw "Virtual environment not found. Run .\scripts\setup_windows.ps1 first."
}

# Development-only configuration. A fresh random signing secret is generated
# for this PowerShell process instead of storing a reusable credential in Git.
if (-not $env:SECUREFLOW_SECRET) {
    $secretBytes = New-Object byte[] 48
    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    try {
        $rng.GetBytes($secretBytes)
    }
    finally {
        $rng.Dispose()
    }
    $env:SECUREFLOW_SECRET = [Convert]::ToBase64String($secretBytes)
}

$env:SECUREFLOW_ENV = "development"
$env:SECUREFLOW_DB_PATH = ".\secureflow.db"
$env:SECUREFLOW_COOKIE_SECURE = "false"
$env:SECUREFLOW_SEED_DEMO_USERS = "true"

Write-Host "Starting SecureFlow at http://127.0.0.1:8000" -ForegroundColor Cyan
.\.venv\Scripts\python.exe -m uvicorn secureflow.app:create_app --factory --reload --host 127.0.0.1 --port 8000

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    throw "Virtual environment not found. Run .\scripts\setup_windows.ps1 first."
}

New-Item -ItemType Directory -Force -Path ".\reports" | Out-Null
.\.venv\Scripts\python.exe -m secureflow.crypto_inventory config\crypto_inventory.json --format markdown --output reports\crypto-readiness.md
Write-Host "Generated reports\crypto-readiness.md" -ForegroundColor Green

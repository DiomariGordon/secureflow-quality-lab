$ErrorActionPreference = "Stop"

function Test-ExternalCommand {
    param(
        [Parameter(Mandatory = $true)][string]$Command,
        [string[]]$Arguments = @()
    )

    try {
        & $Command @Arguments *> $null
        return $LASTEXITCODE -eq 0
    }
    catch {
        return $false
    }
}

Write-Host "SecureFlow environment check" -ForegroundColor Cyan
Write-Host "Project folder: $(Get-Location)"

if (-not (Test-Path ".\pyproject.toml")) {
    throw "pyproject.toml was not found. Open PowerShell in the SecureFlow project root."
}

$pythonFound = $false
if (Get-Command py -ErrorAction SilentlyContinue) {
    foreach ($version in @("3.12", "3.11")) {
        if (Test-ExternalCommand -Command "py" -Arguments @("-$version", "--version")) {
            $reported = & py "-$version" --version
            Write-Host "Python launcher: $reported" -ForegroundColor Green
            $pythonFound = $true
            break
        }
    }
}

if (-not $pythonFound -and (Get-Command python -ErrorAction SilentlyContinue)) {
    if (Test-ExternalCommand -Command "python" -Arguments @("--version")) {
        $reported = & python --version
        Write-Host "Python command: $reported" -ForegroundColor Green
        $pythonFound = $true
    }
}

if (-not $pythonFound) {
    Write-Host "Python 3.11 or 3.12 was not found." -ForegroundColor Red
    Write-Host "Install Python, enable the Python launcher, then open a new PowerShell window."
}

if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Host "Git: $(& git --version)" -ForegroundColor Green
}
else {
    Write-Host "Git was not found. The lab can run, but Git is required for the learning workflow and GitHub publishing." -ForegroundColor Yellow
}

if (Test-Path ".\.venv\Scripts\python.exe") {
    Write-Host "Virtual environment: present" -ForegroundColor Green
    Write-Host "Venv Python: $(& .\.venv\Scripts\python.exe --version)"
}
else {
    Write-Host "Virtual environment: not created yet" -ForegroundColor Yellow
}

if ($pythonFound) {
    Write-Host "Environment check complete." -ForegroundColor Cyan
}
else {
    exit 1
}

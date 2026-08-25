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

if (-not (Test-Path ".\pyproject.toml")) {
    throw "pyproject.toml was not found. Open PowerShell in the SecureFlow project root."
}

$launcherCommand = $null
$launcherArguments = @()

if (Get-Command py -ErrorAction SilentlyContinue) {
    foreach ($version in @("3.12", "3.11")) {
        if (Test-ExternalCommand -Command "py" -Arguments @("-$version", "--version")) {
            $launcherCommand = "py"
            $launcherArguments = @("-$version")
            break
        }
    }
}

if (-not $launcherCommand -and (Get-Command python -ErrorAction SilentlyContinue)) {
    if (Test-ExternalCommand -Command "python" -Arguments @("--version")) {
        $launcherCommand = "python"
    }
}

if (-not $launcherCommand) {
    throw "Python 3.11 or 3.12 was not found. Run .\scripts\check_environment.ps1 for guidance."
}

if (-not (Test-Path ".venv")) {
    Write-Host "Creating isolated virtual environment..." -ForegroundColor Cyan
    & $launcherCommand @launcherArguments -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        throw "Virtual environment creation failed."
    }
}

$venvPython = ".\.venv\Scripts\python.exe"

Write-Host "Upgrading pip and build tooling..." -ForegroundColor Cyan
& $venvPython -m pip install --upgrade pip setuptools wheel
if ($LASTEXITCODE -ne 0) {
    throw "Unable to install Python build tooling."
}

Write-Host "Installing SecureFlow and development dependencies..." -ForegroundColor Cyan
& $venvPython -m pip install -e ".[dev]"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Standard editable install failed; retrying without build isolation..." -ForegroundColor Yellow
    & $venvPython -m pip install --no-build-isolation -e ".[dev]"
    if ($LASTEXITCODE -ne 0) {
        throw "SecureFlow dependency installation failed."
    }
}

Write-Host "Installing Playwright Chromium..." -ForegroundColor Cyan
& $venvPython -m playwright install chromium

Write-Host "Setup complete." -ForegroundColor Green
Write-Host "Next: run .\scripts\run_windows.ps1 in this terminal, then open a second terminal for tests."

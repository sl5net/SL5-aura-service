# uninstall_ahk_copyq.ps1
# script_name: setup/uninstall_ahk_copyq.ps1

Write-Host "Starting uninstallation of optional client tools..." -ForegroundColor Cyan

# Check if winget is available
if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Error "Winget command not found. Cannot proceed with automated uninstallation."
    exit 1
}

# --- STEP 1: Stop running processes ---
Write-Host "Stopping running instances of CopyQ and AutoHotkey..." -ForegroundColor Yellow
Stop-Process -Name "copyq" -Force -ErrorAction SilentlyContinue
Stop-Process -Name "AutoHotkey" -Force -ErrorAction SilentlyContinue
Stop-Process -Name "AutoHotkey64" -Force -ErrorAction SilentlyContinue
Stop-Process -Name "AutoHotkey32" -Force -ErrorAction SilentlyContinue

# --- STEP 2: Uninstall CopyQ ---
Write-Host "Attempting to uninstall CopyQ..." -ForegroundColor Yellow
# We check if it is installed to avoid unnecessary error messages
$copyqCheck = winget list --id "hluk.CopyQ"
if ($copyqCheck) {
    winget uninstall --id "hluk.CopyQ" --silent --accept-source-agreements
    if ($LASTEXITCODE -eq 0) {
        Write-Host "CopyQ uninstalled successfully." -ForegroundColor Green
    } else {
        Write-Warning "CopyQ uninstallation finished with exit code $LASTEXITCODE."
    }
} else {
    Write-Host "CopyQ does not appear to be installed via Winget." -ForegroundColor DarkGray
}

# --- STEP 3: Uninstall AutoHotkey ---
Write-Host "Attempting to uninstall AutoHotkey..." -ForegroundColor Yellow
$ahkCheck = winget list --id "AutoHotkey.AutoHotkey"
if ($ahkCheck) {
    winget uninstall --id "AutoHotkey.AutoHotkey" --silent --accept-source-agreements
    if ($LASTEXITCODE -eq 0) {
        Write-Host "AutoHotkey uninstalled successfully." -ForegroundColor Green
    } else {
        Write-Warning "AutoHotkey uninstallation finished with exit code $LASTEXITCODE."
    }
} else {
    Write-Host "AutoHotkey does not appear to be installed via Winget." -ForegroundColor DarkGray
}

Write-Host "Uninstallation sequence finished." -ForegroundColor Cyan


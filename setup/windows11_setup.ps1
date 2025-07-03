# setup.ps1 - Setup script for Windows 11 Pro
# IMPORTANT: Right-click this file and choose "Run with PowerShell" to run as Administrator.

# 1. Check for Administrator privileges
Write-Host "Checking for Administrator privileges..."
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Warning "Administrator privileges are required to install software."
    Write-Warning "Please re-run this script by right-clicking it and selecting 'Run with PowerShell'."
    Read-Host "Press Enter to exit..."
    exit 1
}

# 2. Check for Winget and install dependencies
Write-Host "Installing system dependencies using Winget..."
try {
    winget --version > $null
} catch {
    Write-Error "Winget is not available. Please install or update it from the Microsoft Store."
    exit 1
}

# Install OpenJDK, Wget, and 7-Zip (for unzipping)
winget install --id Microsoft.OpenJDK.21 -e --accept-package-agreements
winget install --id GnuWin32.Wget -e --accept-source-agreements
winget install --id 7zip.7zip -e

# Add 7-Zip to the path for this session to ensure '7z.exe' is found.
$env:Path += ";C:\Program Files\7-Zip"

# 3. Create Python virtual environment
Write-Host "Creating Python virtual environment..."
if (-not (Test-Path -Path ".venv")) {
    python -m venv .venv
}

# 4. Install Python requirements
Write-Host "Installing Python requirements..."
# We call pip directly from the venv to avoid script execution policy issues with activation
.\.venv\Scripts\pip.exe install -r requirements.txt

# 5. Download external tools and models
Write-Host "Downloading external tools and models..."
$LT_VERSION = "6.6"
if (-not (Test-Path -Path "LanguageTool-$LT_VERSION")) {
  Write-Host "Downloading LanguageTool..."
  wget.exe "https://languagetool.org/download/LanguageTool-$($LT_VERSION).zip" -O "LanguageTool.zip"
  7z.exe x "LanguageTool.zip" -o"." > $null
  Remove-Item "LanguageTool.zip"
}

if (-not (Test-Path -Path "models")) {
    New-Item -ItemType Directory -Path "models" > $null
}

if (-not (Test-Path -Path "models/vosk-model-en-us-0.22")) {
  Write-Host "Downloading English Vosk model..."
  wget.exe "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip" -O "vosk-en.zip"
  7z.exe x "vosk-en.zip" -o"models/" > $null
  Remove-Item "vosk-en.zip"
}

if (-not (Test-Path -Path "models/vosk-model-de-0.21")) {
  Write-Host "Downloading German Vosk model..."
  wget.exe "https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip" -O "vosk-de.zip"
  7z.exe x "vosk-de.zip" -o"models/" > $null
  Remove-Item "vosk-de.zip"
}

Write-Host ""
Write-Host "------------------------------------------------------------------" -ForegroundColor Yellow
Write-Host "IMPORTANT: Windows setup is partially complete." -ForegroundColor Yellow
Write-Host "The application's core file watcher (inotifywait) is NOT compatible with Windows." -ForegroundColor Yellow
Write-Host "The Python code must be modified to use a cross-platform library like 'watchdog'." -ForegroundColor Yellow
Write-Host "------------------------------------------------------------------" -ForegroundColor Yellow
Write-Host ""
Write-Host "Setup finished."
Read-Host "Press Enter to exit..."


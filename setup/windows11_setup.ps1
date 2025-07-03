#
# setup/windows11_setup.ps1 - Setup script for Windows
# Run this setup script from the project's root directory.
# IMPORTANT: Right-click this file and choose "Run with PowerShell" to run it with the necessary permissions.
#

# --- 0. Preamble ---
# Exit immediately if a command fails
$ErrorActionPreference = "Stop"

# --- 1. Check for Administrator Privileges ---
Write-Host "--- Starting STT Setup for Windows ---"
Write-Host "--> Checking for Administrator privileges..."
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Warning "Administrator privileges are required to install system software via Winget."
    Write-Warning "Please re-run this script by right-clicking it and selecting 'Run with PowerShell'."
    Read-Host "Press Enter to exit..."
    exit 1
}

# --- 2. System Dependencies ---
Write-Host "--> Installing system dependencies using Winget..."
try {
    winget --version > $null
} catch {
    Write-Error "Winget is not available. Please install 'App Installer' from the Microsoft Store."
    Read-Host "Press Enter to exit..."
    exit 1
}

# Install OpenJDK for LanguageTool, Wget for downloading, and 7-Zip for unzipping.
winget install --id Microsoft.OpenJDK.21 -e --accept-package-agreements
winget install --id GnuWin32.Wget -e --accept-source-agreements
winget install --id 7zip.7zip -e

# Temporarily add 7-Zip to the PATH for this script session if it's not already there.
if (-not (Get-Command 7z.exe -ErrorAction SilentlyContinue)) {
    $env:Path += ";C:\Program Files\7-Zip"
}

# --- 3. Python Virtual Environment ---
Write-Host "--> Creating Python virtual environment in '.\.venv'..."
if (-not (Test-Path -Path ".\.venv")) {
    python -m venv .venv
} else {
    Write-Host "    -> Virtual environment already exists. Skipping creation."
}

# --- 4. Python Requirements ---
# We call pip directly from the venv to avoid PowerShell script execution policy issues with 'Activate.ps1'.
Write-Host "--> Installing Python requirements into the virtual environment..."
.\.venv\Scripts\pip.exe install -r requirements.txt

# --- 5. External Tools and Models ---
Write-Host "--> Downloading external tools and models (if missing)..."

# Download and extract LanguageTool
$LT_VERSION = "6.6"
if (-not (Test-Path -Path "LanguageTool-$LT_VERSION")) {
  Write-Host "    -> Downloading LanguageTool v$LT_VERSION..."
  wget.exe "https://languagetool.org/download/LanguageTool-$($LT_VERSION).zip" -O "languagetool.zip"
  7z.exe x "languagetool.zip" -o"." | Out-Null
  Remove-Item "languagetool.zip"
}

# Download and extract Vosk Models
New-Item -ItemType Directory -Path "models" -ErrorAction SilentlyContinue | Out-Null
if (-not (Test-Path -Path "models/vosk-model-en-us-0.22")) {
  Write-Host "    -> Downloading English Vosk model..."
  wget.exe "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip" -O "models/en.zip"
  7z.exe x "models/en.zip" -o"models/" | Out-Null
  Remove-Item "models/en.zip"
}

if (-not (Test-Path -Path "models/vosk-model-de-0.21")) {
  Write-Host "    -> Downloading German Vosk model..."
  wget.exe "https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip" -O "models/de.zip"
  7z.exe x "models/de.zip" -o"models/" | Out-Null
  Remove-Item "models/de.zip"
}

# --- 6. Project Configuration ---
# Ensures Python can treat 'config' directories as packages.
Write-Host "--> Creating Python package markers (__init__.py)..."
New-Item -Path "config/__init__.py" -ItemType File -Force | Out-Null
New-Item -Path "config/languagetool_server/__init__.py" -ItemType File -Force | Out-Null

# --- 7. Completion and CRITICAL WARNINGS ---
Write-Host ""
Write-Host "------------------------------------------------------------------" -ForegroundColor Red
Write-Host "CRITICAL: The application is NOT fully functional on Windows." -ForegroundColor Red
Write-Host "------------------------------------------------------------------" -ForegroundColor Red
Write-Host "The setup has installed all possible components, but key scripts must be re-written for Windows:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. File Trigger (`inotify-tools`):" -ForegroundColor Yellow
Write-Host "   The script that waits for '/tmp/vosk_trigger' uses Linux tools. A Windows-native"
Write-Host "   equivalent using PowerShell or a Python library like 'watchdog' is required."
Write-Host ""
Write-Host "2. Text Typing (`xdotool`):" -ForegroundColor Yellow
Write-Host "   The script that types the final text uses a Linux-only tool. A Windows-native"
Write-Host "   solution using PowerShell or a Python library like 'pyautogui' is required."
Write-Host ""
Write-Host "3. Audio (`portaudio`):" -ForegroundColor Yellow
Write-Host "   If the script fails with an audio error, you may need to manually download and"
Write-Host "   install the PortAudio library from its official website."
Write-Host ""
Write-Host "Setup has finished."
Read-Host "Press Enter to exit..."

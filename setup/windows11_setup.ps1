# setup/windows11_setup.ps1 - Vereinfachtes Setup-Skript für den GitHub Actions CI-Workflow
#

# --- Make script location-independent ---
$ProjectRoot = Split-Path -Path $PSScriptRoot -Parent
Set-Location -Path $ProjectRoot
Write-Host "--> Running setup from project root: (Get-Location)"

# --- 0. Preamble ---
$ErrorActionPreference = "Stop"

Write-Host "--- Starting STT Setup for Windows CI ---"

# HINWEIS: Die Admin-Prüfung, Java-Installation, Python-Installation und alle
# 'winget'-Aufrufe werden hier entfernt, da sie vom GitHub-Workflow (ci.yml)
# übernommen werden oder weil die Tools (wie 7-Zip) bereits vorhanden sind.

# --- 3. Python Virtual Environment ---
Write-Host "--> Creating Python virtual environment in '.\.venv'..."
if (-not (Test-Path -Path ".\.venv")) {
    python -m venv .venv
} else {
    Write-Host "    -> Virtual environment already exists. Skipping creation."
}

# --- 4. Python Requirements ---
Write-Host "--> Installing Python requirements into the virtual environment..."
.\.venv\Scripts\pip.exe install -r requirements.txt

# --- 5. External Tools and Models ---
Write-Host "--> Downloading external tools and models (if missing)..."

# Download and extract LanguageTool
$LT_VERSION = "6.6"
if (-not (Test-Path -Path "LanguageTool-$LT_VERSION")) {
  Write-Host "    -> Downloading LanguageTool v$LT_VERSION..."
  Invoke-WebRequest -Uri "https://languagetool.org/download/LanguageTool-$($LT_VERSION).zip" -OutFile "languagetool.zip"
  # Wir verwenden den direkten Pfad zu 7z, da dies auf den Runnern am zuverlässigsten ist.
  & "C:\Program Files\7-Zip\7z.exe" x "languagetool.zip" -o"." | Out-Null
  Remove-Item "languagetool.zip"
}

# Download and extract Vosk Models
New-Item -ItemType Directory -Path "models" -ErrorAction SilentlyContinue | Out-Null
if (-not (Test-Path -Path "models/vosk-model-en-us-0.22")) {
  Write-Host "    -> Downloading English Vosk model..."
  Invoke-WebRequest -Uri "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip" -OutFile "models/en.zip"
  & "C:\Program Files\7-Zip\7z.exe" x "models/en.zip" -o"models/" | Out-Null
  Remove-Item "models/en.zip"
}

if (-not (Test-Path -Path "models/vosk-model-de-0.21")) {
  Write-Host "    -> Downloading German Vosk model..."
  Invoke-WebRequest -Uri "https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip" -OutFile "models/de.zip"
  & "C:\Program Files\7-Zip\7z.exe" x "models/de.zip" -o"models/" | Out-Null
  Remove-Item "models/de.zip"
}

# --- Create central config file ---
Write-Host "--> Creating central config file..."
$ConfigDir = Join-Path -Path $env:USERPROFILE -ChildPath ".config\sl5-stt"
if (-not (Test-Path -Path $ConfigDir)) {
    Write-Host "    -> Creating config directory at $ConfigDir"
    New-Item -ItemType Directory -Path $ConfigDir | Out-Null
}
# Korrigiert, um Backslashes für Windows zu verwenden und dann für TOML zu normalisieren
$ProjectRootPath = (Get-Location).Path
$ConfigContent = @"
[paths]
project_root = "$($ProjectRootPath.Replace('\', '/'))"
"@
$ConfigFile = Join-Path -Path $ConfigDir -ChildPath "config.toml"
Set-Content -Path $ConfigFile -Value $ConfigContent

# --- 6. Project Configuration ---
Write-Host "--> Creating Python package markers (__init__.py)..."
New-Item -Path "config/__init__.py" -ItemType File -Force | Out-Null
New-Item -Path "config/languagetool_server/__init__.py" -ItemType File -Force | Out-Null

# --- 7. Completion ---
Write-Host ""
Write-Host "------------------------------------------------------------------" -ForegroundColor Green
Write-Host "CI Setup for Windows completed successfully." -ForegroundColor Green
Write-Host "------------------------------------------------------------------" -ForegroundColor Green

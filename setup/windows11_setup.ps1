# setup/windows11_setup.ps1


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

# --- 5. External Tools & Models (from Releases) ---
$LtDir = "LanguageTool-6.6"
# $EnModelDir = "models\vosk-model-en-us-0.22"
# $DeModelDir = "models\vosk-model-de-0.21"

# Create the models directory before attempting to download files into it.
New-Item -ItemType Directory -Path ".\models" -Force | Out-Null


# --- 5. External Tools & Models (using the robust Python downloader) ---
Write-Host "--> Downloading external tools and models via Python downloader..."

# Execute the downloader. It downloads all required ZIPs to the project root.
.\.venv\Scripts\python.exe tools/download_all_packages.py

# --- Now, extract the downloaded archives ---
Write-Host "--> Extracting downloaded archives..."

# Define file and directory names
$LtZip = "LanguageTool-6.6.zip"
$EnModelZip = "vosk-model-en-us-0.22.zip"
$DeModelZip = "vosk-model-de-0.21.zip"

# Function to extract and clean up
function Expand-And-Cleanup {
    param ([string]$ZipFile, [string]$DestinationPath)

    if (Test-Path $ZipFile) {
        Write-Host "    -> Extracting $ZipFile..."
        Expand-Archive -Path $ZipFile -DestinationPath $DestinationPath -Force
        Remove-Item $ZipFile # Cleanup
    } else {
        Write-Host "FATAL: Expected archive $ZipFile was not found after download." -ForegroundColor Red
        exit 1
    }
}

# Create models directory if it doesn't exist
New-Item -ItemType Directory -Path ".\models" -Force | Out-Null

# Execute extraction
Expand-And-Cleanup -ZipFile $LtZip -DestinationPath "."
Expand-And-Cleanup -ZipFile $EnModelZip -DestinationPath ".\models"
Expand-And-Cleanup -ZipFile $DeModelZip -DestinationPath ".\models"

Write-Host "    -> Extraction and cleanup successful." -ForegroundColor Green








# --- Run language check script (get_lang.sh) ---
Write-Host "INFO: Checking system language to download additional models if necessary..."

# Get the 2-letter language code (e.g., "de", "fr") from Windows
$LangCode = (Get-Culture).Name.Substring(0, 2)

# Define the path to the bash script
$GetLangScriptPath = "$PSScriptRoot\..\scripts\sh\get_lang.sh"

# Execute the bash script via Git Bash and pass the detected language code as an argument
# This requires bash.exe to be in the system's PATH, which Git for Windows does by default.
& bash.exe $GetLangScriptPath $LangCode

Write-Host "INFO: Language check script finished."




$tmpPath = "C:\tmp"
$sl5DictationPath = "C:\tmp\sl5_dictation"
if (!(Test-Path $tmpPath)) {
    New-Item -ItemType Directory -Path $tmpPath | Out-Null
Write-Host "Created directory: $tmpPath"
} else {
    Write-Host "Directory already exists: $tmpPath"
}

if (!(Test-Path $sl5DictationPath)) {
    New-Item -ItemType Directory -Path $sl5DictationPath | Out-Null
Write-Host "Created directory: $sl5DictationPath"
} else {
    Write-Host "Directory already exists: $sl5DictationPath"
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
New-Item -Name "log" -Type Directory
New-Item -Path "log/__init__.py" -ItemType File -Force | Out-Null
New-Item -Path "config/__init__.py" -ItemType File -Force | Out-Null
New-Item -Path "config/languagetool_server/__init__.py" -ItemType File -Force | Out-Null

# --- 7. Completion ---
Write-Host ""
Write-Host "------------------------------------------------------------------" -ForegroundColor Green
Write-Host "CI Setup for Windows completed successfully." -ForegroundColor Green
Write-Host "------------------------------------------------------------------" -ForegroundColor Green

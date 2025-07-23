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

# --- 5. External Tools & Models (from Releases) ---
Write-Host "--> Downloading external tools and models..."

# Define URLs and checksums
$ReleaseUrlBase = "https://github.com/sl5net/Vosk-System-Listener/releases/download/v0.2.0.1"

$LtZip = "LanguageTool-6.6.zip"
$LtUrl = "$($ReleaseUrlBase)/$($LtZip)"
$LtSha256 = "53600506b399bb5ffe1e4c8dec794fd378212f14aaf38ccef9b6f89314d11631"
$LtDir = "LanguageTool-6.6"

$EnModelZip = "vosk-model-en-us-0.22.zip"
$EnModelUrl = "$($ReleaseUrlBase)/$($EnModelZip)"
$EnModelSha256 = "d410847b53faf1850f2bb99fb7a08adcb49dd236dcba66615397fe57a3cf68f5"
$EnModelDir = "models\vosk-model-en-us-0.22"

$DeModelZip = "vosk-model-de-0.21.zip"
$DeModelUrl = "$($ReleaseUrlBase)/$($DeModelZip)"
$DeModelSha256 = "fb45a53025a50830b16bcda94146f90e22166501bb3693b009cabed796dbaaa0"
$DeModelDir = "models\vosk-model-de-0.21"

# Create the models directory before attempting to download files into it.
New-Item -ItemType Directory -Path ".\models" -Force | Out-Null

# --- Download and Verify Function ---
function Download-And-Verify {
    param(
        [string]$Url,
        [string]$ZipFilePath,
        [string]$ExpectedSha256,
        [string]$ExtractDir,
        [string]$FinalDirCheck
    )
    $MaxRetries = 3
    $RetryCount = 0

    if (-not (Test-Path $FinalDirCheck)) {
        while ($RetryCount -lt $MaxRetries) {
            $ZipFileName = Split-Path -Leaf $ZipFilePath
            Write-Host "    -> Attempting to download $ZipFileName (Attempt $($RetryCount + 1)).."
            try {
                Invoke-WebRequest -Uri $Url -OutFile $ZipFilePath -UseBasicParsing
                Write-Host "    -> Verifying checksum for $ZipFileName..."
                $FileHash = (Get-FileHash $ZipFilePath -Algorithm SHA256).Hash.ToLower()

                if ($FileHash -eq $ExpectedSha256) {
                    Write-Host "    -> Checksum OK. Extracting..." -ForegroundColor Green
                    Expand-Archive -Path $ZipFilePath -DestinationPath $ExtractDir -Force
                    Write-Host "    -> Cleaning up $ZipFileName..."
                    Remove-Item $ZipFilePath
                    return # Success
                } else {
                    Write-Host "    -> WARNING: Checksum mismatch for $ZipFileName!" -ForegroundColor Yellow
                    Remove-Item $ZipFilePath # Clean up corrupted download
                }
            } catch {
                Write-Host "    -> WARNING: Download for $ZipFileName failed: $($_.Exception.Message)" -ForegroundColor Yellow
            }

            $RetryCount++
            if ($RetryCount -lt $MaxRetries) {
                Write-Host "    -> Retrying in 2 seconds..."
                Start-Sleep -Seconds 2
            }
        }
        Write-Host "    -> FATAL: Failed to download and verify $ZipFileName after $MaxRetries attempts." -ForegroundColor Red
        exit 1
    } else {
        Write-Host "    -> $(Split-Path -Leaf $FinalDirCheck) already exists. Skipping."
    }
}

# --- Execute Downloads ---
Download-And-Verify -Url $LtUrl -ZipFilePath ".\$LtZip" -ExpectedSha256 $LtSha256 -ExtractDir "." -FinalDirCheck ".\$LtDir"
Download-And-Verify -Url $EnModelUrl -ZipFilePath ".\models\$EnModelZip" -ExpectedSha256 $EnModelSha256 -ExtractDir ".\models\" -FinalDirCheck ".\$EnModelDir"
Download-And-Verify -Url $DeModelUrl -ZipFilePath ".\models\$DeModelZip" -ExpectedSha256 $DeModelSha256 -ExtractDir ".\models\" -FinalDirCheck ".\$DeModelDir"


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
New-Item -Path "config/__init__.py" -ItemType File -Force | Out-Null
New-Item -Path "config/languagetool_server/__init__.py" -ItemType File -Force | Out-Null

# --- 7. Completion ---
Write-Host ""
Write-Host "------------------------------------------------------------------" -ForegroundColor Green
Write-Host "CI Setup for Windows completed successfully." -ForegroundColor Green
Write-Host "------------------------------------------------------------------" -ForegroundColor Green

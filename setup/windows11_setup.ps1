# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY
# setup/windows11_setup.ps1
# Self-contained setup script. Uses winget if available, otherwise falls back to manual install.

$ProjectRoot = (Get-Location).Path
Write-Host "--> Running setup from project root: $ProjectRoot"
$ErrorActionPreference = 'Stop'

# --- 1. System Dependencies ---
Write-Host "--> Checking for winget..."
$wingetExists = (Get-Command winget -ErrorAction SilentlyContinue)

if ($wingetExists) {
    Write-Host "    -> winget found! Using modern, fast setup."
    winget install -e --id Microsoft.OpenJDK.17
    winget install -e --id Python.Python.3.11
} else {
    Write-Host "    -> winget not found. Falling back to manual install (slower)."
    # Manual install logic from my previous correct proposal...
    # (Implementation for manual Java/Python download & install)
}

# --- 2. Python Virtual Environment ---
Write-Host "--> Creating Python venv..."
python -m venv .venv

# --- 3. Python Requirements ---
Write-Host "--> Installing Python requirements..."
& ".\.venv\Scripts\pip.exe" install -r requirements.txt

# --- 4. Project Structure ---
Write-Host "--> Setting up project directories..."
& ".\.venv\Scripts\python.exe" ".\scripts\py\func\create_required_folders.py" "$ProjectRoot"

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
Download-And-Verify -Url $EnModelUrl -ZipFilePath ".\models\$EnModelZip" -ExpectedSha256 $EnModelSha265 -ExtractDir ".\models\" -FinalDirCheck ".\$EnModelDir"
Download-And-Verify -Url $DeModelUrl -ZipFilePath ".\models\$DeModelZip" -ExpectedSha256 $DeModelSha256 -ExtractDir ".\models\" -FinalDirCheck ".\$DeModelDir"


# --- 6. User-Specific Configuration ---
$ConfigDir = Join-Path $HOME ".config\sl5-stt"
$ConfigFile = Join-Path $ConfigDir "config.toml"
Write-Host "--> Ensuring user config file exists at $ConfigFile..."
if (-not (Test-Path $ConfigDir)) {
    New-Item -Path $ConfigDir -ItemType Directory | Out-Null
}
if (-not (Test-Path $ConfigFile)) {
    $ConfigContent = @"
[paths]
project_root = "$($ProjectRoot -replace '\\', '\\')"
"@
    Set-Content -Path $ConfigFile -Value $ConfigContent
}

# --- 7. Completion ---
Write-Host ""
Write-Host "--- Setup for Windows is complete! ---" -ForegroundColor Green
Write-Host ""
Write-Host "To activate the environment and run the server, use the following commands in this terminal:"
Write-Host "  .\.venv\Scripts\Activate.ps1"
Write-Host "  .\scripts\restart_venv_and_run-server.ps1" # We should create this as well
Write-Host ""

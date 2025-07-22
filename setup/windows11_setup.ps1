# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY
#
# setup/windows11_setup_v2.ps1
#
# Smart setup script: Uses winget if available for speed, otherwise falls back
# to manual downloads to ensure compatibility with CI environments.

# --- Make script location-independent ---
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location (Join-Path $ScriptDir "..")
$ProjectRoot = (Get-Location).Path
Write-Host "--> Running setup from project root: $ProjectRoot"

$ErrorActionPreference = 'Stop'
Write-Host "--- Starting SL5 Dictation Setup for Windows ---"

# --- 1. System Dependencies ---
Write-Host "--> Checking for winget package manager..."
$wingetExists = (Get-Command winget -ErrorAction SilentlyContinue)

if ($wingetExists) {
    Write-Host "    -> winget found! Using modern, fast setup."
    winget install -e --id Microsoft.OpenJDK.17
    winget install -e --id Python.Python.3
} else {
    Write-Host "    -> winget not found. Falling back to manual installation (slower, for CI compatibility)."

    # Manual Python Install
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Host "    -> Manually installing Python 3..."
        $pyUrl = "https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe"
        $pyInstaller = Join-Path $env:TEMP "python_installer.exe"
        Invoke-WebRequest -Uri $pyUrl -OutFile $pyInstaller
        Start-Process -FilePath $pyInstaller -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
        Remove-Item $pyInstaller
        # Refresh PATH for the current session
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        Write-Host "    -> Python installed."
    } else {
        Write-Host "    -> Python is already installed."
    }

    # Manual Java Install
    if (-not (Get-Command java -ErrorAction SilentlyContinue)) {
        Write-Host "    -> Manually installing OpenJDK 17..."
        $jdkUrl = "https://aka.ms/download-jdk/microsoft-jdk-17-windows-x64.zip"
        $jdkZip = Join-Path $env:TEMP "openjdk.zip"
        $jdkDir = "C:\ProgramData\Microsoft\jdk-17"
        Invoke-WebRequest -Uri $jdkUrl -OutFile $jdkZip
        Expand-Archive -Path $jdkZip -DestinationPath $env:TEMP\jdk_extract -Force
        $jdkInnerFolder = (Get-ChildItem -Path $env:TEMP\jdk_extract | Select-Object -First 1).FullName
        Move-Item -Path $jdkInnerFolder -Destination $jdkDir
        # Add Java to PATH for the current session
        $env:Path = "$jdkDir\bin;" + $env:Path
        Remove-Item $jdkZip
        Remove-Item -Recurse -Force $env:TEMP\jdk_extract
        Write-Host "    -> OpenJDK installed and added to PATH."
    } else {
        Write-Host "    -> Java is already installed."
    }
}



# --- 2. Python Virtual Environment ---
if (-not (Test-Path -Path ".\.venv")) {
    Write-Host "--> Creating Python virtual environment in '.\.venv'..."
    python -m venv .venv
} else {
    Write-Host "--> Virtual environment already exists. Skipping creation."
}

# --- 3. Python Requirements ---
Write-Host "--> Installing Python requirements into the virtual environment..."
& ".\.venv\Scripts\pip.exe" install -r requirements.txt

# --- 4. Project Structure and Configuration ---
Write-Host "--> Setting up project directories and initial files via Python script..."
# Centralized script for cross-platform consistency
& ".\.venv\Scripts\python.exe" ".\scripts\py\func\create_required_folders.py" "$ProjectRoot"

# --- 5. External Tools and Models (from GitHub Releases) ---
Write-Host "--> Downloading external tools and models from project GitHub Releases..."

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

# setup/windows11_setup.ps1

#  how to start:
#  .\setup\windows11_setup.ps1 -Exclude "en" or .\setup\windows11_setup.ps1 -Exclude "de" or .\setup\windows11_setup.ps1 -Exclude "all".

# --- Argument Parsing for Exclusion (NEW) ---
param(
    [string]$Exclude = $null
)

# --- Make script location-independent ---
$ProjectRoot = Split-Path -Path $PSScriptRoot -Parent
Set-Location -Path $ProjectRoot
Write-Host "--> Running setup from project root: $(Get-Location)"

$EXCLUDE_LANGUAGES = $Exclude

if (-not [string]::IsNullOrEmpty($EXCLUDE_LANGUAGES)) {
    Write-Host "--> Exclusion list detected: $EXCLUDE_LANGUAGES" -ForegroundColor Yellow
} else {
    Write-Host "No exclusion list provided."
}
# --- End Argument Parsing ---


$ErrorActionPreference = "Stop"

# Configuration: Set to $false to keep ZIP files after extraction or use $true
$should_remove_zips_after_unpack = $true
# --- 1. Admin Rights Check ---
Write-Host "[*] Checking for Administrator privileges"



# Only check for admin rights if NOT running in a CI environment (like GitHub Actions)
if ($env:CI -ne 'true') {
    # Check if the current user is an Administrator
    $isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

    if (-not $isAdmin) {
        Write-Host "[ERROR] Administrator privileges are required. Re-launching..."
        # Re-run the current script with elevated privileges for GitHub Actions
        Start-Process -FilePath $PSCommandPath -Verb RunAs
        # Exit the current (non-admin) script
        exit
    }
}
Write-Host "[SUCCESS] Running with Administrator privileges."









# Only check for java if NOT running in a CI environment (like GitHub Actions)
if ($env:CI -ne 'true')
{
    # --- 2. Java Installation Check ---
    Write-Host "--> Checking Java installation..."
    $JavaVersion = $null
    try
    {
        $JavaOutput = & java -version 2>&1
        if ($JavaOutput -match 'version "(\d+)\.')
        {
            $JavaVersion = [int]$matches[1]
        }
        elseif ($JavaOutput -match 'version "1\.(\d+)\.')
        {
            $JavaVersion = [int]$matches[1]
        }
    }
    catch
    {
        Write-Host "    -> Java not found in PATH."
    }

    # setup/windows11_setup.ps1:81
    if ($JavaVersion -and $JavaVersion -ge 17)
    {
        Write-Host "    -> Java $JavaVersion detected. OK." -ForegroundColor Green
    }
    else
    {
        Write-Host "    -> Java 17+ not found. Installing OpenJDK 17..." -ForegroundColor Yellow
        try
        {
            # setup/windows11_setup.ps1:91
            winget install --id Microsoft.OpenJDK.17 --silent --accept-source-agreements --accept-package-agreements --force
            if ($LASTEXITCODE -eq 0)
            {
                Write-Host "    -> OpenJDK 17 installed successfully." -ForegroundColor Green
                # Refresh PATH for current session
                $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
            }
            else
            {
                Write-Host "ERROR: Failed to install OpenJDK 17. Please install manually." -ForegroundColor Red
                # exit 1 # the script works anywas usuallly. dont exit here!
            }
        }
        catch
        {
            Write-Host "ERROR: Failed to install Java. Please install Java 17+ manually." -ForegroundColor Red
            exit 1
        }
    }
}



# --- 3. Python Installation Check ---
Write-Host "--> Checking Python installation..."
$PythonVersion = $null
try {
    $PythonOutput = & python --version 2>&1
    if ($PythonOutput -match 'Python (\d+)\.(\d+)') {
        $PythonMajor = [int]$matches[1]
        $PythonMinor = [int]$matches[2]
        if ($PythonMajor -eq 3 -and $PythonMinor -ge 8) {
            $PythonVersion = "$PythonMajor.$PythonMinor"
        }
    }
} catch {
    Write-Host "    -> Python not found in PATH."
}

if ($PythonVersion) {
    Write-Host "    -> Python $PythonVersion detected. OK." -ForegroundColor Green
} else {
    Write-Host "    -> Python 3.8+ not found. Installing Python 3.11..." -ForegroundColor Yellow
    try {
        winget install --id Python.Python.3.11 --silent --accept-source-agreements --accept-package-agreements
        if ($LASTEXITCODE -eq 0) {
            Write-Host "    -> Python 3.11 installed successfully." -ForegroundColor Green
            # Refresh PATH for current session
            $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
        } else {
            Write-Host "ERROR: Failed to install Python. Please install manually." -ForegroundColor Red
            exit 1
        }
    } catch {
        Write-Host "ERROR: Failed to install Python. Please install Python 3.8+ manually." -ForegroundColor Red
        exit 1
    }
}

# --- 3. Python Virtual Environment ---
Write-Host "--> Creating Python virtual environment in '.\.venv'..."
if (-not (Test-Path -Path ".\.venv")) {
    python -m venv .venv
} else {
    Write-Host "    -> Virtual environment already exists. Skipping creation."
}


# --- PATCH: Replace fasttext with fasttext-wheel in requirements.txt ---
Write-Host "--> Patching requirements.txt for Windows fasttext-wheel compatibility..."
(Get-Content requirements.txt) -replace '^fasttext.*$', 'fasttext-wheel' | Set-Content requirements.txt


# --- 5. Python Requirements ---
Write-Host "--> Installing Python requirements into the virtual environment..."

.\.venv\Scripts\pip.exe install --upgrade pip

.\.venv\Scripts\pip.exe install -r requirements.txt

# --- 5. External Tools & Models (from Releases) ---
$LtDir = "LanguageTool-6.6"





# --- 6. External Tools & Models (using the robust Python downloader) ---
Write-Host "--> Downloading external tools and models via Python downloader..."

# Create the models directory before attempting to download files into it.
New-Item -ItemType Directory -Path ".\models" -Force | Out-Null

# setup/windows11_setup.ps1:183
# Execute the downloader and check its exit code
#  It downloads all required ZIPs to the project root.
.\.venv\Scripts\python.exe tools/download_all_packages.py --exclude "$EXCLUDE_LANGUAGES"

# $LASTEXITCODE contains the exit code of the last program that was run.
# 0 means success. Anything else is an error.
if ($LASTEXITCODE -ne 0) {
    Write-Host "FATAL: The Python download script failed. Halting setup." -ForegroundColor Red
    # Wir benutzen 'exit 1', um das ganze Skript sofort zu beenden.
    exit 1
}

Write-Host "    -> Python downloader completed successfully." -ForegroundColor Green

# --- Now, extract the downloaded archives ---
Write-Host "--> Extracting downloaded archives..."








# setup/windows11_setup.ps1:207
# --- Configuration: Base List of Archives ---
$Prefix = "Z_"
$MasterConfig = @(
    @{ BaseName = "LanguageTool-6.6";              FinalName = "LanguageTool-6.6"; Dest = "." },
    @{ BaseName = "vosk-model-en-us-0.22";         FinalName = "vosk-model-en-us-0.22"; Dest = ".\models" },
    @{ BaseName = "vosk-model-small-en-us-0.15";   FinalName = "vosk-model-small-en-us-0.15"; Dest = ".\models" },
    @{ BaseName = "vosk-model-de-0.21";            FinalName = "vosk-model-de-0.21"; Dest = ".\models" },
    @{ BaseName = "lid.176";                       FinalName = "lid.176.bin"; Dest = ".\models" }
)

# --- Filter Configuration based on EXCLUDE_LANGUAGES (NEW) ---
$INSTALL_CONFIG = @()
$ExcludeList = @($EXCLUDE_LANGUAGES.Split(',') | ForEach-Object { $_.Trim().ToLower() })

if ($ExcludeList.Count -eq 0 -or $ExcludeList[0] -eq "") {
    # No exclusion, use master list
    $INSTALL_CONFIG = $MasterConfig
} else {
    # Exclusion active, filter the list
    foreach ($ConfigItem in $MasterConfig) {
        $IsMandatory = $ConfigItem.BaseName -like "LanguageTool-*" -or $ConfigItem.BaseName -eq "lid.176"
        $IsExcluded = $false

        # 1. Exclusion Check: exclude=all
        if ($ExcludeList -contains "all" -and -not $IsMandatory) {
            Write-Host "    -> Excluding (all): $($ConfigItem.BaseName)"
            $IsExcluded = $true
        }

        # 2. Exclusion Check: Specific Languages
        if (-not $IsExcluded) {
            # Check for 'de' exclusion
            if ($ExcludeList -contains "de" -and $ConfigItem.BaseName -like "*vosk-model-de-*") {
                Write-Host "    -> Excluding (de): $($ConfigItem.BaseName)"
                $IsExcluded = $true
            }
            # Check for 'en' exclusion (covers both en-us models)
            if ($ExcludeList -contains "en" -and $ConfigItem.BaseName -like "*vosk-model*en-us*") {
                Write-Host "    -> Excluding (en): $($ConfigItem.BaseName)"
                $IsExcluded = $true
            }
            # Add other specific language checks here if needed...
        }

        # Only add if not excluded
        if (-not $IsExcluded) {
            $INSTALL_CONFIG += $ConfigItem
        }
    }
}

# Now, create the ArchiveConfig from the filtered INSTALL_CONFIG
$ArchiveConfig = $INSTALL_CONFIG | ForEach-Object {
    [PSCustomObject]@{
        Zip  = "$($Prefix)$($_.BaseName).zip"
        Dir  = $_.BaseName
        Dest = $_.Dest
    }
}
# --- End Filter Configuration ---

# setup/windows11_setup.ps1:269
# Function to extract and clean up
function Expand-And-Cleanup {
    param (
        [string]$ZipFile,
        [string]$DestinationPath,
        [string]$ExpectedDirName,
        [bool]$CleanupAfterExtraction
    )

    # FIX 1: Use absolute path based on ProjectRoot (Prevents System32 errors)
    $AbsDest = Join-Path -Path $ProjectRoot -ChildPath $DestinationPath
    $FinalFullPath = Join-Path -Path $AbsDest -ChildPath $ExpectedDirName

    # FIX 2: Check for file/folder existence (Handle lid.176 vs lid.176.bin)
    $TargetExists = $false
    if (Test-Path $FinalFullPath) {
        $TargetExists = $true
    } elseif (Test-Path "$FinalFullPath.bin") {
        # This catches the case where config says "lid.176" but file is "lid.176.bin"
        $TargetExists = $true
    }

    if ($TargetExists) {
        Write-Host "    -> Target '$ExpectedDirName' already exists. Skipping extraction."
        return
    }

    # Look for the downloaded ZIP
    $FinalZipPath = Join-Path -Path $ProjectRoot -ChildPath $ZipFile

    if (-not (Test-Path $FinalZipPath)) {
        Write-Host "FATAL: Expected archive not found: '$FinalZipPath'" -ForegroundColor Red
        Write-Host "       The Python download script should have created this file." -ForegroundColor Red
        exit 1
    }

    Write-Host "    -> Extracting $ZipFile to $DestinationPath..."

    # Ensure destination directory exists
    if (-not (Test-Path $AbsDest)) {
        New-Item -ItemType Directory -Force -Path $AbsDest | Out-Null
    }

    Expand-Archive -Path $FinalZipPath -DestinationPath $AbsDest -Force

    if ($CleanupAfterExtraction) {
        Remove-Item $FinalZipPath -Force
        Write-Host "    -> Cleaned up ZIP file: $ZipFile"
    } else {
        Write-Host "    -> Keeping ZIP file: $ZipFile"
    }
}



# Execute extraction for each archive
foreach ($Config in $ArchiveConfig) {
    Expand-And-Cleanup -ZipFile $Config.Zip -DestinationPath $Config.Dest -ExpectedDirName $Config.Dir -CleanupAfterExtraction $should_remove_zips_after_unpack
}


Write-Host "    -> Extraction and cleanup successful." -ForegroundColor Green





# --- Run initial model setup ---
Write-Host "INFO: Setting up initial models based on system language..."

# Get the 2-letter language code (e.g., "de", "fr") from Windows
$LangCode = (Get-Culture).Name.Substring(0, 2)

# Define the path to the Python script
$SetupModelScriptPath = ".\scripts\py\func\setup_initial_model.py"

# Check if the Python script exists
if (Test-Path $SetupModelScriptPath) {
    Write-Host "    -> Running setup_initial_model.py with language code: $LangCode"

    # Execute the Python script with the detected language code
    .\.venv\Scripts\python.exe $SetupModelScriptPath $LangCode

    if ($LASTEXITCODE -eq 0) {
        Write-Host "INFO: Initial model setup completed successfully." -ForegroundColor Green
    } else {
        Write-Host "WARNING: Initial model setup failed with exit code: $LASTEXITCODE" -ForegroundColor Yellow
    }
} else {
    Write-Host "WARNING: Initial model setup script not found at: $SetupModelScriptPath" -ForegroundColor Yellow
}

# --- Create required directories ---
$tmpPath = "C:\tmp"
$sl5DictationPath = "C:\tmp\sl5_aura"

@($tmpPath, $sl5DictationPath) | ForEach-Object {
    if (!(Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ | Out-Null
        Write-Host "Created directory: $_"
    } else {
        Write-Host "Directory already exists: $_"
    }
}

# --- Create central config file ---
Write-Host "--> Creating central config file..."
$ConfigDir = Join-Path -Path $env:USERPROFILE -ChildPath ".config\sl5-stt"
if (-not (Test-Path -Path $ConfigDir)) {
    Write-Host "    -> Creating config directory at $ConfigDir"
    New-Item -ItemType Directory -Path $ConfigDir -Force | Out-Null
}

# Korrigiert, um Backslashes für Windows zu verwenden und dann für TOML zu normalisieren
$ProjectRootPath = (Get-Location).Path
$ConfigContent = @"
[paths]
project_root = "$($ProjectRootPath.Replace('\', '/'))"
"@
$ConfigFile = Join-Path -Path $ConfigDir -ChildPath "config.toml"
Set-Content -Path $ConfigFile -Value $ConfigContent

# --- 9. Project Configuration ---
Write-Host "--> Creating Python package markers (__init__.py)..."

# Create log directory if it doesn't exist
if (-not (Test-Path "log")) {
    New-Item -Name "log" -ItemType Directory | Out-Null
}

# Create __init__.py files
@("log/__init__.py", "config/__init__.py", "config/languagetool_server/__init__.py") | ForEach-Object {
    $Directory = Split-Path -Path $_ -Parent
    if ($Directory -and (-not (Test-Path $Directory))) {
        New-Item -ItemType Directory -Path $Directory -Force | Out-Null
    }
    New-Item -Path $_ -ItemType File -Force | Out-Null
}

# --- 10. Completion ---
Write-Host ""
Write-Host "------------------------------------------------------------------" -ForegroundColor Green
Write-Host "------- setup/windows11_setup.ps1:413 ---" -ForegroundColor Green
Write-Host "Setup for Windows completed successfully." -ForegroundColor Green
Write-Host "------------------------------------------------------------------" -ForegroundColor Green


<#
Source - https://superuser.com/a/882297
Posted by chingNotCHing
Retrieved 2026-01-21, License - CC BY-SA 3.0
#>

call "%~dp0setup\fix_permissions.bat"

& .\SystemCheck.ps1



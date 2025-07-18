#
# setup/windows11_setup.ps1 - Setup script for Windows
# Run this setup script from the project's root directory.
# IMPORTANT: Right-click this file and choose "Run with PowerShell" to run it with the necessary permissions.
#


# --- Make script location-independent ---
# This block ensures the script can be run from any directory by changing
# the working directory to the project root.
$ProjectRoot = Split-Path -Path $PSScriptRoot -Parent
Set-Location -Path $ProjectRoot

Write-Host "--> Running setup from project root: (Get-Location)"
# --- End of location-independent block ---


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



if (!(Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Host "Winget is not installed. Installing Winget..."
    $downloadUrl = "https://github.com/microsoft/winget-cli/releases/latest/download/Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.appxbundle"
    $downloadPath = "C:\Temp\Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.appxbundle"
    $retryCount = 3
    $retryWaitTime = 5 # seconds

    for ($i = 1; $i -le $retryCount; $i++) {
        try {
            Invoke-WebRequest -Uri $downloadUrl -OutFile $downloadPath
            Start-Process -FilePath $downloadPath -Wait -PassThru
            break
        } catch {
            Write-Host "Failed to download Winget installer. Retrying in $retryWaitTime seconds..."
            Start-Sleep -Seconds $retryWaitTime
        }
    }
}




# --- 2. System Dependencies ---
Write-Host "--> Checking for a compatible Java version (>=17)..."
$javaOK = $false
if (Get-Command java -ErrorAction SilentlyContinue) {
    # Wir fangen den erwarteten Fehler von 'java -version' ab, da es auf stderr schreibt.
    $versionOutput = ""
    try {
        # '-ErrorAction Stop' ist hier wichtig, damit der catch-Block zuverlässig ausgelöst wird.
        $versionOutput = java -version -ErrorAction Stop 2>&1
    } catch {
        # Die Versionsinformation, die wir wollen, ist die eigentliche Fehlermeldung.
        $versionOutput = $_.Exception.Message
    }

    # Jetzt prüfen wir die abgefangene Ausgabe
    if ($versionOutput -match 'version "(\d+)\.') {
        $majorVersion = [int]$matches[1]
        if ($majorVersion -ge 17) {
            Write-Host "    -> Found compatible Java version $majorVersion. OK."
            $javaOK = $true
        } else {
            Write-Host "    -> Found Java version $majorVersion, but we need >=17."
        }
    }
} else {
    Write-Host "    -> No Java executable found."
}

if (-not $javaOK) {
    Write-Host "    -> Installing a modern JDK via Winget..."
    winget install --id Microsoft.OpenJDK.21 -e --accept-package-agreements
}

Write-Host "--> Installing other core dependencies..."
winget install --id GnuWin32.Wget -e --accept-source-agreements
winget install --id 7zip.7zip -e

# Temporarily add 7-Zip to the PATH
if (-not (Get-Command 7z.exe -ErrorAction SilentlyContinue)) {
    $env:Path += ";C:\Program Files\7-Zip"
}


# --- 2.5. Python-Installation prüfen (VERBESSERTE VERSION) ---
Write-Host "--> Checking for a real Python installation..."
$PythonCmd = Get-Command python -ErrorAction SilentlyContinue
# Prüft, ob der Befehl nicht existiert ODER ob er der nutzlose App-Alias ist
if (-not $PythonCmd -or $PythonCmd.Source -like "*Microsoft\WindowsApps*") {
    Write-Host "    -> Python not found or is a store alias. Installing Python 3.11 via Winget..."
    winget install --id Python.Python.3.11 -e --accept-source-agreements

    Write-Host ""
    Write-Host "------------------------------------------------------------------" -ForegroundColor Yellow
    Write-Host "WICHTIG: Python wurde soeben installiert." -ForegroundColor Yellow
    Write-Host "Bitte schließen Sie dieses PowerShell-Fenster und starten Sie das" -ForegroundColor Yellow
    Write-Host "Setup-Skript in einem NEUEN PowerShell-Fenster erneut." -ForegroundColor Yellow
    Write-Host "Dies ist notwendig, damit der neue Python-Pfad erkannt wird." -ForegroundColor Yellow
    Write-Host "------------------------------------------------------------------" -ForegroundColor Yellow
    Read-Host "Drücken Sie Enter, um das Skript zu beenden..."
    exit
} else {
    Write-Host "    -> Found a real Python installation at $($PythonCmd.Source). OK."
}

# --- 3. Python Virtual Environment ---
Write-Host "--> Creating Python virtual environment in '.\.venv'..."
if (-not (Test-Path -Path ".\.venv")) {
    py -m venv .venv


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
  Invoke-WebRequest -Uri "https://languagetool.org/download/LanguageTool-$($LT_VERSION).zip" -OutFile "languagetool.zip"
  7z.exe x "languagetool.zip" -o"." | Out-Null
  Remove-Item "languagetool.zip"
}

# Download and extract Vosk Models
New-Item -ItemType Directory -Path "models" -ErrorAction SilentlyContinue | Out-Null
if (-not (Test-Path -Path "models/vosk-model-en-us-0.22")) {
  Write-Host "    -> Downloading English Vosk model..."
  Invoke-WebRequest -Uri "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip" -OutFile "models/en.zip"

  7z.exe x "models/en.zip" -o"models/" | Out-Null
  Remove-Item "models/en.zip"
}

if (-not (Test-Path -Path "models/vosk-model-de-0.21")) {
  Write-Host "    -> Downloading German Vosk model..."
  Invoke-WebRequest -Uri "https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip" -OutFile "models/de.zip"


  7z.exe x "models/de.zip" -o"models/" | Out-Null
  Remove-Item "models/de.zip"
}






# --- Create central config file ---
Write-Host "--> Creating central config file..."
# Pfad zum Konfigurationsverzeichnis erstellen ($env:USERPROFILE entspricht %USERPROFILE%)
$ConfigDir = Join-Path -Path $env:USERPROFILE -ChildPath ".config\sl5-stt"

# Überprüfen, ob das Verzeichnis existiert, und es bei Bedarf erstellen
if (-not (Test-Path -Path $ConfigDir)) {
    Write-Host "    -> Creating config directory at $ConfigDir"
    New-Item -ItemType Directory -Path $ConfigDir | Out-Null
}

# Inhalt für die config.toml-Datei definieren
# (Get-Location).Path entspricht dem aktuellen Verzeichnis
$ConfigContent = @"
[paths]
project_root = "$((Get-Location).Path)"
"@

# Pfad zur Konfigurationsdatei erstellen und den Inhalt schreiben
$ConfigFile = Join-Path -Path $ConfigDir -ChildPath "config.toml"
Set-Content -Path $ConfigFile -Value $ConfigContent



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

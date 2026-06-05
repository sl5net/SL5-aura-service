# update/update_for_windows_users.ps1
# Description: Downloads the latest version and updates the application
#              while preserving user settings. For non-developer use.

$ErrorActionPreference = 'Stop'

$installDir = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$tempDir = Join-Path $env:TEMP "sl5_update_temp"

$localShaPath = Join-Path $installDir "update\.last_commit_sha"



# Detect the active branch from either the current folder or the parent folder
$folder1 = Split-Path -Leaf $installDir
$folder2 = Split-Path -Leaf (Split-Path -Parent $installDir)

$branch = "master"
foreach ($f in @($folder1, $folder2)) {
    if ($f -match "^SL5-aura-service-(.+)$") {
        $rawBranch = $Matches[1]
        # Reconstruct branch slashes from GitHub zipball dash formatting
        if ($rawBranch -match "^(feature|experimental|bugfix|fix|hotfix)-(.*)$") {
            $branch = "$($Matches[1])/$($Matches[2])"
        } else {
            $branch = $rawBranch
        }
        break
    }
}

$repoUrl = "https://github.com/sl5net/SL5-aura-service/archive/refs/heads/$branch.zip"



# 2. Check latest commit SHA from GitHub API to prevent redundant downloads
$remoteSha = ""
try {
    $apiUrl = "https://api.github.com/repos/sl5net/SL5-aura-service/commits/$branch"
    $response = Invoke-RestMethod -Uri $apiUrl -UseBasicParsing
    $remoteSha = $response.sha
} catch {
    Write-Host "WARNING: Could not fetch updates info from GitHub. Proceeding with download..." -ForegroundColor Yellow
}


if ($remoteSha -and (Test-Path $localShaPath)) {
    $localSha = (Get-Content $localShaPath).Trim()
    if ($localSha -eq $remoteSha) {
        Write-Host "Aura is already up to date! ($branch branch is at commit $localSha)" -ForegroundColor Green
        if (-not ($env:CI -eq 'true')) {
            Read-Host -Prompt "Press Enter to exit (optional)"
        }
        exit 0
    }
}




Write-Host "--- SL5 Aura Updater ---" -ForegroundColor Cyan
Write-Host "This will download the latest version and replace all application files."
Write-Host "This will download the latest version and replace all application files."
Write-Host "This will download the latest version and replace all application files."
Write-Host "Your personal settings in 'config\settings_local.py' will be saved."
Write-Host "Your personal settings in 'config\settings_local.py' will be saved."
Write-Host "Your personal settings in 'config\settings_local.py' will be saved."
Write-Host "Your personal settings in 'config\settings_local.py' will be saved."
Write-Host "Your personal settings in 'config\settings_local.py' will be saved."
Write-Host "Your personal settings in 'config\settings_local.py' will be saved."

if (-not ($env:CI -eq 'true'))
{
    Write-Host "this will take some time ..."
#    Write-Host "Please close the main application if it is running."
#    Read-Host -Prompt "Press Enter to continue or CTRL+C to cancel"
}
try {
    # 1. Clean up previous temporary files if they exist
    if (Test-Path $tempDir) {
        Write-Host "INFO: Removing old temporary update folder..."
        Remove-Item -Path $tempDir -Recurse -Force
    }
    New-Item -Path $tempDir -ItemType Directory | Out-Null

    # 2. Backup local settings if they exist
    $localSettingsPath = Join-Path $installDir "config\settings_local.py"

    $backupPath = Join-Path $tempDir "settings_local.py.bak"
    if (Test-Path $localSettingsPath) {
        Write-Host "INFO: Backing up your local settings..." -ForegroundColor Green
        Copy-Item -Path $localSettingsPath -Destination $backupPath
    }

    # 3. Download the latest version
    $zipPath = Join-Path $tempDir "latest.zip"
    Write-Host "INFO: Downloading latest version from GitHub..."

    #  .NET WebClient download
    $webClient = New-Object System.Net.WebClient
    $webClient.DownloadFile($repoUrl, $zipPath)

    # 4. Extract the archive
    Write-Host "INFO: Extracting update..."
    Expand-Archive -Path $zipPath -DestinationPath $tempDir -Force
    $extractedFolder = Get-ChildItem -Path $tempDir -Directory | Select-Object -First 1
    if (-not $extractedFolder) { throw "Could not find extracted folder inside temp directory." }

    # 5. Restore local settings into the new version



    if (Test-Path $backupPath) {
        Write-Host "INFO: Restoring your local settings into the new version..." -ForegroundColor Green
        Copy-Item -Path $backupPath -Destination (Join-Path $extractedFolder.FullName "config\")

    }
    # 6. Create a final batch script to perform the file replacement and update dependencies
#    $installerName = "setup\windows11_setup.bat"
    $installerName = "setup\windows11_setup_with_ahk_copyq_fzf_glogg.bat"

    $batchScript = @'
@echo off
echo Finalizing update, please wait...
timeout /t 3 /nobreak > nul

:: 1. Dateien verschieben
robocopy "{0}" "{1}" /E /MOVE /NFL /NDL /NJH /NJS > nul

:: 2. In Zielordner wechseln
cd /d "{1}"

:: 3. Abhängigkeiten aktualisieren
echo.
echo ---------------------------------------------------
echo Updating dependencies (pip install)...
echo ---------------------------------------------------
:: 3. Installer aufrufen (Dort passiert das pip upgrade und requirements install)
if exist "{2}" (
    echo Starting installer script...
    call "{2}"
) else (

    color 4f
    echo.
    echo ===================================================
    echo FATAL ERROR: SETUP SCRIPT NOT FOUND!
    echo Expected: {2} in %CD%
    echo ===================================================

    echo WARNING: "{2}" not found. Trying manual pip upgrade...
    :: Fallback, falls keine install.bat da ist:
    if exist ".venv\Scripts\activate.bat" (
        call .venv\Scripts\activate.bat
        python.exe -m pip install --upgrade pip
        pip install -r requirements.txt
        color 07
    ) else (
        echo The update cannot proceed. Please verify the filename.
        pause
        exit /b 1
    )
)

echo.
echo Update complete! You can now restart the application.
timeout /t 10 > nul
del "%~f0"
'@ -f $extractedFolder.FullName, $installDir, $installerName

    $batchPath = Join-Path $installDir "_finalize_update.bat"
    Set-Content -Path $batchPath -Value $batchScript
    # update/update_for_windows_users.ps1:110

    # Save the new commit SHA locally for the next run
    if ($remoteSha) {
        Set-Content -Path $localShaPath -Value $remoteSha
    }

    # 7. Launch the batch script and exit this PowerShell script
    Write-Host "INFO: Handing over to final updater script. This window will close." -ForegroundColor Yellow
    Start-Process cmd.exe -ArgumentList "/C `"$batchPath`""

} catch {
    Write-Host "FATAL: An error occurred during the update." -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Read-Host -Prompt "Press Enter to exit."
}

# file: update_for_windows_users.ps1                                       
# Description: Downloads the latest version and updates the application
#              while preserving user settings. For non-developer use.

$ErrorActionPreference = 'Stop'
$repoUrl = "https://github.com/sl5net/Vosk-System-Listener/archive/refs/heads/master.zip"
$installDir = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$tempDir = Join-Path $env:TEMP "sl5_update_temp"

Write-Host "--- SL5 Dictation Updater ---" -ForegroundColor Cyan
Write-Host "This will download the latest version and replace all application files."
Write-Host "Your personal settings in 'config\settings_local.py' will be saved."
Write-Host "Please close the main application if it is running."
Read-Host -Prompt "Press Enter to continue or CTRL+C to cancel"

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
    Invoke-WebRequest -Uri $repoUrl -OutFile $zipPath

    # 4. Extract the archive
    Write-Host "INFO: Extracting update..."
    Expand-Archive -Path $zipPath -DestinationPath $tempDir -Force
    $extractedFolder = Get-ChildItem -Path $tempDir -Directory | Where-Object { $_.Name -like '*-master' } | Select-Object -First 1
    if (-not $extractedFolder) { throw "Could not find extracted '*-master' folder." }

    # 5. Restore local settings into the new version



    if (Test-Path $backupPath) {
        Write-Host "INFO: Restoring your local settings into the new version..." -ForegroundColor Green
        Copy-Item -Path $backupPath -Destination (Join-Path $extractedFolder.FullName "config\")
    }

    # 6. Create a final batch script to perform the file replacement
    $batchScript = @'
@echo off
echo Finalizing update, please wait...
timeout /t 3 /nobreak > nul
robocopy "{0}" "{1}" /E /MOVE /NFL /NDL /NJH /NJS > nul
echo.
echo Update complete! You can now restart the application.
timeout /t 5 > nul
del "%~f0"
'@ -f $extractedFolder.FullName, $installDir

    $batchPath = Join-Path $installDir "_finalize_update.bat"
    Set-Content -Path $batchPath -Value $batchScript

    # 7. Launch the batch script and exit this PowerShell script
    Write-Host "INFO: Handing over to final updater script. This window will close." -ForegroundColor Yellow
    Start-Process cmd.exe -ArgumentList "/C `"$batchPath`""

} catch {
    Write-Host "FATAL: An error occurred during the update." -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Read-Host -Prompt "Press Enter to exit."
}

# install_ahk_copyq.ps1
# script_name: setup/install_ahk_copyq.ps1

$downloadDir = "$env:USERPROFILE\Downloads"
# AHK specific variables
$ahkInstallerName = "ahk-install.exe"
$ahkLocalPath = Join-Path -Path $downloadDir -ChildPath $ahkInstallerName
$ahkInstalledPath = "$env:ProgramFiles\AutoHotkey\v2\AutoHotkey.exe"

Write-Host "Starting setup for client tools..." -ForegroundColor Cyan

# --- TASK 1: AutoHotkey V2 ---
Write-Host "`n[1/2] Checking AutoHotkey V2..." -ForegroundColor Yellow

if (Test-Path -Path $ahkInstalledPath) {
    Write-Host "AutoHotkey V2 is already installed. Skipping." -ForegroundColor Green
} else {
    # Not installed, check local download
    if (Test-Path -Path $ahkLocalPath) {
        Write-Host "Found installer in Downloads folder ($ahkInstallerName). Installing from local file..." -ForegroundColor Cyan
        try {
            # Start local installer silent
            $process = Start-Process -FilePath $ahkLocalPath -ArgumentList "/silent" -Wait -PassThru
            if ($process.ExitCode -eq 0) {
                Write-Host "AutoHotkey installed from local file successfully." -ForegroundColor Green
            } else {
                Write-Warning "Local installer exited with code $($process.ExitCode). Trying Winget as fallback..."
                winget install --id "AutoHotkey.AutoHotkey" -e --source winget --accept-package-agreements --accept-source-agreements
            }
        } catch {
            Write-Error "Failed to run local installer. $_"
        }
    } else {
        # Not installed, no local file -> Use Winget
        Write-Host "No local installer found. Installing via Winget..." -ForegroundColor Cyan
        winget install --id "AutoHotkey.AutoHotkey" -e --source winget --accept-package-agreements --accept-source-agreements
    }
}

# --- TASK 2: CopyQ ---
Write-Host "`n[2/2] Checking CopyQ..." -ForegroundColor Yellow

# We rely on Winget's internal check here, as CopyQ installer filenames vary by version.
# Winget will detect if it's already installed and skip/update accordingly.
winget install --id "hluk.CopyQ" -e --source winget --accept-package-agreements --accept-source-agreements

if ($LASTEXITCODE -eq 0) {
    Write-Host "CopyQ check/install completed successfully." -ForegroundColor Green
} else {
    Write-Warning "CopyQ setup finished with exit code $LASTEXITCODE. It might be already installed or cancelled."
}

winget install --id "hluk.CopyQ" -e --source winget --accept-package-agreements --accept-source-agreements





# Write-Host "CopyQ check/install completed successfully." -ForegroundColor Green

# --- NEU: Konfiguration des Hotkeys ---
Write-Host "    -> Configuring Global Hotkey (Ctrl+Q)..."

# 1. Pfad suchen (Da PATH evtl. noch nicht aktuell ist)
$copyqExe = "copyq" # Fallback
if (Test-Path "C:\Program Files\CopyQ\copyq.exe") {
   $copyqExe = "C:\Program Files\CopyQ\copyq.exe"
} elseif (Test-Path "C:\Program Files (x86)\CopyQ\copyq.exe") {
   $copyqExe = "C:\Program Files (x86)\CopyQ\copyq.exe"
}

# Mit Call-Operator (Achtung: Pfad muss quoted werden)
& "$copyqExe" config global_shortcuts/show "Ctrl+1"
if ($LASTEXITCODE -eq 0) { "OK" } else { "Fehler: $LASTEXITCODE" }

# setup/install_ahk_copyq.ps1:76
Write-Host "Running map_tagger.py..."
#& ".\.venv\Scripts\python.exe" "tools\map_tagger.py" "--yes"

Start-Process ".\.venv\Scripts\python.exe" -ArgumentList "tools\map_tagger.py","--yes" -NoNewWindow -Wait -PassThru
$LASTEXITCODE


# map_tagger.py --yes

Write-Host "Running map_tagger.py..."
& ".\.venv\Scripts\python.exe" "tools\export_to_copyq.py"




# --- Notepad++ ---
# if exist "C:\Program Files\Notepad++\notepad++.exe" (
if (Test-Path "C:\Program Files\Notepad++\notepad++.exe")
{
    echo [OK] Notepad++ ist schon da.
} else
{
    echo [..] Installiere Notepad++...
    winget install -e --id Notepad++.Notepad++ --silent --accept-source-agreements --accept-package-agreements
}

# --- Double Commander ---
if (Test-Path "C:\Program Files\Double Commander\doublecmd.exe")
{
    echo [OK] Double Commander ist schon da.
} else
{
    echo [..] Installiere Double Commander...
    winget install -e --id DoubleCommander.DoubleCommander --silent --accept-source-agreements --accept-package-agreements
}





Write-Host "`nClient tools setup sequence finished." -ForegroundColor Cyan


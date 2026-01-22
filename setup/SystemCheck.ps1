# SystemCheck.ps1
Write-Host "--- STARTE SYSTEM-DIAGNOSE ---" -ForegroundColor Cyan

# 1. PFAD DEFINITIONEN
# $tempDir = "$env:TEMP\VoskTTS_Check"
$tempDir = "C:\tmp\sl5_aura"
$testFile = "$tempDir\write_test.txt"
$pythonPath = ".\.venv\Scripts\python.exe"

# 2. SCHREIBTEST (Simuliert Vosk Service)
Write-Host "[1/3] Prüfe Schreibrechte für Python..." -NoNewline
if (-not (Test-Path $tempDir)) { New-Item -ItemType Directory -Path $tempDir -Force | Out-Null }

try {
    # Versuch, eine Datei zu schreiben
    "Test-Inhalt" | Out-File -FilePath $testFile -Encoding utf8
    if (Test-Path $testFile) {
        Write-Host " OK (Ordner und Datei erzeugbar)" -ForegroundColor Green
    } else {
        throw "Datei konnte nicht erstellt werden."
    }
} catch {
    Write-Host " FEHLER" -ForegroundColor Red
    Write-Host "   Ursache: Windows Defender oder fehlende Rechte blockieren das Schreiben in $tempDir" -ForegroundColor Yellow
    Write-Host "   Lösung: Fügen Sie den Ordner zu den Ausnahmen im Defender hinzu."
    exit
}

# 3. AHK ADMIN CHECK
Write-Host "[2/3] Prüfe AHK Berechtigungen..."
# Wir prüfen, ob der aktuelle Prozess Admin-Rechte hat.
# AHK erbt diese Rechte, wenn es von hier gestartet wird.
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if ($isAdmin) {
    Write-Host " OK (Läuft als Admin)" -ForegroundColor Green
} else {
Write-Host " WARNUNG: Skript läuft NICHT als Admin." -ForegroundColor Yellow
    Write-Host "   Das bedeutet: AHK darf NICHT in Programme schreiben, die als Administrator gestartet wurden." -ForegroundColor Yellow
    Write-Host "   Lösung: Starten Sie ALLES (Vosk & AHK) als Administrator." -ForegroundColor Yellow

}

# 4. TYPING TEST (Visueller Test)
Write-Host "[3/3] Simuliere Tippen..."
Write-Host "   Ein Notepad Fenster öffnet sich gleich. Wenn dort Text erscheint, funktioniert alles." -ForegroundColor Cyan
Start-Sleep -Seconds 2

# Notepad öffnen
$notepad = Start-Process notepad.exe -PassThru
Start-Sleep -Seconds 1

# SendKeys via PowerShell nutzen (ähnlich wie AHK, um zu testen ob Windows Input blockt)
try {
    [void] [System.Reflection.Assembly]::LoadWithPartialName("'System.Windows.Forms")
    [System.Windows.Forms.SendKeys]::SendWait("Test OK")
#    Write-Host "   Wurde Text in Notepad geschrieben? (Ja/Nein)"
} catch {
    Write-Host "   FEHLER beim Senden von Tastenanschlägen." -ForegroundColor Red
}

Write-Host "--- DIAGNOSE ENDE ---"
Start-Sleep -Seconds 2

# Fenster schließen mit Alt+F4
#[System.Windows.Forms.SendKeys]::SendWait("%{F4}")
# Kill all notepad without save !!
Get-Process notepad -ErrorAction SilentlyContinue | Stop-Process -Force

#Pause

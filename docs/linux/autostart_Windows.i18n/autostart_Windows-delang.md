# Windows-Autostart

# start_aura.bat

Bitte überprüfen Sie diese Datei „start_aura.bat“ im Projektordner von SL5net Aura.

**Option A – Startordner (einfachstes, sichtbares Konsolenfenster)**

1. Erstellen Sie eine Batchdatei, z.B. `C:\Benutzer\<IhrName>\Scripts\aura_engine.bat`:

```batch
@echo off
wsl bash -c "if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then exit 0; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh >> /home/linus/SL5-aura-service/aura_engine.log 2>&1; fi"
```

2. Drücken Sie „Win + R“, geben Sie „shell:startup“ ein und drücken Sie die Eingabetaste. Dies öffnet:
`C:\Benutzer\<IhrName>\AppData\Roaming\Microsoft\Windows\Startmenü\Programme\Startup`
3. Klicken Sie mit der rechten Maustaste in diesen Ordner → **Neu → Verknüpfung** → zeigen Sie auf „aura_engine.bat“. Es läuft jetzt bei jedem Login.

**Option B – Taskplaner (empfohlen: ausgeblendet, kein Fenster blinken)**

Führen Sie dies einmal in PowerShell aus:

```powershell
$action = New-ScheduledTaskAction -Execute "wsl.exe" -Argument "bash -c `"if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then exit 0; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh >> /home/linus/SL5-aura-service/aura_engine.log 2>&1; fi`""
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -Hidden -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "AuraEngine" -Action $action -Trigger $trigger -Settings $settings -Description "Starts the SL5 Aura Service at login"
```

Dadurch wird eine Aufgabe „AuraEngine“ erstellt, die bei jeder Anmeldung ausgelöst wird, vollständig im Hintergrund läuft und in dasselbe „aura_engine.log“ schreibt, das in den Linux-/Mac-Versionen verwendet wird.

**Testen ohne sich abzumelden:**

```powershell
Start-ScheduledTask -TaskName "AuraEngine"
Get-Content "\\wsl$\Ubuntu\home\linus\SL5-aura-service\aura_engine.log" -Wait
```

Passen Sie „Ubuntu“ an Ihren tatsächlichen Distributionsnamen an – erkundigen Sie sich bei:

```powershell
wsl -l -v
```

**Überprüfen Sie, ob es registriert ist:**

```powershell
Get-ScheduledTask -TaskName "AuraEngine"
```

**Deaktivieren/Entfernen:**

```powershell
Unregister-ScheduledTask -TaskName "AuraEngine" -Confirm:$false
```

Führen Sie dieses Projekt tatsächlich über WSL auf diesem Windows-Computer aus oder ist eine native Windows/PowerShell-Neuschreibung von „restart_venv_and_run-server.sh“ erforderlich (keine WSL beteiligt)?
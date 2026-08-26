# Windows autostart

# start_aura.bat

please check this file `start_aura.bat` in the project folder of SL5net Aura.

**Option A — Startup folder (simplest, visible console window)**

1. Create a batch file, e.g. `C:\Users\<YourName>\Scripts\aura_engine.bat`:

```batch
@echo off
wsl bash -c "if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then exit 0; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh >> /home/linus/SL5-aura-service/aura_engine.log 2>&1; fi"
```

2. Press `Win + R`, type `shell:startup`, hit Enter. This opens:
   `C:\Users\<YourName>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`
3. Right-click inside that folder → **New → Shortcut** → point it to `aura_engine.bat`. It now runs at every login.

**Option B — Task Scheduler (recommended: hidden, no window flash)**

Run this once in PowerShell:

```powershell
$action = New-ScheduledTaskAction -Execute "wsl.exe" -Argument "bash -c `"if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then exit 0; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh >> /home/linus/SL5-aura-service/aura_engine.log 2>&1; fi`""
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -Hidden -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "AuraEngine" -Action $action -Trigger $trigger -Settings $settings -Description "Starts the SL5 Aura Service at login"
```

This creates a task `AuraEngine` that fires at every logon, runs fully in the background, and writes to the same `aura_engine.log` used in the Linux/Mac versions.

**Test without logging out:**

```powershell
Start-ScheduledTask -TaskName "AuraEngine"
Get-Content "\\wsl$\Ubuntu\home\linus\SL5-aura-service\aura_engine.log" -Wait
```

Adjust `Ubuntu` to your actual distro name — check with:

```powershell
wsl -l -v
```

**Check it's registered:**

```powershell
Get-ScheduledTask -TaskName "AuraEngine"
```

**Disable/remove:**

```powershell
Unregister-ScheduledTask -TaskName "AuraEngine" -Confirm:$false
```

Do you actually run this project through WSL on that Windows machine, or does it need a native Windows/PowerShell rewrite of `restart_venv_and_run-server.sh` (no WSL involved)?

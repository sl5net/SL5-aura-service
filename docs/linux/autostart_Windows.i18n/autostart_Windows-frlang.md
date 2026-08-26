# Démarrage automatique de Windows

# start_aura.bat

veuillez vérifier ce fichier `start_aura.bat` dans le dossier du projet de SL5net Aura.

**Option A — Dossier de démarrage (fenêtre de console la plus simple et visible)**

1. Créez un fichier batch, par ex. `C:\Users\<VotreNom>\Scripts\aura_engine.bat` :

```batch
@echo off
wsl bash -c "if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then exit 0; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh >> /home/linus/SL5-aura-service/aura_engine.log 2>&1; fi"
```

2. Appuyez sur « Win + R », tapez « shell:startup », appuyez sur Entrée. Cela ouvre :
`C:\Users\<VotreNom>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`
3. Faites un clic droit dans ce dossier → **Nouveau → Raccourci** → pointez-le vers `aura_engine.bat`. Il s'exécute désormais à chaque connexion.

**Option B — Planificateur de tâches (recommandé : masqué, pas de flash de fenêtre)**

Exécutez ceci une fois dans PowerShell :

```powershell
$action = New-ScheduledTaskAction -Execute "wsl.exe" -Argument "bash -c `"if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then exit 0; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh >> /home/linus/SL5-aura-service/aura_engine.log 2>&1; fi`""
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -Hidden -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "AuraEngine" -Action $action -Trigger $trigger -Settings $settings -Description "Starts the SL5 Aura Service at login"
```



**Testez sans vous déconnecter :**

```powershell
Start-ScheduledTask -TaskName "AuraEngine"
Get-Content "\\wsl$\Ubuntu\home\linus\SL5-aura-service\aura_engine.log" -Wait
```

Ajustez « Ubuntu » au nom de votre distribution actuelle — vérifiez auprès de :

```powershell
wsl -l -v
```

**Vérifiez qu'il est enregistré :**

```powershell
Get-ScheduledTask -TaskName "AuraEngine"
```

**Désactiver/supprimer :**

```powershell
Unregister-ScheduledTask -TaskName "AuraEngine" -Confirm:$false
```

Exécutez-vous réellement ce projet via WSL sur cette machine Windows, ou nécessite-t-il une réécriture native Windows/PowerShell de « restart_venv_and_run-server.sh » (aucun WSL impliqué) ?
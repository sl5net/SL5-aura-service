# Inicio automático de Windows

#start_aura.bat

verifique este archivo `start_aura.bat` en la carpeta del proyecto de SL5net Aura.

**Opción A: Carpeta de inicio (ventana de consola visible más simple)**

1. Cree un archivo por lotes, p. `C:\Users\<SuNombre>\Scripts\aura_engine.bat`:

```batch
@echo off
wsl bash -c "if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then exit 0; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh >> /home/linus/SL5-aura-service/aura_engine.log 2>&1; fi"
```

2. Presione `Win + R`, escriba `shell:startup`, presione Enter. Esto abre:
`C:\Users\<SuNombre>\AppData\Roaming\Microsoft\Windows\Menú Inicio\Programas\Inicio`
3. Haga clic derecho dentro de esa carpeta → **Nuevo → Acceso directo** → apúntelo a `aura_engine.bat`. Ahora se ejecuta en cada inicio de sesión.

**Opción B: Programador de tareas (recomendado: oculto, sin ventana parpadeante)**

Ejecute esto una vez en PowerShell:

```powershell
$action = New-ScheduledTaskAction -Execute "wsl.exe" -Argument "bash -c `"if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then exit 0; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh >> /home/linus/SL5-aura-service/aura_engine.log 2>&1; fi`""
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -Hidden -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "AuraEngine" -Action $action -Trigger $trigger -Settings $settings -Description "Starts the SL5 Aura Service at login"
```

Esto crea una tarea `AuraEngine` que se activa en cada inicio de sesión, se ejecuta completamente en segundo plano y escribe en el mismo `aura_engine.log` usado en las versiones de Linux/Mac.

**Prueba sin cerrar sesión:**

```powershell
Start-ScheduledTask -TaskName "AuraEngine"
Get-Content "\\wsl$\Ubuntu\home\linus\SL5-aura-service\aura_engine.log" -Wait
```

Ajuste `Ubuntu` al nombre de su distribución real; consulte con:

```powershell
wsl -l -v
```

**Comprueba que esté registrado:**

```powershell
Get-ScheduledTask -TaskName "AuraEngine"
```

**Desactivar/eliminar:**

```powershell
Unregister-ScheduledTask -TaskName "AuraEngine" -Confirm:$false
```

¿Realmente ejecuta este proyecto a través de WSL en esa máquina con Windows, o necesita una reescritura nativa de Windows/PowerShell de `restart_venv_and_run-server.sh` (sin WSL involucrado)?
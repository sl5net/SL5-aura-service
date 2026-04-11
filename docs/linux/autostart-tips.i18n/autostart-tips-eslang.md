Erstelle Autostart Eintrag über dein grafische Benutzeroberfläche für:

reiniciar_venv_and_run-server.sh.desktop   

aura_engine.log.desktop  

Aquí en el orden: `~/.config/autostart/`

öffne en el editor

reiniciar_venv_and_run-server.sh.desktop   
aura_engine.log.desktop  

Den Befehl manuell anpassen

**Anstatt:**
`Exec=/pfad/zu/deinem/script.sh`

**Beispiele Schreibe:**

Exec=xfce4-terminal -e 'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"'

`Exec=xfce4-terminal -e 'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"'`

Exec=konsole -e 'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"'   

Ejecutivo=Exec=kate /home/me/projects/py/STT/log/aura_engine.log

Ejecutivo=kate /home/me/projects/py/STT/config/filters/settings_local_log_filter.py





### ¿Por qué la instalación gráfica no funciona?

En Plasma 6 hay un problema grave con el cambio de "Terminales predeterminados" en la fase de inicio de los sistemas. También tenemos `console` (el terminal estándar de KDE) directamente en el `Exec`-Zeile schreiben, para activar y desactivar automáticamente el inicio.


26.3.'26 08:16 Jue
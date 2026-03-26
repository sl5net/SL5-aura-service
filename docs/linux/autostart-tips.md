
Erstelle Autostart Eintrag über dein grafische Benutzeroberfläche für:

restart_venv_and_run-server.sh.desktop                           ✔ 
aura_engine.log.desktop  

Gehe in den Ordner: `~/.config/autostart/` 

öffne in Editor

restart_venv_and_run-server.sh.desktop                           ✔ 
aura_engine.log.desktop  

Den Befehl manuell anpassen

**Anstatt:**
`Exec=/pfad/zu/deinem/script.sh`

**Schreibe:**

xfce4-terminal -e 'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"'

Exec=kate /home/me/projects/py/STT/log/aura_engine.log

Exec=kate /home/me/projects/py/STT/config/filters/settings_local_log_filter.py





### Warum hat die grafische Einstellung nicht funktioniert?

In Plasma 6 gibt es gelegentlich Probleme mit der Zuweisung des "Default Terminals" in der Startphase des Systems. Indem wir `konsole` (das Standard-Terminal von KDE) direkt in die `Exec`-Zeile schreiben, umgehen wir die automatische Erkennung und erzwingen den Start.


26.3.'26 08:16 Thu

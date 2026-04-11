Erstelle Autostart Eintrag über dein grafische Benutzeroberfläche für:

restart_venv_and_run-server.sh.desktop   

aura_engine.log.desktop  

Wpisz polecenie: `~/.config/autostart/`

öffne w edytorze

restart_venv_and_run-server.sh.desktop   
aura_engine.log.desktop  

Den Befehl Manuell Anpassen

**Anstatt:**
`Exec=/pfad/zu/deinem/script.sh`

**Beispiele Schreibe:**

Exec=xfce4-terminal -e 'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"'

`Exec=xfce4-terminal -e 'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"''

Exec=konsole -e 'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"' XSPACEbreakX

Exec=Exec=kate /home/me/projects/py/STT/log/aura_engine.log

Exec=kate /home/me/projects/py/STT/config/filters/settings_local_log_filter.py





### Warum hat die grafische Einstellung nicht funktioniert?

W Plazmie 6 gibt es gelegentlich Probleme mit der Zuweisung des „Default Terminals” w Startphase des Systems. Użyj `konsole` (das Standard-Terminal von KDE) bezpośrednio w `Exec`-Zeile schreiben, umgehen wir die automatische Erkennung und erzwingen den Start.


26.3.'26 08:16 Czw
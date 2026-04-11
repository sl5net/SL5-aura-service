Erstelle Autostart Eintrag über dein grafische Benutzeroberfläche für:

restart_venv_and_run-server.sh.desktop   

aura_engine.log.desktop  

Ordner의 내용: `~/.config/autostart/`

편집기에서 öffne

restart_venv_and_run-server.sh.desktop   
aura_engine.log.desktop  

덴 베펠 마누엘 안파센

**안슈타트:**
`Exec=/pfad/zu/deinem/script.sh`

**바이스필레 슈라이베:**

Exec=xfce4-terminal -e 'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"'

`Exec=xfce4-terminal -e 'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"'`

Exec=konsole -e 'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"'   

Exec=Exec=케이트 /home/me/projects/py/STT/log/aura_engine.log

Exec=케이트 /home/me/projects/py/STT/config/filters/settings_local_log_filter.py





### Warum hat die grafische Einstellung nicht funktioniert?

Plasma 6 gibt es gelegentlich Probleme mit der Zuweisung des "Default Terminals" in der Startphase des Systems. Indem wir `konsole` (das Standard-Terminal von KDE) direct in die `Exec`-Zeile schreiben, umgehen wir die automatische Erkennung und erzwingen den Start.


26.3.'26 08:16 목
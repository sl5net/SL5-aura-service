Erstelle Autostart Eintrag über dein grafische Benutzeroberfläche para:

restart_venv_and_run-server.sh.desktop   

aura_engine.log.desktop  

Gehe in den Ordner: `~/.config/autostart/`

desligado no Editor

restart_venv_and_run-server.sh.desktop   
aura_engine.log.desktop  

Den Befehl Manuel Anpassen

**Anstatt:**
`Exec=/pfad/zu/deinem/script.sh`

**Beispiele Schreibe:**

Exec = xfce4-terminal -e 'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"'

`Exec = xfce4-terminal -e 'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"'`

Exec = konsole -e 'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"'   

Exec=Exec=kate /home/me/projects/py/STT/log/aura_engine.log

Exec=kate /home/me/projects/py/STT/config/filters/settings_local_log_filter.py





### Warum hat die grafische Einstellung nicht funktioniert?

No Plasma 6, o problema é resolvido com o ajuste dos "terminais padrão" na fase inicial do sistema. Indem wir `konsole` (o Terminal Padrão do KDE) diretamente na tela `Exec`-Zeile, umgehen wir the automatische Erkennung und start.


26.3.'26 08:16 Qui
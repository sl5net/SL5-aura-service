Erstelle Autostart Eintrag über dein grafische Benutzeroberfläche für：

restart_venv_and_run-server.sh.desktop   

aura_engine.log.desktop  

Gehe 在 den Ordner: `~/.config/autostart/`

编辑器中的 öffne

restart_venv_and_run-server.sh.desktop   
aura_engine.log.desktop  

登·贝菲尔·曼努埃尔·安帕森

**安斯塔特：**
`Exec=/pfad/zu/deinem/script.sh`

**贝斯皮埃莱·施赖贝：**

Exec=xfce4-terminal -e 'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"'

`Exec=xfce4-terminal -e 'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"'`

Exec=konsole -e 'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"'   

Exec=Exec=kate /home/me/projects/py/STT/log/aura_engine.log

Exec=kate /home/me/projects/py/STT/config/filters/settings_local_log_filter.py





### Warum hat die grafische Einstellung nicht funktioniert？

在 Plasma 6 中，系统启动阶段中出现了“默认终端”的严重问题。 Indem wir `konsole`（das Standard-Terminal von KDE）直接在`Exec`-Zeile schreiben中，umgehen wir die automatische Erkennung und erzwingen den Start。


26.3.'26 08:16 星期四
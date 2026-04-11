Erstelle Autostart Eintrag über dein grafische Benutzeroberfläche für:

restart_venv_and_run-server.sh.desktop   

aura_engine.log.desktop  

オードナーの洞窟: `~/.config/autostart/`

エディターのオフネ

restart_venv_and_run-server.sh.desktop   
aura_engine.log.desktop  

デン・ベフェール マヌエル・アンパッセン

**アンシュタット:**
`Exec=/pfad/zu/deinem/script.sh`

**シュライベの例:**

Exec=xfce4-terminal -e 'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"'

`Exec=xfce4-terminal -e 'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"'`

Exec=konsole -e 'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"'   

Exec=Exec=kate /home/me/projects/py/STT/log/aura_engine.log

Exec=kate /home/me/projects/py/STT/config/filters/settings_local_log_filter.py





### Warum の帽子は、グラフィックを楽しむのに最適ですか?

Plasma 6 では、システムの開始段階で「デフォルトの端末」に関する問題が発生します。 Indem wir `konsole` (das Standard- Terminal von KDE) direkt in die `Exec`-Zeile schreiben, umgehen wir die automatische Erkennung und erzwingen den Start。


'26.3.26 08:16 木
Erstelle Autostart Eintrag über dein grafische Benutzeroberfläche für：

restart_venv_and_run-server.sh.desktop  ✔
aura_engine.log.desktop  

Gehe 在 den Ordner: `~/.config/autostart/`

编辑器中的 öffne

restart_venv_and_run-server.sh.desktop  ✔
aura_engine.log.desktop  

登·贝菲尔·曼努埃尔·安帕森

**安斯塔特：**
`Exec=/pfad/zu/deinem/script.sh`

**施赖贝：**
`Exec=konsole --noclose -e /pfad/zu/deinem/script.sh`

贝兹。

`Exec=kate /pfad/zu/deinem/script.sh`


### Warum hat die grafische Einstellung nicht funktioniert？

在 Plasma 6 中，系统启动阶段中出现了“默认终端”的严重问题。 Indem wir `konsole`（das Standard-Terminal von KDE）直接在`Exec`-Zeile schreiben中，umgehen wir die automatische Erkennung und erzwingen den Start。


26.3.'26 08:16 星期四
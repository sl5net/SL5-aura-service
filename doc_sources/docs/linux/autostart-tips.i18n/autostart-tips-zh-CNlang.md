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

[桌面入口]
评论[zh_CN]=
评论=
Exec=konsole -e bash -c 'if [ -f /tmp/sl5_aura/sl5net_aura_project_root ];然后回显“光环已经运行。”；否则触摸/tmp/sl5_aura/sl5net_aura_project_root； /home/......../projects/py/STT/scripts/restart_venv_and_run-server.sh;菲；执行 zsh'
通用名称[en_GB]=
通用名称=
图标=文本-x-log
哑剧类型=
名称[en_GB]=aura_engine
名称=aura_engine
路径=
启动通知=true
终端=假
类型=应用
X-KDE-AutostartScript=true
X-KDE-SubstituteUID=false
X-KDE-用户名=


### Warum hat die grafische Einstellung nicht funktioniert？

在 Plasma 6 中，系统启动阶段中出现了“默认终端”的严重问题。 Indem wir `konsole`（das Standard-Terminal von KDE）直接在`Exec`-Zeile schreiben中，umgehen wir die automatische Erkennung und erzwingen den Start。


26.3.'26 08:16 星期四
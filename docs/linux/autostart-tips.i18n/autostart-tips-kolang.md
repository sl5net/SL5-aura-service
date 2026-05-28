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

[데스크톱 항목]
댓글[en_GB]=
댓글=
Exec=konsole -e bash -c 'if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; 그런 다음 echo "aura가 이미 실행 중입니다."; 그렇지 않으면 /tmp/sl5_aura/sl5net_aura_project_root를 터치하세요. /home/......../projects/py/STT/scripts/restart_venv_and_run-server.sh; fi; exec zsh'
일반 이름[en_GB]=
일반 이름=
아이콘=텍스트-x-로그
마임 유형=
이름[en_GB]=aura_engine
이름=aura_engine
경로=
시작 알림=true
터미널=거짓
유형=애플리케이션
X-KDE-AutostartScript=true
X-KDE-대체UID=false
X-KDE-사용자 이름=


### Warum hat die grafische Einstellung nicht funktioniert?

In Plasma 6 gibt es gelegentlich Probleme mit der Zuweisung des "Default Terminals" in der Startphase des Systems. Indem wir `konsole` (das Standard-Terminal von KDE) direct in die `Exec`-Zeile schreiben, umgehen wir die automatische Erkennung und erzwingen den Start.


26.3.'26 08:16 목
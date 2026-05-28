Erstelle Autostart Eintrag über dein grafische Benutzeroberfläche für:

restart_venv_and_run-server.sh.desktop   

aura_engine.log.desktop  

オードナーでの話: `~/.config/autostart/`

エディターのオフネ

restart_venv_and_run-server.sh.desktop   
aura_engine.log.desktop  

デン・ベフェール マヌエル・アンパッセン

**アンシュタット:**
`Exec=/pfad/zu/deinem/script.sh`

**シュライベの例:**

［デスクトップ入力］
コメント[en_GB]=
コメント=
Exec=konsole -e bash -c 'if [ -f /tmp/sl5_aura/sl5net_aura_project_root ];次に、「オーラはすでに実行されています。」をエコーします。それ以外の場合は /tmp/sl5_aura/sl5net_aura_project_root をタッチします。 /home/....../projects/py/STT/scripts/restart_venv_and_run-server.sh;フィ; zshを実行してください
一般名[en_GB]=
一般名=
アイコン=テキスト-x-ログ
MimeType=
名前[en_GB]=aura_engine
名前=aura_engine
パス=
StartupNotify=true
ターミナル=false
タイプ=アプリケーション
X-KDE-AutostartScript=true
X-KDE-SubstituteUID=false
X-KDE-ユーザー名=


### Warum の帽子は、グラフィックを楽しむのに最適ですか?

Plasma 6 では、システムの開始段階で「デフォルトの端末」に関する問題が発生します。 Indem wir `konsole` (das Standard- Terminal von KDE) direkt in die `Exec`-Zeile schreiben, umgehen wir die automatische Erkennung und erzwingen den Start。


'26.3.26 08:16 木
# docs/Developer_Guide/Trino_Integration.md
歴史 |少ない  ✔
10093 docker rm trino 2>/dev/null; docker run -d --name trino -p 8083:8080 trinodb/trino
10094 docker ログ trino -f | grep -m1 "サーバーが開始されました"
10095 ソース .venv/bin/activate

10098 ピップ ショー トリノ
10099 python3 -c "\nimport trino\nconn = trino.dbapi.connect(host='localhost', port=8083, user='aura')\ncur = conn.cursor()\ncur.execute('SELECT 1')\nprint('Trino connection:', cur.fetchone())\n"




アクトゥエル:
config.json ──────► Ebene 2 (ターミナル)
└──► Ebene 3 (ストリームリット)
└──► Ebene 3.5 (Web)
↑
ALLE lesen ディーゼル構成

イディー：

エベネ２（ターミナル）─┐
Ebene 3 (Streamlit) ─┼─► Trino ──► user_configs
Ebene 3.5 (Web) ─┘ §─ ターミナル: EN 翻訳 = true
§── web: DE、kein 翻訳
└── ユーザーごと: eigene オーバーライド




構成/
§── settings.py ← Haupt-Config
§── settings_local.py ← lokale オーバーライド
§── settings_local.py_Example.txt
§── settings_local.py_Example_user_...txt
└── フィルター/.backlock/first_run/
└── settings_local_log_filter.py ← einziger "コンテキスト分割"

+ 多様な JSON-Dateien と verschiedenen Orten
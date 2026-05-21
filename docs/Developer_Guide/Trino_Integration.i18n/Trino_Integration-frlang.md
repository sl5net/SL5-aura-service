# docs/Developer_Guide/Trino_Integration.md
histoire | moins  ✔
10093 docker rm trino 2>/dev/null ; docker run -d --name trino -p 8083:8080 trinodb/trino
10094 journaux Docker trino -f | grep -m1 "SERVEUR DÉMARRÉ"
10095 source .venv/bin/activer
10096 pip installer trino
10098 pip show trino
10099 python3 -c "\nimport trino\nconn = trino.dbapi.connect(host='localhost', port=8083, user='aura')\ncur = conn.cursor()\ncur.execute('SELECT 1')\nprint('Trino connection:', cur.fetchone())\n"




Actuel :
config.json ──────► Ebène 2 (Terminal)
└──► Ebène 3 (Streamlit)
└──► Ébène 3.5 (Web)
↑
ALLE lesen dieselbe Config

Idée :

Ébène 2 (Terminal) ─┐
Ebène 3 (Streamlit) ─┼──► Trino ──► user_configs
Ebène 3.5 (Web) ─┘ ├── terminal : traduction EN = vrai
├── web : DE, kein traduire
└── par utilisateur : remplacements propres




configuration/
├── settings.py ← Haupt-Config
├── settings_local.py ← remplacements lokale
├── settings_local.py_Example.txt
├── settings_local.py_Example_user_...txt
└── filtres/.backlock/first_run/
└── settings_local_log_filter.py ← un seul "Context-Split"

+ Divers JSON-Dateien et verschiedenen Orten
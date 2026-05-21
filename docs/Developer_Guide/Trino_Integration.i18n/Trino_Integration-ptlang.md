# docs/Developer_Guide/Trino_Integration.md
história | menos  ✔
10093 docker rm trino 2>/dev/null; docker run -d --name trino -p 8083:8080 trinodb/trino
10094 docker registra trino -f | grep -m1 "SERVIDOR INICIADO"
10095 fonte .venv/bin/activate
10096 pip instalar trino
10098 pip mostrar trino
10099 python3 -c "\nimport trino\nconn = trino.dbapi.connect(host='localhost', port=8083, user='aura')\ncur = conn.cursor()\ncur.execute('SELECT 1')\nprint('Conexão Trino:', cur.fetchone())\n"




Atual:
config.json ──────► Ebene 2 (Terminal)
└──► Ebene 3 (Streamlit)
└──► Ebene 3.5 (Web)
↑
TODAS as configurações dieselbe

Idéia:

Ebene 2 (Terminal) ─┐
Ebene 3 (Streamlit) ─┼──► Trino ──► user_configs
Ebene 3.5 (Web) ─┘ ├── terminal: EN traduzir = verdadeiro
├── web: DE, não traduz
└── por usuário: substituições próprias




configuração/
├── settings.py ← Haupt-Config
├── settings_local.py ← substituições locais
├── settings_local.py_Example.txt
├── configurações_local.py_Example_user_...txt
└── filtros/.backlock/first_run/
└── settings_local_log_filter.py ← einziger "Divisão de contexto"

+ Diversos JSON-Dateien e Verschiedenen Orten
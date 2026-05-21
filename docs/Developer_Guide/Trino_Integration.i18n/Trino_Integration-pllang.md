# docs/Developer_Guide/Trino_Integration.md
historia | mniej  ✔
10093 doker rm trino 2>/dev/null; docker run -d --name trino -p 8083:8080 trinodb/trino
10094 dzienniki dokowane trino -f | grep -m1 „SERWER URUCHOMIONY”
10095 źródło .venv/bin/activate
10096 pip zainstaluj trino
Trino pokazowe o wartości 10098 pipsów
10099 python3 -c "\nimport trino\nconn = trino.dbapi.connect(Host='localhost', port=8083, użytkownik='aura')\ncur = conn.cursor()\ncur.execute('WYBIERZ 1')\nprint('Połączenie Trino:', cur.fetchone())\n"




Aktualność:
config.json ────── ► Ebene 2 (Terminal)
└── ► Ebene 3 (w strumieniu)
└── ► Ebene 3.5 (Internet)
↑
ALLE lesen dieselbe Config

Pomysł:

Ebene 2 (Terminal) ─┐
Ebene 3 (Streamlit) ─┼── ► Trino ── ► user_configs
Ebene 3.5 (Web) ─┘ ├── terminal: EN tłumaczenie = prawda
├── strona internetowa: DE, kein tłumacz
└── na użytkownika: przesłonięcia własne




konfiguracja/
├── ustawienia.py ← Haupt-Config
├── settings_local.py ← lokalne Zastąpienia
├── ustawienia_local.py_Example.txt
├── ustawienia_local.py_Example_user_...txt
└── filtry/.backlock/first_run/
└── settings_local_log_filter.py ← einziger „Podział kontekstu”

+ różnorodne dane JSON i verschiedenen Orten
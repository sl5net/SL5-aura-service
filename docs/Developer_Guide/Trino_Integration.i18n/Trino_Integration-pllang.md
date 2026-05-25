# docs/Developer_Guide/Trino_Integration.md
__KOD_BLOKU_0__
df -h / /home 2>/dev/null XSPACEbreakX
docker pull trinodb/trino
__KOD_BLOKU_1__
doker rm trino 2>/dev/null || PRAWDA
docker run -d --name trino -p 8083:8080 trinodb/trino
__KOD_BLOKU_2__
dzienniki dokowane trino -f | grep -m1 „SERWER URUCHOMIONY”
__KOD_BLOKU_3__
pip zainstaluj trino
__KOD_BLOKU_4__
importuj trino
conn = trino.dbapi.connect(host='localhost', port=8083, użytkownik='aura')
cur = połączenie.kursor()
cur.execute('WYBIERZ 1')
print('Sprawdzanie połączenia Trino:', cur.fetchone())
__KOD_BLOKU_5__
Warstwa 2 (Terminal) ─┐
Warstwa 3 (Streamlit) ─┼── ► Trino ── ► Tabela: user_configs
Warstwa 3.5 (sieć) ─┘ ├── terminal: {translate: true}
├── web: {język: „DE”, tłumacz: fałsz}
└── identyfikator_użytkownika: {custom_overrides}
__KOD_BLOKU_6__
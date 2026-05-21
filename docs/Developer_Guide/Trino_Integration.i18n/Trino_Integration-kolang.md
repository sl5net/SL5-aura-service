# docs/Developer_Guide/Trino_Integration.md
역사 | 덜  ✔
10093 docker rm trino 2>/dev/null; docker run -d --name trino -p 8083:8080 trinodb/trino
10094 docker 로그 trino -f | grep -m1 "서버가 시작되었습니다"
10095 소스 .venv/bin/활성화
10096 pip 설치 트리노
10098 pip 쇼 트리노
10099 python3 -c "\nimport trino\nconn = trino.dbapi.connect(host='localhost', port=8083, user='aura')\ncur = conn.cursor()\ncur.execute('SELECT 1')\nprint('Trino 연결:', cur.fetchone())\n"




현재:
config.json ──────► Ebene 2 (터미널)
└──► 에벤3(스트림라이트)
└──► 에벤 3.5 (웹)
↑
모든 디젤 비 구성

아이디어:

에벤2(터미널) ─┐
Ebene 3 (Streamlit) ─┼──► Trino ──► user_configs
Ebene 3.5 (웹) ─┘ ├── 터미널: EN 번역 = true
├── 웹: DE, kein 번역
└── 사용자별: eigene 재정의




구성/
├── settings.py ← Haupt-Config
├── settings_local.py ← lokale 재정의
├── settings_local.py_Example.txt
├── settings_local.py_Example_user_...txt
└── 필터/.backlock/first_run/
└── settings_local_log_filter.py ← einziger "Context-Split"

+ 다양한 JSON 데이터 및 Orten 버전
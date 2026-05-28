# Trino 통합 — 개발자 가이드

## 건축학
Aura 인터페이스:
음성 → INTERFACE=음성(.py의 기본 대체)
터미널 → INTERFACE=터미널 (s() zshrc에 명시적)
웹 → INTERFACE=웹(start_service에 명시적)
↓
aura_state.py ← 개발자를 위한 고급 API
↓
trino_client.py ← 하위 수준 DB 작업
↓
Trino 메모리 카탈로그
memory.aura.features ← 인터페이스별 번역 켜기/끄기
memory.aura.translation_state ← 인터페이스별 대상 언어

## 로컬 설정

### 1. 도커

```bash
docker pull trinodb/trino
docker run -d --name trino -p 8083:8080 trinodb/trino
docker logs trino -f | grep -m1 "SERVER STARTED"
```

### 2. Python 클라이언트

```bash
source .venv/bin/activate
pip install trino
```

### 3. DB 초기화(Aura 시작 시 자동 호출)

```bash
python3 scripts/py/func/db/init_trino_db.py
```

## 개발자 API — aura_state.py

```python
from scripts.py.func.db.aura_state import (
    enable_translation,
    disable_translation,
    set_language,
    get_current_language,
    is_translation_enabled,
    get_all_status,
)

# Enable translation for speech interface
enable_translation('speech', lang='en')

# Check status
is_translation_enabled('speech')  # True
get_current_language('speech')    # 'en'

# Disable
disable_translation('speech')

# All interfaces
get_all_status()
# [
#   {'interface': 'speech',   'translation': 'on',  'language': 'en'},
#   {'interface': 'terminal', 'translation': 'off', 'language': None},
#   {'interface': 'web',      'translation': 'off', 'language': None},
# ]
```

## 관리 UI

http://localhost:8084

시작:
```bash
streamlit run scripts/py/chat/streamlit-admin.py --server.port 8084
```

## Trino UI(쿼리 모니터)

http://localhost:8083/ui/

스크립트/py/func/db/
├── init.py
├── trino_client.py ← 하위 수준: feature_state, target_lang 가져오기/설정
├── init_trino_db.py ← 시작: Docker 시작 + 스키마 + 테이블
└── aura_state.py ← 개발자를 위한 고수준 API
스크립트/py/chat/
└── streamlit-admin.py ← 포트 8084의 관리 UI


## 로드맵

- [x] Docker에서 실행되는 Trino
- [x] Python 클라이언트가 연결됨
- [x] Aura 시작 시 DB 초기화
- [x] 인터페이스 인식 번역 상태
- [x] 음성/터미널에서 분리된 웹(Streamlit)
- [x] 포트 8084의 관리 UI
- [ ] 터미널과 음성이 완전히 독립적입니다.
- [ ] 사용자별 재정의(다중 사용자)
- [ ] 영구 스토리지(메모리 카탈로그 교체)
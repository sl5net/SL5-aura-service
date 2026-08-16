# Trino Integration — Developer Guide

## Architecture
Aura Interfaces:
speech   → INTERFACE=speech   (default fallback in .py)
terminal → INTERFACE=terminal (explicit in s() zshrc)
web      → INTERFACE=web      (explicit in start_service)
↓
aura_state.py          ← high-level API for developers
↓
trino_client.py        ← low-level DB operations
↓
Trino memory catalog
memory.aura.features           ← translation on/off per interface
memory.aura.translation_state  ← target language per interface

## Local Setup

### 1. Docker

```bash
docker pull trinodb/trino
docker run -d --name trino -p 8083:8080 trinodb/trino
docker logs trino -f | grep -m1 "SERVER STARTED"
```

### 2. Python Client

```bash
source .venv/bin/activate
pip install trino
```

### 3. DB Initialization (called automatically at Aura startup)

```bash
python3 scripts/py/func/db/init_trino_db.py
```

## Developer API — aura_state.py

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

## Admin UI

http://localhost:8084

Start:
```bash
streamlit run scripts/py/chat/streamlit-admin.py --server.port 8084
```

## Trino UI (Query Monitor)

http://localhost:8083/ui/

scripts/py/func/db/
├── init.py
├── trino_client.py      ← low-level: get/set feature_state, target_lang
├── init_trino_db.py     ← startup: Docker start + schema + tables
└── aura_state.py        ← high-level API for developers
scripts/py/chat/
└── streamlit-admin.py   ← Admin UI on port 8084


## Roadmap

- [x] Trino running in Docker
- [x] Python client connected
- [x] DB initialized at Aura startup
- [x] Interface-aware translation state
- [x] Web (Streamlit) separated from speech/terminal
- [x] Admin UI on port 8084
- [ ] terminal and speech fully independent
- [ ] User-specific overrides (multi-user)
- [ ] Persistent storage (replace memory catalog)


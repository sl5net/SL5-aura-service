# Trino-Integration – Entwicklerhandbuch

## Architektur
Aura-Schnittstellen:
Speech → INTERFACE=Speech (Standard-Fallback in .py)
terminal → INTERFACE=terminal (explizit in s() zshrc)
web → INTERFACE=web (explizit in start_service)
↓
aura_state.py ← High-Level-API für Entwickler
↓
trino_client.py ← Low-Level-DB-Operationen
↓
Trino-Speicherkatalog
Memory.aura.features ← Übersetzung ein/aus pro Schnittstelle
memory.aura.translation_state ← Zielsprache pro Schnittstelle

## Lokales Setup

### 1. Docker

```bash
docker pull trinodb/trino
docker run -d --name trino -p 8083:8080 trinodb/trino
docker logs trino -f | grep -m1 "SERVER STARTED"
```

### 2. Python-Client

```bash
source .venv/bin/activate
pip install trino
```

### 3. DB-Initialisierung (wird automatisch beim Aura-Start aufgerufen)

```bash
python3 scripts/py/func/db/init_trino_db.py
```

## Entwickler-API – aura_state.py

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

## Admin-Benutzeroberfläche

http://localhost:8084

Start:
```bash
streamlit run scripts/py/chat/streamlit-admin.py --server.port 8084
```

## Trino-Benutzeroberfläche (Abfragemonitor)

http://localhost:8083/ui/

scripts/py/func/db/
├── init.py
├── trino_client.py ← low-level: get/set feature_state, target_lang
├── init_trino_db.py ← Startup: Docker-Start + Schema + Tabellen
└── aura_state.py ← High-Level-API für Entwickler
scripts/py/chat/
└── streamlit-admin.py ← Admin-Benutzeroberfläche auf Port 8084


## Roadmap

- [x] Trino läuft in Docker
- [x] Python-Client verbunden
- [x] DB wurde beim Aura-Start initialisiert
- [x] Schnittstellenbewusster Übersetzungsstatus
- [x] Web (Streamlit) getrennt von Sprache/Terminal
- [x] Admin-Benutzeroberfläche auf Port 8084
- [ ] Terminal und Sprache völlig unabhängig
- [ ] Benutzerspezifische Überschreibungen (Mehrbenutzer)
- [ ] Persistenter Speicher (Speicherkatalog ersetzen)
# Integración de Trino: guía para desarrolladores

## Arquitectura
Interfaces de aura:
voz → INTERFAZ=voz (respaldo predeterminado en .py)
terminal → INTERFAZ=terminal (explícito en s() zshrc)
web → INTERFACE=web (explícito en start_service)
↓
aura_state.py ← API de alto nivel para desarrolladores
↓
trino_client.py ← operaciones de base de datos de bajo nivel
↓
Catálogo de memorias Trino
Memory.aura.features ← traducción activada/desactivada por interfaz
Memory.aura.translation_state ← idioma de destino por interfaz

## Configuración local

### 1. Ventana acoplable

```bash
docker pull trinodb/trino
docker run -d --name trino -p 8083:8080 trinodb/trino
docker logs trino -f | grep -m1 "SERVER STARTED"
```

### 2. Cliente Python

```bash
source .venv/bin/activate
pip install trino
```

### 3. Inicialización de la base de datos (llamada automáticamente al iniciar Aura)

```bash
python3 scripts/py/func/db/init_trino_db.py
```

## API de desarrollador: aura_state.py

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

## Interfaz de usuario de administrador

http://localhost:8084

Comenzar:
```bash
streamlit run scripts/py/chat/streamlit-admin.py --server.port 8084
```

## Interfaz de usuario de Trino (monitor de consultas)

http://localhost:8083/ui/

scripts/py/func/db/
├── inicio.py
├── trino_client.py ← nivel bajo: obtener/establecer feature_state, target_lang
├── init_trino_db.py ← inicio: inicio de Docker + esquema + tablas
└── aura_state.py ← API de alto nivel para desarrolladores
scripts/py/chat/
└── streamlit-admin.py ← UI de administrador en el puerto 8084


## Hoja de ruta

- [x] Trino ejecutándose en Docker
- [x] Cliente Python conectado
- [x] DB inicializada al inicio de Aura
- [x] Estado de traducción compatible con la interfaz
- [x] Web (Streamlit) separada de voz/terminal
- [x] UI de administrador en el puerto 8084
- [ ] terminal y voz totalmente independientes
- [] Anulaciones específicas del usuario (multiusuario)
- [] Almacenamiento persistente (reemplaza el catálogo de memoria)
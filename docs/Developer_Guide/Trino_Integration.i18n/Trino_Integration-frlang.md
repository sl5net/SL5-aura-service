# Intégration Trino — Guide du développeur

## Architecture
Interfaces Aura :
parole → INTERFACE=parole (repli par défaut dans .py)
terminal → INTERFACE=terminal (explicite dans s() zshrc)
web → INTERFACE=web (explicite dans start_service)
↓
aura_state.py ← API de haut niveau pour les développeurs
↓
trino_client.py ← opérations de base de données de bas niveau
↓
Catalogue mémoire Trino
memory.aura.features ← traduction activée/désactivée par interface
memory.aura.translation_state ← langue cible par interface

## Configuration locale

### 1. Docker

```bash
docker pull trinodb/trino
docker run -d --name trino -p 8083:8080 trinodb/trino
docker logs trino -f | grep -m1 "SERVER STARTED"
```

### 2. Client Python

```bash
source .venv/bin/activate
pip install trino
```

### 3. Initialisation de la base de données (appelée automatiquement au démarrage d'Aura)

```bash
python3 scripts/py/func/db/init_trino_db.py
```

## API de développeur — aura_state.py

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

## Interface utilisateur d'administration

http://localhost:8084

Commencer:
```bash
streamlit run scripts/py/chat/streamlit-admin.py --server.port 8084
```

## Interface utilisateur Trino (moniteur de requêtes)

http://localhost:8083/ui/

scripts/py/func/db/
├── init.py
├── trino_client.py ← bas niveau : obtenir/définir feature_state, target_lang
├── init_trino_db.py ← démarrage : démarrage Docker + schéma + tables
└── aura_state.py ← API de haut niveau pour les développeurs
scripts/py/chat/
└── streamlit-admin.py ← Interface utilisateur d'administration sur le port 8084


## Feuille de route

- [x] Trino fonctionnant dans Docker
- [x] Client Python connecté
- [x] DB initialisée au démarrage d'Aura
- [x] État de traduction compatible avec l'interface
- [x] Web (Streamlit) séparé de la parole/terminal
- [x] Interface utilisateur d'administration sur le port 8084
- [ ] terminal et parole totalement indépendants
- [ ] Remplacements spécifiques à l'utilisateur (multi-utilisateurs)
- [ ] Stockage persistant (remplacer le catalogue de mémoire)
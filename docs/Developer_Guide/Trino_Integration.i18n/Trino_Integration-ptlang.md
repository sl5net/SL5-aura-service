# Integração Trino – Guia do desenvolvedor

## Arquitetura
Interfaces da Aura:
fala → INTERFACE = fala (fallback padrão em .py)
terminal → INTERFACE=terminal (explícito em s() zshrc)
web → INTERFACE=web (explícito em start_service)
↓
aura_state.py ← API de alto nível para desenvolvedores
↓
trino_client.py ← operações de banco de dados de baixo nível
↓
Catálogo de memórias Trino
memory.aura.features ← tradução ativada/desativada por interface
memory.aura.translation_state ← idioma alvo por interface

## Configuração local

### 1. Janela de encaixe

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

### 3. Inicialização do banco de dados (chamada automaticamente na inicialização do Aura)

```bash
python3 scripts/py/func/db/init_trino_db.py
```

## API do desenvolvedor — aura_state.py

__CODE_BLOCO_3__

## UI do administrador

http://localhost:8084

Começar:
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

## Trino UI (monitor de consulta)

http://localhost:8083/ui/

scripts/py/func/db/
├── init.py
├── trino_client.py ← baixo nível: obter/definir feature_state, target_lang
├── init_trino_db.py ← inicialização: início do Docker + esquema + tabelas
└── aura_state.py ← API de alto nível para desenvolvedores
scripts/py/chat/
└── streamlit-admin.py ← Admin UI na porta 8084


## Roteiro

- [x] Trino rodando no Docker
- [x] Cliente Python conectado
- [x] DB inicializado na inicialização do Aura
- [x] Estado de tradução com reconhecimento de interface
- [x] Web (Streamlit) separada da fala/terminal
- [x] UI Admin na porta 8084
- [] terminal e fala totalmente independentes
- [] Substituições específicas do usuário (multiusuário)
- [] Armazenamento persistente (substituir catálogo de memória)
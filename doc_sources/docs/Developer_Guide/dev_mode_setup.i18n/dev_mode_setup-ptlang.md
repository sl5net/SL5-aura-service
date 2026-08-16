# Guia de configuração DEV_MODE

## O problema

como somos compatíveis com Weyland, usamos `threading.Lock` para registro.

Agora (21.3.26 sábado) as regras para registro mudaram. Em Manjaro não houve problemas.

Quando `DEV_MODE = 1` está ativo, o Aura produz centenas de entradas de log por segundo
de vários threads. Isso pode causar um impasse em `SafeStreamToLogger`, tornando
Aura trava após o primeiro acionamento do ditado.

## A correção: use o filtro LOG_ONLY

Ao desenvolver com `DEV_MODE = 1`, você **deve** também configurar um filtro de log em:
`config/filtros/settings_local_log_filter.py`

### Filtro de trabalho mínimo para DEV_MODE:
```python
LOG_ONLY = [
    r"Successfully",
    r"CRITICAL",
    r"📢📢📢 #",
    r"Title",
    r"window",
    r":st:",
]
LOG_EXCLUDE = []
```

## Uma linha para settings_local.py
Adicione este comentário como lembrete ao lado da configuração DEV_MODE:
```python
DEV_MODE = 1  # ⚠️ Requires LOG_ONLY filter! See docs/dev_mode_setup.md
```

## Causa raiz
`SafeStreamToLogger` usa um `threading.Lock` para proteger gravações stdout.
Sob alta carga de log (DEV_MODE), a contenção de bloqueio causa conflitos nos sistemas
com agendamento agressivo de threads (por exemplo, CachyOS com kernels/glibc mais recentes).
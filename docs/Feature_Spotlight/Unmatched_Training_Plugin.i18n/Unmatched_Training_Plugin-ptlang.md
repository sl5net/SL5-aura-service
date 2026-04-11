# Plug-in de treinamento incomparável (`1_collect_unmatched_training`)

## Propósito

Este plugin coleta automaticamente entradas de voz não reconhecidas e as adiciona
como novas variantes para o regex do mapa difuso. Isso permite que o sistema se "autotreine"
ao longo do tempo, aprendendo com resultados de reconhecimento incomparáveis.

##Como funciona

1. A regra abrangente `COLLECT_UNMATCHED` é acionada quando nenhuma outra regra corresponde.
2. `collect_unmatched.py` é chamado via `on_match_exec` com o texto correspondente.
3. O regex na chamada `FUZZY_MAP_pre.py` é estendido automaticamente.

## Uso

Adicione esta regra abrangente no final de qualquer `FUZZY_MAP_pre.py` que você deseja treinar:
```python
from pathlib import Path
import os
PROJECT_ROOT = Path(os.environ["SL5NET_AURA_PROJECT_ROOT"])

FUZZY_MAP_pre = [
    # 1. Your rule to optimize (result first!)
    ('Blumen orchestrieren',
     r'^(Blumen giesen|Blumen gessen|Blumen essen)$', 100,
     {'flags': re.IGNORECASE}
    ),

    #################################################
    # 2. Activate this rule (place it after the rule you want to optimize)
    (f'{str(__file__)}', r'^(.*)$', 10,
     {'on_match_exec': [PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),
    #################################################
]
```

O rótulo `f'{str(__file__)}'` informa `collect_unmatched.py` exatamente qual
`FUZZY_MAP_pre.py` para atualizar - então a regra é portátil em qualquer plugin.

## Desativando o plugin

Quando você tiver coletado dados de treinamento suficientes, desative:

- Comentando a regra geral
- Renomear a pasta com um nome inválido (por exemplo, adicionar um espaço)
- Removendo a pasta do plugin do diretório `maps`

## Estrutura do arquivo
```
1_collect_unmatched_training/
├── collect_unmatched.py       # Plugin logic, called by engine
└── de-DE/
    └── FUZZY_MAP_pre.py       # Example with catch-all rule
```

## Observação

O plugin modifica `FUZZY_MAP_pre.py` em tempo de execução. Confirme o atualizado
arquivar regularmente para preservar os dados de treinamento coletados.
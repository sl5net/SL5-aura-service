# Complemento de entrenamiento inigualable (`1_collect_unmatched_training`)

## Objetivo

Este complemento recopila automáticamente entradas de voz no reconocidas y las agrega
como nuevas variantes de la expresión regular del mapa difuso. Esto permite que el sistema se "autoentrene"
con el tiempo aprendiendo de resultados de reconocimiento inigualables.

## Cómo funciona

1. La regla general `COLLECT_UNMATCHED` se activa cuando ninguna otra regla coincide.
2. `collect_unmatched.py` se llama a través de `on_match_exec` con el texto coincidente.
3. La expresión regular en la llamada `FUZZY_MAP_pre.py` se extiende automáticamente.

## Uso

Agrega esta regla general al final de cualquier `FUZZY_MAP_pre.py` que quieras entrenar:
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

La etiqueta `f'{str(__file__)}'` le dice a `collect_unmatched.py` exactamente qué
`FUZZY_MAP_pre.py` para actualizar, por lo que la regla es portátil en cualquier complemento.

## Deshabilitar el complemento

Cuando haya recopilado suficientes datos de entrenamiento, deshabilítelo mediante:

- Comentando la regla general.
- Cambiar el nombre de la carpeta con un nombre no válido (por ejemplo, agregar un espacio)
- Eliminar la carpeta del complemento del directorio `maps`

## Estructura de archivos
```
1_collect_unmatched_training/
├── collect_unmatched.py       # Plugin logic, called by engine
└── de-DE/
    └── FUZZY_MAP_pre.py       # Example with catch-all rule
```

## Nota

El complemento modifica `FUZZY_MAP_pre.py` en tiempo de ejecución. Confirmar la actualización
archivar periódicamente para preservar los datos de entrenamiento recopilados.
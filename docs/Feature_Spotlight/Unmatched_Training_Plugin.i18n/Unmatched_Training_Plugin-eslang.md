# Complemento de entrenamiento inigualable (`a_collect_unmatched_training`)

## Objetivo

Este complemento recopila automáticamente entradas de voz no reconocidas y las agrega
como nuevas variantes de la expresión regular del mapa difuso. Esto permite que el sistema se "autoentrene"
con el tiempo aprendiendo de resultados de reconocimiento inigualables.

## Cómo funciona

1. La regla general `COLLECT_UNMATCHED` en `FUZZY_MAP_pre.py` se activa cuando
ninguna otra regla coincidía con la entrada de voz.
2. `collect_unmatched.py` se llama a través de `on_match_exec` con el texto coincidente.
3. El texto se agrega a `unmatched_list.txt` (separado por tubería).
4. La expresión regular en `FUZZY_MAP_pre.py` se extiende automáticamente con la nueva variante.

## Deshabilitar el complemento

Cuando haya recopilado suficientes datos de entrenamiento, desactive este complemento de la siguiente manera:

- Desactivarlo en la configuración de Aura
- Eliminar la carpeta del complemento del directorio `maps`
- Cambiar el nombre de la carpeta con un nombre no válido (por ejemplo, agregar un espacio: `a_collect unmatched_training`)

## Estructura de archivos
```
a_collect_unmatched_training/
├── collect_unmatched.py       # Plugin logic, called by engine
└── de-DE/
    └── FUZZY_MAP_pre.py       # Catch-all rule + growing regex variants
```

## Nota

El complemento modifica `FUZZY_MAP_pre.py` en tiempo de ejecución. Asegúrate de comprometerte
el archivo actualizado periódicamente para preservar los datos de entrenamiento recopilados.
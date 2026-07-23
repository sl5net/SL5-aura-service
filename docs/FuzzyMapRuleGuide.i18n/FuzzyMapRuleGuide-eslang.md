# Guía de reglas FUZZY_MAP

## Formato de regla

```python
('replacement', r'regex_pattern', threshold, {'command_flags': re.IGNORECASE})
```

| Posición | Nombre | Descripción |
|---|---|---|
| 1 | reemplazo | El texto de salida después de la regla coincide con |
| 2 | patrón | Regex o cadena difusa para comparar |
| 3 | umbral | Para reglas de expresiones regulares: ignoradas. Para reglas difusas: puntuación mínima de coincidencia (0–100) |
| 4 | opciones | Diccionario opcional (consulte "Referencia de opciones" a continuación). Utilice `0` u omítalo para los valores predeterminados |
### Reemplazos crudos
De forma predeterminada (`False`), las cadenas de reemplazo son procesadas por `re.sub()` de Python, que admite el uso de referencias inversas de expresiones regulares como `\1` o `\2` para insertar grupos capturados (por ejemplo: `(r'\1', r'(\d)\s+(?=\d)', 95)`).
Si su reemplazo es una cadena de varias líneas o contiene barras invertidas sin escape (como plantillas de código o rutas de acceso) y debe conservarse exactamente como está, habilite `'raw_replacement': True` en el diccionario de opciones:
```python
(System_Instructions, r'^(system instructions)$', 10, {'command_flags': re.IGNORECASE, 'raw_replacement': True})
```

### Opciones disponibles configurables por el usuario:

* **`command_flags`** (entero): indicadores Regex utilizados durante la compilación del patrón.
*Ejemplo:* `{'command_flags': re.IGNORECASE}`
* **`raw_replacement`** (booleano): cuando es `True`, el texto de reemplazo se trata como una cadena literal pura y se omite mediante el análisis de barra invertida `re.sub` de Python. Es crucial para mensajes de varias líneas o cadenas con barras invertidas sin escape (`\`).
*Ejemplo:* `{'raw_replacement': Verdadero}`
* **`cache`** (booleano): alterna la caché de resultados de AURA. Establezca en "False" las reglas que generan resultados dinámicos (por ejemplo, hora actual, chistes aleatorios) para garantizar que se evalúen de nuevo en cada partido.
*Ejemplo:* `{'caché': Falso}`
* **`skip_list`** (lista de cadenas): especifica los módulos de canalización de posprocesamiento que se omitirán cuando esta regla coincida.
*Ejemplo:* `{'skip_list': ['LanguageTool']}` (omite la revisión gramatical)
* **`only_in_windows`** (lista de cadenas de expresiones regulares): restringe la regla para que solo se active si el título de la ventana activa coincide con uno de los patrones especificados.
*Ejemplo:* `{'only_in_windows': [r'^Mozilla Firefox$', r'Chrome']}`
* **`exclude_windows`** (lista de cadenas de expresiones regulares): evita que la regla se active si el título de la ventana activa coincide con uno de los patrones especificados.
*Ejemplo:* `{'exclude_windows': [r'Terminal', r'Claude']}`
* **`window_ignore_case`** (booleano): controla si la coincidencia de ventanas (`only_in_windows` / `exclude_windows`) se evalúa sin distinguir entre mayúsculas y minúsculas (`True`) o sin distinguir entre mayúsculas y minúsculas (`False`). Si se omite, vuelve a la configuración global `LOWERCASE_WINDOW_TITLES` en `config/settings.py`.
*Ejemplo:* `{'window_ignore_case': Falso}`
* **`on_match_exec`** (lista de rutas/objetos de cadena): rutas a scripts/complementos que deben ejecutarse cuando esta regla coincide (utilizada en gran medida por reglas generales y alternativas).
*Ejemplo:* `{'on_match_exec': [PROJECT_ROOT / 'scripts' / 'custom_action.py']}`

## Lógica de canalización
- Las reglas se procesan **de arriba hacia abajo**


## Lógica de canalización

- Las reglas se procesan **de arriba hacia abajo**
- **Todas** las reglas de coincidencia se aplican (acumulativas)
- Una **fullmatch** (`^...$`) detiene la canalización inmediatamente
- Las reglas anteriores tienen prioridad sobre las reglas posteriores.

## Patrones comunes

### Coincidir con una sola palabra (límite de palabra)
```python
('Python', r'\bpython\b', 0, {'command_flags': re.IGNORECASE})
```

### Coincidir con múltiples variantes
```python
('OpenAI', r'\bopen\s*ai\b', 0, {'command_flags': re.IGNORECASE})
```

### Fullmatch – detiene el proceso
```python
('hello koan', r'^.*$', 0, {'command_flags': re.IGNORECASE})
```
⚠️ Esto coincide con **todo**. El oleoducto se detiene aquí. Las normas anteriores siguen teniendo prioridad.

### Coincidir con el inicio de la entrada
```python
('Note: ', r'^notiz\b', 0, {'command_flags': re.IGNORECASE})
```

### Coincide con la frase exacta
```python
('New York', r'\bnew york\b', 0, {'command_flags': re.IGNORECASE})
```

## Ubicaciones de archivos

| Archivo | Fase | Descripción |
|---|---|---|
| `FUZZY_MAP_pre.py` | Herramienta previa al lenguaje | Aplicado antes de la revisión ortográfica |
| `FUZZY_MAP.py` | Herramienta post-idioma | Aplicado después de la revisión ortográfica |
| `PUNCTUATION_MAP.py` | Herramienta previa al lenguaje | Reglas de puntuación |

## Consejos

- Poner reglas **específicas** antes que las **generales**
- Utilice `^...$` fullmatch solo cuando desee detener todo procesamiento posterior
- `FUZZY_MAP_pre.py` es ideal para correcciones antes de la revisión ortográfica
- Pruebe las reglas con: `s su entrada de prueba` en la consola Aura
- Las copias de seguridad se crean automáticamente como `.peter_backup`

## Ejemplos

```python
FUZZY_MAP_pre = [
    # Correct a common STT mistake
    ('Raspberry Pi', r'\braspberry\s*pie?\b', 0, {'command_flags': re.IGNORECASE}),

    # Expand abbreviation
    ('zum Beispiel', r'\bzb\b', 0, {'command_flags': re.IGNORECASE}),

    # Stop pipeline for testing
    # ('test koan', r'^.*$', 0, {'command_flags': re.IGNORECASE}),
]
```

## Tu primera regla: paso a paso

1. Abra `config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py`
2. Agregue su regla dentro de `FUZZY_MAP_pre = [...]`
3. Guardar: Aura se recarga automáticamente, no es necesario reiniciar
4. Dicta tu frase desencadenante y observa cómo se dispara


## Estructura de archivos recomendada

Coloque sus reglas **antes** de bloques de comentarios largos:
```python
# config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py
import re  # noqa: F401
# too<-from
FUZZY_MAP_pre = [
    ('My Rule', r'my rule', 0, {'command_flags': re.IGNORECASE}),
]
# ============================================================
# Longer explanations, task descriptions, notes...
# can be as long as needed — they go AFTER the rules.
# ============================================================
```

**¿Por qué?** Auto-Fix de Aura escanea solo el primer ~1 KB de un archivo.
Si sus reglas aparecen después de un encabezado largo, Auto-Fix no puede encontrarlas ni repararlas.
También se recomienda el comentario de ruta en la línea 1: ayuda a los humanos a identificar rápidamente el archivo.
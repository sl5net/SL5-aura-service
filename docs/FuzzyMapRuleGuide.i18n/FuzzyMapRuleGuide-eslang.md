# Guía de reglas FUZZY_MAP

## Formato de regla

```python
('replacement', r'regex_pattern', threshold, {'flags': re.IGNORECASE})
```

| Posición | Nombre | Descripción |
|---|---|---|
| 1 | reemplazo | El texto de salida después de la regla coincide con |
| 2 | patrón | Regex o cadena difusa para comparar |
| 3 | umbral | Ignorado por reglas de expresiones regulares. Se utiliza para coincidencias aproximadas (0–100) |
| 4 | banderas | `{'flags': re.IGNORECASE}` para que no distinga entre mayúsculas y minúsculas, `0` para que distinga entre mayúsculas y minúsculas |

## Lógica de canalización

- Las reglas se procesan **de arriba hacia abajo**
- **Todas** las reglas de coincidencia se aplican (acumulativas)
- Una **fullmatch** (`^...$`) detiene la canalización inmediatamente
- Las reglas anteriores tienen prioridad sobre las reglas posteriores.

## Patrones comunes

### Coincidir con una sola palabra (límite de palabra)
```python
('Python', r'\bpython\b', 0, {'flags': re.IGNORECASE})
```

### Coincidir con múltiples variantes
```python
('OpenAI', r'\bopen\s*ai\b', 0, {'flags': re.IGNORECASE})
```

### Fullmatch – detiene el proceso
```python
('hello koan', r'^.*$', 0, {'flags': re.IGNORECASE})
```
⚠️ Esto coincide con **todo**. El oleoducto se detiene aquí. Las normas anteriores siguen teniendo prioridad.

### Coincidir con el inicio de la entrada
```python
('Note: ', r'^notiz\b', 0, {'flags': re.IGNORECASE})
```

### Coincide con la frase exacta
```python
('New York', r'\bnew york\b', 0, {'flags': re.IGNORECASE})
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
    ('Raspberry Pi', r'\braspberry\s*pie?\b', 0, {'flags': re.IGNORECASE}),

    # Expand abbreviation
    ('zum Beispiel', r'\bzb\b', 0, {'flags': re.IGNORECASE}),

    # Stop pipeline for testing
    # ('test koan', r'^.*$', 0, {'flags': re.IGNORECASE}),
]
```
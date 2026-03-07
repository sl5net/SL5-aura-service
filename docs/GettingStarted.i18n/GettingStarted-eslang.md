# Primeros pasos con SL5 Aura

## ¿Qué es SL5 Aura?

SL5 Aura es un asistente de voz sin conexión que convierte voz en texto (STT) y aplica reglas configurables para limpiar, corregir y transformar la salida.

Funciona sin GUI: todo se ejecuta a través de CLI o consola.

## Cómo funciona

```
Microphone → Vosk (STT) → Maps (Pre) → LanguageTool → Maps (Post) → Output
```

1. **Vosk** convierte tu discurso en texto sin formato
2. **Pre-Maps** limpia y corrige el texto antes de revisar la ortografía
3. **LanguageTool** corrige la gramática y la ortografía
4. **Post-Maps** aplica transformaciones finales
5. **Salida** es el texto limpio final (y opcionalmente TTS)

## Tus primeros pasos

### 1. Iniciar aura
```bash
python main.py
```

### 2. Prueba con entrada de consola
Escriba `s` seguido de su texto:
```
s hello world
```

### 3. Vea una regla en acción
Abra `config/maps/koans_deutsch/01_koan_erste_schritte/de-DE/FUZZY_MAP_pre.py`

Descomente la regla interna y pruebe nuevamente. ¿Lo que sucede?

## Comprender las reglas

Las reglas se encuentran en `config/maps/` en archivos Python llamados `FUZZY_MAP_pre.py` o `FUZZY_MAP.py`.

Una regla se ve así:
```python
('Hello World', r'\bhello world\b', 0, {'flags': re.IGNORECASE})
#   ^output        ^pattern          ^threshold  ^case-insensitive
```

La **salida** es lo primero: inmediatamente verás lo que produce la regla.

Las reglas se procesan **de arriba a abajo**. La primera coincidencia completa (`^...$`) detiene todo.

## Koans – Aprender haciendo

Los koans son pequeños ejercicios en `config/maps/koans_deutsch/` y `config/maps/koans_english/`.

Cada koan enseña un concepto:

| Koan | Tema |
|---|---|
| 01_koan_erste_schritte | Primera regla, partido completo, parada del oleoducto |
| 02_koan_escuchar | Listas, múltiples reglas |
| 03_koan_schwierige_namen | Nombres difíciles, concordancia fonética |

Comience con Koan 01 y avance.

## Consejos

- Las reglas en `FUZZY_MAP_pre.py` se ejecutan **antes** de la revisión ortográfica: buena para corregir errores STT
- Las reglas en `FUZZY_MAP.py` se ejecutan **después** de la revisión ortográfica – buena para formatear
- Los archivos de respaldo (`.peter_backup`) se crean automáticamente antes de cualquier cambio
- Utilice `peter.py` para permitir que una IA trabaje con los koans automáticamente
# Atributos de regla: `only_in_windows` y `exclude_windows`

Estos dos atributos controlan **en qué ventanas activas se permite activar una regla**.
Se definen dentro del dictado de "opciones" de una regla y aceptan una **lista de patrones de expresiones regulares**
que coinciden con el título de la ventana activa actual (`_active_window_title`).

---

## `solo_en_ventanas`

La regla se activa **solo si** el título de la ventana activa coincide con **al menos uno** de los patrones dados.
Todas las demás ventanas se ignoran.

**Caso de uso:** Restringir una regla a una aplicación específica.


> La regla se activará **solo** cuando Firefox o Chromium sea la ventana activa.

---

## `excluir_ventanas`

La regla se activa **a menos que** el título de la ventana activa coincida con **al menos uno** de los patrones dados.
Se omiten las ventanas coincidentes.

**Caso de uso:** Deshabilite una regla para aplicaciones específicas.

Ejemplos

```py
Targets
    Occurrences of 'exclude_windows' in Project with mask '*pre.py'
Found occurrences in Project with mask '*pre.py'  (3 usages found)
    Usage in string constants  (3 usages found)
        STT  (3 usages found)
            config/maps/plugins/z_fallback_llm/de-DE  (3 usages found)
                FUZZY_MAP_pre.py  (3 usages found)
                    90 'exclude_windows': [r'element',r'firefox', r'chrome', r'brave'],
                    105 'exclude_windows': [r'element',r'firefox', r'chrome', r'brave'],
                    119 'exclude_windows': [r'element',r'firefox', r'chrome', r'brave',r'doublecmd'],

```



La coincidencia **no distingue entre mayúsculas y minúsculas** y utiliza **expresiones regulares** de Python.

---

## Resumen

| Atributo | Se dispara cuando... |
|-------------------|--------------------------------------------|
| `solo_en_ventanas` | título de la ventana **coincide** con uno de los patrones |
| `excluir_ventanas` | título de la ventana **NO coincide** con ningún patrón |

---

## Ver también

- `scripts/py/func/process_text_in_background.py` — líneas ~1866 y ~1908
- `scripts/py/func/get_active_window_title.py` — cómo se recupera el título de la ventana
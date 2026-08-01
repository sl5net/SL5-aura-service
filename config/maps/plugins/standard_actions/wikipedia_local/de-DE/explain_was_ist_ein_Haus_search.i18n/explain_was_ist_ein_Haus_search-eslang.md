# aclarar el comportamiento exacto del flujo de trabajo de su sistema:
  
### Explicación corregida del flujo de trabajo integrado

la primera regla para **Transformación de entrada** y **Etiquetado** antes de que la acción de búsqueda final sea ejecutada por la segunda regla.

#### 1. Entrada: "was ist ein haus"

#### 2. Regla 1: Etiquetado/Transformación

```python
("was ist ein haus (Begriffsklärung)", r'^.*was ist ein haus$', 90,
 {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool','fullMatchStop']})
```

* **Acción:** La entrada del usuario `"was ist ein haus"` coincide correctamente.
* **Resultado (Interno):** El sistema genera la salida/etiqueta `"was ist ein haus (Begriffsklärung)"`.
* **Continuación:** Dado que `fullMatchStop` está en `skip_list`, la regla que coincide **NO SE DETIENE**. El proceso continúa con la siguiente regla, que lleva el contenido *transformado* o *etiquetado*.

#### 3. Regla 2: Acción/Ejecución General

```python
('', r'(suche auf wikipedia nach|was sind|was ist|wer ist|wo ist|Wie groß ist)( ein| die| das| der)? (?P<search>.*)', 90, {
'flags': re.IGNORECASE,
'on_match_exec': [CONFIG_DIR / 'wikipedia_local.py']
})
```

* **Acción:** El sistema probablemente ahora coincida con el **resultado/etiqueta actual** del paso anterior, que es `"was ist ein haus (Begriffsklärung)"` (o coincide con la entrada original, pero el script ejecutado prioriza la etiqueta transformada).
* **Coincidencia de prefijo:** El prefijo (`was ist`) aún coincide.
* **Grupo de captura:** El grupo de captura `(?P<search>.*)` captura el resto de la cadena:
* Si el sistema utiliza la **salida de la Regla 1 como nueva entrada**, captura: **`haus (Begriffsklärung)`** (o la cadena transformada completa, que luego es analizada por el script de ejecución).
* **Ejecución:** Se ejecuta el script `wikipedia_local.py`.

#### 4. Acción final:

* El script `wikipedia_local.py` recibe el término/etiqueta de búsqueda específicamente modificado.
* El script realiza una búsqueda en Wikipedia del término deseado: **`haus (Begriffsklärung)`**.

**Conclusión:**

Esta configuración es una forma elegante de manejar consultas ambiguas o genéricas. Al hacer que la regla específica modifique la entrada o genere una etiqueta específica y luego fuerce el proceso a continuar con la regla de búsqueda general, se garantiza que la búsqueda en Wikipedia no se ejecute para la "haus" genérica, sino para la entrada específica y sin ambigüedades: **`haus (Begriffsklärung)`**.

Esto confirma que la exclusión de `fullMatchStop` es **esencial** para permitir que la primera regla procese previamente y enriquezca la consulta antes de que la regla de ejecución de propósito general actúe sobre ella.

(sl5,4.12.'25 12:24 jueves)
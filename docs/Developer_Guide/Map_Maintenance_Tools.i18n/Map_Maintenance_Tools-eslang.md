# Herramientas de mantenimiento de mapas Regex

Para admitir la funcionalidad de búsqueda rápida (comando `s` / `search_rules.sh`), utilizamos un script auxiliar que anota automáticamente patrones de expresiones regulares con ejemplos legibles por humanos.

## ¿Por qué necesitamos esto?
Nuestros archivos `FUZZY_MAP.py` contienen expresiones regulares complejas. Para que se puedan buscar mediante buscadores difusos (fzf) sin necesidad de comprender la expresión regular sin formato, agregamos comentarios `# EJEMPLO:` encima de los patrones.

**Antes:**
```python
('CreditCard', r'\b(?:\d[ -]*?){13,16}\b', ...)
```

**Después (generado automáticamente):**
```python
# EXAMPLE: 1234-5678-9012-3456
('CreditCard', r'\b(?:\d[ -]*?){13,16}\b', ...)
```

## El script del etiquetador (`map_tagger.py`)

Proporcionamos un script de Python que escanea todos los archivos `FUZZY_MAP.py` y `FUZZY_MAP_pre.py` y genera estos ejemplos automáticamente.

### Instalación
El script requiere que la biblioteca `exrex` genere coincidencias aleatorias para expresiones regulares complejas.

```bash
pip install exrex
```

### Uso
Ejecute el script desde la raíz del proyecto:

```bash
python3 tools/map_tagger.py
```

### Flujo de trabajo
1. **Crear o editar** un archivo de mapa (por ejemplo, agregar nuevas reglas).
2. **Ejecute** el script del etiquetador.
3. **Modo interactivo:**
- El script te mostrará una sugerencia generada.
- Pulsa `ENTER` para aceptarlo.
- Escriba `s` para omitir.
- Escriba `sa` (omitir todo) si desea omitir todos los patrones restantes que fallan en la generación.
4. **Confirmar** los cambios.

> **Nota:** El script ignora las etiquetas `# EJEMPLO:` existentes, por lo que es seguro ejecutarlo repetidamente.
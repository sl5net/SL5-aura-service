# Módulo de reparación automática (modo de entrada rápida de reglas)

## Qué hace

Cuando escribe una palabra simple (sin comillas ni sintaxis de Python) en un archivo de mapa
como `FUZZY_MAP_pre.py`, el sistema lo convierte automáticamente en una regla válida.

Esta es la forma más rápida de crear nuevas reglas: no es necesario recordar el formato.

## Ejemplo

Escribe esto en `FUZZY_MAP_pre.py`:

```
oma
```

El módulo de reparación automática detecta un `NameError` (palabra simple, Python no válido)
y transforma el archivo automáticamente en:

```python
# config/maps/.../de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
# too<-from
FUZZY_MAP_pre = [
    ('oma', 'oma'),
]
```

Ahora edite la regla según lo que realmente necesita:

```python
('Oma', 'oma'),              # capitalize
('Großmutter', 'oma'),       # synonym
('Thomas Müller', 'thomas'), # from a phone book
```

## Cómo funciona

El módulo `scripts/py/func/auto_fix_module.py` se activa automáticamente
cuando Aura detecta un `NameError` mientras carga un archivo de mapa.

Entonces:
1. Agrega el encabezado de ruta de archivo correcto
2. Agrega `import re` si falta
3. Agrega la definición de lista `FUZZY_MAP_pre = [`
4. Convierte palabras simples en tuplas `('palabra', 'palabra')
5. Cierra la lista con `]`

## Reglas y límites

- Sólo funciona en archivos de menos de **1 KB** (límite de seguridad)
- Sólo aplica a: `FUZZY_MAP.py`, `FUZZY_MAP_pre.py`, `PUNCTUATION_MAP.py`
- El archivo debe estar en una carpeta de idioma válido (por ejemplo, `de-DE/`)
- Funciona para varias palabras a la vez (por ejemplo, de una lista de directorio telefónico)

## El comentario `# también<-from`

Este comentario se agrega automáticamente como recordatorio de la dirección de la regla:

```
too <- from
```

Significado: **salida** (también) ← **entrada** (de). El reemplazo es lo primero.

Para `PUNCTUATION_MAP.py` la dirección se invierte: `# from->too`

## Entrada masiva de una lista

Puedes pegar varias palabras a la vez:

```
thomas
maria
berlin
```

Cada palabra desnuda se convierte en su propia regla:

```python
('thomas', 'thomas'),
('maria', 'maria'),
('berlin', 'berlin'),
```

Luego edite cada reemplazo según sea necesario.

## Archivo: `scripts/py/func/auto_fix_module.py`
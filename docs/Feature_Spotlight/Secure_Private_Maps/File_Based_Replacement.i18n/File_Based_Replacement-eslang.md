# FUNCIÓN DESTACADA: Reemplazos de reglas basadas en archivos

Este documento describe cómo mantener valores confidenciales (contraseñas, claves API, tokens)
del código fuente `FUZZY_MAP_pre` / `FUZZY_MAP` y del historial de Git cargando el
Texto de "reemplazo" de un archivo separado en tiempo de ejecución en lugar de codificarlo.

Esto es especialmente útil durante transmisiones en vivo o pantallas compartidas, donde el mapa
El código fuente en sí puede ser visible, pero el archivo al que se hace referencia no.

---

## 1. El concepto

Normalmente, el campo "reemplazo" de una regla es el texto de salida literal:

```python
('my-secret-value', r'^(trigger)$', 85, {'command_flags': re.IGNORECASE})
```

Con el reemplazo basado en archivos habilitado, un valor de "reemplazo" que comienza con un
El prefijo configurado (por defecto `-` o `.`) se trata como un **nombre de archivo**.
Aura resuelve ese nombre de archivo en relación con el propio directorio del complemento, lee su
contenido y utiliza ese contenido como texto de reemplazo.

```python
('-api_key.txt', r'^(show api key)$', 85, {'command_flags': re.IGNORECASE})
```

Si `api_key.txt` existe junto a `FUZZY_MAP_pre.py` del complemento, está (eliminado)
El contenido se utiliza como reemplazo. Si el archivo no existe, el literal
en su lugar se devuelve la cadena `-api_key.txt` (a prueba de fallos: no hay fugas accidentales de
"archivo no encontrado" como texto utilizable y sin fallas).

---

## 2. Configuración

Configurado en `config/settings.py` (o `config/settings_local.py` para local
anula):

| Configuración | Tipo | Predeterminado | Descripción |
|---|---|---|---|
| `FILE4REPLACEMENT_USE` | `bool` | `Verdadero` | Interruptor maestro para toda la función. Si es "Falso", "reemplazo" siempre se usa literalmente. |
| `FILE4REPLACEMENT_ALLOWED_PREFIXES` | `tupla[cadena]` | `('-', '.')` | Los valores de "reemplazo" deben comenzar con uno de estos prefijos para activar una búsqueda de archivos. Vacío/`Ninguno` = cualquier valor que no comience con una letra se trata como un nombre de archivo potencial. |
| `FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL` | `bool` | `Falso` | Si es `True`, permite resolver archivos fuera del propio directorio del complemento (por ejemplo, rutas absolutas o secuencias `../`). Consulte la sección Seguridad a continuación. |
| `FILE4REPLACEMENT_DENY_PREFIXES` | `tupla[cadena]` | p.ej. `('/etc', '/proc', '/dev', '/var/lib', '/root', 'C:\\Windows', 'C:\\Archivos de programa')` | Las rutas absolutas resueltas que comienzan con cualquiera de estas **siempre** se rechazan, independientemente de `FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL`. Límite de seguridad estricto contra los directorios del sistema. |

---

## 3. Resolución de ruta

El expediente se resuelve de la siguiente manera:

1. La `ruta_fuente` del complemento (grabada automáticamente por el cargador de mapas) es
unido contra `PROJECT_ROOT` (leído del `SL5NET_AURA_PROJECT_ROOT`
variable de entorno) para obtener el directorio del complemento.
2. El valor de "reemplazo" se une a ese directorio.
3. A menos que `FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL` sea `True`, la ruta resuelta
debe permanecer dentro del directorio del complemento, o la búsqueda será rechazada.
4. Independientemente de lo anterior, cualquier ruta resuelta que comience con una entrada en
`FILE4REPLACEMENT_DENY_PREFIXES` siempre se rechaza.
5. Si el archivo existe, se devuelve su contenido eliminado. De lo contrario, el
La cadena de "reemplazo" original se devuelve sin cambios.

---

## 4. Notas de seguridad

- Solo habilite `FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL` si comprende el
Implicaciones: permite a cualquier usuario que pueda editar un archivo `FUZZY_MAP_pre` (p. ej.
a través de un editor de mapas en línea) para leer archivos arbitrarios que el proceso Aura puede
acceder y hacer que su contenido aparezca como texto de salida en vivo.
- `FILE4REPLACEMENT_DENY_PREFIXES` proporciona una protección básica contra
directorios comunes del sistema incluso cuando se permite el recorrido de ruta, pero es
no sustituye a restringir quién puede editar archivos de mapas en primer lugar.
- Los archivos referenciados son texto sin formato en el disco. Combina con el archivo de tu sistema operativo
permisos si el contenido es confidencial.

---

## 5. Ejemplo

Consulte `config/maps/plugins/TEST_FILE4REPLACEMENT/` para ver un complemento de ejemplo funcional.
y `tools/tests/TEST_FILE4REPLACEMENT.sh` para un script de prueba que ejercita
tanto una búsqueda en el directorio como una búsqueda fuera del directorio del complemento.

```python
# config/maps/plugins/TEST_FILE4REPLACEMENT/de-DE/FUZZY_MAP_pre.py
FUZZY_MAP_pre = [
    ('.Zebra.txt', r'^(Zebra)$', 85, {'command_flags': re.IGNORECASE}),
]
```

Cree `.Zebra.txt` junto a este archivo con el texto de reemplazo deseado, luego
diga (o escriba a través de la consola) `s Zebra` para activarlo.
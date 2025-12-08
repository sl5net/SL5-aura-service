## Funciones destacadas: implementación de un modo de traducción en vivo alternable

Nuestro marco de asistente de voz conectable está diseñado para ofrecer la máxima flexibilidad. Esta guía demuestra una característica poderosa: un modo de traducción en vivo que se puede activar y desactivar con un simple comando de voz. Imagínese hablar con su asistente en alemán y escuchar el mensaje en portugués y luego volver a su comportamiento normal al instante.

Esto se logra no cambiando el motor central, sino manipulando inteligentemente el propio archivo de configuración de reglas.

### Cómo usarlo

Configurar esto implica agregar dos reglas a su archivo `FUZZY_MAP_pre.py` y crear los scripts correspondientes.

**1. La regla de alternancia:** Esta regla escucha el comando para activar o desactivar el modo de traducción.

```python
# Rule to turn the translation mode on or off
    ('', r'^(portugiesisch|übersetzung|übersetzer) (aktivieren|aktiviert|aktiv|einschalten|deaktivieren|ausschalten|toggle|Dogge|doppelt)\b', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),
```
Cuando dices "Übersetzung einschalten" (Activar traducción), se ejecuta el script `toggle_translation_mode.py`.

**2. La regla de traducción:** Esta es una regla general que, cuando está activa, coincide con cualquier texto y lo envía al script de traducción.

```python
    # ANCHOR: The following line is controlled by the toggle script.
    # TRANSLATION_RULE
    ('', r'.+', 5, {'flags': re.IGNORECASE,'on_match_exec': [CONFIG_DIR / 'translate_from_to.py']}),
```
La clave aquí es el comentario `# TRANSLATION_RULE`. Esto actúa como un "ancla" que el script de alternancia utiliza para buscar y modificar la regla debajo de él.

### Cómo funciona: la magia detrás del telón

En lugar de utilizar un estado interno, este método edita directamente el mapa de reglas en el sistema de archivos. El script `toggle_translation_mode.py` actúa como un administrador de configuración.

1. **Encuentre la regla:** Cuando se activa, el script lee el contenido de `FUZZY_MAP_pre.py`. Busca el comentario ancla único `# TRANSLATION_RULE`.

2. **Alternar el estado:**
* **Para deshabilitar:** Si la línea de regla debajo del ancla está activa, el script agrega un `#` al principio de la línea, comentándola efectivamente y deshabilitándola.
* **Para habilitar:** Si la línea de la regla ya está comentada, el script elimina cuidadosamente el `#` inicial, reactivando la regla.

3. **Guardar y volver a cargar:** El script guarda el contenido modificado nuevamente en `FUZZY_MAP_pre.py`. Luego crea un archivo activador especial (por ejemplo, `RELOAD_RULES.trigger`). El servicio principal busca constantemente este archivo desencadenante. Cuando aparece, el servicio sabe que su configuración ha cambiado y recarga todo el mapa de reglas desde el disco, aplicando el cambio instantáneamente.

### Filosofía del diseño: ventajas y consideraciones

Se eligió este enfoque de modificar el archivo de configuración directamente por su claridad y simplicidad para el usuario final.

#### Ventajas:

* **Alta transparencia:** El estado actual del sistema siempre es visible. Un vistazo rápido al archivo `FUZZY_MAP_pre.py` revela inmediatamente si la regla de traducción está activa o comentada.
* **Sin cambios en el motor principal:** Esta poderosa característica se implementó sin alterar una sola línea del motor de procesamiento de reglas principal. Demuestra la flexibilidad del sistema de complementos.
* **Intuitivo para desarrolladores:** El concepto de habilitar o deshabilitar una parte de la configuración comentándola es un patrón familiar, simple y confiable para cualquiera que haya trabajado con código o archivos de configuración.

#### Consideraciones:

* **Permisos del sistema de archivos:** Para que este método funcione, el proceso del asistente debe tener permisos de escritura en sus propios archivos de configuración. En algunos entornos de alta seguridad, esto podría ser una consideración.
Ganchos Aura SL5: Agregados

HOOK_PLUGIN_LOAD = 'on_plugin_load'
HOOK_FILE_LOAD = 'en_carga_archivo'
HOOK_RELOAD = 'al_recargar'
HOOK_UPSTREAM = 'on_folder_change'

on_folder_change() y
on_reload() para activar la lógica después de recargas en caliente. Utilice esto para la ejecución en cadena de scripts principales como Secure_packer.py para paquetes complejos.

# Guía para desarrolladores: enlaces del ciclo de vida de los complementos

Aura SL5 permite que los complementos (Mapas) definan "Hooks" específicos que se ejecutan automáticamente cuando cambia el estado del módulo. Esto es esencial para flujos de trabajo avanzados como el sistema **Secure Private Map**.

## El gancho `on_folder_change`

Se implementó la detección de gancho `on_folder_change`. El recargador ahora escanea el directorio.

## El gancho `on_reload()`

La función `on_reload()` es una función opcional que puede definir en cualquier módulo de Mapa.

### Comportamiento
* **Activador:** Se ejecuta inmediatamente después de que un módulo se **recarga en caliente** exitosamente (modificación de archivo + activador de voz).
* **Contexto:** Se ejecuta dentro del hilo principal de la aplicación.
* **Seguridad:** Envuelto en un bloque `try/except`. Los errores aquí se registrarán pero **no bloquearán** la aplicación.

### Patrón de uso: la "cadena tipo margarita"
Para paquetes complejos (como Private Maps), a menudo tienes muchos subarchivos, pero solo un script central (`secure_packer.py`) debe manejar la lógica.

Puedes usar el gancho para delegar la tarea hacia arriba:

__CODE_BLOCK_0__
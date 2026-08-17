# Ganchos del ciclo de vida del complemento

Aura SL5 admite enlaces de ciclo de vida que permiten que los complementos (Mapas) ejecuten lógica específica automáticamente cuando cambia su estado.

## El gancho `on_reload()`

La función `on_reload()` es una función opcional especial que puede definir dentro de cualquier mapa de complementos (`.py`).

### Comportamiento
* **Activador:** Esta función se ejecuta **inmediatamente después** de que el módulo se haya recargado en caliente exitosamente (cambio de archivo detectado + activador de voz).
* **Contexto:** Se ejecuta dentro del flujo principal de la aplicación.
* **Alcance:** **NO** se ejecuta durante el inicio inicial del sistema (arranque en frío). Es estrictamente para escenarios de *re*carga.

### Casos de uso
* **Seguridad:** Vuelva a cifrar o comprimir automáticamente archivos confidenciales después de editarlos.
* **Gestión de estado:** Restablecer contadores globales o borrar cachés específicos.
* **Notificación:** Registro de información de depuración específica para verificar que se aplicó un cambio.

### Detalles técnicos y seguridad
* **Manejo de errores:** La ejecución se incluye en un bloque `try/except`. Si su función `on_reload` falla (por ejemplo, `DivisionByZero`), registrará un error (`❌ Error al ejecutar on_reload...`) pero **no bloqueará Aura**.
* **Rendimiento:** La función se ejecuta de forma sincrónica. Evite tareas de larga duración (como descargas grandes) directamente en esta función, ya que bloquearán brevemente el procesamiento del comando de voz. Para tareas pesadas, genera un hilo.

### Código de ejemplo

__CODE_BLOCK_0__
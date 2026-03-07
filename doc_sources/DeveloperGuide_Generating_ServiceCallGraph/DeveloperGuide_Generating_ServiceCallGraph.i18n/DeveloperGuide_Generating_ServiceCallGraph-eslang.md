# Guía para desarrolladores: generación del gráfico de llamadas de servicio

Este documento describe el método robusto y seguro para subprocesos para generar un gráfico de llamadas visual del `aura_engine.py` de larga duración. Usamos el perfilador `yappi` (para soporte de subprocesos múltiples) y `gprof2dot` para visualización.

### Requisitos previos

Asegúrese de tener las herramientas necesarias instaladas globalmente o en su entorno virtual:

```bash
# Required Python libraries for profiling
pip install yappi gprof2dot

# Required system library for visualization
# Linux: sudo apt install graphviz 
```

### Paso 1: Modificar el servicio de creación de perfiles

El script `aura_engine.py` debe modificarse para iniciar manualmente el generador de perfiles `yappi` y guardar correctamente los datos del perfil en caso de interrupción (`Ctrl+C`).

**Cambios clave en `aura_engine.py`:**

1. **Importaciones y controlador de señales:** Importe `yappi` y defina la función `generate_graph_on_interrupt` (como se implementó anteriormente) para llamar a `yappi.stop()` y `stats.save(...)`.
2. **Iniciar/Detener:** Agregue `yappi.start()` y `signal.signal(signal.SIGINT, ...)` dentro del bloque `if __name__ == "__main__":` para ajustar la ejecución de `main(...)`.

### Paso 2: ejecutar el servicio y recopilar datos

Ejecute el script modificado directamente y permita que procese los datos durante un tiempo suficiente (por ejemplo, de 10 a 20 segundos) para garantizar que se llamen a todas las funciones principales, incluidas las de subprocesos (como la corrección de LanguageTool).

```bash
# Execute the service directly (do NOT use the pycallgraph wrapper)
python3 aura_engine.py
```

Presione **Ctrl+C** una vez para activar el controlador de señales. Esto detendrá el generador de perfiles y guardará los datos sin procesar en:

`\mathbf{yappi\_profile\_data.prof`

### Paso 3: Generar y filtrar el gráfico visual

Usamos `gprof2dot` para convertir los datos sin procesar de `pstats` al formato SVG. Dado que es posible que nuestro entorno específico no admita opciones de filtrado avanzadas como `--include` y `--threshold`, utilizamos el filtro básico **`--strip`** para limpiar la información de ruta y reducir el desorden interno del sistema.

**Ejecute el comando de visualización:**

```bash
python3 -m gprof2dot -f pstats yappi_profile_data.prof --strip | dot -Tsvg -o yappi_call_graph_stripped.svg
```

### Paso 4: Documentación (Recorte manual)

El archivo resultante `yappi_call_graph_stripped.svg` (o `.png`) será grande, pero contiene con precisión el flujo de ejecución completo, incluidos todos los subprocesos.

Para fines de documentación, **recorte manualmente la imagen** para centrarse en la lógica central (los 10 a 20 nodos centrales y sus conexiones) para crear un gráfico de llamadas enfocado y legible para la documentación del repositorio.

### Archivar

El archivo de configuración modificado y la visualización final de Call Graph deben archivarse en el directorio fuente de la documentación:

| Artefacto | Ubicación |
| :--- | :--- |
| **Archivo de servicio modificado** | `doc_sources/profiling/aura_engine_profiling_base.py` |
| **Imagen recortada final** | `doc_sources/profiling/core_logic_call_graph.svg` |
| **Datos de perfil sin procesar** | *(Opcional: debe excluirse de la documentación final del repositorio)* |


![yappi_call_graph](../yappi_call_graph_stripped.svg_20251024_010459.png "yappi_call_graph_stripped.svg_20251024_010459.png")
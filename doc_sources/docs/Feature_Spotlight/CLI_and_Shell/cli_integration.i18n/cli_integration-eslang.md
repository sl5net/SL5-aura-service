# Característica destacada: integración de la interfaz de línea de comandos (CLI)

**Dedicado a mi muy importante amigo, Lub.**

La nueva interfaz de línea de comandos (CLI) basada en FastAPI proporciona una forma limpia y sincrónica de interactuar con nuestro servicio central de procesamiento de texto en ejecución desde cualquier shell local o remoto. Esta es una solución sólida diseñada para integrar la lógica central en entornos de shell.

---

## 1. Arquitectura y concepto de CLI síncrona

El servicio funciona con el servidor **Uvicorn/FastAPI** y utiliza un punto final personalizado (`/process_cli`) para entregar un resultado sincrónico (bloqueo) de un proceso en segundo plano inherentemente asincrónico basado en archivos.

### Estrategia de sondeo de esperar y leer

1. **Anulación de salida única:** La API crea un directorio temporal único para cada solicitud.
2. **Inicio del proceso:** Llama a `process_text_in_background` para ejecutar la lógica central en un hilo sin bloqueo, escribiendo el resultado en un archivo `tts_output_*.txt` dentro de esa carpeta única.
3. **Espera sincrónica:** La función API luego **bloquea** y sondea la carpeta única hasta que se crea el archivo de salida o se alcanza un tiempo de espera.
4. **Entrega de resultados:** La API lee el contenido del archivo, realiza la limpieza necesaria (eliminando el archivo y el directorio temporal) y devuelve el texto procesado final en el campo `result_text` de la respuesta JSON.

Esto garantiza que el cliente CLI solo reciba una respuesta *después* de que se complete el procesamiento del texto, lo que garantiza una experiencia de shell confiable.

## 2. Acceso remoto y mapeo de puertos de red

Para permitir el acceso desde clientes remotos como la terminal de Lub, se requirió la siguiente configuración de red, abordando la restricción común de disponibilidad limitada de puertos externos:

### Solución: Mapeo de puertos externos

Dado que el servicio se ejecuta internamente en el **Puerto 8000** y nuestro entorno de red limita el acceso externo a un rango de puertos específico (por ejemplo, `88__-8831`), implementamos **Mapeo de puertos** en el enrutador (Fritz!Box).

| Punto final | Protocolo | Puerto | Descripción |
| :--- | :--- | :--- | :--- |
| **Externo/Público** | TCP | `88__` (Ejemplo) | El puerto que debe utilizar el cliente (Lub). |
| **Interno/Local** | TCP | `8000` | El puerto en el que realmente escucha el servicio FastAPI (`--puerto 8000`). |

El enrutador traduce cualquier conexión entrante en el puerto externo (`88__`) al puerto interno (`8000`) de la máquina host, lo que hace que el servicio sea accesible globalmente sin cambiar la configuración del servidor central.

## 3. Uso del cliente CLI

El cliente debe estar configurado con la dirección IP pública, el puerto externo y la clave API correcta.

### Sintaxis del comando final

__CODE_BLOCK_0__
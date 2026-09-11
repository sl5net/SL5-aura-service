# Superposición de grabación (visualización en pantalla)

La superposición de grabación proporciona un indicador visual inmediato y multiplataforma del estado del dictado. Funciona independientemente de los demonios de notificación del escritorio y de los filtros "No molestar", mostrando el estado directamente en la pantalla principal.

## Ejemplos visuales

| Abajo izquierda (`bl`) | Arriba a la derecha (`tr`) |
| :---: | :---: |
| ![Top-Right Overlay 1](../images/recording_overlay_1.png) | ![Top-Right Overlay 2](../images/recording_2.png) |
| *Se combina con paneles oscuros y bandejas de sistema* | *Alto contraste sobre ventanas claras o complejas* |

## Estados

- **Grabación (`🔴`)**: un círculo rojo intenso con un contorno resaltado (`#e62222` en `#181818`) indica una grabación de audio activa.
- **Inactivo**:
- `oculto` (predeterminado): la ventana se retira por completo, liberando espacio en el escritorio para la interacción normal.
- `pentágono`: muestra una sutil insignia de pentágono geométrico (`⬟`) durante el modo inactivo.

## Configuración

La configuración se administra en `config/settings.py`:

```python
# Enable/disable on-screen overlay
RECORDING_OVERLAY_ENABLED = True

# Keep window always on top without borders
RECORDING_OVERLAY_TOPMOST = True

# Placement: "tr" (top-right) or "bl" (bottom-left)
RECORDING_OVERLAY_POSITION = "tr"

# Inactivity mode: "hidden" or "pentagon"
RECORDING_OVERLAY_IDLE_MODE = "hidden"

# Window dimension in pixels
RECORDING_OVERLAY_SIZE = 36
```

## Arquitectura

- Construido utilizando la biblioteca estándar de Python (`tkinter`), que no requiere dependencias C externas.
- Se ejecuta en un subproceso de demonio en segundo plano con manejo de eventos de cola seguro para subprocesos.
- Detecta dinámicamente el monitor principal en entornos de múltiples pantallas.

(s, 10.9.'26 14:41 jueves)
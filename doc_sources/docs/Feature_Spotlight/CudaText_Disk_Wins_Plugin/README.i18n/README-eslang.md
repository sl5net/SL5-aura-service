# Complemento CudaText: "Disk Wins" (Forzar recarga automática en cambios externos)

CudaText no tiene una opción incorporada que recargue silenciosamente un archivo en el momento en que
cambios en el disco: cada modo integrado "cambiado en el disco" todavía muestra algunos
tipo de mensaje (modal o sin modal) antes de recargar
(ver `ui_notif_confirm` en `default.json`, valores `0`-`4`, todos los cuales
preguntar). Este complemento cierra esa brecha: **el disco siempre gana**, sin aviso, nunca.

Archivado aquí para que nadie tenga que volver a derivar la API del complemento CudaText para esto
de nuevo. La fuente de la verdad para el complemento en sí se encuentra en
[`cuda_disk_wins/`](.././cuda_disk_wins/) en esta carpeta.

## Qué hace

- Sondea cada archivo abierto con nombre una vez por segundo (configurable a través de
`TIMER_INTERVAL` en `__init__.py`).
- Si el tiempo mtime de un archivo en el disco cambió, el complemento lo vuelve a leer y llama
`Editor.set_text_all()` — **sobrescribiendo cualquier cambio no guardado en el
pestaña del editor sin preguntar**.
- Borra el indicador "modificado" después (`PROP_MODIFIED = False`), por lo que el
La pestaña se ve limpia, como si nada se hubiera desviado.
- Best-effort restaura la posición del cursor y la línea superior visible después
recargar.
- Agrega dos comandos en `Complementos → Disk Wins`:
- `Activar/desactivar la recarga automática`
- `Verificar ahora` (verificación manual de una sola vez)

## ¿Por qué un complemento en lugar de una configuración?

El propio observador de archivos de CudaText (`ui_notif`) solo ofrece comportamientos de "preguntar":

| `ui_notif_confirm` | Comportamiento |
|---------------------|----------------------------------------------------|
| 0 | aviso sin modal, siempre |
| 1 | mensaje sin modal, si el editor se modificó o Deshacer no vaciar |
| 2 | mensaje sin modal, si se modifica el editor |
| 3 | aviso modal, siempre |
| 4 | mensaje modal, si se modificó el editor |

No hay ningún valor que signifique "recargar automáticamente, sin aviso, continuar".
De ahí este pequeño complemento, que ejecuta su propio ciclo de sondeo y recarga
directamente a través de la API de Python.

## Instalación

```bash
mkdir -p ~/.config/cudatext/py
cp -r cuda_disk_wins ~/.config/cudatext/py/
```

Reinicie CudaText.

**Importante:** también deshabilite el cuadro de diálogo de notificación de cambios propio de CudaText para que
no pelea con el complemento. En
`~/.config/cudatext/settings/user.json`:

```json
{
    "ui_notif": false
}
```

(Equivalente a `Opciones → Configuración – configuración de usuario` en la interfaz de usuario). Reiniciar
CudaText nuevamente después de este cambio.

## Advertencias

- Esto es intencionalmente destructivo: las ediciones del editor no guardadas se descartan
silenciosamente en el momento en que el archivo cambia externamente. eso es todo
punto del complemento: no lo instale si a veces desea conservar
ediciones locales sobre cambios externos.
- Sólo reacciona a cambios en el tiempo m del archivo; escribiendo en el propio editor
no activa una recarga (sin bucle de retroalimentación).
- Si el archivo se elimina externamente, el complemento no hace nada hasta que
reaparece (sin fallas, sin intentos repetidos de recarga).
- La codificación se lee mediante `PROP_ENC` y se asigna al códec Python más cercano;
extienda `ENC_MAP` en `__init__.py` si aún no usa una codificación
listado.

## Origen

Creado para "preferir siempre los cambios en el sistema de archivos en lugar del editor no guardado"
buffers, sin requisito de confirmación" discutido al configurar CudaText
a través de `yay -S cudatext-qt6-bin python` en Arch.
> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../matrix_threema_relay.md).*

# Element ↔ Threema Beta GUI Relay

Un pequeño demonio que refleja mensajes entre **Element Desktop** (Matrix) y
**Threema Beta** (el cliente de escritorio Threema) en Linux/X11 conduciendo ambos
ventanas como lo haría un usuario: atajos de teclado, el portapapeles y unos cuantos clics del ratón.

Sin API, sin tokens, sin bibliotecas adicionales de Python. Solo herramientas de línea de comandos estándar de X11.

## Qué hace

| Dirección | Qué sucede |
|---|---|
| **Element → Threema** | El último mensaje *que tú* escribiste en Element se lee y, si es nuevo, se pega en Threema Beta y se envía. |
| **Threema → Element** | El último mensaje *entrante* del chat abierto de Threema se copia mediante su menú contextual y, si es nuevo, se pega en Element y se envía. |

Uso típico: dictar o escribir en una sala de Element (por ejemplo, con Aura's)
reconocimiento de voz a texto) y que el texto llegue a un chat de Threema, y ver el
Las respuestas de Threema aparecen en la misma sala de Element.

Ambas ventanas deben estar abiertas, iniciadas sesión y mostrando el chat/sala que deseas retransmitir.

## Loop protection

Un espejo ingenuo de dos vías rebotaría cada mensaje de ida y vuelta para siempre. El relé
evita esto con una historia de corta duración (`relay_history.py`):

1. Cada texto que el relé adelante se recuerda **antes** es enviado, por 180 segundos.
2. Si un texto aparece en el otro lado que está en esta historia, es nuestro propio
   eco: está marcado como visto pero **no** reenviado de nuevo.
3. Un texto nuevo *y* desconocido es un mensaje genuino y se envía.

Los textos se comparan con el espacio blanco colapsado, por lo que las diferencias de ruptura de línea
copy/paste no derrota al guardia. Porque las entradas mueren, puedes enviar las entradas
El mismo texto (por ejemplo "ok") de nuevo después de que la ventana haya pasado.

En el inicio del último mensaje actual de cada lado se lee como **baseline** y es
*no* reenviado. Sólo se transmiten mensajes que llegan después del inicio.

## Requisitos

- Linux con **X11** (`echo $XDG_SESSION_TYPE` debe imprimir `x11`). Wayland no es compatible.
- `xdotool`, `xclip`, `wmctrl` y `xset` (opcional, usado para desactivar el protector de pantalla)
- Element Desktop (clase WM `element.Element`)
- Threema Beta (clase WM `threema beta.Threema Beta`, p. ej., el Flatpak
  `ch.threema.threema-desktop`)
- Python 3 con el virtualenv del proyecto
- `zsh` para el script de calibración única

## Setup: one-time calibration

Threema Beta dibuja su propio menú contextual que no puede ser operado con el teclado,
así el relé hace clic en "Copy Message" con el ratón en posiciones relativas al
Ventana de tres. Medirlos una vez:

```zsh
scripts/py/func/threema/threema-relay.zsh calibrate
```

El script pide tres posiciones de ratón, cada una con una cuenta regresiva (no toque el
Teclado, no muevas ni redimensionen la ventana:

1. **Clic derecho** el último mensaje entrante* (una burbuja en el lado izquierdo) y dejar
   El menú abierto.
2. Mueve el ratón, sin hacer clic, en **"Copy Message"**.
3. Mueva el ratón sobre el campo de entrada **mensaje**.

El resultado se almacena en `~/.config/threema-relay.conf`:

TENER Llavero TENIDO Significado
|---|---|
TEN `FX` TENIDO Posición de clic horizontal como una fracción de la anchura de la ventana
TEN `BOTTOM` TENIDO Click position, pixels above the window's bottom edge TEN
TEN `DX`, `DY` TENIDO Sin conexión desde el punto de clic hasta "Paquete de compra"
TEN `INPUT_FX`, `INPUT_BOTTOM` ANTERIOR Posición del campo de entrada de mensajes
Silencio `DELAY_MENU`, `DELAY_COPY` TENIDO Esperas opcionales en segundos (defaults 0.30 / 0.20)

Verifique la calibración con un mensaje entrante nuevo como el último en el chat:

```zsh
scripts/py/func/threema/threema-relay.zsh test
```

Imprime el texto copiado sin reenviarlo. La calibración depende de la ventana
geometría: si cambias mucho el tamaño de la ventana de Threema, calibra de nuevo.

## Uso

Desde la raíz del repositorio:

```zsh
PYTHONPATH=. .venv/bin/python3 scripts/py/func/threema/matrix_threema_relay.py
```

Opciones:

| Opción | Efecto |
|---|---|
| `--poll SECONDS` | Intervalo de sondeo (predeterminado `2.0`) |
| `--no-threema-to-element` | Solo retransmitir elemento → Threema |
| `--no-element-enter` | Pega mensajes de Threema en el campo de entrada de Element, pero **no** los envíes (modo de prueba seguro) |

Detente con `Ctrl+C`.

Ejecución recomendada por primera vez: usa `--no-element-enter`, envíate un mensaje en Threema
y verifica que aparezca en el campo de entrada de Element. Luego ejecuta sin la opción.

Ejemplo de registro:

```
[INFO] Initial Element baseline: 'Test'
[INFO] Initial Threema baseline: 'kaa'
[INFO] New Element message -> Threema: 'Hallo Welt'
[INFO] New Threema message -> Element: 'müsli'
[INFO] Element shows our own relayed text - not sending back.
```

## How it works

```
every poll interval
├─ Element:  focus window (wmctrl) → Up, Ctrl+A, Ctrl+C, Escape (xdotool) → read clipboard (xclip)
│            new + unknown  → paste into Threema + Return, remember text
│            new + known    → echo, ignore
└─ Threema:  focus window → right-click last incoming bubble → click "Copy Message"
                          → click input field (restores focus) → read clipboard
             new + unknown  → paste into Element (+ Return), remember text
             new + known    → echo, ignore
```

- *Up* en el compositor de Element edita su último mensaje; *Ctrl+A / Ctrl+C* copias
  y *Escape* deja el modo de edición. Esta es la razón por la que sólo **su propio** último elemento
  El mensaje se transmite a Threema.
- Para Threema una cadena **Sentinel** se coloca en el portapapeles primero. Si sigue siendo
  allí después, nada fue copiado (por ejemplo porque su propio mensaje es el
  El último y el clic no golpeó burbuja) y el intento es ignorado.

## Archivos

Silencio Silencio .
|---|---|
TEN `matrix_threema_relay.py` TENIDO El bucle principal, CLI, la lógica de la decisión (`classify_candidate`)
Silencio `read_last_element_message.py`
Silencio `send_to_threema_window.py` Silencio Pastes texto en Threema Beta
Silencio `read_last_threema_message.py` TENIDO Lee el último mensaje entrante de Threema, carga la calibración ANTE
Silencio `send_to_element_window.py`
Silencio `relay_history.py`
TEN `threema-relay.zsh` TENIDO Calibración y herramienta de prueba manual (`calibrate`, `test`)
Silencio `test_threema_relay.py` Exámenes de la unidad (no se requiere X11)

Ejecute las pruebas con:

```zsh
PYTHONPATH=. .venv/bin/python3 -m unittest scripts.py.func.threema.test_threema_relay
```

## Limitaciones

- **El relé utiliza el enfoque del ratón y del teclado. . Durante cada encuesta el Threema y
  Element Windows se centra y el ratón salta brevemente (se restaura). No
  escriba mientras una encuesta se ejecuta, o utilice un `--poll` más largo.
- Sobrescribe el portapapeles en cada encuesta.
- **Own message last in Threema:** cuando tu propio mensaje es el último en la Threema
  Chat, una respuesta que llegó justo antes de que no se vea.
- **Sólo el último mensaje** es leído por encuesta. Si varios mensajes llegan dentro de uno
  intervalo, sólo el más nuevo es retransmitido.
- Sólo texto. Imágenes, archivos, reacciones y ediciones no se transmiten.
- Un par de charlas. Se utiliza cualquier chat/room abierto en cada ventana.
- **Un borrador en el campo de entrada de Element** se combinará con el siguiente pegado
  Mensaje.
- **X11 sólo.** Wayland bloquea los cambios de entrada y de enfoque de ventana.
- El relé desactiva el salvapantallas X11 y DPMS en el inicio (`xset s off -dpms`);
  Se mantienen alejados hasta que vuelvas a habilitarlos o inicies sesión de nuevo.

## Solución de problemas

Silencioso tóxico Causa o solución ideal
|---|---|
Silencio `Threema window ... not found` Silencio Revisa `xdotool search --class "Threema Beta"` y `xprop WM_CLASS` (haga clic en la ventana).
← `Nothing copied` / no Threema → Element ← Re-run `calibrate`; ejecutar `test` con un mensaje entrante como el último. Aumentar `DELAY_MENU`/`DELAY_COPY` en el config en una máquina lenta.
Silencio Texto llega a Threema pero no se envía ¦ Input field not focused; ver `INPUT_FX`/`INPUT_BOTTOM` de la calibración.
Silencio El texto de Threema aparece en Element pero no es enviado El relé se inició con `--no-element-enter`.
← Números decimales como `0,9353` en el config tención Escrito por una versión de script anterior bajo un local alemán. El código Python los acepta; Calibrando de nuevo con el script actual escribe puntos. Silencio

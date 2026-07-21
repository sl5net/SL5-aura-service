# Notas: problema de clave atascada en type_watcher.sh (dotool)

## Síntoma
Poco después del reinicio de Manjaro, en el primer dictado después de `sl5net Aura`
iniciado automáticamente, un solo carácter se atascó y se repitió infinitamente
(por ejemplo, "n" repetida cientos de veces) hasta que se presionó la tecla de activación
nuevamente como una solución manual.

Observado una vez el 21/07/2026 ~ 09:44 (martes), texto: "Die Ideen niemand wird
mehr gefragt, aber es soll trotzdem genauso sein wie...nnnnn...".

## Cronología (comprobada mediante registros)
- 09:29:17 - Se inició `type_watcher.sh` (log/type_watcher.log)
- 09:41:56 - dictado "ideen niemand wird mehr gefragt..." recibido
(log/aura_engine.log, hilo-13/14)
- 09:42:03 - procesamiento de texto finalizado (`mejor puntuación difusa: 0%`),
presumiblemente escrito en un archivo `tts_output_*.txt`
- ~09:42:04-09:42:09 - `type_watcher.sh` falló (inferido: perro guardián)
El intervalo de sondeo es de 5 segundos, ver más abajo)
- 09:42:09 - registro de vigilancia (log/type_watcher_keep_alive.log):
"WATCHDOG: 'type_watcher.sh' no se está ejecutando. Iniciándolo ahora".
- 09:42:13 - `type_watcher.sh` reiniciado (log/type_watcher.log)
- No se encontró ninguna entrada `contenido escrito de...` para el archivo "ideen niemand..."
encontrado alguna vez en log/type_watcher.log: la escritura de ese específico
El texto nunca se completó/registró.

## Estado de la causa raíz
- CONFIRMADO: `type_watcher.sh` falló entre el texto final
procesando (09:42:03) y el perro guardián detecta que no se está ejecutando
(09:42:09). El perro guardián (`type_watcher_keep_alive.sh`) solo mata
y se reinicia al cambiar la marca de tiempo del archivo de configuración (`ts1`/`ts2`,
confirmado sin cambios en este incidente) o se reinicia automáticamente cuando
`pgrep -f "type_watcher.sh"` no encuentra ningún proceso, es decir, esto fue muy
Probablemente se trate de un autochoque, no de una muerte externa.
- HIPÓTESIS (no comprobada): `set -euo pipefail` (type_watcher.sh línea 5)
provocó que el script saliera con algún código de salida distinto de cero dentro del
tubería, posiblemente mientras que la tubería `dotool` de `do_type()` (línea 125) estaba
centro de la corriente. Si el proceso bash muere mientras se transmite a `dotool`,
el demonio `dotoold` separado (que sigue ejecutándose de forma independiente)
se puede dejar con una llave en un estado "abajo" sin que coincida "arriba" nunca
recibido, lo que provoca la repetición de clave a nivel del sistema operativo.
- AÚN NO PROBADO: el comando/línea exacto que causó el valor distinto de cero
salga en `set -euo pipefail`. No hay ruido del accidentado.
Se capturó el proceso `type_watcher.sh` (el organismo de control lo llama
sin ninguna redirección de salida, `type_watcher_keep_alive.sh` línea 79).
- La clave afectada NO siempre fue el mismo carácter en diferentes
apariciones de este error (informe del usuario: anteriormente también "t").

## Ya investigado y descartado
- No es un reinicio provocado por un cambio de configuración (confirmado por el usuario: config
sin cambios, y la verificación `ts1_old != ts1_new` registraría "Configuración cambiada").
- No es un inicio automático duplicado de `type_watcher.sh` que se superpone con
(sólo una entrada "Hola desde Watcher" precedió al bloqueo).
- La llamada `dotool type` de `do_type()` es atómica por invocación y no
no envía la clave por carácter hacia abajo/arriba, descartando `type_watcher.sh`
lógica de aplicación como fuente directa de una clave atascada en condiciones normales
funcionamiento (sin colisiones).

## Solución ya aplicada (respaldo/mitigación, no solución de causa raíz)
Tanto `cleanup()` en `type_watcher.sh` como `do_cleanup()` en
`keep-keys-up.sh` anteriormente lanzado solo teclas modificadoras (shift, ctrl,
alt, etc.) a través de `dotool`/`xdotool`. Esto no hizo nada por un regular estancado.
clave (letra, número, puntuación).

- `type_watcher.sh`: `cleanup()` ahora envía `dotool key <nombre>:up` para
todas las letras, números y teclas comunes de puntuación/espacios en blanco, no
solo modificadores.
- `type_watcher.sh`: `INPUT_METHOD` ahora se exporta después de la detección, por lo que
otros scripts pueden ver qué backend (`dotool` / `xdotool`) está activo.
- `keep-keys-up.sh`: `do_cleanup()` obtuvo una rama `dotool` (usando el
verbo `keyup`, sin demora por tecla, para rendimiento) activo solo cuando
`INPUT_METHOD=dotool`, reflejando la llamada existente `xdotool keyup`
para modificadores.

Esto no soluciona el fallo subyacente de `type_watcher.sh`; es solo
garantiza que si el fallo vuelve a ocurrir, se liberará una tecla atascada
el siguiente paso de limpieza (`--cleanup`, llamado después de cada `do_type()`, y
a través del controlador `trap cleanup EXIT INT TERM`) en lugar de repetir
indefinidamente hasta que se presione una tecla de activación manual.

## Próximos pasos si esto vuelve a suceder
- Captura stderr de `type_watcher.sh` en caso de falla. Actualmente
La línea 79 de `type_watcher_keep_alive.sh` lo llama sin redirección, por lo que
cualquier mensaje de error de bash se pierde (va al propio sistema de vigilancia)
stdout/stderr, dondequiera que lo indique el mecanismo de inicio automático).
- Considere un modo de depuración, p.e. `bash -x scripts/type_watcher/type_watcher.sh
2 >> log/type_watcher_debug.log`, alternado a través de una var env como
`TYPE_WATCHER_DEBUG=1`, para capturar la línea fallida exacta en la siguiente
chocar.
- Verifique qué inicia `type_watcher_keep_alive.sh` en el arranque de Manjaro
(archivo de inicio automático `.desktop`, unidad systemd `--user`, etc.) y si
su stdout/stderr se captura en cualquier lugar.
- Si es reproducible, pruebe si el accidente se correlaciona con
`dotoold` todavía se inicializa inmediatamente después del arranque (consulte `sleep 0.1`
en type_watcher.sh línea 8 y el bucle de inicio `dotoold` en las líneas
102-110).
# Abschlussbericht: SL5 Aura – Prueba de activación de extremo a extremo

**Dato:** 2026-03-15  
**Fecha:** `scripts/py/func/checks/test_trigger_end_to_end.py`

---

## 1. El plan

Cada una de las pruebas de extremo a extremo del problema mencionado es:
**Bei manchen Aufnahmen fehlt das letzte Wort im Output.**

La prueba se resuelve:
1. Una fecha WAV con micrófonos virtuosos incorporados
2. Aura per `touch /tmp/sl5_record.trigger` starten — genau wie im echten Betrieb
3. Mit zweitem Trigger stoppen
4. Den Output mit dem YouTube-Transcript vergleichen
5. Feststellen ob ein Wort am Ende fehlt

---

## 2. Fue erreicht wurde ✅

- Aura reagiert auf den Trigger korrekt
- LT läuft und ist erreichbar (`http://127.0.0.1:8082`)
- `_wait_for_output()` encuentra la fecha `tts_output_*.txt`
- `_fetch_yt_transcript_segment()` desde el texto de referencia corregido
- El banco de pruebas básico es sólido y funcionalmente adaptado

---

## 3. El único problema 🔴

### Problema de Kern: `manage_audio_routing` überschreibt alles

Beim Session-Start ruft Aura pasante auf:
```python
manage_audio_routing(SYSTEM_DEFAULT)
```

Esta función también puede ser la primera:
```python
subprocess.run(["pactl", "unload-module", "module-loopback"], capture_output=True)
subprocess.run(["pactl", "unload-module", "module-null-sink"], capture_output=True)
```

**Sie löscht jeden Sink den wir vorher erstellt haben.**

Asegúrese de que no haya ningún fregadero bien `mode == 'SYSTEM_DEFAULT'` (no `MIC_AND_DESKTOP`).

### Versuchte Lösungen

| Versuch | Problema |
|---|---|
| Fuente virtual PulseAudio escrita | PipeWire ignoró `módulo-fuente-virtual` |
| `settings_local.py` en `MIC_AND_DESKTOP` configurado | Datei wurde mit mehrfachen Einträgen korrumppiert |
| Bloqueo de anulación marcado y cierre final | Aura lädt Configuración nicht schnell genug neu bevor Trigger kommt |
| `_create_mic_and_desktop_sink()` directamente en Prueba | Wid von `manage_audio_routing` en el inicio de sesión gelöscht |
| `pw-bucle invertido` | Erscheint als Source aber Aura hört nicht darauf |

### Warum `settings_local.py` Anular no funciona

`dynamic_settings.py` vigila la fecha y la lleva después, con un intervalo. Der Trigger kommt zu schnell nach dem Schreiben. Aura inicia la sesión ahora con el otro Wert `SYSTEM_DEFAULT`.

Además: cuando se activa Aura `MIC_AND_DESKTOP`, el fregadero comienza en **nächsten** Session-Start — nicht sofort.

---

## 4. Mögliche Lösungswege

### Opción A — Largo tiempo después de la configuración
```python
_set_audio_input_device("MIC_AND_DESKTOP")
time.sleep(5.0)   # statt 1.5s — mehr Zeit für dynamic_settings reload
TRIGGER_FILE.touch()
```
Riesgo: Nicht zuverlässig, timing-abhängig.

### Opción B — Aura neu starten nach Settings-Änderung
```python
_set_audio_input_device("MIC_AND_DESKTOP")
subprocess.run(["./scripts/restart_venv_and_run-server.sh"])
time.sleep(60)   # warten bis LT bereit
TRIGGER_FILE.touch()
```
Nachteil: Prueba dauert über 1 minuto. Aber zuverlässig.

### Opción C — `manage_audio_routing` directamente en la prueba
```python
from scripts.py.func.manage_audio_routing import manage_audio_routing
manage_audio_routing("MIC_AND_DESKTOP", logger=null_logger)
```
Luego existe el fregadero antes del activador, y `manage_audio_routing` en el inicio de sesión activado `is_mic_and_desktop_sink_active() == True` y sobre la configuración.

Das ist wahrscheinlich die **sauberste Lösung**.

### Opción D — `process_text_in_background` activado directamente (sin disparador)
Como en `test_youtube_audio_regression.py`: salida directa en el Pipeline, sin el mecanismo de activación. Dann testet man die Pipeline aber nicht das Abschneiden des letzten Wortes.

### Opción E — Aura con `run_mode_override=TEST` iniciada
Falls Aura es un modo de prueba que supera el enrutamiento de audio.

---

## 5. Empfehlung

**Opción C** para probar — una prueba de importación realizada:

```bash
python3 -c "from scripts.py.func.manage_audio_routing import manage_audio_routing; print('OK')"
```

Cuando funciona:
```python
from scripts.py.func.manage_audio_routing import manage_audio_routing

manage_audio_routing("MIC_AND_DESKTOP", logger=null_logger)
time.sleep(0.5)
TRIGGER_FILE.touch()
```

Entonces activa Aura en Session-Start `is_mic_and_desktop_sink_active() == True` y finalmente el Sink en Ruhe.

---

## 6. Fue esta prueba langfristig trajo

Sobald er läuft, kann man:
- `SPEECH_PAUSE_TIMEOUT` Werte testen (1.0, 2.0, 4.0s) y sehen ob das letzte Wort abgeschnitten wird
- Optimización del parámetro `transcribe_audio_with_feedback.py`
- Regresiones realizadas cuando se activa el manejo de audio
- Beweisen dass ein Fix wirklich hilft

---

---

# Informe final: SL5 Aura: prueba de activación de un extremo a otro

**Fecha:** 2026-03-15  
**Archivo:** `scripts/py/func/checks/test_trigger_end_to_end.py`

---

## 1. El plan

Una prueba real de extremo a extremo para investigar el problema conocido:
**En algunas grabaciones, la última palabra se corta en la salida.**

La prueba debe:
1. Alimente un archivo WAV como micrófono virtual
2. Inicie Aura mediante `touch /tmp/sl5_record.trigger`, exactamente como el uso real
3. Detente con un segundo disparador
4. Compare el resultado con la transcripción de YouTube.
5. Detecta si falta una palabra al final

---

## 2. Lo que se logró ✅

- Aura responde al disparador correctamente.
- LT se está ejecutando y es accesible (`http://127.0.0.1:8082`)
- `_wait_for_output()` busca el archivo `tts_output_*.txt`
- `_fetch_yt_transcript_segment()` recupera el texto de referencia correctamente
- La estructura básica de la prueba es sólida y funciona conceptualmente.

---

## 3. El problema sin resolver 🔴

### Problema principal: `manage_audio_routing` sobrescribe todo

Al inicio de la sesión, Aura llama internamente:
```python
manage_audio_routing(SYSTEM_DEFAULT)
```

Esta función primero hace:
```python
subprocess.run(["pactl", "unload-module", "module-loopback"], capture_output=True)
subprocess.run(["pactl", "unload-module", "module-null-sink"], capture_output=True)
```

**Elimina cualquier receptor que hayamos creado previamente.**

Luego no crea ningún nuevo sumidero porque `mode == 'SYSTEM_DEFAULT'` (no `MIC_AND_DESKTOP`).

### Soluciones intentadas

| Intento | Problema |
|---|---|
| Crear fuente virtual PulseAudio | PipeWire ignora `módulo-virtual-fuente` |
| Establezca `settings_local.py` en `MIC_AND_DESKTOP` | El archivo estaba dañado con varias entradas |
| Escriba el bloque de anulación marcado al final del archivo | Aura no recarga la configuración lo suficientemente rápido antes de que se active el disparador |
| `_create_mic_and_desktop_sink()` directamente en prueba | Eliminado por `manage_audio_routing` al inicio de la sesión |
| `pw-bucle invertido` | Aparece como fuente pero Aura no la escucha |

---

## 4. Siguiente paso recomendado

Llame a `manage_audio_routing` directamente desde la prueba antes del disparador:

```python
from scripts.py.func.manage_audio_routing import manage_audio_routing

manage_audio_routing("MIC_AND_DESKTOP", logger=null_logger)
time.sleep(0.5)
TRIGGER_FILE.touch()
```

Cuando Aura inicia la sesión, verifica `is_mic_and_desktop_sink_active()`; si es `True`, omite la configuración y deja el fregadero en paz. Esta es la solución más limpia.

---

## 5. Qué permitirá esta prueba a largo plazo

Una vez en ejecución:
- Pruebe los valores `SPEECH_PAUSE_TIMEOUT` (1.0, 2.0, 4.0s) y detecte el corte de palabras
- Optimizar los parámetros `transcribe_audio_with_feedback.py`
- Captar regresiones cuando cambia el manejo del audio.
- Demostrar que una solución realmente funciona
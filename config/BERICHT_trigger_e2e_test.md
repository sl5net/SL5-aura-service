# Abschlussbericht: SL5 Aura – Trigger End-to-End Test

**Datum:** 2026-03-15  
**Datei:** `scripts/py/func/checks/test_trigger_end_to_end.py`

---

## 1. Der Plan

Ein echter End-to-End Test der das bekannte Problem untersucht:
**Bei manchen Aufnahmen fehlt das letzte Wort im Output.**

Der Test sollte:
1. Eine WAV-Datei als virtuelles Mikrofon einspeisen
2. Aura per `touch /tmp/sl5_record.trigger` starten — genau wie im echten Betrieb
3. Mit zweitem Trigger stoppen
4. Den Output mit dem YouTube-Transcript vergleichen
5. Feststellen ob ein Wort am Ende fehlt

---

## 2. Was erreicht wurde ✅

- Aura reagiert auf den Trigger korrekt
- LT läuft und ist erreichbar (`http://127.0.0.1:8082`)
- `_wait_for_output()` findet die `tts_output_*.txt` Datei
- `_fetch_yt_transcript_segment()` holt den Referenz-Text korrekt
- Der grundlegende Testaufbau ist solide und funktioniert konzeptionell

---

## 3. Das ungelöste Problem 🔴

### Kern-Problem: `manage_audio_routing` überschreibt alles

Beim Session-Start ruft Aura intern auf:
```python
manage_audio_routing(SYSTEM_DEFAULT)
```

Diese Funktion macht als erstes:
```python
subprocess.run(["pactl", "unload-module", "module-loopback"], capture_output=True)
subprocess.run(["pactl", "unload-module", "module-null-sink"], capture_output=True)
```

**Sie löscht jeden Sink den wir vorher erstellt haben.**

Danach erstellt sie keinen neuen Sink weil `mode == 'SYSTEM_DEFAULT'` (nicht `MIC_AND_DESKTOP`).

### Versuchte Lösungen

| Versuch | Problem |
|---|---|
| PulseAudio Virtual Source erstellen | PipeWire ignoriert `module-virtual-source` |
| `settings_local.py` auf `MIC_AND_DESKTOP` setzen | Datei wurde mit mehrfachen Einträgen korrumpiert |
| Markierten Override-Block ans Ende schreiben | Aura lädt Settings nicht schnell genug neu bevor Trigger kommt |
| `_create_mic_and_desktop_sink()` direkt im Test | Wird von `manage_audio_routing` beim Session-Start gelöscht |
| `pw-loopback` | Erscheint als Source aber Aura hört nicht darauf |

### Warum `settings_local.py` Override nicht funktioniert

`dynamic_settings.py` überwacht die Datei und lädt sie nach — aber mit einem Intervall. Der Trigger kommt zu schnell nach dem Schreiben. Aura startet die Session noch mit dem alten Wert `SYSTEM_DEFAULT`.

Außerdem: selbst wenn Aura `MIC_AND_DESKTOP` lädt, erstellt es den Sink erst beim **nächsten** Session-Start — nicht sofort.

---

## 4. Mögliche Lösungswege

### Option A — Längeres Warten nach Settings-Änderung
```python
_set_audio_input_device("MIC_AND_DESKTOP")
time.sleep(5.0)   # statt 1.5s — mehr Zeit für dynamic_settings reload
TRIGGER_FILE.touch()
```
Risiko: Nicht zuverlässig, timing-abhängig.

### Option B — Aura neu starten nach Settings-Änderung
```python
_set_audio_input_device("MIC_AND_DESKTOP")
subprocess.run(["./scripts/restart_venv_and_run-server.sh"])
time.sleep(60)   # warten bis LT bereit
TRIGGER_FILE.touch()
```
Nachteil: Test dauert über 1 Minute. Aber zuverlässig.

### Option C — `manage_audio_routing` direkt im Test aufrufen
```python
from scripts.py.func.manage_audio_routing import manage_audio_routing
manage_audio_routing("MIC_AND_DESKTOP", logger=null_logger)
```
Dann existiert der Sink bevor der Trigger kommt — und `manage_audio_routing` beim Session-Start erkennt `is_mic_and_desktop_sink_active() == True` und überspringt das Setup.

Das ist wahrscheinlich die **sauberste Lösung**.

### Option D — `process_text_in_background` direkt aufrufen (kein Trigger)
Wie in `test_youtube_audio_regression.py` — Vosk-Output direkt in die Pipeline übergeben, ohne den echten Trigger-Mechanismus. Dann testet man die Pipeline aber nicht das Abschneiden des letzten Wortes.

### Option E — Aura mit `run_mode_override=TEST` starten
Falls Aura einen Test-Modus hat der das Audio-Routing überspringt.

---

## 5. Empfehlung

**Option C** zuerst probieren — einen Import-Test machen:

```bash
python3 -c "from scripts.py.func.manage_audio_routing import manage_audio_routing; print('OK')"
```

Wenn das funktioniert:
```python
from scripts.py.func.manage_audio_routing import manage_audio_routing

manage_audio_routing("MIC_AND_DESKTOP", logger=null_logger)
time.sleep(0.5)
TRIGGER_FILE.touch()
```

Dann erkennt Aura beim Session-Start `is_mic_and_desktop_sink_active() == True` und lässt den Sink in Ruhe.

---

## 6. Was dieser Test langfristig bringt

Sobald er läuft, kann man:
- `SPEECH_PAUSE_TIMEOUT` Werte testen (1.0, 2.0, 4.0s) und sehen ob das letzte Wort abgeschnitten wird
- `transcribe_audio_with_feedback.py` Parameter optimieren
- Regressionen erkennen wenn sich das Audio-Handling ändert
- Beweisen dass ein Fix wirklich hilft

---

---

# Final Report: SL5 Aura – Trigger End-to-End Test

**Date:** 2026-03-15  
**File:** `scripts/py/func/checks/test_trigger_end_to_end.py`

---

## 1. The Plan

A real end-to-end test to investigate the known problem:
**In some recordings, the last word is cut off in the output.**

The test should:
1. Feed a WAV file as a virtual microphone
2. Start Aura via `touch /tmp/sl5_record.trigger` — exactly like real usage
3. Stop with a second trigger
4. Compare output with the YouTube transcript
5. Detect if a word is missing at the end

---

## 2. What was achieved ✅

- Aura responds to the trigger correctly
- LT is running and reachable (`http://127.0.0.1:8082`)
- `_wait_for_output()` finds the `tts_output_*.txt` file
- `_fetch_yt_transcript_segment()` fetches the reference text correctly
- The basic test structure is solid and works conceptually

---

## 3. The Unsolved Problem 🔴

### Core problem: `manage_audio_routing` overwrites everything

At session start, Aura internally calls:
```python
manage_audio_routing(SYSTEM_DEFAULT)
```

This function first does:
```python
subprocess.run(["pactl", "unload-module", "module-loopback"], capture_output=True)
subprocess.run(["pactl", "unload-module", "module-null-sink"], capture_output=True)
```

**It deletes any sink we created beforehand.**

Then it creates no new sink because `mode == 'SYSTEM_DEFAULT'` (not `MIC_AND_DESKTOP`).

### Attempted solutions

| Attempt | Problem |
|---|---|
| Create PulseAudio Virtual Source | PipeWire ignores `module-virtual-source` |
| Set `settings_local.py` to `MIC_AND_DESKTOP` | File was corrupted with multiple entries |
| Write marked override block to end of file | Aura doesn't reload settings fast enough before trigger fires |
| `_create_mic_and_desktop_sink()` directly in test | Deleted by `manage_audio_routing` at session start |
| `pw-loopback` | Appears as source but Aura doesn't listen to it |

---

## 4. Recommended Next Step

Call `manage_audio_routing` directly from the test before the trigger:

```python
from scripts.py.func.manage_audio_routing import manage_audio_routing

manage_audio_routing("MIC_AND_DESKTOP", logger=null_logger)
time.sleep(0.5)
TRIGGER_FILE.touch()
```

When Aura starts the session it checks `is_mic_and_desktop_sink_active()` — if `True`, it skips the setup and leaves the sink alone. This is the cleanest solution.

---

## 5. What this test will enable long-term

Once running:
- Test `SPEECH_PAUSE_TIMEOUT` values (1.0, 2.0, 4.0s) and detect word cutoff
- Optimize `transcribe_audio_with_feedback.py` parameters
- Catch regressions when audio handling changes
- Prove that a fix actually works

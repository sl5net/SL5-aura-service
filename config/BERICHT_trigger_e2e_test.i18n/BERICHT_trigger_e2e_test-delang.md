# Abschlussbericht: SL5 Aura – End-to-End-Test auslösen

**Datum:** 2026-03-15  
**Datei:** `scripts/py/func/checks/test_trigger_end_to_end.py`

---

## 1. Der Plan

Ein echter End-to-End-Test der das bekannte Problem untersucht:
**Bei manchen Aufnahmen fehlt das letzte Wort im Output.**

Der Test sollte:
1. Eine WAV-Datei als virtuelles Mikrofon einspeisen
2. Aura per `touch /tmp/sl5_record.trigger` starten – genau wie im echten Betrieb
3. Mit zweitem Trigger stoppen
4. Den Output mit dem YouTube-Transcript vergleichen
5. Feststellen ob ein Wort am Ende fehlt

---

## 2. Was erreicht wurde ✅

- Aura reagiert auf den Trigger korrekt
- LT läuft und ist erreichbar (`http://127.0.0.1:8082`)
- `_wait_for_output()` findet die `tts_output_*.txt` Datei
- `_fetch_yt_transcript_segment()` hält den Referenz-Text korrekt
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

**Sie löscht jedes Waschbecken, das wir zuvor erstellt haben.**

Danach erstellt sie keinen neuen Sink weil `mode == 'SYSTEM_DEFAULT'` (nicht `MIC_AND_DESKTOP`).

### Versuchte Lösungen

| Versuch | Problem |
|---|---|
| PulseAudio Virtual Source erstellen | PipeWire ignoriert „module-virtual-source“ |
| `settings_local.py` auf `MIC_AND_DESKTOP` setzen | Datei wurde mit mehrfachen Einträgen korrumpiert |
| Markierten Override-Block ans Ende schreiben | Aura lädt Settings nicht schnell genug neu, bevor Trigger kommt |
| `_create_mic_and_desktop_sink()` direkt im Test | Wird von `manage_audio_routing` beim Session-Start gelöscht |
| `pw-loopback` | Erscheint als Quelle aber Aura hört nicht darauf |

### Warum `settings_local.py` Override nicht funktioniert

`dynamic_settings.py` überwacht die Datei und lädt sie nach — aber mit einem Intervall. Der Trigger kommt zu schnell nach dem Schreiben. Aura startet die Sitzung noch mit dem alten Wert `SYSTEM_DEFAULT`.

Außerdem: selbst wenn Aura `MIC_AND_DESKTOP` lädt, erstellt es den Sink erst beim **nächsten** Session-Start — nicht sofort.

---

## 4. Mögliche Lösungswege

### Option A – Längeres Warten nach Settings-Änderung
```python
_set_audio_input_device("MIC_AND_DESKTOP")
time.sleep(5.0)   # statt 1.5s — mehr Zeit für dynamic_settings reload
TRIGGER_FILE.touch()
```
Risiko: Nicht zuverlässig, zeitabhängig.

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
Dann existiert der Sink bevor der Trigger kommt — und `manage_audio_routing` erkennt beim Session-Start `is_mic_and_desktop_sink_active() == True` und überspringt das Setup.

Das ist wahrscheinlich die **sauberste Lösung**.

### Option D — `process_text_in_background` direkt aufrufen (kein Trigger)
Wie in `test_youtube_audio_regression.py` — Vosk-Output direkt in die Pipeline übergeben, ohne den echten Trigger-Mechanismus. Dann testet man die Pipeline, aber nicht das Abschneiden des letzten Wortes.

### Option E – Aura mit `run_mode_override=TEST` starten
Falls Aura einen Test-Modus hat, der das Audio-Routing aktiviert hat.

---

## 5. Empfehlung

**Option C** zuerst ausprobieren — einen Import-Test machen:

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
- `SPEECH_PAUSE_TIMEOUT` testen Werte (1.0, 2.0, 4.0s) und sehen, ob das letzte Wort abgeschnitten wird
- `transcribe_audio_with_feedback.py` Parameter optimieren
- Regressionen erkennen, wenn sich das Audio-Handling ändert
- Beweise dafür, dass ein Fix wirklich hilft

---

---

# Abschlussbericht: SL5 Aura – End-to-End-Test auslösen

**Datum:** 15.03.2026  
**Datei:** `scripts/py/func/checks/test_trigger_end_to_end.py`

---

## 1. Der Plan

Ein echter End-to-End-Test zur Untersuchung des bekannten Problems:
**Bei manchen Aufnahmen wird das letzte Wort in der Ausgabe abgeschnitten.**

Der Test sollte:
1. Führen Sie eine WAV-Datei als virtuelles Mikrofon ein
2. Starten Sie Aura über „touch /tmp/sl5_record.trigger“ – genau wie bei der echten Verwendung
3. Stoppen Sie mit einem zweiten Auslöser
4. Vergleichen Sie die Ausgabe mit dem YouTube-Transkript
5. Erkennen Sie, ob am Ende ein Wort fehlt

---

## 2. Was wurde erreicht ✅

- Aura reagiert korrekt auf den Auslöser
- LT läuft und ist erreichbar (`http://127.0.0.1:8082`)
- „_wait_for_output()“ findet die Datei „tts_output_*.txt“.
- `_fetch_yt_transcript_segment()` ruft den Referenztext korrekt ab
- Der grundsätzliche Testaufbau ist solide und funktioniert konzeptionell

---

## 3. Das ungelöste Problem 🔴

### Kernproblem: „manage_audio_routing“ überschreibt alles

Zu Beginn der Sitzung ruft Aura intern auf:
```python
manage_audio_routing(SYSTEM_DEFAULT)
```

Diese Funktion führt zunächst Folgendes aus:
```python
subprocess.run(["pactl", "unload-module", "module-loopback"], capture_output=True)
subprocess.run(["pactl", "unload-module", "module-null-sink"], capture_output=True)
```

**Es löscht alle zuvor erstellten Senken.**

Dann wird keine neue Senke erstellt, weil „mode == ‚SYSTEM_DEFAULT‘“ (nicht „MIC_AND_DESKTOP“).

### Lösungsversuche

| Versuch | Problem |
|---|---|
| Erstellen Sie eine virtuelle PulseAudio-Quelle | PipeWire ignoriert „module-virtual-source“ |
| Setzen Sie „settings_local.py“ auf „MIC_AND_DESKTOP“ | Datei wurde mit mehreren Einträgen beschädigt |
| Markierten Override-Block an das Ende der Datei schreiben | Aura lädt die Einstellungen nicht schnell genug neu, bevor der Auslöser ausgelöst wird |
| `_create_mic_and_desktop_sink()` direkt im Test | Von „manage_audio_routing“ beim Sitzungsstart gelöscht |
| `pw-loopback` | Erscheint als Quelle, aber Aura hört sie nicht |

---

## 4. Empfohlener nächster Schritt

Rufen Sie „manage_audio_routing“ direkt aus dem Test vor dem Trigger auf:

```python
from scripts.py.func.manage_audio_routing import manage_audio_routing

manage_audio_routing("MIC_AND_DESKTOP", logger=null_logger)
time.sleep(0.5)
TRIGGER_FILE.touch()
```

Wenn Aura die Sitzung startet, prüft es „is_mic_and_desktop_sink_active()“ – wenn „True“, überspringt es die Einrichtung und lässt die Senke in Ruhe. Das ist die sauberste Lösung.

---

## 5. Was dieser Test langfristig ermöglichen wird

Einmal ausgeführt:
- Testen Sie die „SPEECH_PAUSE_TIMEOUT“-Werte (1,0, 2,0, 4,0 s) und erkennen Sie Wortunterbrechungen
- Optimieren Sie die Parameter „transcribe_audio_with_feedback.py“.
- Erfassen Sie Regressionen, wenn sich die Audioverarbeitung ändert
- Beweisen Sie, dass ein Fix tatsächlich funktioniert
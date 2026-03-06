# AUDIO_DIAGNOSTICS_EN.md

# Linux-Audiodiagnose für Aura


### 1. Geräte identifizieren
Listen Sie alle Audiogeräte auf, wie sie von der Python-Umgebung erkannt werden:
```bash
./.venv/bin/python3 -m sounddevice > /tmp/aura_devices.txt && kate /tmp/aura_devices.txt
```
* **Worauf Sie achten sollten:** Notieren Sie sich die **Indexnummer** und **Hardware-ID (hw:X,Y)** Ihres Mikrofons.

### 2. Wer nutzt die Hardware?
Wenn Sie die Fehlermeldung „Gerät ausgelastet“ oder „Zeitüberschreitung“ erhalten, überprüfen Sie, welcher Prozess (PID) derzeit die Audio-Hardware sperrt:
```bash
fuser -v /dev/snd/*
```
* **Tipp:** Wenn Sie „pipewire“ oder „wireplumber“ sehen, verwaltet der Soundserver das Gerät. Wenn Sie eine „python3“- oder „obs“-PID direkt auf einem PCM-Gerät sehen, blockieren diese möglicherweise andere.

### 3. Echtzeitüberwachung (PipeWire)
Wenn Ihr System PipeWire (Standard im modernen Manjaro) verwendet, ist dies das beste Tool für die Live-Diagnose:
```bash
pw-top
```
* **Worauf Sie achten sollten:** Überprüfen Sie die Spalte „ERR“ auf Aussetzer und stellen Sie sicher, dass Aura (16.000 Hz) und OBS (48.000 Hz) keine Resampling-Überlastung auf der CPU verursachen.

### 4. Überwachen von Audioereignissen
Sehen Sie sich Live-Updates an, wenn Mikrofone stummgeschaltet oder die Stummschaltung aufgehoben sind oder neue Streams erstellt werden:
```bash
pactl subscribe
```
* **Verwendung:** Führen Sie dies aus und starten Sie dann Aura. Wenn Sie viele „Entfernungs“-Ereignisse gleichzeitig sehen, stürzt ein Prozess ab oder wird abgelehnt.

### 5. Hardware-Bypass-Test
Testen Sie, ob Ihr Mikrofon auf reiner Hardwareebene funktioniert (unter Umgehung von PulseAudio/PipeWire). Dadurch werden 5 Sekunden Audio aufgezeichnet:
```bash
# Replace hw:1,0 with your device index
arecord -D hw:1,0 -f S16_LE -r 16000 -d 5 /tmp/test.wav && vlc /tmp/test.wav
```
* **Ergebnis:** Wenn dies funktioniert, Aura jedoch nicht, liegt das Problem in der Sound-Server-Konfiguration und nicht in der Hardware.

### 6. Notfall-Reset
Wenn das Audiosystem hängen bleibt:
```bash
systemctl --user restart pipewire wireplumber
# Or for older PulseAudio systems:
pulseaudio -k
```


**Hinweis einfacherer Workflow:**

`/tmp/diagnose.txt && kate /tmp/diagnose.txt` an den Befehl an. 🌵🚀
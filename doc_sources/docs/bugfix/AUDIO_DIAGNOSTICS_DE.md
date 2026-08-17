# Deutsche Version: `AUDIO_DIAGNOSTICS_DE.md`

# Linux Audio-Diagnose für Aura 

Beim gleichzeitigen Betrieb vom Aura Service können Audio-Konflikte auftreten (Timeouts, "Device Busy" oder Sample-Rate-Konflikte). Diese Befehle helfen bei der Fehlersuche.

### 1. Geräte identifizieren
Zeigt alle Audio-Geräte aus Sicht der Python-Umgebung an:
```bash
./.venv/bin/python3 -m sounddevice > /tmp/aura_devices.txt && kate /tmp/aura_devices.txt
```
*   **Ziel:** Notiere die **Index-Nummer** und die **Hardware-ID (hw:X,Y)** deines Mikrofons.

### 2. Wer belegt die Hardware?
Wenn Fehler wie "Device Busy" oder "Timeout" auftreten, prüfe, welcher Prozess (PID) die Hardware blockiert:
```bash
fuser -v /dev/snd/*
```
*   **Tipp:** Wenn `pipewire` oder `wireplumber` erscheint, verwaltet der Sound-Server das Gerät. Wenn eine `python3` oder `obs` PID direkt auf einem PCM-Gerät erscheint, blockieren diese evtl. den Zugriff für andere.

### 3. Echtzeit-Monitoring (PipeWire)
Für moderne Manjaro-Systeme mit PipeWire ist dies das wichtigste Tool:
```bash
pw-top
```
*   **Ziel:** Prüfe die Spalte `ERR` auf Fehler und stelle sicher, dass Aura (16000Hz) und OBS (48000Hz) keine CPU-Überlastung durch Resampling verursachen.

### 4. Überwachung von Audio-Events
Verfolge live, wenn Mikrofone stummgeschaltet werden oder neue Streams entstehen:
```bash
pactl subscribe
```
*   **Anwendung:** Starte dies und dann Aura. Wenn sofort viele `remove`-Events kommen, bricht ein Prozess ab oder wird vom System abgewiesen.

### 5. Hardware-Direkttest
Testet, ob das Mikrofon auf Hardware-Ebene funktioniert (umgeht PulseAudio/PipeWire). Nimmt 5 Sekunden auf:
```bash
# Ersetze hw:1,0 durch deinen Geräte-Index
arecord -D hw:1,0 -f S16_LE -r 16000 -d 5 /tmp/test.wav && vlc /tmp/test.wav
```
*   **Ergebnis:** Wenn dies funktioniert, Aura aber nicht, liegt das Problem in der Konfiguration des Sound-Servers, nicht an der Hardware.

### 6. Notfall-Reset
Falls das Audio-System komplett hängt:
```bash
systemctl --user restart pipewire wireplumber
# Oder für ältere PulseAudio-Systeme:
pulseaudio -k
```

---

**Tipp für den Workflow:** Um Ausgaben direkt in Kate zu betrachten, hänge einfach `> /tmp/diagnose.txt && kate /tmp/diagnose.txt` an den Befehl an. 🌵🚀

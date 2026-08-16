# Versión alemana: `AUDIO_DIAGNOSTICS_DE.md`

# Diagnóstico de audio de Linux para Aura

Beim gleichzeitigen Betrieb vom Aura Service können Audio-Konflikte auftreten (Tiempos de espera, "Dispositivo ocupado" o Sample-Rate-Konflikte). Diese Befehle helfen bei der Fehlersuche.

### 1. Identificadores del equipo
Zeigt alle Audio-Geräte aus Sicht der Python-Umgebung an:
```bash
./.venv/bin/python3 -m sounddevice > /tmp/aura_devices.txt && kate /tmp/aura_devices.txt
```
* **Ziel:** Notifica el **Número de índice** y el **ID de hardware (hw:X,Y)** deines Mikrofons.

### 2. ¿Estamos preocupados por el hardware?
Cuando se activan "Device Busy" o "Timeout", se bloquea el proceso welcher (PID) del hardware:
```bash
fuser -v /dev/snd/*
```
* **Consejo:** Cuando `pipewire` o `wireplumber` erscheint, verwaltet der Sound-Server das Gerät. Cuando un PID `python3` o `obs` se conecta directamente a un dispositivo PCM, estos se bloquean constantemente. den Zugriff para otros.

### 3. Monitoreo del Echtzeit (PipeWire)
Para el moderno sistema Manjaro con PipeWire, esta es la herramienta más adecuada:
```bash
pw-top
```
* **Ziel:** Pruebe el Spalte `ERR` auf Fehler y stelle sicher, dass Aura (16000Hz) y OBS (48000Hz) sin duración de CPU durante el resampling.

### 4. Supervisión de eventos de audio
Verfolge live, wenn Mikrofone stummgeschaltet werden oder nuevas Streams entstehen:
```bash
pactl subscribe
```
* **Anwendung:** Starte muere y dann Aura. Cuando haya algo de `remove`-Events kommen, bricht ein Prozess ab oder wird vom System abgewiesen.

### 5. Prueba directa de hardware
Pruebe el micrófono en la función Hardware (como PulseAudio/PipeWire). Durante menos de 5 segundos:
```bash
# Ersetze hw:1,0 durch deinen Geräte-Index
arecord -D hw:1,0 -f S16_LE -r 16000 -d 5 /tmp/test.wav && vlc /tmp/test.wav
```
* **Ergebnis:** Wenn dies funktioniert, Aura aber nicht, liegt das Problem in der Konfiguration des Sound-Servers, nicht an der Hardware.

### 6. Restablecimiento de no caída
Cae el sistema de audio completo colgado:
```bash
systemctl --user restart pipewire wireplumber
# Oder für ältere PulseAudio-Systeme:
pulseaudio -k
```

---

**Consejo para el flujo de trabajo:** Para utilizar directamente Kate zu betrachten, hänge einfach `> /tmp/diagnose.txt && kate /tmp/diagnose.txt` an den Befehl an. 🌵🚀
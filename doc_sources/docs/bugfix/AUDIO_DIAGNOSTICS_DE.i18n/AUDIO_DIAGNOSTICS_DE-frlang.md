# Version allemande : `AUDIO_DIAGNOSTICS_DE.md`

# Diagnostic audio Linux pour Aura

Beim gleichzeitigen Betrieb vom Aura Service können Audio-Konflikte auftreten (Timeouts, "Device Busy" ou Sample-Rate-Konflikte). Diese Befehle helfen bei der Fehlersuche.

### 1. Informations d'identification
Consultez tous les générateurs audio à la recherche de l'utilisation de Python :
```bash
./.venv/bin/python3 -m sounddevice > /tmp/aura_devices.txt && kate /tmp/aura_devices.txt
```
* **Ziel:** Notez le **Index-Nummer** et le **Hardware-ID (hw:X,Y)** deines Mikrofons.

### 2. Le matériel est-il requis ?
Lorsque vous indiquez « Device Busy » ou « Timeout » auftreten, prüfe, welcher Prozess (PID) die Hardware blockiert :
```bash
fuser -v /dev/snd/*
```
* **Conseil :** Lorsque `pipewire` ou `wireplumber` est utilisé, utilisez le Sound-Server de l'appareil. Lorsqu'un `python3` ou un `obs` PID directement sur un générateur PCM est utilisé, cela bloquera cet événement. den Zugriff für andere.

### 3. Surveillance réelle (PipeWire)
Pour le système Manjaro moderne avec PipeWire, cet outil est le meilleur :
```bash
pw-top
```
* **Ziel:** Prüfe die Spalte `ERR` auf Fehler et stelle sicher, ass Aura (16000Hz) et OBS (48000Hz) keine CPU-Uberlastung durch Resampling Verursachen.

### 4. Surveillance des événements audio
En direct, lorsque le microphone est connecté ou diffusé sur les nouveaux Streams :
```bash
pactl subscribe
```
* **Réponse :** Starte meurt et puis Aura. Lorsqu'il est facile de « supprimer » des événements, il suffit d'un processus sur ou d'un système abgewiesen.

### 5. Test direct du matériel
Testez le microphone sur la fonction Hardware-Ebene (avec PulseAudio/PipeWire). Pas plus de 5 secondes auf :
```bash
# Ersetze hw:1,0 durch deinen Geräte-Index
arecord -D hw:1,0 -f S16_LE -r 16000 -d 5 /tmp/test.wav && vlc /tmp/test.wav
```
* **Ergebnis:** Lorsque la fonction est activée, Aura n'existe pas, il s'agit d'un problème dans la configuration des serveurs de son, ni dans le matériel.

### 6. Notfall-Réinitialisation
Le système audio est entièrement suspendu :
```bash
systemctl --user restart pipewire wireplumber
# Oder für ältere PulseAudio-Systeme:
pulseaudio -k
```

---

**Conseil pour le flux de travail :** Pour passer directement à Kate, suspendez-le simplement `> /tmp/diagnose.txt && Kate /tmp/diagnose.txt` à votre adresse. 🌵🚀
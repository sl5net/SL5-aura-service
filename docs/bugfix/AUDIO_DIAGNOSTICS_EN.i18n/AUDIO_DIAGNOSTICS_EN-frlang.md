# AUDIO_DIAGNOSTICS_FR.md

# Diagnostic audio Linux pour Aura


### 1. Identification des appareils
Répertoriez tous les périphériques audio vus par l'environnement Python :
```bash
./.venv/bin/python3 -m sounddevice > /tmp/aura_devices.txt && kate /tmp/aura_devices.txt
```
* **Ce qu'il faut rechercher :** Notez le **numéro d'index** et l'**ID matériel (hw:X,Y)** de votre microphone.

### 2. Qui utilise le matériel ?
Si vous obtenez des erreurs « Device Busy » ou « Timeout », vérifiez quel processus (PID) verrouille actuellement le matériel audio :
```bash
fuser -v /dev/snd/*
```
* **Conseil :** Si vous voyez « pipewire » ou « wireplumber », le serveur de son gère l'appareil. Si vous voyez un PID « python3 » ou « obs » directement sur un périphérique PCM, il se peut qu'ils en bloquent d'autres.

### 3. Surveillance en temps réel (PipeWire)
Si votre système utilise PipeWire (Standard en Manjaro moderne), c'est le meilleur outil pour les diagnostics en direct :
```bash
pw-top
```
* **Que rechercher :** Vérifiez la colonne « ERR » pour les pertes et vérifiez qu'Aura (16 000 Hz) et OBS (48 000 Hz) ne provoquent pas de surcharge de rééchantillonnage sur le processeur.

### 4. Surveillance des événements audio
Consultez des mises à jour en direct lorsque les microphones sont désactivés, réactivés ou que de nouveaux flux sont créés :
```bash
pactl subscribe
```
* **Utilisation :** Exécutez ceci, puis démarrez Aura. Si vous voyez immédiatement de nombreux événements « supprimer », un processus plante ou est rejeté.

### 5. Test de contournement matériel
Testez si votre microphone fonctionne au niveau matériel brut (en contournant PulseAudio/PipeWire). Cela enregistre 5 secondes d'audio :
```bash
# Replace hw:1,0 with your device index
arecord -D hw:1,0 -f S16_LE -r 16000 -d 5 /tmp/test.wav && vlc /tmp/test.wav
```
* **Résultat :** Si cela fonctionne mais pas Aura, le problème vient de la configuration du Sound-Server, pas du matériel.

### 6. Réinitialisation d'urgence
Si le système audio est bloqué :
```bash
systemctl --user restart pipewire wireplumber
# Or for older PulseAudio systems:
pulseaudio -k
```


**indice de flux de travail plus simple :**

`/tmp/diagnose.txt && kate /tmp/diagnose.txt` et le fichier. 🌵🚀
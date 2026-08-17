# AUDIO_DIAGNOSTICS_ES.md

# Diagnóstico de audio de Linux para Aura


### 1. Identificación de dispositivos
Enumere todos los dispositivos de audio tal como los ve el entorno Python:
```bash
./.venv/bin/python3 -m sounddevice > /tmp/aura_devices.txt && kate /tmp/aura_devices.txt
```
* **Qué buscar:** Anote el **Número de índice** y el **ID de hardware (hw:X,Y)** de su micrófono.

### 2. ¿Quién utiliza el hardware?
Si recibe errores de "Dispositivo ocupado" o "Tiempo de espera", verifique qué proceso (PID) está bloqueando actualmente el hardware de audio:
```bash
fuser -v /dev/snd/*
```
* **Consejo:** Si ve "pipewire" o "wireplumber", el servidor de sonido está administrando el dispositivo. Si ve un PID `python3` u `obs` directamente en un dispositivo PCM, es posible que estén bloqueando a otros.

### 3. Monitoreo en tiempo real (PipeWire)
Si su sistema utiliza PipeWire (estándar en Manjaro moderno), esta es la mejor herramienta para diagnósticos en vivo:
```bash
pw-top
```
* **Qué buscar:** Verifique la columna `ERR` para ver si hay interrupciones y verifique que Aura (16000 Hz) y OBS (48000 Hz) no estén causando una sobrecarga de remuestreo en la CPU.

### 4. Monitoreo de eventos de audio
Vea actualizaciones en vivo cuando los micrófonos estén silenciados, activados o cuando se creen nuevas transmisiones:
```bash
pactl subscribe
```
* **Uso:** Ejecute esto y luego inicie Aura. Si ve muchos eventos de "eliminación" inmediatamente, un proceso falla o está siendo rechazado.

### 5. Prueba de omisión de hardware
Pruebe si su micrófono funciona en un nivel de hardware sin formato (sin pasar por PulseAudio/PipeWire). Esto graba 5 segundos de audio:
```bash
# Replace hw:1,0 with your device index
arecord -D hw:1,0 -f S16_LE -r 16000 -d 5 /tmp/test.wav && vlc /tmp/test.wav
```
* **Resultado:** Si esto funciona pero Aura no, el problema está en la configuración del servidor de sonido, no en el hardware.

### 6. Restablecimiento de emergencia
Si el sistema de audio está atascado:
```bash
systemctl --user restart pipewire wireplumber
# Or for older PulseAudio systems:
pulseaudio -k
```


**un flujo de trabajo más sencillo:**

`/tmp/diagnose.txt && kate /tmp/diagnose.txt` an den Befehl an. 🌵🚀
# AUDIO_DIAGNOSTICS_EN.md

# Linux Audio Diagnostics for Aura 


### 1. Identifying Devices
List all audio devices as seen by the Python environment:
```bash
./.venv/bin/python3 -m sounddevice > /tmp/aura_devices.txt && kate /tmp/aura_devices.txt
```
*   **What to look for:** Note the **Index Number** and **Hardware ID (hw:X,Y)** of your microphone.

### 2. Who is using the hardware?
If you get "Device Busy" or "Timeout" errors, check which process (PID) is currently locking the audio hardware:
```bash
fuser -v /dev/snd/*
```
*   **Tip:** If you see `pipewire` or `wireplumber`, the sound server is managing the device. If you see a `python3` or `obs` PID directly on a PCM device, they might be blocking others.

### 3. Real-time Monitoring (PipeWire)
If your system uses PipeWire (Standard in modern Manjaro), this is the best tool for live diagnostics:
```bash
pw-top
```
*   **What to look for:** Check the `ERR` column for dropouts and verify that Aura (16000Hz) and OBS (48000Hz) are not causing resampling-overload on the CPU.

### 4. Monitoring Audio Events
See live updates when microphones are muted, unmuted, or new streams are created:
```bash
pactl subscribe
```
*   **Usage:** Run this, then start Aura. If you see many `remove` events immediately, a process is crashing or being rejected.

### 5. Hardware Bypass Test
Test if your microphone works on a raw hardware level (bypassing PulseAudio/PipeWire). This records 5 seconds of audio:
```bash
# Replace hw:1,0 with your device index
arecord -D hw:1,0 -f S16_LE -r 16000 -d 5 /tmp/test.wav && vlc /tmp/test.wav
```
*   **Result:** If this works but Aura doesn't, the issue is in the Sound-Server configuration, not the hardware.

### 6. Emergency Reset
If the audio system is stuck:
```bash
systemctl --user restart pipewire wireplumber
# Or for older PulseAudio systems:
pulseaudio -k
```


**hint easier Workflow:** 

`/tmp/diagnose.txt && kate /tmp/diagnose.txt` an den Befehl an. 🌵🚀



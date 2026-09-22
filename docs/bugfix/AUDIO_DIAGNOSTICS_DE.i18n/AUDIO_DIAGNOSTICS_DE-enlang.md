> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../AUDIO_DIAGNOSTICS_DE.md).*

# German Version: `AUDIO_DIAGNOSTICS_DE.md`

# Linux Audio Diagnostic for Aura 

When running the Aura Service simultaneously, audio conflicts can occur (timeouts, 'Device Busy', or sample rate conflicts). These commands help with troubleshooting.

### 1. Identify Devices
Displays all audio devices from the perspective of the Python environment:
```bash
./.venv/bin/python3 -m sounddevice > /tmp/aura_devices.txt && kate /tmp/aura_devices.txt
```
*   **Goal:** Note down the **index number** and the **hardware ID (hw:X,Y)** of your microphone.

### 2. Who occupies the hardware?
If errors like "Device Busy" or "Timeout" occur, check which process (PID) is blocking the hardware:
```bash
fuser -v /dev/snd/*
```
*   **Tip:** If `pipewire` or `wireplumber` appears, the sound server manages the device. If an `python3` or `obs` PID appears directly on a PCM device, these may block access for others.

### 3. Real-time Monitoring (PipeWire)
For modern Manjaro systems with PipeWire, this is the most important tool:
```bash
pw-top
```
*   **Goal:** Check column `ERR` for errors and ensure that Aura (16000Hz) and OBS (48000Hz) do not cause CPU overload due to resampling.

### 4. Monitoring of Audio Events
Follow live when microphones are muted or new streams are created:
```bash
pactl subscribe
```
*   **Application:** Start this and then Aura. If many `remove` events occur immediately, a process is terminating or being rejected by the system.

### 5. Hardware Direct Test
Tests whether the microphone works at the hardware level (bypasses PulseAudio/PipeWire). Records for 5 seconds:
```bash
# Ersetze hw:1,0 durch deinen Geräte-Index
arecord -D hw:1,0 -f S16_LE -r 16000 -d 5 /tmp/test.wav && vlc /tmp/test.wav
```
*   **Result:** If this works but Aura does not, the problem lies in the configuration of the sound server, not in the hardware.

### 6. Emergency Reset
If the audio system is completely hanging:
```bash
systemctl --user restart pipewire wireplumber
# Oder für ältere PulseAudio-Systeme:
pulseaudio -k
```

---

**Tip for the workflow:** To view outputs directly in Kate, simply append `> /tmp/diagnose.txt && kate /tmp/diagnose.txt` to the command. 🌵🚀

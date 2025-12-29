# Bugfix: Audio Distortion & PipeWire Hang (Linux)

This document describes how to resolve audio distortion ("klirren"), robotic voice artifacts, and system audio hangs that can occur when using **SL5-aura-service** alongside other media applications like OBS, AnyDesk, or high-frequency TTS streams.

## Symptoms
- Voice output/input sounds distorted, metallic, or "clirring."
- System audio hangs with the message: `Establishing connection to PulseAudio` or `Please wait`.
- Total audio loss after high CPU load or concurrent stream usage.
- Journal logs show: `spa.alsa: hw:X: snd_pcm_status error: No such device`.

## Root Cause
On Manjaro and other modern Linux distros, **PipeWire** manages audio. Distortion usually stems from:
1. **Buffer Underruns:** Conflict between concurrent streams (e.g., AnyDesk capturing audio while TTS/OBS is running).
2. **Sample Rate Mismatch:** Frequent switching between 44.1kHz and 48kHz.
3. **USB Timing Issues:** High bus load causing USB headsets (like Plantronics/Poly) to temporarily disconnect.

---

## Solutions

### 1. Immediate Recovery (The "Nuclear" Reset)
If the audio stack is frozen or distorted, kill all audio-related processes. They will auto-restart immediately.

```bash
# Force kill PipeWire and its PulseAudio compatibility layer
killall -9 pulseaudio pipewire pipewire-pulse
```

### 2. Prevention & Stability Settings

#### Disable AnyDesk Audio
AnyDesk often tries to hook into the audio device, causing hardware conflicts.
- **Action:** Open AnyDesk Settings -> **Audio** -> Disable **"Transmit audio"** and **"Reproduce audio"**.

#### Fix PipeWire Sample Rate (Recommended)
Force PipeWire to stay at 48kHz to avoid resampling artifacts during TTS playback.

1. Create the config directory: `mkdir -p ~/.config/pipewire`
2. Copy the default config: `cp /usr/share/pipewire/pipewire.conf ~/.config/pipewire/`
3. Edit `~/.config/pipewire/pipewire.conf` and set:
   ```conf
   default.clock.rate = 48000
   ```
4. Restart services:
   ```bash
   systemctl --user restart pipewire pipewire-pulse wireplumber
   ```

---

## 3. Post-Production Recovery (FFmpeg)
If you recorded a session and the audio is distorted ("clirring"), use the following `ffmpeg` filter chain to repair the file.

### Recommended Repair Command
This command applies a de-clipper, noise reduction, and a low-pass filter to remove high-frequency digital artifacts without re-encoding the video.

tested and very good:

```bash
ffmpeg -i input_video.mp4 
    -af "adeclip, afftdn, lowpass=f=5000, volume=1.5" \
    -c:v copy reparatur_output.mp4  
```

may a better with (not tested):

```bash
ffmpeg -i input_video.mp4 \
  -af "adeclip, afftdn, lowpass=f=3500, volume=1.8" \
  -c:v copy repaired_audio_output.mp4
```



not tested:
```bash
ffmpeg -i input_video.mp4 -af "arnndn=m=cb.rnnn, lowpass=f=5000" -c:v copy ki_reparatur.mp4
```




**Filter Breakdown:**
- `adeclip`: Rounds off digital clipping spikes.
- `afftdn`: Reduces FFT-based digital noise.
- `lowpass=f=3500`: Cuts off frequencies above 3.5kHz where most "clirring" occurs (makes the voice clearer/warmer).
- `volume=1.8`: Compensates for volume loss during filtering.
- `-c:v copy`: Keeps original video quality (extremely fast).

---

## Debugging Tools
To monitor audio health in real-time during development:
- `pw-top`: Shows real-time errors (ERR column) and buffer status.
- `journalctl --user -u pipewire`: Checks for hardware disconnects.


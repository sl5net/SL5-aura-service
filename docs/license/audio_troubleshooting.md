# Audio Troubleshooting (Linux)

## Problem: Espeak / Fallback is silent
If the fallback audio (espeak) is not audible, it is likely muted in the system's sound mixer (e.g., PulseAudio or PipeWire). 

### The "Long String Trick" to Unmute
Short audio fragments often disappear too quickly from the mixer GUI to be unmuted manually. To fix this, force a long audio stream:

```bash
echo "$(yes "Testing sound. " | head -n 50)" | espeak

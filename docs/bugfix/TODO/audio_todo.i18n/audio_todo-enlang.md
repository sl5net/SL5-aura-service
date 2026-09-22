> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../audio_todo.md).*

12/31/'25 6:25 PM Wed

Summary and the to-do list for the future:

### Documentation: Attempt "Unified Audio Input" (Mic + Desktop)
**Status:** Paused (Proof of Concept exists, but not stable/performant).

**Experiences / Findings:**
*   **Routing:** PipeWire/PulseAudio tend to reset the Python stream (ALSA bridge) to the standard physical microphone (stream restore logic).
*   **Performance:** The processing of RMS, VAD and Vosk in a tight loop, combined with external `pactl` calls, leads to high CPU load (fan rotation).
*   **Signal:** Despite the correct device index, there was often only a RMS level of ~1.7, which indicates a wrong mapping between ALSA and PipeWire.

---

### To-Do List (Future Sprint)
1.  **[ ] WirePlumber Integration:** Exploring native PipeWire rules (`scripts`) to permanently bind the stream without `pactl` hooks.
2.  **[ ] Performance Optimization:** Relieve the audio loop (e.g. perform RMS checks less often or optimize VAD parameters).
3.  **[ ] Native Mono Sink:** Ensure that the virtual sink is fixed at 16kHz Mono system-wide to avoid resampling load.
4.  **[ ] Robust Device Mapping:** Finding a more stable method to address the virtual monitor sink in `sounddevice` by name.

---

### Update `config/settings.py`
```python
# config/settings.py

# AUDIO_INPUT_DEVICE = None 
# PLANNED: UNIFIED_AUDIO_INPUT (Mic + Desktop Sound)
# Current status: Experimental. Requires stable PipeWire routing and CPU optimization.
# AUDIO_INPUT_DEVICE = 'UNIFIED_AUDIO_INPUT' 
```

** [EN] Summary:**
Attempted to merge Mic and Desktop audio using a virtual `null-sink`. Routing was unstable due to PipeWire's stream-restore. High CPU load was observed. Logic is now documented for a future iteration.

I am curious whether we will succeed in a later attempt with a more performant solution (perhaps directly via PipeWire interfaces)! Done for today.

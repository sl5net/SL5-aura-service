# Session Audio Handling & Voice Toggles

Aura implements a session-based audio processing loop. Voice commands for state management are only active within an established recording session.

## Configuration
The session-internal behavior is controlled by:
`ENABLE_WAKE_WORD = True/False` (in `config/settings.py`)

## Operational Logic
Unlike a persistent background listener, Aura's STT engine (Vosk) only processes audio when a recording session has been triggered externally (e.g., via Hotkey).

### The In-Session Toggle ("Teleskop")
When `ENABLE_WAKE_WORD` is set to **True**:
1. **Trigger:** The user starts a session manually.
2. **Toggle:** Saying "Teleskop" during the session toggles between **ACTIVE** and **SUSPENDED** states.
3. **Behavior:** This allows the user to "pause" and "resume" text processing using voice commands without terminating the audio stream.

### Privacy & Efficiency
When `ENABLE_WAKE_WORD` is set to **False** (Default):
- **STT Suppression:** While in a suspended state, calls to `AcceptWaveform` and `PartialResult` are completely skipped.
- **Privacy:** No audio data is analyzed unless the system is in an explicit active state.
- **Resource Management:** CPU usage is minimized by bypassing neural network analysis during suspension.

## Latency & Performance
- **Instant Resume:** Because the `RawInputStream` remains open throughout the session, switching from SUSPENDED back to ACTIVE has **0ms additional latency**.
- **Loop Timing:** The processing loop operates at a ~100ms interval (`q.get(timeout=0.1)`), ensuring near-instant response times.

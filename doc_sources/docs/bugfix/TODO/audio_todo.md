31.12.'25 18:25 Wed

Zusammenfassung und die To-Do-Liste für die Zukunft:

### Dokumentation: Versuch "Unified Audio Input" (Mic + Desktop)
**Status:** Pausiert (Proof of Concept existiert, aber nicht stabil/performant).

**Erfahrungen / Findings:**
*   **Routing:** PipeWire/PulseAudio neigen dazu, den Python-Stream (ALSA-Bridge) hartnäckig auf das physische Standard-Mikrofon zurückzusetzen (Stream-Restore-Logik).
*   **Performance:** Die Verarbeitung von RMS, VAD und Vosk in einem engen Loop, kombiniert mit externen `pactl`-Aufrufen, führt zu hoher CPU-Last (Lüfterdrehen).
*   **Signal:** Trotz korrektem Device-Index kam oft nur ein RMS-Pegel von ~1.7 an, was auf ein falsches Mapping zwischen ALSA und PipeWire hindeutet.

---

### To-Do List (Future Sprint)
1.  **[ ] WirePlumber Integration:** Erforschung von nativen PipeWire-Rules (`scripts`), um den Stream permanent ohne `pactl`-Hooks zu binden.
2.  **[ ] Performance Optimization:** Den Audio-Loop entlasten (z.B. RMS-Checks seltener durchführen oder VAD-Parameter optimieren).
3.  **[ ] Native Mono Sink:** Sicherstellen, dass der virtuelle Sink systemweit fest auf 16kHz Mono steht, um Resampling-Last zu vermeiden.
4.  **[ ] Robust Device Mapping:** Eine stabilere Methode finden, um den virtuellen Monitor-Sink in `sounddevice` namentlich zu adressieren.

---

### Update `config/settings.py`
```python
# config/settings.py

# AUDIO_INPUT_DEVICE = None 
# PLANNED: UNIFIED_AUDIO_INPUT (Mic + Desktop Sound)
# Current status: Experimental. Requires stable PipeWire routing and CPU optimization.
# AUDIO_INPUT_DEVICE = 'UNIFIED_AUDIO_INPUT' 
```

**[EN] Summary:**
Attempted to merge Mic and Desktop audio using a virtual `null-sink`. Routing was unstable due to PipeWire's stream-restore. High CPU load was observed. Logic is now documented for a future iteration.

Ich bin gespannt, ob wir bei einem späteren Versuch mit einer performanteren Lösung (vielleicht direkt über PipeWire-Schnittstellen) Erfolg haben! Erledigt für heute.

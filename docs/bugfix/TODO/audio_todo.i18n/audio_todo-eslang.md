31.12.'25 18:25 mié

Zusammenfassung und die To-Do-Liste für die Zukunft:

### Documentación: Versuch "Entrada de audio unificada" (micrófono + escritorio)
**Estado:** Pausiert (Prueba de concepto existente, pero no estable/performante).

**Erfahrungen / Hallazgos:**
* **Enrutamiento:** PipeWire/PulseAudio no está conectado al micrófono estándar físico (Stream-Restore-Logik) de Python-Stream (ALSA-Bridge).
* **Rendimiento:** Die Verarbeitung von RMS, VAD und Vosk in einem engen Loop, combinado con externo `pactl`-Aufrufen, führt zu hoher CPU-Last (Lüfterdrehen).
* **Señal:** Este índice de dispositivo corregido a menudo no tiene un valor RMS de ~1.7 an, y se encuentra en un mapeo falso entre ALSA y PipeWire.

---

### Lista de tareas pendientes (sprint futuro)
1. **[] Integración de WirePlumber:** Erforschung von Nativen PipeWire-Rules (`scripts`), un Stream permanente sin `pactl`-Hooks para vincular.
2. **[ ] Optimización del rendimiento:** El bucle de audio se activa (por ejemplo, se seleccionan las comprobaciones RMS o se optimizan los parámetros VAD).
3. **[ ] Native Mono Sink:** Sicherstellen, dass der virtual Sink systemweit fest auf 16kHz Mono steht, um Resampling-Last zu vermeiden.
4. **[ ] Mapeo robusto de dispositivos:** Un método estable para encontrar el Monitor-Sink virtuoso en `sounddevice` nombra sus direcciones.

---

### Actualizar `config/settings.py`
```python
# config/settings.py

# AUDIO_INPUT_DEVICE = None 
# PLANNED: UNIFIED_AUDIO_INPUT (Mic + Desktop Sound)
# Current status: Experimental. Requires stable PipeWire routing and CPU optimization.
# AUDIO_INPUT_DEVICE = 'UNIFIED_AUDIO_INPUT' 
```

**[ES] Resumen:**
Se intentó fusionar el audio del micrófono y del escritorio mediante un "disipador nulo" virtual. El enrutamiento era inestable debido a la restauración de flujo de PipeWire. Se observó una alta carga de CPU. La lógica ahora está documentada para una iteración futura.

Ich bin gespannt, ob wir bei einem späteren Versuch mit einer performanteren Lösung (vielleicht direkt über PipeWire-Schnittstellen) Erfolg haben! Erledigt für heute.
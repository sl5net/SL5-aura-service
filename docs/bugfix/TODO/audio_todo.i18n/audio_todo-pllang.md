31.12.'25 18:25 śr

Zusammenfassung und die To-Do-Liste für die Zukunft:

### Dokumentacja: Versuch „Ujednolicone wejście audio” (mikrofon + komputer stacjonarny)
**Stan:** Pausiert (Dowód koncepcji istnieje, aber nicht stabil/performant).

**Erfahrungen / Ustalenia:**
* **Routing:** PipeWire/PulseAudio nie jest używany, ani Python-Stream (ALSA-Bridge) hartnäckig auf das physische Standard-Mikrofon zurückzusetzen (Stream-Restore-Logik).
* **Wydajność:** Die Verarbeitung von RMS, VAD und Vosk in einem engen Loop, kombiniert mit externen `pactl`-Aufrufen, führt zu hoher CPU-Last (Lüfterdrehen).
* **Sygnał:** Trotz korrektem Device-Index kam często nur ein RMS-Pegel von ~1.7 an, był auf ein falsches Mapping zwischen ALSA und PipeWire hideutet.

---

### Lista rzeczy do zrobienia (przyszły sprint)
1. **[ ] Integracja z WirePlumber:** Erforschung von nativen PipeWire-Rules (`skrypty`), um den Stream permanent ohne `pactl`-Hooks zu binden.
2. **[ ] Optymalizacja wydajności:** Den Audio-Loop entlasten (np. RMS-Checks seltener durchführen oder VAD-Parameter optimieren).
3. **[ ] Natywny zlew Mono:** Sicherstellen, dass der constelle Sink systemweit feest auf 16kHz Mono steht, um Resampling-Last zu vermeiden.
4. **[ ] Solidne mapowanie urządzeń:** Można znaleźć stabilną metodę, a następnie znaleźć monitor-sink w `sounddevice` namentlich zu adressieren.

---

### Zaktualizuj `config/settings.py`
__KOD_BLOKU_0__

**[PL] Podsumowanie:**
Próbowano połączyć dźwięk z mikrofonu i pulpitu przy użyciu wirtualnego „null-sink”. Trasowanie było niestabilne z powodu przywracania strumienia przez PipeWire. Zaobserwowano duże obciążenie procesora. Logika jest teraz udokumentowana dla przyszłej iteracji.

Ich bin gespannt, ob wir bei einem späteren Versuch mit einer performanteren Lösung (vielleicht direkt über PipeWire-Schnittstellen) Erfolg haben! Erledigt für heute.
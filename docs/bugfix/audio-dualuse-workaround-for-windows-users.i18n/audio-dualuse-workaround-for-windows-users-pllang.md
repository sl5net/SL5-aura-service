# Zunifikowany_ujście
## ustawienia.AUDIO_INPUT_DEVICE == 'MIC_AND_DESKTOP
### Strategia dla systemu Windows (obejście)
Dla systemu Windows **Wirtualne kable audio** w połączeniu z **Monitorowaniem OBS**.

**Ta konfiguracja:**
1. **Instalacja wirtualnego kabla:** (tzn. B. *VB-Cable*). Jest to również nazwa „Unified_Sink” w systemie Windows.
2. **Monitorowanie OBS:** In den OBS-Einstellungen unter *Audio -> Erweitert -> Monitoring-Gerät* wählst du das „Virtual Cable” aus.
3. **Mix erstellen:** Für jede Quelle in OBS (mikrofon, komputer stacjonarny) stellst du in den *Erweiterten Audioeigenschaften* „Monitoring und Ausgabe” ein.
4. **Python:** W ustawieniach setzt du `AUDIO_INPUT_DEVICE = "Wyjście KABLA"`.

### Analizuj
* **Vorteil:** OBS übernimmt das kompletne miksowanie. Keine kompleksen Python-Ęnderungen für Windows nötig.
* **Nachteil:** Der Benutzer muss OBS im Hintergrund laufen lassen.

Für Windows-User wäre das der stabilste Weg.

**Befehl für Windows (PowerShell) zum Suchen des Cable-Namens:**
`Pobierz listę urządzeń audio`
*(Hinweis: Erfordert oft das AudioDeviceCmdlets-Modul).*
# Unified_Sink
## Settings.AUDIO_INPUT_DEVICE == 'MIC_AND_DESKTOP
### Die Strategie für Windows (Workaround)
Unter Windows nutzt **Virtual Audio Cables** in Kombination mit dem **OBS-Monitoring**.

**Das Setup:**
1. **Virtual Cable installieren:** (z. B. *VB-Cable*). Es beginnt als dein „Unified_Sink“ auf Windows.
2. **OBS-Überwachung:** Wählen Sie in den OBS-Einstellungen unter *Audio -> Erweitert -> Monitoring-Gerät* das „Virtual Cable“ aus.
3. **Mix erstellen:** Für jede Quelle in OBS (Mic, Desktop) stellst du in den *Erweiterten Audioeigenschaften* „Monitoring und Ausgabe“ ein.
4. **Python:** In den Einstellungen setzt du „AUDIO_INPUT_DEVICE = „CABLE Output““.

### Analysieren
* **Vorteil:** OBS übernimmt das komplette Mixing. Keine komplexen Python-Änderungen für Windows nötig.
* **Nachteil:** Der Benutzer muss OBS im Hintergrund laufen lassen.

Für Windows-Benutzer wäre das der stabilste Weg.

**Befehl für Windows (PowerShell) zum Suchen des Cable-Namens:**
„Get-AudioDevice -List“.
*(Hinweis: Erfordert oft das AudioDeviceCmdlets-Modul).*
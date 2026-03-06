# Unified_Sink
## configurações.AUDIO_INPUT_DEVICE == 'MIC_AND_DESKTOP
### A estratégia para Windows (solução alternativa)
No Windows nutzt **Cabos de áudio virtuais** em combinação com **Monitoramento OBS**.

**A configuração:**
1. **Instalação de cabo virtual:** (por exemplo, *VB-Cable*). Foi implementado em “Unified_Sink” no Windows.
2. **Monitoramento OBS:** No OBS-Einstellungen unter *Audio -> Erweitert -> Monitoring-Gerät* wählst du das „Virtual Cable“ aus.
3. **Mix erstellen:** Para qualquer coisa em OBS (Mic, Desktop) stellst du in den *Erweiterten Audioeigenschaften* „Monitoring und Ausgabe“ ein.
4. **Python:** Nas configurações defina `AUDIO_INPUT_DEVICE = "CABLE Output"`.

### Analisar
* **Vorteil:** OBS übernimmt da mixagem completa. Nenhuma aplicação complexa de Python para Windows não é necessária.
* **Nachteil:** Der Benutzer muss OBS im Hintergrund laufen lassen.

Para usuários do Windows, o Weg está estável.

**Befehl for Windows (PowerShell) zum suchen des Cable Namens:**
`Get-AudioDevice -List`
*(Hinweis: Erfordert oft the AudioDeviceCmdlets-Modul).*
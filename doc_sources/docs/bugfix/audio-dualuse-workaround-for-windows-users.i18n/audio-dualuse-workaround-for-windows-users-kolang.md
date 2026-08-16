# 통합_싱크
## settings.AUDIO_INPUT_DEVICE == 'MIC_AND_DESKTOP
### Windows용 다이 전략(해결 방법)
Windows에서는 **OBS 모니터링**과 결합하여 **가상 오디오 케이블**을 사용합니다.

**설정:**
1. **가상 케이블 설치 방법:** (z. B. *VB-케이블*). 이 기능은 Windows에서 "Unified_Sink"로 정의됩니다.
2. **OBS 모니터링:** In den OBS-Einstellungen unter *Audio -> Erweitert -> Monitoring-Gerät* wählst du das "Virtual Cable" aus.
3. **먼저 혼합하세요:** OBS(마이크, 데스크톱)의 Für jede Quelle stellst du in den *Erweiterten Audioeigenschaften* "Monitoring und Ausgabe" ein.
4. **Python:** 설정에서 `AUDIO_INPUT_DEVICE = "CABLE Output"`을 설정합니다.

### 분석
* **Vorteil:** OBS übernimmt das komplette Mixing. Keine komplexen Python-änderungen for Windows nötig.
* **Nachteil:** Der Benutzer는 OBS im Hintergrund laufen lassen을 muss합니다.

Windows 사용자를 위해 Weg의 안정성을 확인하세요.

**Windows(PowerShell)를 위한 Befehl zum Suchen des Cable-Namens:**
`Get-AudioDevice -목록`
*(힌웨이: Erfordert oft das AudioDeviceCmdlets-Modul).*
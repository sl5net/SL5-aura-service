# 統合シンク
## settings.AUDIO_INPUT_DEVICE == 'MIC_AND_DESKTOP
### Windows の戦略 (回避策)
Windows では、**OBS モニタリング** と組み合わせて **仮想オーディオ ケーブル** を使用できます。

**セットアップ:**
1. **仮想ケーブルのインストール先:** (z.B. *VB-Cable*)。 Windows の「Unified_Sink」機能も提供します。
2. **OBS モニタリング:** OBS-Einstellungen では、*オーディオ -> ERWEITERT -> Monitoring-Gerät* を使用して「仮想ケーブル」を表示します。
3. **ミックス erstellen:** OBS (マイク、デスクトップ) で *Erweiterten Audioeigenschaften* 「Monitoring und Ausgabe」 ein を実行します。
4. **Python:** デン設定で `AUDIO_INPUT_DEVICE = "CABLE Output"` を設定します。

### 分析する
* **Vorteil:** OBS übernimmt das komplette ミキシング。 Keine komplexen Python と Windows の統合。
* **Nachteil:** Der Benutzer muss OBS im Hintergrund laufen lassen.

Windows ユーザーは安定性を維持できます。

**Windows (PowerShell) のケーブル名の詳細:**
`Get-AudioDevice -List`
*(ヒント: AudioDeviceCmdlets-Modul のエラー).*
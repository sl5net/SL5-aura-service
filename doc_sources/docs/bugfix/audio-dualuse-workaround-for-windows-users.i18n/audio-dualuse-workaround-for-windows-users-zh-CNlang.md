# 统一接收器
## settings.AUDIO_INPUT_DEVICE == 'MIC_AND_DESKTOP
### Windows 的死亡策略（解决方法）
在 Windows 下，**虚拟音频电缆**与 **OBS 监控**相结合。

**Das 设置：**
1. **虚拟电缆安装：** (z. B. *VB-Cable*)。它是 Windows 上的“Unified_Sink”。
2. **OBS 监控：** 在 OBS-Einstellungen 下 *Audio -> Erweitert -> Monitoring-Gerät* wählst du das “Virtual Cable” aus。
3. **混音：** 将 OBS（麦克风、桌面）中的声音混合到 *Erweiterten Audioeigenschaften* “Monitoring und Ausgabe” 中。
4. **Python：** 在设置中设置 `AUDIO_INPUT_DEVICE = "CABLE Output"`。

＃＃＃ 分析
* **Vorteil:** OBS übernimt das komplette Mixing。 Python 与 Windows 的复杂性。
* **Nachteil:** Der Benutzer muss OBS im Hintergrund laufen lassen。

对于 Windows 用户来说，这是稳定的。

**适用于 Windows (PowerShell) 的电缆名称：**
`获取音频设备-列表`
*（注意：Erfordert oft das AudioDeviceCmdlets-Modul）。*
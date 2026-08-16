# 德语版本：`AUDIO_DIAGNOSTICS_DE.md`

# Linux 音频诊断 Aura

Beim gleichzeitigen Betrieb vom Aura Service können Audio-Konflikte auftreten（超时、“设备繁忙”或采样率Konflikte）。 Diese Befehle helfen bei der Fehlersuche。

### 1. 身份证明
所有 Audio-Geräte aus Sicht der Python-Umgebung 和：
__代码_块_0__
* **Ziel:** 注意 **索引号** 和 **硬件 ID (hw:X,Y)** 定义 Mikrofons。

### 2. 我们有硬件吗？
Wenn Fehler wie “设备繁忙”或“超时”auftreten、prüfe、welcher Prozess (PID) die 硬件块：
__代码_块_1__
* **Tipp：** Wenn `pipewire` 或 `wireplumber` erscheint，verwaltet der Sound-Server das Gerät。 Wenn eine `python3` 或 `obs` PID 指令来自于 PCM-Gerät erscheint，blockieren diese evtl。 den Zugriff für andere。

### 3. Echtzeit 监控 (PipeWire)
带有 PipeWire 的现代 Manjaro-Systeme 工具已死亡：
__代码_块_2__
* **Ziel:** Prüfe die Spalte `ERR` auf Fehler und stelle sicher, dass Aura (16000Hz) 和 OBS (48000Hz) keine CPU-Überlastung durch Resampling verursachen。

### 4. 音频事件的高级处理
Verfolge live，wenn Mikrofone Stummgeschaltet werden oder neue Streams entstehen：
__代码_块_3__
* **注释：** Starte 死亡并失去 Aura。 Wenn sofort viele ‘remove’-Events kommen, bricht ein Prozess ab oder wird vom System abgewiesen.

### 5. 硬件直接测试
测试仪，ob das Mikrofon auf Hardware-Ebene funktioniert (umgeht PulseAudio/PipeWire)。 Nimmt 5 Sekunden auf：
__代码_块_4__
* **说明：** Wenn 因功能而死亡，Aura aber nicht，这是声音服务器配置中的问题，而不是硬件。

### 6. Notfall-重置
音频系统的功能如下：
__代码_块_5__

---

**提示工作流程：** Um Ausgaben direkt in Kate zu betrachten, hänge einfach `> /tmp/diagnose.txt && kate /tmp/diagnose.txt` and den Befehl an。 🌵🚀
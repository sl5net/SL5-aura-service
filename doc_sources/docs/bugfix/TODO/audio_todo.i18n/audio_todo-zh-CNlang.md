31.12.'25 18:25 星期三

Zusammenfassung 和 die To-Do-Liste for die Zukunft：

### 文档：Versuch“统一音频输入”（麦克风 + 桌面）
**状态：** Pausiert（概念证明存在，aber nicht stable/performant）。

**Erfahrungen /调查结果：**
* **路由：** PipeWire/PulseAudio neigen dazu，den Python-Stream (ALSA-Bridge) hartnäckig auf das physche Standard-Mikrofon zurückzusetzen (Stream-Restore-Logik)。
* **性能：** 在 einem engen Loop、kombiniert mit externen `pactl`-Aufrufen、führt zu hoher CPU-Last (Lüfterdrehen) 中执行 RMS、VAD 和 Vosk。
* **信号：** Trotz korrektem 设备索引通常在 RMS-Pegel von ~1.7 上，是 auf ein falsches 映射 zwischen ALSA 和 PipeWire 后置。

---

### 待办事项列表（未来冲刺）
1. **[ ] WirePlumber 集成：** 本地 PipeWire 规则（“脚本”）的实现，是永久性的“pactl”-Hooks zu Binden。
2. **[ ] 性能优化：** Den Audio-Loop entlasten (z.B. RMS-Checks seltener durchführen oder VAD-Parameter optimieren)。
3. **[ ] Native Mono Sink：** Sicherstellen，dass der Virdlle Sink 系统，具有 16kHz Mono steht，um Resampling-Last zu vermeiden。
4. **[ ] 鲁棒设备映射：** 找到一个稳定的方法，在“声音设备”名称中找到一个美德监视器接收器。

---

### 更新 `config/settings.py`
__代码_块_0__

**[EN] 摘要：**
尝试使用虚拟“空接收器”合并麦克风和桌面音频。由于 PipeWire 的流恢复，路由不稳定。观察到 CPU 负载较高。现在已记录逻辑以供将来迭代使用。

Ich bin gespannt, ob wir bei einem späteren Versuch mit einer Performanteren Lösung (vielleicht direkt über PipeWire-Schnittstellen) Erfolg haben！ Erledigt für heute。
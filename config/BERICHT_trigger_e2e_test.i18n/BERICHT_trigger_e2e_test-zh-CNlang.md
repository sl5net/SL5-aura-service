# 概要：SL5 Aura – 触发端到端测试

**日期：** 2026-03-15  
**Datei：** `scripts/py/func/checks/test_trigger_end_to_end.py`

---

## 1. 计划

Ein echter End-to-End Test der das bekannte Problem untersucht:
**Bei manchen Aufnahmen fehlt das letzte Wort im Output.**

测试溶液：
1. 与 Mikrofon einspeisen 相关的 Eine WAV-Datei
2. Aura per `touch /tmp/sl5_record.trigger` starten — genau wie im echten Betrieb
3. Mit zweitem 触发器停止
4. Den Output mit dem YouTube-Transcript vergleichen
5. Feststellen ob ein Wort am Ende fehlt

---

## 2. 是 erreicht wurde ✅

- Aura reagiert auf den Trigger korrekt
- LT läuft und ist erreichbar (`http://127.0.0.1:8082`)
- `_wait_for_output()` findet die `tts_output_*.txt` Datei
- `_fetch_yt_transcript_segment()` holt den Referenz-Text korrekt
- Der grundlegende Testaufbau ist Solide und Funktioniert Konzeptionell

---

## 3. Das ungelöste 问题 🔴

### 核心问题：`manage_audio_routing` überschreibt alles

Beim 会议开始 ruft Aura 实习生 auf：
__代码_块_0__

Diese Funktion macht erstes：
__代码_块_1__

**Sie löscht jeden Sink den wir vorher erstellt haben。**

Danach erstellt sie keinen neuen Sink weil `mode == 'SYSTEM_DEFAULT'` (nicht `MIC_AND_DESKTOP`)。

### Versuchte Lösungen

|维苏奇|问题 |
|---|---|
| PulseAudio 虚拟源说明 | PipeWire 忽略“模块虚拟源” |
| `settings_local.py` auf `MIC_AND_DESKTOP` setzen | Datei wurde mit mehrfachen Einträgen korrumpiert | 日期
|标记覆盖阻止和结束 | Aura lädt Settings nicht schnell genug neu bevor 触发器 kommt |
|测试 | `_create_mic_and_desktop_sink()` 直接会话启动时的“manage_audio_routing”接线 |
| `pw-环回` | Erscheint als Source aber Aura hört nicht darauf |

### Warum `settings_local.py` 覆盖 nicht funktioniert

`dynamic_settings.py` 超过日期和时间 — aber mit einem Intervall。 Der Trigger kommt zu schnell nach dem Schreiben。会话开始时，Aura 会以“SYSTEM_DEFAULT”的形式启动。

Außerdem: 自行打开 Aura `MIC_AND_DESKTOP` 按钮，然后将 Sink 放在 **nächsten** 会话开始 — 不舒服。

---

## 4.Mögliche Lösungswege

### 选项 A — Längeres Warten nach 设置-änderung
__代码_块_2__
Risiko：Nicht zuverlässig，timing-abhängig。

### 选项 B — Aura neu starten nach Settings-änderung
__代码_块_3__
Nachteil：测试时间超过 1 分钟。 Aber zuverlässig。

### 选项 C — `manage_audio_routing` direkt im Test aufrufen
__代码_块_4__
触发条件之前存在 Sink — 和会话启动时的“manage_audio_routing”，并且“is_mic_and_desktop_sink_active() == True”和“Setup”。

Das ist wahrscheinlich die **sauberste Lösung**。

### 选项 D — `process_text_in_background` direkt aufrufen（kein 触发器）
Wie 在 `test_youtube_audio_regression.py` — Vosk 输出直接在 Pipeline übergeben，ohne den echten Trigger-Mechanismus。 Dann testet man die Pipeline aber nicht das Abschneiden des letzten Wortes。

### 选项 E — Aura mit `run_mode_override=TEST` starten
跌落 Aura einen Test-Modus hat der das Audio-Routing überspringt。

---

## 5. 恩惠

**选项 C** zuerst probieren — einen 导入测试机器：

__代码_块_5__

功能说明：
__代码_块_6__

Dann erkennt Aura 位于 Ruhe 的 Session-Start `is_mic_and_desktop_sink_active() == True` 和 lässt den Sink 中。

---

## 6. Was dieser Test langfristig Bringt

Sobald er läuft，kann man：
- `SPEECH_PAUSE_TIMEOUT` Werte testen (1.0, 2.0, 4.0s) and sehen ob das letzte Wort abgeschnitten wird
- `transcribe_audio_with_feedback.py` 参数优化
- 音频处理回归
- 修复wirklich hilft

---

---

# 最终报告：SL5 Aura – 触发端到端测试

**日期：** 2026-03-15  
**文件：** `scripts/py/func/checks/test_trigger_end_to_end.py`

---

## 1. 计划

真正的端到端测试来调查已知问题：
**在某些录音中，最后一个单词在输出中被截断。**

测试应该：
1.输入WAV文件作为虚拟麦克风
2. 通过 `touch /tmp/sl5_record.trigger` 启动 Aura — 与实际使用完全相同
3. 用第二个触发器停止
4. 将输出与 YouTube 脚本进行比较
5.检测末尾是否漏字

---

## 2. 取得了什么成果 ✅

- Aura 正确响应触发
- LT 正在运行且可访问 (`http://127.0.0.1:8082`)
- `_wait_for_output()` 查找 `tts_output_*.txt` 文件
- `_fetch_yt_transcript_segment()` 正确获取参考文本
- 基本测试结构扎实且在概念上有效

---

## 3. 未解决的问题🔴

### 核心问题：`manage_audio_routing`覆盖所有内容

在会话开始时，Aura 内部调用：
__代码_块_7__

该函数首先执行以下操作：
__代码_块_8__

**它会删除我们之前创建的任何接收器。**

然后它不会创建新的接收器，因为“mode == 'SYSTEM_DEFAULT'”（不是“MIC_AND_DESKTOP”）。

### 尝试的解决方案

|尝试|问题 |
|---|---|
|创建 PulseAudio 虚拟源 | PipeWire 忽略“模块虚拟源” |
|将 `settings_local.py` 设置为 `MIC_AND_DESKTOP` |文件已损坏，有多个条目 |
|将标记的覆盖块写入文件末尾 |在触发器触发之前，Aura 重新加载设置的速度不够快 |
|直接在测试中`_create_mic_and_desktop_sink()`在会话开始时被 `manage_audio_routing` 删除 |
| `pw-环回` |显示为源，但 Aura 不听 |

---

## 4. 建议的下一步

在触发之前的测试中直接调用“manage_audio_routing”：

__代码_块_9__

当 Aura 启动会话时，它会检查“is_mic_and_desktop_sink_active()”——如果“True”，它会跳过设置并保留接收器。这是最干净的解决方案。

---

## 5. 这项测试将带来什么长期效果

一旦运行：
- 测试`SPEECH_PAUSE_TIMEOUT`值（1.0、2.0、4.0s）并检测单词截止
- 优化 `transcribe_audio_with_feedback.py` 参数
- 当音频处理发生变化时捕获回归
- 证明修复确实有效
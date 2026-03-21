# SL5 Aura – 音频回归测试：Statusbericht

**日期：** 2026-03-14  
**Datei:** `scripts/py/func/checks/test_youtube_audio_regression.py`

---

## 1. 是 wurde gebaut

Ein 测试系统：
1. Ein Audio-Segment aus einem YouTube-Video herunterlädt（通过 `yt-dlp` + `ffmpeg`）
2. Den automatisch Generierten YouTube-Transcript für dasselbe Segment abruft（通过 `youtube-transcript-api`）
3. Das Audio durch Vosk transkribiert
4. 可选的 das Ergebnis durch die **volle Aura-Pipeline** schickt (`process_text_in_background`)
5. 字错误率 (WER) zwischen Aura-Output 和 YouTube-Transcript berechnet
6. 根据“pytest”作为自动回归测试läuft

所有下载 werden gecacht (`scripts/py/func/checks/fixtures/youtube_clips/`)，sodass Folgetests schnell laufen。

---

## 2. 达田

|达亭|兹韦克 |
|---|---|
| `scripts/py/func/checks/test_youtube_audio_regression.py` |上测试日期 |
| `scripts/py/func/checks/fixtures/youtube_clips/*.wav` | Gecachte 音频剪辑 |
| `scripts/py/func/checks/fixtures/youtube_clips/*.transcript.json` | Gecachte 成绩单 |
| `scripts/py/func/checks/fixtures/youtube_clips/.gitignore` | Git 缓存 | 缓存
| `conftest.py`（仓库根目录）|设置 PYTHONPATH 进行 pytest |

---

## 3. 测试-Modi

### 方式 A – 仅 Vosk（基线）
__代码_块_0__
Vosk-Qualität 测试。凯因光环。施内尔。

### Modus B – Volle Aura-Pipeline，WER-Vergleich
__代码_块_1__
Schickt Vosk-FuzzyMap Pre → LanguageTool → FuzzyMap Post 的输出。

### Modus C – Volle Aura-Pipeline，exakter 输出
__代码_块_2__
Für Segmente wo ein bekannter Befehl gesprochen wrd。沙夫斯特测试。

---

## 4. Was wird getestet — was nicht

|是 |得到泰斯特？ |
|---|---|
| Vosk STT 质量 | ✅ |
| FuzzyMap 预注册 | ✅ (wenn Aura läuft) |
|语言工具-Korrekturen | ✅ (wenn LT läuft) |
| FuzzyMap 后Regeln | ✅ (wenn Aura läuft) |
|键盘输出（AutoHotkey/CopyQ）| ❌ bewusst — OS-Ebene，keine Logik |
| Vosk 模型加载 | ❌ — Aura liest Output-Datei，lädt kein Modell neu |

在 Temp-Verzeichnis gelesen 中输出 `tts_output_*.txt` — genau so wie Aura es intern macht, nicht aus dem Terminal。

---

## 5. 开始

### Normaler Testlauf (Aura muss bereits laufen):
__代码_块_3__

### Mit vollem 日志：
__代码_块_4__

### Nur bestimmte 测试：
__代码_块_5__

### Aura + LT 最开始：
__代码_块_6__

---

## 6. Wichtige 配置

### 语言代码 — zwei verschiedene Systeme！

|系统|代码|贝斯皮尔 |
|---|---|---|
| Vosk-模型-Ordner | `德` | `模型/vosk-model-de-0.21` |
|光环模糊地图-Ordner | `de-DE` | `config/maps/.../de-DE/` |
| YouTube 转录 API | `德` | `api.fetch(..., languages=["de"])` |

**Lösung 代码：** `language="de-DE"` setzen。自动代码：
- Für Vosk: `"de-DE"` → `"de"` (分割 auf `-`)
- Für YouTube：`"de-DE"` → `"de"`（拆分 auf `-`）
- Für Aura：“de-DE”直接

### 自动翻译器 deaktivieren vor 测试：
__代码_块_7__
Sonst übersetzt Aura deutschen Text ins English — das verfälscht den WER。

---

## 7. Bekannte Probleme & Lösungen

|问题 |乌萨凯 |洛松 |
|---|---|---|
| “跳过”软体| YouTube 脚本 nicht gefunden | `api.list('video_id')` aufrufen um verfügbare Sprachen zu sehen |
|音频|“跳过” Vosk-Modell 不存在 | `language.split("-")[0]` 代码中的后备 |
| `找到 0 条 FUZZY_MAP_pre 规则` | Falscher Sprachcode 和 Aura | `"de-DE"` statt `"de"` verwenden |
| `连接被拒绝 8010` | LT nicht gestartet | LT nicht gestartet Aura zuerst starten, 60 年代 Warten |
| `zsh：终止` | X11-Watchdog 杀戮进程 | `SDL_VIDEODRIVER=dummy` 版本；看门狗-Schwellenwert erhöhen |
| YouTube `>>` 标记 | Zweitsprecher 文字记录 | `re.sub(r'>>', '', text)` — nur `>>` entfernen，Wörter behalten |
| `属性错误：get_transcript` | youtube-transcript-api v1.x | youtube-transcript-api v1.x | `api = YouTubeTranscriptApi(); api.fetch(...)` 统计 Klassenmethod |
|缓存 enthält leeren 文本 |更改 Lauf 与 kaputtem 正则表达式 | `rm 固定装置/youtube_clips/*.transcript.json` |

---

## 8.Ergebnisse bis jetzt

### 视频：`sOjRNICiZ7Q`（德语），片段 5–20s

__代码_块_8__

**贝奥巴赫通根：**
- Aura hat eine Regel angewendet：`zehn Finger` → `10 Finger` ✅
- LT-Status während dieses Laufs unklar — Verbindung wurde verweigert
- Hoher WER liegt am Segment：YouTube-Transcript beginnt mit Wörtern die Vosk nicht hört (Sprecher noch nicht am Mikro)
- **使用：** Segment verschieben auf einen Bereich wo klar gesprochen wird

---

## 9. Empfehlungen für nächste Schritte

1. **Besseres Segment wählen** — `ffplay` nutzen um die genaue Sekunde zu finden wo klar gesprochen wrd
2. **LT-Status im Test prüfen** — `curl http://localhost:8010/v2/linguals` vor dem Test
3. **Modus C 测试 hinzufügen** — Segmente wo bekannte Befehle gesprochen werden (`expected_output`)

---
---

# SL5 Aura – 音频回归测试：状态报告

**日期：** 2026-03-14  
**文件：** `scripts/py/func/checks/test_youtube_audio_regression.py`

---

## 1. 建造了什么

测试系统：
1. 从 YouTube 视频下载音频片段（通过 `yt-dlp` + `ffmpeg`）
2. 获取同一片段自动生成的 YouTube 转录内容（通过 `youtube-transcript-api`）
3.通过Vosk转录音频
4. 可以选择将结果通过 **完整 Aura 管道** (`process_text_in_background`)
5. 计算 Aura 输出和 YouTube 转录内容之间的字错误率 (WER)
6. 通过“pytest”作为自动回归测试运行

所有下载都会被缓存（`scripts/py/func/checks/fixtures/youtube_clips/`），因此后续运行速度很快。

---

## 2. 文件

|文件|目的|
|---|---|
| `scripts/py/func/checks/test_youtube_audio_regression.py` |主要测试文件 |
| `scripts/py/func/checks/fixtures/youtube_clips/*.wav` |缓存的音频剪辑|
| `scripts/py/func/checks/fixtures/youtube_clips/*.transcript.json` |缓存的成绩单 |
| `scripts/py/func/checks/fixtures/youtube_clips/.gitignore` |从 Git 中排除缓存 |
| `conftest.py`（存储库根目录）|为 pytest 设置 PYTHONPATH |

---

## 3. 测试模式

### 模式 A – 仅 Vosk（基线）
__代码_块_9__
仅测试 Vosk 质量。没有灵气。快速地。

### 模式 B – 完整 Aura 流程，WER 比较
__代码_块_10__
通过 FuzzyMap Pre → LanguageTool → FuzzyMap Post 发送 Vosk 输出。

### 模式 C – 完整 Aura 管道，精确输出匹配
__代码_块_11__
对于包含已知语音命令的片段。最严格的测试模式。

---

## 4. 测试了什么——未测试什么

|什么 |测试过吗？ |
|---|---|
| Vosk STT 品质 | ✅ |
| FuzzyMap 预规则 | ✅（当 Aura 运行时）|
|语言工具修正 | ✅（LT 运行时）|
| FuzzyMap 发布规则 | ✅（当 Aura 运行时）|
|键盘输出（AutoHotkey/CopyQ）| ❌ 故意的——操作系统级别，没有逻辑 |
| Vosk 模型重装 | ❌ — Aura 读取输出文件，不重新加载模型 |

输出是从临时目录中的“tts_output_*.txt”读取的——与 Aura 内部的操作完全相同，而不是从终端读取。

---

## 5. 启动命令

### 正常测试运行（Aura 必须已经运行）：
__代码_块_12__

### 完整日志：
__代码_块_13__

### 仅特定测试：
__代码_块_14__

### 首先启动 Aura + LT：
__代码_块_15__

---

## 6. 重要配置

### 语言代码——两个不同的系统！

|系统|代码|示例|
|---|---|---|
| Vosk 模型文件夹 | `德` | `模型/vosk-model-de-0.21` |
| Aura FuzzyMap 文件夹 | `de-DE` | `config/maps/.../de-DE/` |
| YouTube 转录 API | `德` | `api.fetch(..., languages=["de"])` |

**代码中的解决方案：**设置 `language="de-DE"`。代码自动处理：
- 对于 Vosk：`"de-DE"` → `"de"`（在 `-` 上分割）
- 对于 YouTube：`"de-DE"` → `"de"`（按 `-` 分割）
- 对于 Aura：直接`"de-DE"`

### 在测试前禁用自动翻译器：
__代码_块_16__
否则，Aura 会将德语文本翻译成英语，这会破坏 WER 测量结果。

---

## 7. 已知问题及解决方案

|问题 |原因 |修复 |
|---|---|---|
|立即“跳过”|未找到 YouTube 文字记录 |调用 `api.list('video_id')` 查看可用语言 |
|音频后“跳过”|未找到 Vosk 型号 |代码中的 `language.split("-")[0]` 后备 |
| `找到 0 条 FUZZY_MAP_pre 规则` |错误的语言代码传递给 Aura |使用 `"de-DE"` 而不是 `"de"` |
| `连接被拒绝 8010` | LT 未启动 |先启动 Aura，等待 60 秒 |
| `zsh：终止` | X11 看门狗杀死进程 |使用 `SDL_VIDEODRIVER=dummy`；提高看门狗门槛|
| YouTube `>>` 标记 |文字记录中的第二位发言者 | `re.sub(r'>>', '', text)` — 仅删除 `>>`，保留单词 |
| `属性错误：get_transcript` | youtube-transcript-api v1.x | youtube-transcript-api v1.x |使用 `api = YouTubeTranscriptApi(); api.fetch(...)` |
|缓存包含空文本 |正则表达式损坏的旧运行 | `rm 固定装置/youtube_clips/*.transcript.json` |

---

## 8. 到目前为止的结果

### 视频：`sOjRNICiZ7Q`（德语），片段 5–20 秒

__代码_块_17__

**观察结果：**
- Aura 应用了规则：`zehn 手指` → `10 手指` ✅
- 本次运行期间的 LT 状态不清楚 - 连接被拒绝
- 高 WER 是由于片段选择：YouTube 转录内容以 Vosk 听不到的单词开头（扬声器尚未对准麦克风）
- **建议：** 将片段移至语音清晰的部分

---

## 9. 建议的后续步骤

1. **选择更好的片段** — 使用 `ffplay` 找到语音清晰的确切秒数
2. **测试前验证 LT 状态** — 运行前`curl http://localhost:8010/v2/linguals`
3. **添加模式 C 测试** — 包含已知语音命令的片段（`expected_output`）
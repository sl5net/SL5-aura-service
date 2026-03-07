## 目标：“听写会话”模型

### Unser Ziel（德语）：Die "Diktier-Sitzung"

Ein einziger Trigger startet eine **“Diktier-Sitzung”**，die aus drei Phasen besteht：

1. **开始阶段（Warten auf Sprache）：**
* Nach dem 触发系统。
* Wenn **keine** Spracheingabe erfolgt, endet die gesamte Sitzung nach `PRE_RECORDING_TIMEOUT` (z.B. 12s)。

2. **活动阶段（Kontinuierliches Diktieren）：**
* Sobald die erste Spracheingabe erkannt wrd, wechselt die Sitzung in den aktiven Modus。
* 在 VOSK eine Sprechpause erkennt 和 einen Textblock liefert (z.B. einen Satz) 中，wird dieser Block **sofort** zur Verarbeitung（LanguageTool 等） weitergegeben 和 als Text ausgegeben。
* Die Aufnahme läuft währenddessen **nahtlos weiter**。 Die Sitzung wartet auf den nächsten Satz。

3. **结束阶段（Ende der Sitzung）：**
* Die gesamte Sitzung endet nur, wenn eine dieser beiden Bedingungen erfüllt ist:
* Der Nutzer bleibt für die Dauer des `SPEECH_PAUSE_TIMEOUT` (z.B. 1-2s) 仍然完成。
* Der Nutzer stoppt die Sitzung manuell per Trigger。

**Zusammengefast：** Eine Sitzung，viele sofortige Textausgaben。启动后，Nutzer 会暂停并暂停。


### **目标：“听写会话”模型**

单个触发器启动**“听写会话”**，它由三个阶段组成：
1. **启动阶段（等待发言）：**
* 触发后，系统开始监听。
* 如果**未检测到语音**，整个会话将在“PRE_RECORDING_TIMEOUT”（例如 12 秒）后终止。
2. **活动阶段（连续听写）：**
* 一旦检测到第一个语音输入，会话就会切换到活动模式。
* 每当 VOSK 检测到暂停并传送文本块（例如，句子）时，该块就会**立即**传递到处理管道（LanguageTool 等）并作为文本输出。
* 录音在后台**无缝**继续，等待下一句话。
3. **终止阶段（结束会话）：**
* 仅当满足两个条件之一时整个会话才会终止：
* 用户在“SPEECH_PAUSE_TIMEOUT”期间（例如 1-2 秒）保持完全沉默。
* 用户通过触发器手动停止会话。
**简而言之：** 一次会话，多个即时文本输出。会话保持活动状态，直到用户长时间暂停或手动终止它。
# 🧠 SL5 Aura：Erweiterte 离线 LLM 集成

**状态：** Produktionsbereit
**发动机：** Ollama (Llama 3.2 3B)
**延迟：** Sofort（缓存命中<0.1s）/~20s（Generierung auf CPU）

## 1.“Architekt & Praktikant”哲学
Aura nutzt ein Hybrid-Modell，嗯 **Präzision** 和 **Flexibilität** zu vereinen：
* **Der Architekt (RegEx/Python)：** 确定性，sofortige Ausführung für Systembefehle（“浏览器 öffnen”、“Lauter”）。
* **Der Praktikant (Lokales LLM)：** Übernimt unscharfe Anfragen、Zusammenfassungen und Allgemeinwissen。 Wird nur aktiv，wenn keine strikte Regel greift。

---

## 2. 性能架构

Um ein lokales LLM auf normalen CPUs (ohne GPU) nutzbar zu machen, setzen wir auf eine **3-Stufen-Strategie**:

### Stufe 1：“即时模式”（Schlagworte）
* **触发器：** Wörter wie“即时”、“Schnell”、“Sofort”。
* **逻辑：** Umgeht das LLM komplett。直接与 SQLite-Datanbank 进行交互。
* **延迟：** **< 0.05s**

### Stufe 2：智能缓存 (SQLite)
* **逻辑：** Jeder Prompt wird gehasht (SHA256)。您可以使用 `llm_cache.db` geprüft 来 Anfrage 和 Ollama。
* **“主动变化”功能：** Auch bei einem Cache-Treffer Geniert das System manchmal (20% Chance) proaktiv eine *neue* Antwort-Variante。 Ziel：~5 Varianten pro Frage für mehr Lebendigkeit。
* **功能“语义散列”：** Bei langen Fragen (>50 Zeichen) extrahiert das LLM zuerst keywords (z.B.“installation anleitung”) und hasht diese。那么“Wie installiere ich es?”是怎么回事？和“Installationshilfe bitte”是相同的。
* **延迟：** **~0.1s**

### Stufe 3：Die API-Generierung（后备）
* **逻辑：** Wenn kein Cache 存在，rufen wir die Ollama API (`http://localhost:11434/api/generate`)。
* **优化：**
* **硬限制：** `num_predict=60` zwingt das Modell，nach ca。 40 Wörtern zu stoppen。
* **输入管道：** Große Texte (README) werden über STDIN übergeben, um Argumenten-Limits des Betriebssystems zu umgehen。
* **延迟：** **~15-25s** (abhängig von CPU)

---

## 3. 系统接地（防幻觉）

通用法学硕士经常使用 GUI（按钮、菜单）。 Wir injizieren bei jedem Aufruf das strikte **`AURA_TECH_PROFILE`**：

1. **Keine GUI：** Aura 是 Headless CLI-Dienst 中的。
2. **Keine 配置文件：** Logik ist reiner Python-Code, kein `.json`/`.xml`。
3. **触发器：** 外部 Steuerung erfolgt über Dateisystem-Events (`touch /tmp/sl5_record.trigger`)，nicht über API。
4. **安装：** Dauert real 10-20 分钟 4GB 模型下载 (verhindert falsche Versprechen)。

---

## 4. 芯片剪贴板桥（Linux 安全）

Hintergrunddienste (systemd) können aus Sicherheitsgründen oft nicht auf die Zwischenablage (X11/Wayland) zugreifen。
* **说明：** 用户会话中的 Skript (`clipboard_bridge.sh`) 是在 RAM-Disk-Datei (`/tmp/aura_clipboard.txt`) 中吸入的。
* **光环：** Liest diese Datei und umgeht so alle Rechte-Probleme。

---

## 5.Selbst-Lernen（缓存预热）

Wir nutzen das Skript `warm_up_cache.py`：
1. 这是项目的“README.md”。
2. Es beauftragt das LLM，sich wahrscheinliche User-Fragen auszudenken。
3. Es stellt diese Fragen an Aura, um die Datenbank automatisch zu befüllen。
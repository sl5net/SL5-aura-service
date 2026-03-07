## 配置的 Mächtigkeit：Keine Programmierung notwendig

系统的初始结构是一种复杂的复杂系统，而不是传统的程序设计。

### 1. Fokussierung auf 配置统计代码

在 **Konfiguration** der Regel-Tupel (`(Zielwert, Regex-Muster, Fuzzy-Wert, Optionen)`) 中实现完整的系统逻辑，并在 **physical Position** dieser Regeln in den jeweiligen Dateien (Modul-Reihenfolge und Zeilennummer)优先。

* **关键程序不是：** 新的转换或特殊的Verhaltensweisen erfordern Eingreifen in den Kerncode order die Anwendung komplexer Funktionen, sondern lediglich das Hinzufügen order Neuanordnen von Konfigurationseinträgen in den Mapping-Dateien.

### 2. Die Rolle von Regulären Ausdrücken (Regex)

正则表达式配置的基本配置（z. B. einfache String-Ersetzung bei exaktem Full Match），以及 **正则表达式 (PregReg)** 的集成，是一个非常重要的功能。

* **请注意以下事项：** 对于我的 Anwendungsfälle，请参阅 Stopp-Kriterien (`^Wort$`) 或 Inklusionsmustern 的定义，因为它是 Regex-Kenntnisse erforderlich 的元素。
* **专家的操作：** Wer komplexe Muster (Lookaheads wie `(?!Haus)`) nutzen mochte, kann dies tun, um hochspezifische Kontrollmechanismen zu Implementieren, ohne die Einfachheit für Gelegenheitsnutzer zu opfern.
* **Möglichkeit für Experten:** Geräte/Spiele zu steuern ... siehe 插件 **config/maps/plugins/game/0ad/**

**Fazit：** Das System ist darauf ausgelegt，ein maximales Maß an Kontrolle über die Textverarbeitung zu bieten，wobei die **Regel-Daten** die Geschäftslogik definieren und die Kern-Engine lediglich der zuverlässige Interpret und Ausführer dieser Prioritäten und Kaskaden是。
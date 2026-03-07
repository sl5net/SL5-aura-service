## Regelwerks 的灵活性：Von Binärlogik zur Komplexität

Die kombinierte Prioritäts- und Verarbeitungslogik (sequentielle Sortierung, Full Match Stopp, Kumulation, Fuzzy-Fallback) bietet eine bemerkenswerte Flexibilität:

### 1. Einfache (Binäre) Steuerung durch höchste Priorität

在位置上 **höchst Priorisierten Regel mit einem Full Match Stopp** kann ein einfacher Ein-/Ausschalt-Mechanismus (`Toggle`) konfiguriert werden。

* **说明：** Eine Regel ganz oben in `FUZZY_MAP_pre` 可以最好地使用 Eingabestring (z. B. ein einfaches Kommandowort) erkennen、sofort verarbeiten 和 damit die gesamte nachfolgende Kaskade für dieses Token blockieren。执行命令或Zuständen 时的配置，即为Worte/Befehle zulassen。

### 2. 复杂的分析和框架集成

复杂的实施、修改、特殊框架的设计（即 CodeIgniter 或其他）不是这样的：

* **累积：** 在文本范围内进行累积，然后将其顺序排列，以在最佳实践中使用 Benennungskonventionen 或 Platzhalter eines Frameworks schrittweise。
* **插件：** 层次结构 Ladelogik über `plugins/` stellt sicher，dass projektspezifische oder Frameworkspezifische Regeln (z. B. für CodeIgniter) 以及单独的模块 hinzugefügt werden können。插件管理已定义，优先级为内核语言，内核逻辑未定义，并且已定义。

**方法：** Ob es sich um die binäre Umschaltung von Steuerwörtern oder dieDetaillierte Anpassung and die Konventionen eines komplexen Frameworks handelt – die Hierarchie der Prioritäten (Modul > Zeile) und die Steuerung durch das Stopp-Kriterium des Full Match bieten die nötige Kontrolle über den Verarbeitungsprozess。
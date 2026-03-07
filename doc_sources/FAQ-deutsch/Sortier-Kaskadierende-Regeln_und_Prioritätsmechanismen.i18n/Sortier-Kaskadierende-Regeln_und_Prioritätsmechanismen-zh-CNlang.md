# Kaskadierende Regelausführung und Priorität Mechanismen

所有其他细节、优先级、模式和后备的复杂性。

---

# Kaskadierende Regelausführung und Priorität Mechanismen

Unser Regelsystem basic auf einer strikten, sequenziellen Verarbeitung, bei der die Positioneiner Regel in der Liste `fuzzy_map_pre` ihre Priorität bestimmt (Modul-Lade-Reihenfolge > Zeilennummer)。

根据 **Kaskadierenden Regelausführung** 的原理（`default_mode_is_all = True`），我将在 Regeln nacheinander angewendet werden 上进行所有操作，这是一种特殊的 Stopp-Kriterium erfüllt。

## 1. Die Hohe Priorität：确定性杜尔奇劳夫

Die Verarbeitung 是从 Durchlauf der Regeln in der geladenen Reihenfolge 开始的。 Hierbei gibt es zwei Typen von Anwendungen, die die Priorität festlegen:

### A. Absolutes Stopp-Kriterium (Höchste Priorität)
Die Regel mit der höchsten Priorität, die einen **vollständigen Match** (von `^` bis `$`) auf das Token erzielt, wird angewendet und Beendet die gesamte Verarbeitung für dieses Token sofort (**第一场比赛获胜**)。这就是 Regel Vorrang 帽子的特殊性和决定性。

### B. 累积（Transformationsreihenfolge）
Wenn eine Regel zutrifft， aber keinen vollständigen Match (`^...$`) erzielt，wird die Ersetzung angewendet。 Die Verarbeitung geht jedoch zur nächsten Regel über。 Da jede Regel auf dem **bereits modifizierten** Text arbeitet, ist die Listenreihenfolge entscheidend für die **Kaskadierung** der Transformationen.

## 2. Die Niedrige Priorität：模糊后备

Der Einsatz der Fuzzy-Logik (ähnlichkeitsscore 0–100) dient ausschließlich als Fallback, um Tippfehler im Rohtext zu korrigieren.

Aus Performance- und Stabilitätsgründen wird die Fuzzy-Logik **nur dann** aktiviert, wenn der gesamte defistische Durchlauf (Punkt 1) **keine einzige Regel** angewendet hat. Jede erfolgreiche Regelanwendung setzt die notwendige Flag und **blockiert** damit den Fuzzy-Fallback für das aktuelle Token.

## 3. 外部验证（语言工具）

Nach Abschluss aller Regel-basierten Ersetzungen wird eine zusätzliche Prüfung durch LanguageTool (LT) durchgeführt, um stilistische oder grammatikalische Fehler zu beheben.

使用该工具时，请使用 Textlänge einen Schwellenwert übersteigt (`LT_SKIP_RATIO_THRESHOLD`)。就这样，LT nicht auf Texte angewendet wird，die durch unsere Kaskade bereits so stark transtiert wurden，dass die Korrektur durch LT fehleranfällig wäre。
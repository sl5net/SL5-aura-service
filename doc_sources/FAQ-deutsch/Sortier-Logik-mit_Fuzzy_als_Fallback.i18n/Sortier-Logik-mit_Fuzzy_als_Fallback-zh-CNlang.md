# Prioritätslogik (mit Fuzzy als Fallback)
模糊测试的复杂性可以作为后备参数。


---

## Die neue Prioritätslogik (mit Fuzzy als Fallback)

Mit dieser Bedingung (`if not current_rule_matched:`)，在与 Modus `default_mode_is_all = True` (Kumulierung) 的组合中，ergibt sich ein **zweistufiger Prioritätäts-Workflow**：

### 第一阶段：高优先级（确定性）Durchlauf

Die Engine durchläuft die gesamte Liste `fuzzy_map_pre` (Modul-Reihenfolge > Zeilennummer)。

#### A. Stopp-Kriterium (Höchste Priorität)

Wenn eine Regel einen **完整匹配** (`^...$`) erzielt，stoppt die Verarbeitung für dieses Token sofort。

* **优先顺序：** Die Regel，die am höchsten in der Liste steht und einen Full Match erzielt，gewinnt definitiv und bedet den Prozess。

#### B. Kumulations-Kriterium (Hohe Priorität)

Wenn eine Regel **keinen Full Match**, aber einen **partiellen Match** oder eine sonstige Ersetzung (ohne Stopp-Kriterium) erzielt:

* Die Ersetzung wird angewendet。
* **WIHTIG：** 模具变量“current_rule_matched”与“True”gesetzt。
* Die Verarbeitung geht zur nächsten Regel über（累积）。

**优先顺序：** Reihenfolge der Regeln ist hier entscheidend für die **Anwendungsreihenfolge**。 Frühere Regeln modifizieren den für spätere Regeln 的文本。

---

### 第 2 阶段：低优先级（模糊）后备

Der Fuzzy-Check wird nur ausgelöst, wenn der gesamte defistische Durchlauf (Phase 1) abgeschlossen ist und **keine einzige Regel** angewendet wurde (`current_rule_matched` ist immer noch `False`).

Wenn der Fuzzy-Check ausgeführt wird，镀金：

1. Die Fuzzy-Funktion sucht im gesamten Text nach Wörtern, die dem **Zielwert** (`replacement`) ähnlich sind (basierend auf der Schwelle)。
2. 在模糊匹配中进行模糊匹配，然后再进行设置。
3. **WICHTIG：** Die **Fuzzy-Funktion stoppt die Verarbeitung sofort，nachdem der erste Fuzzy-Match gefunden wurde**。

#### 模糊管理的优先级是：

__代码_块_0__

**模糊功能，wird nur am Ende aufgerufen。

---

## Finales Prioritäts-Fazit

Unabhängig davon，wie die Fuzzy-Suche im Detail Implementiert ist，solange die **确定性阶段（阶段 1）** zuerst 和 in der Reihenfolge der Liste durchläuft，镀金：

**Die höchste Priorität liegt bei den Regeln，die ganz oben in `fuzzy_map_pre` stehen，以及 sich an der Decisionismus-Logik beteiligen（完全匹配或累积）。**

1. **Regeln mit Stopp-Kriterium (^...$):** Müssen zuerst stehen, um ihre hohe Priorität auszuspielen。
2. **Regeln zur Kumulation（部分匹配）：** Müssen in der logischen Reihenfolge der Transformationen stehen (vom Rohtext zur Finalen Form)。 Sie setzen `current_rule_matched` auf `True` 和 **blockieren** damit den späteren Fuzzy-Fallbacks for diesen Token.
3. **模糊后备：** Dies ist die **niedrigste Priorität**。在我们行动之前，我们已经决定了决定论的全部内容。

**Wichtig：** Jede Regel（auch eine kumulierende，nicht-stoppende Regel），在第 1 阶段 zuschlägt 中死亡，**deaktiviert den Fuzzy-Fallback** für dieses Token。死因是设计 der Generischen Regeln berücksichtigt werden。
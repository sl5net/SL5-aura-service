# Prioritätslogik (z Fuzzy jako awarią)
Die komplekse Fuzzy-Berechnungen werden nur als Fallback genutzt.


---

## Die neue Prioritätslogik (mit Fuzzy als Fallback)

Mit dieser Bedingung (`if not current_rule_matched:`), in Kombination mit dem Modus `default_mode_is_all = True` (Kumulierung), ergibt sich ein **zweistufiger Prioritäts-Workflow**:

### Faza 1: Der Highpriorytet (Deterministische) Durchlauf

Die Engine durchläuft die gesamte Liste `fuzzy_map_pre` (Modul-Reihenfolge > Zeilennummer).

#### A. Stopp-Kriterium (Höchste Priorität)

Wenn eine Regel einen **Full Match** (`^...$`) stwórz, zatrzymaj Verarbeitung für dieses Token sofort.

* **Prioritäts-Konsequenz:** Die Regel, die am höchsten in der Liste steht und einen Full Match erzielt, gewinnt definitiv und bedet den Prozess.

#### B. Kumulations-Kriterium (Hohe Priorität)

Wenn eine Regel **keinen Full Match**, aber einen **partiellen Match** lub eine sonstige Ersetzung (ohne Stopp-Kriterium) erzielt:

* Die Ersetzung wird angewendet.
* **WICHTIG:** Zmienna `current_rule_matched` wird auf `True` gesetzt.
* Die Verarbeitung geht zur nächsten Regel über (Kumulacja).

**Prioritäts-Konsequenz:** Die Reihenfolge der Regeln ist hier entscheidend für die **Anwendungsreihenfolge**. Frühere Regeln modifizieren den Text für spätere Regeln.

---

### Faza 2: Rezerwa awaryjna o niskim priorytecie (rozmyta).

Der Fuzzy-Check wird nur ausgelöst, wenn der gesamte deterministische Durchlauf (Phase 1) abgeschlossen ist und **keine einzige Regel** angewendet wurde („current_rule_matched” ist immer noch `False`).

Wenn der Fuzzy-Check ausgeführt wird, złocony:

1. Die Fuzzy-Funktion sucht im gesamten Text nach Wörtern, die dem **Zielwert** („zastąpienie”) ähnlich sind (basierend auf der Schwelle).
2. Wenn ein Fuzzy-Match gefunden wird, erfolgt die Ersetzung.
3. **WICHTIG:** Die **fuzzy-Funktion stoppt die Verarbeitung sofort, nachdem der erste Fuzzy-Match gefunden wurde**.

#### Was das für die Priorität der Fuzzy-Regeln bedeutet:

__KOD_BLOKU_0__

**Die Fuzzy-Funktion, wird nur am Ende aufgerufen.

---

## Finały Prioritäts-Fazit

Unabhängig davon, wie die Fuzzy-Suche im Detail implementiert ist, solange die **deterministische Phase (Phase 1)** zuerst und in der Reihenfolge der Liste durchläuft, złocony:

**Die höchste Priorität Liegt bei den Regeln, die ganz oben in `fuzzy_map_pre` stehen, und sich an der Determinismus-Logik beteiligen (Pełny mecz lub Kumulacja).**

1. **Regeln mit Stopp-Kriterium (^...$):** Müssen zuerst stehen, um ihre hohe Priorität auszuspielen.
2. **Regeln zur Kumulation (mecz partiellerowy):** Müssen in der logischen Reihenfolge der Transformationen stehen (vom Rohtext zur finalen Form). Sie setzen `current_rule_matched` auf `True` i **blockieren** damit den späteren Fuzzy-Fallbacks für diesen Token.
3. **Fuzzy-Fallback:** Dies ist die **niedrigste Priorität**. Es wird nur aktiv, wenn die gesamte Kaskade der deterministischen Regeln versagt hat.

**Wichtig:** Jede Regel (auch eine kumulierende, nicht-stoppende Regel), umrzeć w fazie 1 zuschlägt, **deaktiviert den Fuzzy-Fallback** für dieses Token. Dies muss beim Design der generischen Regeln berücksichtigt werden.
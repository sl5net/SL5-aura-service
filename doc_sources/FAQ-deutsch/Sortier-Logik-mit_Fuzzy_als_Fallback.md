# Prioritätslogik (mit Fuzzy als Fallback)
Die komplexe Fuzzy-Berechnungen werden nur als Fallback genutzt.


---

## Die neue Prioritätslogik (mit Fuzzy als Fallback)

Mit dieser Bedingung (`if not current_rule_matched:`), in Kombination mit dem Modus `default_mode_is_all = True` (Kumulierung), ergibt sich ein **zweistufiger Prioritäts-Workflow**:

### Phase 1: Der High-Priority (Deterministische) Durchlauf

Die Engine durchläuft die gesamte Liste `fuzzy_map_pre` (Modul-Reihenfolge > Zeilennummer).

#### A. Stopp-Kriterium (Höchste Priorität)

Wenn eine Regel einen **Full Match** (`^...$`) erzielt, stoppt die Verarbeitung für dieses Token sofort.

*   **Prioritäts-Konsequenz:** Die Regel, die am höchsten in der Liste steht und einen Full Match erzielt, gewinnt definitiv und beendet den Prozess.

#### B. Kumulations-Kriterium (Hohe Priorität)

Wenn eine Regel **keinen Full Match**, aber einen **partiellen Match** oder eine sonstige Ersetzung (ohne Stopp-Kriterium) erzielt:

*   Die Ersetzung wird angewendet.
*   **WICHTIG:** Die Variable `current_rule_matched` wird auf `True` gesetzt.
*   Die Verarbeitung geht zur nächsten Regel über (Kumulation).

**Prioritäts-Konsequenz:** Die Reihenfolge der Regeln ist hier entscheidend für die **Anwendungsreihenfolge**. Frühere Regeln modifizieren den Text für spätere Regeln.

---

### Phase 2: Der Low-Priority (Fuzzy) Fallback

Der Fuzzy-Check wird nur ausgelöst, wenn der gesamte deterministische Durchlauf (Phase 1) abgeschlossen ist und **keine einzige Regel** angewendet wurde (`current_rule_matched` ist immer noch `False`).

Wenn der Fuzzy-Check ausgeführt wird, gilt:

1.  Die Fuzzy-Funktion sucht im gesamten Text nach Wörtern, die dem **Zielwert** (`replacement`) ähnlich sind (basierend auf der Schwelle).
2.  Wenn ein Fuzzy-Match gefunden wird, erfolgt die Ersetzung.
3.  **WICHTIG:** Die **die Fuzzy-Funktion stoppt die Verarbeitung sofort, nachdem der erste Fuzzy-Match gefunden wurde**.

#### Was das für die Priorität der Fuzzy-Regeln bedeutet:

```python
# Pseudo-Code:
for rule in fuzzy_map_pre:
    # 1. Deterministic/Regex checks here...

# Wenn Phase 1 beendet ist und KEIN Match gefunden wurde:
if not current_rule_matched:
    # 2. Fuzzy Fallback
    for rule in fuzzy_map_pre: # WIRD HIER DIE LISTE NOCHMAL DURCHLAUFEN?
        # Führe den Fuzzy-Check auf Basis der replacement/threshold der Regel durch.
```

**Die Fuzzy-Funktion, wird nur am Ende aufgerufen.

---

## Finales Prioritäts-Fazit

Unabhängig davon, wie die Fuzzy-Suche im Detail implementiert ist, solange die **deterministische Phase (Phase 1)** zuerst und in der Reihenfolge der Liste durchläuft, gilt:

**Die höchste Priorität liegt bei den Regeln, die ganz oben in `fuzzy_map_pre` stehen, und sich an der Determinismus-Logik beteiligen (Full Match oder Kumulation).**

1.  **Regeln mit Stopp-Kriterium (^...$):** Müssen zuerst stehen, um ihre hohe Priorität auszuspielen.
2.  **Regeln zur Kumulation (partieller Match):** Müssen in der logischen Reihenfolge der Transformationen stehen (vom Rohtext zur finalen Form). Sie setzen `current_rule_matched` auf `True` und **blockieren** damit den späteren Fuzzy-Fallbacks für diesen Token.
3.  **Fuzzy-Fallback:** Dies ist die **niedrigste Priorität**. Es wird nur aktiv, wenn die gesamte Kaskade der deterministischen Regeln versagt hat.

**Wichtig:** Jede Regel (auch eine kumulierende, nicht-stoppende Regel), die in Phase 1 zuschlägt, **deaktiviert den Fuzzy-Fallback** für dieses Token. Dies muss beim Design der generischen Regeln berücksichtigt werden.

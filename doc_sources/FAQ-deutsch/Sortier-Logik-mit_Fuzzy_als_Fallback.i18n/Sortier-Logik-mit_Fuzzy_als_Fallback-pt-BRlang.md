# Prioridade lógica (com Fuzzy e Fallback)
O complexo Fuzzy-Berechnungen foi criado apenas como Fallback.


---

## A nova lógica de prioridade (com Fuzzy e Fallback)

Com esta configuração (`if not current_rule_matched:`), em combinação com o modo `default_mode_is_all = True` (Kumulierung), ergibt sich ein **zweistufiger Prioritäts-Workflow**:

### Fase 1: A Alta Prioridade (Deterministische) Durchlauf

O motor fornece a lista `fuzzy_map_pre` (Modul-Reihenfolge > Zeilennummer).

#### A. Stopp-Kriterium (Höchste Priorität)

Se um Regel einen **Full Match** (`^...$`) for exibido, pare a Verarbeitung para este Token sofort.

* **Consequências prioritárias:** Die Regel, die am höchsten in der Liste steht und einen Full Match erzielt, gewinnt definitiv und bedet den Prozess.

#### B. Kumulations-Kriterium (Hohe Priorität)

Quando um Regel **keinen Full Match**, ou um **partiellen Match** ou um sontige Ersetzung (ohne Stopp-Kriterium) erzielt:

* Die Ersetzung wird angewendet.
* **WICHTIG:** A variável `current_rule_matched` será definida como `True`.
* Die Verarbeitung geht zur nächsten Regel über (Kumulation).

**Prioritäts-Konsequenz:** Die Reihenfolge der Regeln ist hier entscheidend für die **Anwendungsreihenfolge**. Frühere Regeln modifica o texto para spätere Regeln.

---

### Fase 2: Fallback de baixa prioridade (fuzzy)

O Fuzzy-Check foi apenas usado quando o gesamte deterministische Durchlauf (Fase 1) foi fechado e **nenhuma regra** foi alterada (`current_rule_matched` é mais tarde `False`).

Wenn der Fuzzy-Check ausgeführt wird, dourado:

1. A função Fuzzy é a mesma do texto nach Wörtern, die dem **Zielwert** (`replacement`) ähnlich sind (basierend auf der Schwelle).
2. Quando um Fuzzy-Match for encontrado, siga a configuração.
3. **WICHTIG:** Die **die Fuzzy-Funktion stoppt die Verarbeitung sofort, nachdem der erste Fuzzy-Match gefunden wurde**.

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

**A função difusa será finalmente atualizada.

---

## Finales Prioritäts-Fazit

Unabhängig davon, wie the Fuzzy-Suche im Detail implementiert ist, solange the **deterministische Phase (Phase 1)** zuerst und in der Reihenfolge der Liste durcläuft, gilt:

**A prioridade mais alta é a regra, o ganz oben em `fuzzy_map_pre` stehen, e assim por diante o Determinismo-Logik beteiligen (Full Match ou Kumulation).**

1. **Regeln mit Stopp-Kriterium (^...$):** Müssen zuerst stehen, um ihre hohe Priorität auszuspielen.
2. **Regeln zur Kumulation (partieller Match):** Müssen in der logischen Reihenfolge der Transformationen stehen (do Rohtext zur finalen Form). Você define `current_rule_matched` em `True` e **bloqueia** os Fuzzy-Fallbacks para esse Token.
3. **Fuzzy-Fallback:** Dies ist die **niedrigste Priorität**. Ele está sempre ativo quando o conjunto de regras determinísticas é aplicado.

**O que é importante:** Jede Regel (auch eine kumulierende, nicht-stoppende Regel), morre na Fase 1 zuschlägt, **deaktiviert den Fuzzy-Fallback** para este Token. Dies muss beim Design der generischen Regeln berücksichtigt werden.
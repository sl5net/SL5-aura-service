# 우선순위(Fuzzy와 Fallback 포함)
Fuzzy-Berechnungen werden nur als Fallback Genutzt의 Komplexe Komplexe가 있습니다.


---

## Die neue Prioritätslogik(Fuzzy와 Fallback 포함)

Mit dieser Bedingung(`if not current_rule_matched:`), in Kombination mit dem Modus `default_mode_is_all = True`(Kumulierung), ergibt sich ein **zweistufiger Prioritäts-Workflow**:

### 1단계: 높은 우선순위(결정) Durchlauf

Die Engine durchläuft die gesamte Liste `fuzzy_map_pre`(Modul-Reihenfolge > Zeilennummer).

#### A. Stopp-Kriterium(Höchste Priorität)

Wenn eine Regel einen **Full Match** (`^...$`) erzielt, stoppt die Verarbeitung für dieses Token sofort.

* **우선 순위 설명:** Die Regel, die am höchsten in der Liste steht und einen Full Match erzielt, gewinnt definitiv und beendet den Prozess.

#### B. Kumulations-Kriterium (Hohe Priorität)

Wenn eine Regel **keinen Full Match**, aber einen **partiellen Match** oder eine sonstige Ersetzung (ohne Stopp-Kriterium) erzielt:

* Die Ersetzung wird angewende.
* **WICHTIG:** 다이 변수 `current_rule_matched` wird auf `True` gesetzt.
* Die Verarbeitung geht zur nächsten Regel über(Kumulation).

**Prioritäts-Konsequenz:** Die Reihenfolge der Regeln ist hier entscheidend für die **Anwendungsreihenfolge**. Frühere Regeln modifizieren den Text für spätere Regeln.

---

### 2단계: 낮은 우선순위(퍼지) 폴백

Der Fuzzy-Check wird nur ausgelöst, wenn der gesamte deterministische Durchlauf(1단계) abgeschlossen ist und **keine einzige Regel** angewendet wurde(`current_rule_matched` ist immer noch `False`).

Wenn der Fuzzy-Check ausgeführt wird, gilt:

1. Die Fuzzy-Funktion sucht im gesamten Text nach Wörtern, die dem **Zielwert** (`replacement`) ähnlich sind (basierend auf der Schwelle).
2. Wenn ein Fuzzy-Match gefunden wird, erfolgt die Ersetzung.
3. **WICHTIG:** Die **fuzzy-Funktion stoppt die Verarbeitung sofort, nachdem derste Fuzzy-Match gefunden wurde**.

#### Fuzzy-Regeln의 우선 순위가 다음과 같았습니다.

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

**Die Fuzzy-Funktion, ende aufgerufen의 경우도 마찬가지입니다.

---

## Finales Prioritäts-Fazit

Unabhängig davon, wie die Fuzzy-Suche im Detail Implementiert ist, solange die **결정론적 단계(1단계)** zuerst und in der Reihenfolge der Liste durchläuft, gilt:

**Die höchste Priorität liegt bei den Regeln, die ganz oben in `fuzzy_map_pre` stehen, und sich an der Determinismus-Logik beteiligen(Full Match oder Kumulation).**

1. **Regeln mit Stopp-Kriterium (^...$):** Müssen zuerst stehen, um ihre hohe Priorität auszuspielen.
2. **Regeln zur Kumulation(partieller Match):** Müssen in der logischen Reihenfolge der Transformationen stehen(vom Rohtext zur finalen Form). 'current_rule_matched'를 'True'로 설정하고 **차단**하여 디젠 토큰에 대한 퍼지 폴백을 차단했습니다.
3. **퍼지 폴백:** 죽는 것은 **우선 순위**입니다. 활동이 활발할 경우 Kaskade의 결정론적 위치를 변경하는 것이 가능합니다.

**위치:** Jede Regel(Auch eine kumulierende, nicht-stoppende Regel), 1단계에서 사망, **deaktiviert den Fuzzy-Fallback** für dieses Token. Dies Muss beim Design der generischen Regeln berücksichtigt werden.
# Prioridades lógicas (con Fuzzy y Fallback)
El complejo Fuzzy-Berechnungen no es más que un respaldo genuino.


---

## La nueva lógica de prioridades (con Fuzzy y Fallback)

Con esta información (`if not current_rule_matched:`), en combinación con el modo `default_mode_is_all = True` (Kumulierung), ergibt sich ein **zweistufiger Prioritäts-Workflow**:

### Fase 1: Der High-Priority (Deterministische) Durchlauf

El motor utiliza la lista asignada `fuzzy_map_pre` (Modul-Reihenfolge > Zeilennummer).

#### A. Stopp-Kriterium (Höchste Priorität)

Cuando se activa un **Partido completo** (`^...$`), se detiene la conversión para este token de forma segura.

* **Consecuencias prioritarias:** Die Regel, die am höchsten in der Liste steht und einen Full Match erzielt, gewinnt definitiv und beendet den Prozess.

#### B. Kumulaciones-Kriterium (Hohe Priorität)

Cuando un Regel **no es Full Match**, aber einen **partiellen Match** oder eine sonstige Ersetzung (ohne Stopp-Kriterium) erzielt:

* Die Ersetzung wird angewendet.
* **WICHTIG:** La variable `current_rule_matched` se activa en `True`.
* Die Verarbeitung geht zur nächsten Regel über (Kumulación).

**Consecuencias prioritarias:** Die Reihenfolge der Regeln ist hier entscheidend für die **Anwendungsreihenfolge**. Frühere Regeln modificazieren den Text für spätere Regeln.

---

### Fase 2: El retroceso de baja prioridad (difuso)

Der Fuzzy-Check no será ausgelöst, cuando el gesamte deterministische Durchlauf (Fase 1) se abgeschlossen y **keine einzige Regel** angewendet wurde (`current_rule_matched` ist immer noch `False`).

Wenn der Fuzzy-Check ausgeführt wird, dorado:

1. La función Fuzzy tal como se escribe en el texto en el trabajo, el **Zielwert** ("reemplazo") está disponible (basierend auf der Schwelle).
2. Cuando se utiliza un Fuzzy-Match, se activa la configuración.
3. **WICHTIG:** Die **die Fuzzy-Funktion stoppt die Verarbeitung sofort, nachdem der erste Fuzzy-Match gefunden wurde**.

#### Fue la prioridad para las reglas difusas:

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

**La función Fuzzy no se activará hasta el final.

---

## Finales Prioritäts-Fazit

Unabhängig davon, wie die Fuzzy-Suche im Detail implementiert ist, solange die **deterministische Phase (Phase 1)** zuerst und in der Reihenfolge der Liste durchläuft, gilt:

**Die höchste Priorität liegt bei den Regeln, die ganz oben in `fuzzy_map_pre` stehen, y sich an der Determinismo-Logik beteiligen (Full Match o Kumulation).**

1. **Regeln mit Stopp-Kriterium (^...$):** Müssen zuerst stehen, um ihre hohe Priorität auszuspielen.
2. **Regeln zur Kumulation (partieller Match):** Müssen in der logischen Reihenfolge der Transformationen stehen (vom Rohtext zur finalen Form). Configure `current_rule_matched` en `True` y **bloquee** los Fuzzy-Fallbacks utilizados para este token.
3. **Fuzzy-Fallback:** Esta es la **prioridad negativa**. Es wird nur aktiv, wenn die gesamte Kaskade der deterministischen Regeln versagt hat.

**Wichtig:** Jede Regel (auch eine kumulierende, nicht-stoppende Regel), muere en la Fase 1 zuschlägt, **deaktiviert de Fuzzy-Fallback** para este Token. Dies muss beim Design der generischen Regeln berücksichtigt werden.
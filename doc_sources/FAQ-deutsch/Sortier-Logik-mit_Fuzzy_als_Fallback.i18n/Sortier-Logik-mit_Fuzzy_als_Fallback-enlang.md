> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../Sortier-Logik-mit_Fuzzy_als_Fallback.md).*

# Priority logic (with fuzzy as a fallback)
The complex fuzzy calculations are only used as a fallback.


---

## The new priority logic (with fuzzy as a fallback)

This condition (`if not current_rule_matched:`), in combination with the `default_mode_is_all = True` (cumulation) mode, results in a **two-stage priority workflow**:

### Phase 1: The High-Priority (Deterministic) Run

The engine goes through the entire list `fuzzy_map_pre` (module order > line number).

#### A. Stop criteria (highest priority)

If a rule achieves a **Full Match** (`^...$`), processing for that token stops immediately.

*   **Priority Consequence:** The rule that is highest in the list and achieves a full match definitely wins and ends the process.

#### B. Accumulation criterion (high priority)

If a rule achieves **not a full match**, but a **partial match** or other replacement (without stopping criteria):

*   The replacement is applied.
*   **IMPORTANT:** The variable `current_rule_matched` is set to `True`.
*   Processing moves on to the next rule (cumulation).

**Priority Consequence:** The order of the rules here is crucial for the **order of application**. Previous rules modify the text for later rules.

---

### Phase 2: The low-priority (fuzzy) fallback

The fuzzy check is only triggered when the entire deterministic run (Phase 1) is completed and **not a single rule** has been applied (`current_rule_matched` is still `False`).

When the fuzzy check is executed:

1.  The fuzzy function searches for words similar to the **target value** (`replacement`) throughout the text (based on the threshold).
2.  If a fuzzy match is found, the replacement occurs.
3.  **IMPORTANT:** The **fuzzy function stops processing immediately after the first fuzzy match is found**.

#### What this means for the priority of the fuzzy rules:

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

**The fuzzy function is only called at the end.

---

## Final priority conclusion

Regardless of how the fuzzy search is implemented in detail, as long as the **deterministic phase (Phase 1)** goes through first and in the order of the list, then:

**The highest priority goes to the rules at the top of `fuzzy_map_pre` that participate in determinism logic (full match or cumulation).**

1.  **Rules with stopping criteria (^...$):** Must come first to fulfill their high priority.
2.  **Rules for cumulation (partial match):** Must be in the logical order of transformations (from raw text to final form). You set `current_rule_matched` to `True` and thereby **block** future fuzzy fallbacks for this token.
3.  **Fuzzy fallback:** This is the **lowest priority**. It only becomes active when the entire cascade of deterministic rules has failed.

**Important:** Any rule (even a cumulative, non-stopping rule) that strikes in Phase 1 **disables the fuzzy fallback** for that token. This must be taken into account when designing the generic rules.

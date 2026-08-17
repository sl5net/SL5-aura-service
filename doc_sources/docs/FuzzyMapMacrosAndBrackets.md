# Fuzzy Map Macros and Bracket Logic

Aura supports grouping multiple preprocessing rules in `FUZZY_MAP_pre.py` files to execute them sequentially as a cohesive pipeline once a "Start Rule" is triggered. This document describes the design philosophy, syntax, and execution flow of this feature.

## Core Design Principles

1. **Zero Redundancy**: Rules inside a group remain standard Python tuples:
   `('replacement_text', r'regex_pattern', threshold, flags_and_options)`
2. **Double Usability**: Individual rules inside a group are fully functional standalone rules. If the group is not triggered, they are evaluated normally in the parent loop.
3. **Passive End Marker**: The end of a group is defined by a passive rule entry that is never matched on its own. It acts purely as a boundary marker for the parser.
4. **Hybrid Fallback (Append-on-Non-Match)**: When a group is active, every inner rule must contribute to the output. If an inner rule's regex matches the text, the normal substitution takes place. If it does not match, its replacement text is appended to the current text with a space.

---

## Syntax and Structure

A macro group is defined by wrapping a series of standard rules between a **Start Rule** and an **End Rule** in `FUZZY_MAP_pre.py`. 

### 1. The Start Rule
The start rule is a standard rule that triggers the macro when matched. It includes a `'group_start'` key in its options dictionary:
```python
('replacement', r'start_pattern', 100, {'group_start': 'unique_group_name'})
```

### 2. Inner Rules
Inner rules are standard rules placed sequentially after the Start Rule. They do not require any special metadata:
```python
('inner_replacement', r'inner_pattern', 100, {})
```

### 3. The End Rule (Passive Marker)
The end rule has a `None` replacement, an empty pattern, and a `'group_end'` key in its options dictionary:
```python
(None, r'', 100, {'group_end': 'unique_group_name'})
```

---

## Concrete Example

Here is a practical test case defined in a `FUZZY_MAP_pre.py` file:

```python
FUZZY_MAP_pre = [
    # Start Rule: Triggers the group 'sandbox_test' when "start sandbox" matches
    ('Sandbox:', r'start\w* sandbox', 100, {'group_start': 'sandbox_test'}),
    
    # Inner Rule 1: Replaces "apfel" with "birne" if present
    ('birne', r'apfel', 100, {}),
    
    # Inner Rule 2: Replaces "banane" if present, otherwise appends "banane"
    ('banane', r'banane', 100, {}),
    
    # End Rule: Passive boundary marker
    (None, r'', 100, {'group_end': 'sandbox_test'}),
]
```

### Execution Flow Scenarios:

* **Scenario A (Triggered Macro)**:
  * Input: `"start sandbox mit apfel"`
  * Expected Flow:
    1. The start rule matches `"start sandbox"` and replaces it with `"Sandbox:"` -> current text: `"Sandbox: mit apfel"`.
    2. The group `'sandbox_test'` is triggered.
    3. We run the inner rules recursively on `"Sandbox: mit apfel"`:
       - Inner rule 1 matches `"apfel"` and replaces with `"birne"` -> current text: `"Sandbox: mit birne"`.
       - Inner rule 2 does not match `"banane"`. Since the group is active, it falls back to appending `"banane"` -> Current text: `"Sandbox: mit birne banane"`.
    4. The final text `"Sandbox: mit birne banane"` is returned and corrected by LanguageTool.
  * Output: `"Sandbox: mit Birne Banane"`

* **Scenario B (Un-triggered Macro - Double Usability)**:
  * Input: `"ein apfel und eine kirsche"`
  * Expected Flow:
    1. The Start Rule does not match. The group `'sandbox_test'` remains inactive.
    2. The loop proceeds to the next rule.
    3. **Inner Rule 1**: Matches `"apfel"` and replaces it with `"birne"` -> Current text: `"ein birne und eine kirsche"`.
    4. **Inner Rule 2**: Does not match. Since the group was not triggered, the rule behaves as a normal standalone rule and **nothing is appended**.
    5. The End Rule is ignored.
  * Output: `"ein birne und eine kirsche"`

---

## Technical Details (Under the Hood)

* **Isolated Recursion**: When a group is triggered, the engine recursively invokes `process_text_in_background` with `custom_rules=[inner_rule]`. This allows each inner rule to execute within a full, synchronous pipeline pass.
* **Performance and Stability Safeguards**:
  * **Sequence Bypass**: Inner recursive runs bypass the `chunk_id` sequence queue to prevent deadlocks and execution delays.
  * **I/O and TTS Suppression**: Recursive runs suppress intermediate file-writing and TTS speech outputs, ensuring only the final stabilized text is written and spoken.
  * **Stability Safeguard**: Recursive runs strictly break after one iteration to prevent infinite stability loops during fallback appends.
  * **Safe Termination**: The stability check relies strictly on maximum iteration counts (`MAX_ITERATIONS_FOR_SAFETY`) to prevent infinite loops, bypassing time-based throttling that could prematurely abort legitimate, slower macro executions.
```

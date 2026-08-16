# Regelattribute: „only_in_windows“ und „exclude_windows“.

Diese beiden Attribute steuern, **in welchen aktiven Fenstern eine Regel ausgelöst werden darf**.
Sie werden im „Options“-Dikt einer Regel definiert und akzeptieren eine **Liste von Regex-Mustern**
die mit dem aktuell aktiven Fenstertitel („_active_window_title“) abgeglichen werden.

---

## `only_in_windows`

Die Regel wird **nur ausgelöst, wenn** der Titel des aktiven Fensters **mindestens einem** der angegebenen Muster entspricht.
Alle anderen Fenster werden ignoriert.

**Anwendungsfall:** Eine Regel auf eine bestimmte Anwendung beschränken.


> Die Regel wird **nur** ausgelöst, wenn Firefox oder Chromium das aktive Fenster ist.

---

## `exclude_windows`

Die Regel wird ausgelöst, **es sei denn**, dass der Titel des aktiven Fensters mit **mindestens einem** der angegebenen Muster übereinstimmt.
Passende Fenster werden übersprungen.

**Anwendungsfall:** Deaktivieren Sie eine Regel für bestimmte Anwendungen.

Beispiele

```py
Targets
    Occurrences of 'exclude_windows' in Project with mask '*pre.py'
Found occurrences in Project with mask '*pre.py'  (3 usages found)
    Usage in string constants  (3 usages found)
        STT  (3 usages found)
            config/maps/plugins/z_fallback_llm/de-DE  (3 usages found)
                FUZZY_MAP_pre.py  (3 usages found)
                    90 'exclude_windows': [r'element',r'firefox', r'chrome', r'brave'],
                    105 'exclude_windows': [r'element',r'firefox', r'chrome', r'brave'],
                    119 'exclude_windows': [r'element',r'firefox', r'chrome', r'brave',r'doublecmd'],

```



Beim Matching wird die Groß-/Kleinschreibung nicht beachtet und es werden **reguläre Ausdrücke** von Python verwendet.

---

## Zusammenfassung

| Attribut | Wird ausgelöst, wenn... |
|-----|-----------------------------|
| `only_in_windows` | Fenstertitel **stimmt** mit einem der Muster überein |
| `exclude_windows` | Fenstertitel **stimmt mit keinem Muster überein** |

---

## Siehe auch

- „scripts/py/func/process_text_in_background.py“ – Zeilen ~1866 und ~1908
- „scripts/py/func/get_active_window_title.py“ – wie der Fenstertitel abgerufen wird
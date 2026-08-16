# Rule Attributes: `only_in_windows` and `exclude_windows`

These two attributes control **in which active windows a rule is allowed to fire**.
They are defined inside a rule's `options` dict and accept a **list of regex patterns**
that are matched against the current active window title (`_active_window_title`).

---

## `only_in_windows`

The rule fires **only if** the active window title matches **at least one** of the given patterns.
All other windows are ignored.

**Use case:** Restrict a rule to a specific application.


> The rule will fire **only** when Firefox or Chromium is the active window.

---

## `exclude_windows`

The rule fires **unless** the active window title matches **at least one** of the given patterns.
Matching windows are skipped.

**Use case:** Disable a rule for specific applications.

Examples

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



Matching is **case-insensitive** and uses Python **regular expressions**.

---

## Summary

| Attribute         | Fires when...                              |
|-------------------|--------------------------------------------|
| `only_in_windows` | window title **matches** one of the patterns |
| `exclude_windows` | window title **does NOT match** any pattern  |

---

## See also

- `scripts/py/func/process_text_in_background.py` — lines ~1866 and ~1908
- `scripts/py/func/get_active_window_title.py` — how the window title is retrieved

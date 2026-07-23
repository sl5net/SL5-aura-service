# FUZZY_MAP Rule Guide

## Rule Format

```python
('replacement', r'regex_pattern', threshold, {'command_flags': re.IGNORECASE})
```

| Position | Name | Description                                                                      |
|---|---|---|
| 1 | replacement | The output text after the rule matches |
| 2 | pattern | Regex or fuzzy string to match against |
| 3 | threshold | For regex rules: ignored. For fuzzy rules: minimum match score (0–100) |
| 4 | options | Optional dictionary (see "Options Reference" below). Use `0` or omit for defaults |
### Raw Replacements
By default (`False`), replacement strings are processed by Python's `re.sub()`, which supports using regex backreferences like `\1` or `\2` to insert captured groups (for example: `(r'\1', r'(\d)\s+(?=\d)', 95)`). 
If your replacement is a multiline string or contains unescaped backslashes (such as code templates or paths) and should be preserved exactly as-is, enable `'raw_replacement': True` in the options dictionary:
```python
(System_Instructions, r'^(system instructions)$', 10, {'command_flags': re.IGNORECASE, 'raw_replacement': True})
```

### Available user-configurable options:

*   **`command_flags`** (integer): Regex flags used during pattern compilation.
    *Example:* `{'command_flags': re.IGNORECASE}`
*   **`raw_replacement`** (boolean): When `True`, the replacement text is treated as a pure string literal and bypassed by Python's `re.sub` backslash parsing. Crucial for multiline prompts or strings with unescaped backslashes (`\`).
    *Example:* `{'raw_replacement': True}`
*   **`cache`** (boolean): Toggles the AURA result cache. Set to `False` for rules that generate dynamic output (e.g., current time, random jokes) to ensure they are evaluated fresh on every match.
    *Example:* `{'cache': False}`
*   **`skip_list`** (list of strings): Specifies post-processing pipeline modules to skip when this rule matches.
    *Example:* `{'skip_list': ['LanguageTool']}` (skips grammar checking)
*   **`only_in_windows`** (list of regex strings): Restricts the rule to only trigger if the active window title matches one of the specified patterns.
    *Example:* `{'only_in_windows': [r'^Mozilla Firefox$', r'Chrome']}`
*   **`exclude_windows`** (list of regex strings): Prevents the rule from triggering if the active window title matches one of the specified patterns.
    *Example:* `{'exclude_windows': [r'Terminal', r'Claude']}`
*   **`window_ignore_case`** (boolean): Controls whether window matching (`only_in_windows` / `exclude_windows`) is evaluated case-insensitively (`True`) or case-sensitively (`False`). If omitted, falls back to the global setting `LOWERCASE_WINDOW_TITLES` in `config/settings.py`.
    *Example:* `{'window_ignore_case': False}`
*   **`on_match_exec`** (list of Path/string objects): Paths to scripts/plugins that should be executed when this rule matches (used heavily by catch-all and fallback rules).
    *Example:* `{'on_match_exec': [PROJECT_ROOT / 'scripts' / 'custom_action.py']}`

## Pipeline Logic
- Rules are processed **top-down**


## Pipeline Logic

- Rules are processed **top-down**
- **All** matching rules are applied (cumulative)
- A **fullmatch** (`^...$`) stops the pipeline immediately
- Earlier rules have priority over later rules

## Common Patterns

### Match a single word (word boundary)
```python
('Python', r'\bpython\b', 0, {'command_flags': re.IGNORECASE})
```

### Match multiple variants
```python
('OpenAI', r'\bopen\s*ai\b', 0, {'command_flags': re.IGNORECASE})
```

### Fullmatch – stops the pipeline
```python
('hello koan', r'^.*$', 0, {'command_flags': re.IGNORECASE})
```
⚠️ This matches **everything**. The pipeline stops here. Earlier rules still have priority.

### Match start of input
```python
('Note: ', r'^notiz\b', 0, {'command_flags': re.IGNORECASE})
```

### Match exact phrase
```python
('New York', r'\bnew york\b', 0, {'command_flags': re.IGNORECASE})
```

## File Locations

| File | Phase | Description |
|---|---|---|
| `FUZZY_MAP_pre.py` | Pre-LanguageTool | Applied before spell checking |
| `FUZZY_MAP.py` | Post-LanguageTool | Applied after spell checking |
| `PUNCTUATION_MAP.py` | Pre-LanguageTool | Punctuation rules |

## Tips

- Put **specific** rules before **general** ones
- Use `^...$` fullmatch only when you want to stop all further processing
- `FUZZY_MAP_pre.py` is ideal for corrections before spell checking
- Test rules with: `s your test input` in the Aura console
- Backups are created automatically as `.peter_backup`

## Examples

```python
FUZZY_MAP_pre = [
    # Correct a common STT mistake
    ('Raspberry Pi', r'\braspberry\s*pie?\b', 0, {'command_flags': re.IGNORECASE}),

    # Expand abbreviation
    ('zum Beispiel', r'\bzb\b', 0, {'command_flags': re.IGNORECASE}),

    # Stop pipeline for testing
    # ('test koan', r'^.*$', 0, {'command_flags': re.IGNORECASE}),
]
```

## Your First Rule — Step by Step

1. Open `config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py`
2. Add your rule inside `FUZZY_MAP_pre = [...]`
3. Save — Aura reloads automatically, no restart needed
4. Dictate your trigger phrase and watch it fire


## Recommended File Structure

Put your rules **before** long comment blocks:
```python
# config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py
import re  # noqa: F401
# too<-from
FUZZY_MAP_pre = [
    ('My Rule', r'my rule', 0, {'command_flags': re.IGNORECASE}),
]
# ============================================================
# Longer explanations, task descriptions, notes...
# can be as long as needed — they go AFTER the rules.
# ============================================================
```

**Why?** Aura's Auto-Fix scans only the first ~1KB of a file.
If your rules appear after a long header, Auto-Fix cannot find or repair them.
The path comment on line 1 is also recommended — it helps humans quickly identify the file.


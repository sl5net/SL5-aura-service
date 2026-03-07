# FUZZY_MAP Rule Guide

## Rule Format

```python
('replacement', r'regex_pattern', threshold, {'flags': re.IGNORECASE})
```

| Position | Name | Description |
|---|---|---|
| 1 | replacement | The output text after the rule matches |
| 2 | pattern | Regex or fuzzy string to match against |
| 3 | threshold | Ignored for regex rules. Used for fuzzy matching (0–100) |
| 4 | flags | `{'flags': re.IGNORECASE}` for case-insensitive, `0` for case-sensitive |

## Pipeline Logic

- Rules are processed **top-down**
- **All** matching rules are applied (cumulative)
- A **fullmatch** (`^...$`) stops the pipeline immediately
- Earlier rules have priority over later rules

## Common Patterns

### Match a single word (word boundary)
```python
('Python', r'\bpython\b', 0, {'flags': re.IGNORECASE})
```

### Match multiple variants
```python
('OpenAI', r'\bopen\s*ai\b', 0, {'flags': re.IGNORECASE})
```

### Fullmatch – stops the pipeline
```python
('hello koan', r'^.*$', 0, {'flags': re.IGNORECASE})
```
⚠️ This matches **everything**. The pipeline stops here. Earlier rules still have priority.

### Match start of input
```python
('Note: ', r'^notiz\b', 0, {'flags': re.IGNORECASE})
```

### Match exact phrase
```python
('New York', r'\bnew york\b', 0, {'flags': re.IGNORECASE})
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
    ('Raspberry Pi', r'\braspberry\s*pie?\b', 0, {'flags': re.IGNORECASE}),

    # Expand abbreviation
    ('zum Beispiel', r'\bzb\b', 0, {'flags': re.IGNORECASE}),

    # Stop pipeline for testing
    # ('test koan', r'^.*$', 0, {'flags': re.IGNORECASE}),
]
```

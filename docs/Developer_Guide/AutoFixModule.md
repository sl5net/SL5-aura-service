# Auto-Fix Module (Quick Rule Entry Mode)

## What it does

When you type a plain word (without quotes or Python syntax) into a map file
like `FUZZY_MAP_pre.py`, the system automatically converts it into a valid rule.

This is the fastest way to create new rules — no need to remember the format.

## Example

You type this into `FUZZY_MAP_pre.py`:

```
oma
```

The auto-fix module detects a `NameError` (bare word, not valid Python)
and transforms the file automatically into:

```python
# config/maps/.../de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
# too<-from
FUZZY_MAP_pre = [
    ('oma', 'oma'),
]
```

Now edit the rule to what you actually need:

```python
('Oma', 'oma'),              # capitalize
('Großmutter', 'oma'),       # synonym
('Thomas Müller', 'thomas'), # from a phone book
```

## How it works

The module `scripts/py/func/auto_fix_module.py` is triggered automatically
when Aura detects a `NameError` while loading a map file.

It then:
1. Adds the correct file path header
2. Adds `import re` if missing
3. Adds the `FUZZY_MAP_pre = [` list definition
4. Converts bare words into `('word', 'word'),` tuples
5. Closes the list with `]`

## Rules and Limits

- Only works on files smaller than **1KB** (safety limit)
- Only applies to: `FUZZY_MAP.py`, `FUZZY_MAP_pre.py`, `PUNCTUATION_MAP.py`
- The file must be in a valid language folder (e.g. `de-DE/`)
- Works for multiple words at once (e.g. from a phone book list)

## Known Issues (not fully tested)

> ⚠️ This module is functional but not exhaustively tested. The following cases may not work correctly:

- **Numbers** – `5` or `6` are not valid Python identifiers, auto-fix may not handle them
- **Special characters** – words with `-`, `.`, umlauts may not trigger a `NameError`
- **Multi-word entries** – `thomas mueller` (with space) causes `SyntaxError` not `NameError`, so auto-fix may not trigger
- **Comma-separated values** – `drei, vier` may be inserted as-is without becoming a proper tuple

If auto-fix does not trigger, add the rule manually:
```python
('replacement', 'input word'),
```

## The `# too<-from` comment

This comment is added automatically as a reminder of the rule direction:

```
too <- from
```

Meaning: **output** (too) ← **input** (from). The replacement comes first.

For `PUNCTUATION_MAP.py` the direction is reversed: `# from->too`

## Bulk entry from a list

You can paste multiple words at once:

```
thomas
maria
berlin
```

Each bare word becomes its own rule:

```python
('thomas', 'thomas'),
('maria', 'maria'),
('berlin', 'berlin'),
```

Then edit each replacement as needed.

## File: `scripts/py/func/auto_fix_module.py`

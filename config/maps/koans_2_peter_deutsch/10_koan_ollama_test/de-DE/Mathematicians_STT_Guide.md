# Famous Mathematicians – STT Correction Guide

## The Problem

Speech recognition (STT) systems like Vosk often mishear or misspell names of famous mathematicians.
This is especially common with German names that contain special characters (ß, ü, ä, ö)
or names borrowed from other languages.

## Common STT Errors

| Spoken / STT Output | Correct Spelling | Notes |
|---|---|---|
| gaus, gauss | Gauß | German mathematician, ß often missing |
| oiler, oyler | Euler | Swiss, name sounds like "oiler" in German |
| leibnitz, lipnitz | Leibniz | z at end, common misspelling |
| riman, riemann | Riemann | double-n often missed |
| hilbert | Hilbert | usually correct, just capitalization |
| cantor | Cantor | usually correct, just capitalization |
| poincare, poincaré | Poincaré | accent often missing |
| noether, nöter | Noether | umlaut often missed |

## Example Rules

```python
FUZZY_MAP_pre = [
    ('Gauß', r'\bgau[sß]{1,2}\b', 0, {'flags': re.IGNORECASE}),
    ('Euler', r'\b(oiler|oyler|euler)\b', 0, {'flags': re.IGNORECASE}),
    ('Leibniz', r'\bleib(nitz|niz|nits)\b', 0, {'flags': re.IGNORECASE}),
    ('Riemann', r'\bri{1,2}e?mann?\b', 0, {'flags': re.IGNORECASE}),
    ('Noether', r'\bn[oö]e?th?er\b', 0, {'flags': re.IGNORECASE}),
]
```

## Why Pre-LanguageTool?

These corrections should happen in `FUZZY_MAP_pre.py` (before LanguageTool),
because LanguageTool might "correct" a misspelled name into a different wrong word.
Better to fix it first, then let LanguageTool check grammar.

## Testing

After adding a rule, test with the Aura console:
```
s euler hat die formel e hoch i pi plus eins gleich null bewiesen
```
Expected: `Euler hat die Formel e hoch i pi plus eins gleich null bewiesen`

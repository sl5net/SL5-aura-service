# Getting Started with SL5 Aura

## What is SL5 Aura?

SL5 Aura is an offline-first voice assistant that converts speech to text (STT) and applies configurable rules to clean, correct and transform the output.

It works without a GUI – everything runs via CLI or console.

## How it Works

```
Microphone → Vosk (STT) → Maps (Pre) → LanguageTool → Maps (Post) → Output
```

1. **Vosk** converts your speech to raw text
2. **Pre-Maps** clean and correct the text before spell checking
3. **LanguageTool** fixes grammar and spelling
4. **Post-Maps** apply final transformations
5. **Output** is the final clean text (and optionally TTS)

## Your First Steps

### 1. Start Aura
```bash
python main.py
```

### 2. Test with console input
Type `s` followed by your text:
```
s hello world
```

### 3. See a rule in action
Open `config/maps/koans_deutsch/01_koan_erste_schritte/de-DE/FUZZY_MAP_pre.py`

Uncomment the rule inside and test again. What happens?

## Understanding Rules

Rules live in `config/maps/` in Python files called `FUZZY_MAP_pre.py` or `FUZZY_MAP.py`.

A rule looks like this:
```python
('Hello World', r'\bhello world\b', 0, {'flags': re.IGNORECASE})
#   ^output        ^pattern          ^threshold  ^case-insensitive
```

The **output** comes first – you immediately see what the rule produces.

Rules are processed **top to bottom**. The first fullmatch (`^...$`) stops everything.

## Koans – Learning by Doing

Koans are small exercises in `config/maps/koans_deutsch/` and `config/maps/koans_english/`.

Each koan teaches one concept:

| Koan | Topic |
|---|---|
| 01_koan_erste_schritte | First rule, fullmatch, pipeline stop |
| 02_koan_listen | Lists, multiple rules |
| 03_koan_schwierige_namen | Difficult names, phonetic matching |

Start with Koan 01 and work your way up.

## Tips

- Rules in `FUZZY_MAP_pre.py` run **before** spell checking – good for fixing STT errors
- Rules in `FUZZY_MAP.py` run **after** spell checking – good for formatting
- Backup files (`.peter_backup`) are created automatically before any change
- Use `peter.py` to let an AI work through the koans automatically

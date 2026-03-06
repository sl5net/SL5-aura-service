# Regex Map Maintenance Tools

To support the rapid search functionality (`...`  / `search_rules.sh`), we use a helper script that automatically annotates regex patterns with human-readable examples.

## Why do we need this?
Our `FUZZY_MAP.py` files contain complex regular expressions. To make them searchable via fuzzy finders (fzf) without needing to understand the raw regex, we add `# EXAMPLE:` comments above the patterns.

**Before:**
```python
('CreditCard', r'\b(?:\d[ -]*?){13,16}\b', ...)
```

**After (Auto-generated):**
```python
# EXAMPLE: 1234-5678-9012-3456
('CreditCard', r'\b(?:\d[ -]*?){13,16}\b', ...)
```

## The Tagger Script (`map_tagger.py`)

We provide a Python script that scans all `FUZZY_MAP.py` and `FUZZY_MAP_pre.py` files and generates these examples automatically.

### Installation
The script requires the `exrex` library to generate random matches for complex regexes.

```bash
pip install exrex
```

### Usage
Run the script from the project root:

```bash
python3 tools/map_tagger.py
```

### Workflow
1. **Create or Edit** a Map file (e.g., adding new rules).
2. **Run** the tagger script.
3. **Interactive Mode:**
   - The script will show you a generated suggestion.
   - Press `ENTER` to accept it.
   - Type `s` to skip.
   - Type `sa` (skip all) if you want to skip all remaining patterns that fail generation.
4. **Commit** the changes.

> **Note:** The script ignores existing `# EXAMPLE:` tags, so it is safe to run repeatedly.


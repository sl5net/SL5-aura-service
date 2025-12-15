planned not work at the momente without a passworde in folders up somwhere . pasword files need to be start with a dot "."


# Auto-Zip Workflow & Embedded Documentation

## Concept
SL5 Aura automatically monitors folders starting with `_` (e.g., `_my_application`). When changes are detected, Aura automatically compresses the folder into a zip archive.

**Critical Constraint:**
Aura's "Hot-Reload" and monitoring system specifically listens for changes in **valid Python files**. A simple text file (`.txt`) update will **not** trigger the auto-zip process.

## The "Embedded Docs" Pattern
To include instructions for non-technical recipients (e.g., HR, Clients) while ensuring Aura detects the change and updates the zip, we use a **Python Docstring File**.

This file is technically a valid Python script (satisfying Aura's parser) but visually appears as a standard text document to the user.

### Implementation
Create a file named `README_AUTOZIP.py` inside your monitored folder.

**Style Guide:**
1. Use `# Documentation` as the first line (instead of a technical script name) to be welcoming.
2. Use a Triple-Quote (`"""`) Docstring for the content.
3. No other code is required.

### Example Code

```python
# Documentation

"""
# AUTOMATED ARCHIVE GENERATION

This archive was automatically created and updated by SL5 Aura.

TRIGGER:
Folders starting with "_" are monitored by SL5 Aura.
Any change to the content automatically triggers a re-zip process.

TECHNICAL NOTE:
You will find `__init__.py` and `README_AUTOZIP.py` included.
You don't need them when you don't use Aura.

---
Generiert von SL5 Aura
The Architect's Solution for Offline Voice Control.
"""

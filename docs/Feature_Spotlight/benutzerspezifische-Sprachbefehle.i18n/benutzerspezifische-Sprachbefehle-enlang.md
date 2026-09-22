> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../benutzerspezifische-Sprachbefehle.md).*

# User-specific voice commands

Aura allows you to define your own commands that are **only active for you** (or certain team members). This prevents private abbreviations or test commands from being triggered on other users.

## Establishment

The adjustment takes place directly in a rule file (e.g. `FUZZY_MAP_pre.py` or `FUZZY_MAP_pre.py`). `FUZZY_MAP.py` rules that are executed only after the language correction:

### Code example

Add the following block at the end of the file:

```python
from scripts.py.func.determine_current_user import determine_current_user

# 1. Wer bin ich?
current_user, _ = determine_current_user()

# 2. Eigene Befehle nur für 'misterx' aktivieren
if current_user in ['misterx']:
    MY_USER_RULES = [
        ('Guten morgen zusammen', r'^(hallo)$')
    ]
    # 3. In die Hauptliste einfügen
    FUZZY_MAP_pre.extend(MY_USER_RULES)

    # Benutzerspezifische Sprachbefehle

Aura erlaubt es dir, eigene Befehle zu definieren, die **nur für dich** (oder bestimmte Teammitglieder) aktiv sind. Dies verhindert, dass private Kürzel oder Test-Befehle bei anderen Benutzern ausgelöst werden.

## Einrichtung

Die Anpassung erfolgt direkt in einer Regel-Datei (z.B. `FUZZY_MAP_pre.py` bzw. `FUZZY_MAP.py` Regeln die erst nach der Sprach-Korrektur ausgeführt werden):

### Code-Beispiel

Füge am Ende der Datei folgenden Block hinzu:

```python
from scripts.py.func.determine current user import determine current user

#1: Who am I?
current user,   = determine current user()

if current user in ['misterx']:
    MY USER RULES = []
        # Format: (response/action, regex pattern, min-accuracy, options)
        (f"Hello {current user}", r'^(hello|hi)$')
    ]
    FUZZY MAP pre.extend(MY USER RULES)

__CODE_BLOCK_1__

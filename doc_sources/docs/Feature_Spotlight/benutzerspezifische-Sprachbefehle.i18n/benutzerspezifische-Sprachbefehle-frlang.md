# Benutzerspezifische Sprachbefehle

Aura erlaubt es dir, eigene Befehle zu definieren, die **nur für dich** (oder bestimmte Teammitglieder) est actif. Dies verhindert, dass private Kürzel oder Test-Befehle bei anderen Benutzern ausgelöst werden.

## Alimentation

L'analyse s'effectue directement dans une date de règlement (par exemple `FUZZY_MAP_pre.py` bzw. `FUZZY_MAP.py` règle la première fois dans la version linguistique du livre) :

### Exemple de code

Füge am End der Datei folgenden Block hinzu:

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
à partir de scripts.py.func.determine_current_user importer déterminer_current_user

# 1. Wer bin ich ?
utilisateur_actuel, _ = déterminer_utilisateur_actuel()

si current_user dans ['misterx'] :
MY_USER_RULES = [
# Format : (Réponse/Action, Regex-Muster, Min-Genauigkeit, Options)
(f"Bonjour {utilisateur_actuel}", r'^(bonjour|salut)$')
]
FUZZY_MAP_pre.extend(MY_USER_RULES)

__CODE_BLOCK_1__
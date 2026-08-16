# Benutzerspezifische Sprachbefehle

Aura erlaubt es dir, eigene Befehle zu definieren, die **nur für dich** (oder bestimmte Teammitglieder) aktiv sind. Dies verhindert, dass private Kürzel oder Test-Befehle bei anderen Benutzern ausgelöst werden.

## 아인리히퉁

Die Anpassung erfolgt in einer Regel-Datei (z.B. `FUZZY_MAP_pre.py` bzw. `FUZZY_MAP.py` Regeln die erst nach der Sprach-Korrektur ausgeführt werden):

### 코드-Beispiel

Füge am Ende der Datei folgenden Block hinzu:

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
scripts.py.func.determine_current_user에서 importdetermine_current_user

# 1. Wer bin ich?
current_user, _ = 현재_사용자 결정()

['misterx']에 current_user가 있는 경우:
MY_USER_RULES = [
# 형식: (Antwort/Aktion, Regex-Muster, Min-Genauigkeit, Optionen)
(f"안녕하세요 {current_user}", r'^(안녕하세요|안녕)$')
]
FUZZY_MAP_pre.extend(MY_USER_RULES)

__CODE_BLOCK_1__
# Benutzerspezifische Sprachbefehle

Aura erlaubt é dir, eigene Befehle zu definieren, die **nur für dich** (ou bestimmte Teammitglieder) ativo sind. Isso impede que o particular Kürzel ou Test-Befehle bei outro Benutzern seja usado.

##Einrichtung

A Anpassung foi atualizada diretamente em um Regel-Datei (z.B. `FUZZY_MAP_pre.py` bzw. `FUZZY_MAP.py` Regeln die erst nach der Sprach-Korrektur ausgeführt werden):

### Código-Beispiel

Fuge am Ende der Datei segue o bloco abaixo:

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
de scripts.py.func.determine_current_user importar determine_current_user

# 1. O que você fez?
usuário_atual, _ = determine_usuário_atual()

se usuário_atual em ['misterx']:
MINHAS_RULES_USUÁRIO = [
# Formato: (Antwort/Aktion, Regex-Muster, Min-Genauigkeit, Optionen)
(f"Olá {usuário_atual}", r'^(alô|oi)$')
]
FUZZY_MAP_pre.extend(MY_USER_RULES)

__CODE_BLOCK_1__
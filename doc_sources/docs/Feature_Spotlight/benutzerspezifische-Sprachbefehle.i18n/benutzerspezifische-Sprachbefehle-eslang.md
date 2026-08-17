# Benutzerspezifische Sprachbefehle

Aura erlaubt es dir, eigene Befehle zu definieren, die **nur für dich** (oder bestimmte Teammitglieder) aktiv sind. Dies verhindert, dass private Kürzel oder Test-Befehle bei otheren Benutzern ausgelöst werden.

## Enriquecimiento

El paso se realiza directamente en una fecha regional (por ejemplo, `FUZZY_MAP_pre.py` bzw. `FUZZY_MAP.py` Regeln die erst nach der Sprach-Korrektur ausgeführt werden):

### Código-Beispiel

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
desde scripts.py.func.determinar_actual_usuario importar determinar_actual_usuario

# 1. ¿Wer bin ich?
usuario_actual, _ = determinar_usuario_actual()

si usuario_actual en ['misterx']:
MI_USUARIO_RULES = [
# Formato: (Respuesta/Acción, Regex-Muster, Min-Genauigkeit, Optionen)
(f"Hola {usuario_actual}", r'^(hola|hola)$')
]
FUZZY_MAP_pre.extend(MY_USER_RULES)

__CODE_BLOCK_1__
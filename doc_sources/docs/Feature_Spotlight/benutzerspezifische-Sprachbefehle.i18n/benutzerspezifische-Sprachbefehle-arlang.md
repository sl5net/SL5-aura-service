# Benutzerspezifische Sprachbefehle

Aura erlaubt es dir, eigene Befehle zu definieren, die **nur für dich** (oder bestimmte Teammitglieder) aktiv sind. Dies verhindert, dass Private Kürzel oder Test-Befehle bei anderen Benutzern ausgelöst werden.

                                                      ## اينريشتونج

يتم تنفيذ عملية الاختراق مباشرة في أحد سجلات البيانات (z.B. `FUZZY_MAP_pre.py` bzw. `FUZZY_MAP.py` يتم إعادة تسجيلها في المرة الأولى التي يتم فيها إصلاح تصحيح الأخطاء):

                                                      ### كود بيسبيل

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
من scripts.py.func.determine_current_user قم باستيراد تحديد_current_user

                                                    # 1. وير بن إيش؟
                 current_user, _ = تحديد_المستخدم الحالي()

               إذا كان المستخدم الحالي في [\'misterx']:
                                                            MY_USER_RULES = [
# التنسيق: (Antwort/Aktion، Regex-Muster، Min-Genauigkeit، Optionen)
         (f"مرحبًا {المستخدم_الحالي}"، r\'^(hallo|hi)$')
                                                                            ]
                                          FUZZY_MAP_pre.extend(MY_USER_RULES)

                                                             __CODE_BLOCK_1__
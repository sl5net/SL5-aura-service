# Benutzerspezifische Sprachbefehle

Aura erlaubt es dir, eigene Befehle zu definieren, die **nur für dich** (oder bestimmte Teammitglieder) aktiv sind. Dies verhindert, dass private Kürzel oder Test-Befehle bei anderen Benutzern ausgelöst werden.

## Zwiększenie

Die Anpassung erfolgt direkt in einer Regel-Datei (z.B. `FUZZY_MAP_pre.py` bzw. `FUZZY_MAP.py` Regeln die erst nach der Sprach-Korrektur ausgeführt werden):

### Kod-Beispiel

Füge am Ende der Datei folgenden Block hinzu:

__KOD_BLOKU_0__
z importu scripts.py.func.determine_current_user określ_prąd_użytkownika

# 1. Wer bin ich?
bieżący_użytkownik, _ = określ_bieżący_użytkownik()

jeśli bieżący_użytkownik w ['misterx']:
MY_USER_RULES = [
# Format: (Antwort/Aktion, Regex-Muster, Min-Genauigkeit, Optionen)
(f"Witam {aktualny_użytkownik}", r'^(halo|cześć)$')
]
FUZZY_MAP_pre.extend(MY_USER_RULES)

__KOD_BLOKU_1__
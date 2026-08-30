# ==============================================================================
# 🌐 AUTOMATICALLY GENERATED / MACHINE-TRANSLATED MAP
# ==============================================================================
# ℹ️  Source Language: German (de-DE)
# ⚙️  Note: Speech recognition regexes (VOSK) and Koan instructions in this
#     file were machine-translated. Spoken patterns may require refinement
#     or tuning for natural speech in the target language.
#
# 🤝  CONTRIBUTIONS WELCOME!
#     We would love your help improving this map! If you test or refine these
#     regex patterns, please open a Pull Request with your improvements.
# ==============================================================================

# configmaps/koans deutsch/07_koan_auto_fix_map_errors/de-DE/FUZZY_MAP_pre.py


# ============================================================
# Koan 07 : Auto-Fix & LanguageTool en pratique

# ============================================================
#
# OBJECTIF D'APPRENTISSAGE :

# La correspondance floue corrige les fautes de frappe dans la transcription.

# LanguageTool corrige ensuite la grammaire.

#
# TÂCHE:

# Dire : "Serviette" (intentionnellement incorrect)

# Résultat : Aura corrigée en "fuzzy1", LT en "manuel" ?

#
# LanguageTool est en cours d'exécution ?

# curl http://localhost:8082/v2/languages | head -3

#
# PROCHAINE ÉTAPE : Koan 08

# ============================================================


import re

# depuis pathlib import Path as p;import os as o

# avec open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())




FUZZY_MAP_pre = [
    ('fuzzy1', 'handuch',1,{'command_flags': re.IGNORECASE}),
]


"""
Bitte schreiben Sie ein Wort in die erste Zeile vor den Anführungstrichen.

Lernziel:

Automatische Fehlerbehebung in Map-Plugins (z.B. NameError für nicht definierte Variablen)
Umwandlung von "bare words" in gültige Tuples
Header-Cleanup (Dubletten entfernen, Pfade aktualisieren)



Beispiel für einen anderen Helfen der beim Schreiben hilft.

LanguageTool ( https://languagetool.org/ )

Bitte öffnen Sie das Fenster und diktieren Text in der Formular-Feld.


Hier sind die Methoden, um auf Windows 11 zu prüfen, ob der LanguageTool im Hintegrund läuft:

http://localhost:8081/v2/languages


Erfolg: Du siehst eine JSON-Liste mit unterstützten Sprachen.

netstat -ano | findstr 8081

Get-CimInstance Win32_Process -Filter "CommandLine LIKE '%languagetool%'" | Select-Object ProcessId, CommandLine

Per Browser (Funktionstest)
Öffne diese URL im Browser:

http://localhost:8081/v2/languages

Erfolg: Du siehst eine JSON-Liste mit unterstützten Sprachen.


"""

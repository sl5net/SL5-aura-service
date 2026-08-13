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

# config/maps/plugins/standard_actions/zip_all/de-DE/FUZZY_MAP_pre.py

# its using https://github.com/scrollmapper/bible_databases/tree/master/formats/sqlite


import re # noqa: F401
# depuis pathlib import Path as p;import os as o # noqa: E702

# avec open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa : E702



from pathlib import Path

# Cette carte utilise une approche hybride :

# 1. Les entrées Regex sont vérifiées en premier. Ils sont puissants et peuvent ne pas être sensibles à la casse.

# Structure : ('remplacement', rregex_pattern', seuil, drapeaux)

# - Le seuil est ignoré pour les regex.

# - flags : utilisez {'flags' : ...} pour l'insensibilité à la casse, ou 0 pour la sensibilité à la casse.

# 2. Si aucune expression régulière ne correspond, une simple correspondance floue est effectuée sur les règles restantes.


CONFIG_DIR = Path(__file__).parent

    # Un fichier de type bien sûrinternesLa recherche lève la maisoninternesChips Mettre à jour la base de donnéesinternesScript Rénover la base de donnéesinternesMettre à jour la puce twitter shareinternalsTous les dossiers SkillinternalsTous les dossiers mis à jourinternesUne mise en page par moiinternalsLire tous les dossiersClavier MorphinLireinternalsZwick données ininternalsJeep données ininternals


    # Trouver un fichier zipinternalsMettre à jour tous les fichiersRapportMettre à jour un fichier zipinternalsTrouver vos fichiers zipRapport de voyage


    # === General Terms (Case-Insensitive) ===
    # Utiliser les limites des mots (\b) et le regroupement (|) pour détecter efficacement les variations.

    # Important à savoir :

    # - ça s'arrête au premier match complet. Exemples : ^...$ = Correspondance complète = Critère d'arrêt !

    # - le premier est lu en premier et les règles inférieures peuvent ne pas être lues.

FUZZY_MAP_pre = [
    ('find all zips', r'''^(
            (Alle\s)?(ZIP|Sip|Chip|Tipp|Zipp|Seb)[-\s]?(Dateien|Ordner|Daten|s)?\s(suchen|hinzu|scannen|aktualisieren|einlesen|finden|checken|neu laden)
            |
            (Scanne|Suche|Aktualisiere)\s(alle\s)?(Zips|Zip-Dateien|Chips|Tipps)
            |
            (Zip|Zips)\s(Registry|Datenbank)\s(aktualisieren|erneuern)
            |
            jagen aktualisieren
            )$''', 90, {
                'flags': re.IGNORECASE | re.VERBOSE,
                'on_match_exec': [CONFIG_DIR / 'zip.py']
            }
        ),
]

# Ajouter un fichier zipAnalyse terminée. J'ai trouvé 11 cibles. Zips mis à jour.

#

readme = '''
Was deckt das jetzt alles ab?
Dank der Kombinationen funktionieren nun hunderte Varianten. Hier ein paar Beispiele, die jetzt erkannt werden:

Der Standard:

"Zip Dateien suchen"
"Zips scannen"
"Zip Ordner aktualisieren"
"Alle Zips neu laden"

Die "Kreativen" (Verhörer):

"Chips suchen"
"Tipps scannen"
"Sip Dateien finden"
"Seb Ordner checken"
"Zipps einlesen"

Die Befehlsform:

"Scanne Zips"
"Aktualisiere alle Chips"

Technische Begriffe:

"Zip Registry aktualisieren"
"Zip Datenbank erneuern"

Hinweis: Ich habe re.VERBOSE (in den Flags) hinzugefügt, damit wir den Regex über mehrere Zeilen schreiben können (bessere Lesbarkeit). Falls deine Engine re.VERBOSE nicht unterstützt oder mag, sag Bescheid, dann schrumpfe ich es wieder in eine lange Zeile.

'''

# config/languagetool_server/maps/plugins/ki-maker.space/de-DE/FUZZY_MAP_pr.py
# https://regex101.com/
import re # noqa: F401

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.



"""

Mi

 Reboot - Wednesday



Do

Scratch-Thursday

    OpenLab:  11:00 - 22:00 Uhr



Fr

Fabric-Friday:  Feiertag - 3.10.2025

Open Lab ist geschlossen.

DO
Do
Scratch-Thursday
    OpenLab:  11:00 - 22:00 Uhr

Sa

Supercreative-Saturday

"""
FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - in our implementation it stops with first match!
    # - means first is most imported, lower rules maybe not get read.

    # ki make espace  KI Weckers  KI im weg ist k E-Mail Gespräch Per E-Mail Gespräch
    # K i Säcke Makerspace KI Säcke Espe
    #  Per E-Mail gesperrt ki-maker.space

    # EXAMPLE: ki-maker
    ('ki-maker.space', r'^(ki-maker|ki[\s]*make[\se]*space|k i [\s]*make[\s\w]*space|space|ki weckers|KI im weg ist|KI Säcke Espe|Kain weggesprengt|K \w*\s*make space|KI es|K i \w+ \w*|ki menkes)\s*\w*$', 60, {'flags': re.IGNORECASE}),

    # EXAMPLE: Gregor
    ('Gregor Schulte, 07071- 6395627 Gregor.Schulte@ki-maker.space', r'^(Gregor|Schulte|ki-maker.space)\s*\w*$', 80, {'flags': re.IGNORECASE}),

    # EXAMPLE: Büro ki-maker.space s x
    ('Bulsat', r'^(Büro ki-maker.space)\s*\w*$', 85, {'flags': re.IGNORECASE}),

    #  Gregor  schulte  Gregor
    #  Per E-Mail Gespräch K i Säcke Respekt

]


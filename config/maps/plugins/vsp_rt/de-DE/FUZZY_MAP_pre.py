# config/languagetool_server/maps/plugins/vsp_rt/de-DE/FUZZY_MAP_pr.py
# https://regex101.com/
import re # noqa: F401

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - in our implementation it stops with first match!
    # - means first is most imported, lower rules maybe not get read.


    ('Torsten Hau,Katja Janssens,Harald Uetz,Juliana Kunrad', r'^\b(V\s*S\s*P|V\s*[FS]\s*B)\s*(Person\w+)\b$', 70, {'flags': re.IGNORECASE}),

    ('Torsten Hau', r'^\b(V\s*S\s*P|V\s*[FS]\s*B|Frau\s*s\s*p)\s*(Geschäftsf\w+|Chef)\b$', 70, {'flags': re.IGNORECASE}),

    ('Torsten Hau ist gerne mit dem MTB unterwegs', r'^(\w+ubis|Hobbys)\b.*(V\s*S\s*P|V\s*[FS]\s*B|Frau\s*s\s*p)\s*(Geschäftsf\w+|Chef)\b$', 70, {'flags': re.IGNORECASE}),


    ('Herr Schröer', r'^(Herr Schröder|Herr hersteller|Herr Schröer|herr schrill)\b$', 70, {'flags': re.IGNORECASE}),
    ('Schröer', r'^(Schrö\w*r|schwör\w*|schworen|schon besorgt)\b$', 70, {'flags': re.IGNORECASE}),

    ('Ergotherapie Schröer', r'^Ergo\w* (Schrö\w*|schwör\w*|schworen|schon besorgt)\b$', 70, {'flags': re.IGNORECASE}),

    ('Schröer Ergotherapie', r'^(Schrö\w*|schwör\w*|schworen|schon besorgt)\b Ergo\w*$', 70, {'flags': re.IGNORECASE}),

    ('Schröer Ergotherapie', r'^(Früher|Speyer) (eher|ergo|erst)\b$', 70, {'flags': re.IGNORECASE}),


]


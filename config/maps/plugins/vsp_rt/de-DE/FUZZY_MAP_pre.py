# config/languagetool_server/maps/plugins/vsp_rt/de-DE/FUZZY_MAP_pr.py
# https://regex101.com/
import re # noqa: F401

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use re.IGNORECASE for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - in our implementation it stops with first match!
    # - means first is most imported, lower rules maybe not get read.

#  V s p Person
#  VfB personal
# VfB passen  VfB personal VfB per Sünde Torsten Hau,Katja Janssens,Harald Uetz,Juliana Kunrad


    ('Torsten Hau,Katja Janssens,Harald Uetz,Juliana Kunrad', r'^\b(V\s*S\s*P|V\s*[FS]\s*B)\s*(Person\w+)\b$', 70, re.IGNORECASE),

    ('Torsten Hau', r'^\b(V\s*S\s*P|V\s*[FS]\s*B|Frau\s*s\s*p)\s*(Geschäftsf\w+|Chef)\b$', 70, re.IGNORECASE),

    ('Torsten Hau ist gerne mit dem MTB unterwegs', r'^(\w+ubis|Hobbys)\b.*(V\s*S\s*P|V\s*[FS]\s*B|Frau\s*s\s*p)\s*(Geschäftsf\w+|Chef)\b$', 70, re.IGNORECASE),


    # Frau s p Geschäftsführer Torsten Hau Hobbys Foulspiel Geschäftsführer


]


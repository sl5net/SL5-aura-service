# config/maps/plugins/empty_all/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
#from pathlib import Path as p;import os as o # noqa: E702
#with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702
#(f'{str(__file__)}', r'^(.*)$', 10,{'on_match_exec':[PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}) # noqa: E702



# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

# too<-from
FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - it stops with first full-match. Examples: ^...$ = Full Match = Stop Criterion! 
    # - first is read first imported, lower rules maybe not get read.

    # Kumulation: Regeln (kumulieren) so das vielleicht nur die letzte Regeln sichbar wird. Beispiele:

    # Folgende regel betrifft alles:
    # ('---', r'^.*$', 5, # min_accuracy {'flags': re.IGNORECASE}),

    # Folgende regel betrifft alles außer dem Wort Haus:
    # EXAMPLE: Haus
    # ('', r'^(?!Haus).*$', 5, {'flags': re.IGNORECASE}),
    #TestTestTestHausHausHausFrau ausHaus Baum unterGuten TagSchachmattSchachmatt
    #SchachmattSchachmatt

    # Folgende regel betrifft alles außer den Wörtern Schach,Matt:
    # EXAMPLE: Schach
    # ('', r'^(?!Schach|Matt|bad|Haus).*$', 5, {'flags': re.IGNORECASE}),
    #SchachSchachHausSchachSchachBad
    #Schachmatt

    # EXAMPLE: Schach
    # ('Schachmatt', r'^(Schach|Matt|bad|Haus).*$', 5, {'flags': re.IGNORECASE}),
    #SchachmattSchachmatt



    ('LECKER_EXAKT', 'Marmelade', 100, {'flags': re.IGNORECASE}),
    # Marmelade MarmeladeLECKER_EXAKT

    # Test 2: Tolerante Regel (Tippfehler erlaubt)
    # 'Marmelada' oder 'Marmelad' sollte auch erkannt werden.
    # ('LECKER_FUZZY', 'Marmelade', 1, {'flags': re.IGNORECASE}),

    #Marmelade Marmelade Mammon Mammon Mama Marion Málaga
    # Mama MarionA lager mal mager




]

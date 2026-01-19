# config/maps/plugins/empty_all/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401


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
    # ('---', r'^.*$', 5, {'flags': re.IGNORECASE}),

    # Folgende regel betrifft alles außer dem Wort Haus:
    # EXAMPLE: Haus
    ('', r'^(?!Haus).*$', 5, {'flags': re.IGNORECASE}),
    #TestTestTestHausHausHausFrau ausHaus Baum unterGuten TagSchachmattSchachmatt
    #SchachmattSchachmatt

    # Folgende regel betrifft alles außer den Wörtern Schach,Matt:
    # EXAMPLE: Schach
    ('', r'^(?!Schach|Matt|bad|Haus).*$', 5, {'flags': re.IGNORECASE}),
    #SchachSchachHausSchachSchachBad
    #Schachmatt

    # EXAMPLE: Schach
    ('Schachmatt', r'^(Schach|Matt|bad|Haus).*$', 5, {'flags': re.IGNORECASE}),
    #SchachmattSchachmatt






    ('LECKER_EXAKT', 'Marmelade', 100, {'flags': re.IGNORECASE}),
    # Marmelade MarmeladeLECKER_EXAKT

    # Test 2: Tolerante Regel (Tippfehler erlaubt)
    # 'Marmelada' oder 'Marmelad' sollte auch erkannt werden.
    # ('LECKER_FUZZY', 'Marmelade', 1, {'flags': re.IGNORECASE}),

    #Marmelade Marmelade Mammon Mammon Mama Marion Málaga
    # Mama MarionA lager mal mager




]

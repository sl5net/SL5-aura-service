# config/maps/koans_2_peter_deutsch/09_personal_signature/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
#from pathlib import Path as p;import os as o # noqa: E702
#with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702


# Regel-Format: ('Ersatztext', r'muster', schwellwert, flags)
# Logik: Top-Down, erster Treffer gewinnt. Fullmatch (^...$) stoppt die Pipeline.


user_name = "USER_NAME"
# user_name = getattr(settings, "USER_NAME", "[Name fehlt]")

# too<-from
# PETER-AUFGABE fuer Koan: 09_personal_signature
# Keine auskommentierten Regeln gefunden.
# -> Erstelle eine sinnvolle neue Regel fuer diesen Koan.
FUZZY_MAP_pre = [
    # EXAMPLE: mfg
    (f"Mit freundlichen Grüßen, {user_name}\n", r"^(mfg|best regards|Mit freundlichen Grüßen|Baum)\w*$", 55, {
        'command_flags': re.IGNORECASE,
        'only_in_windows': 'koans_2_peter_deutsch',
        },
    ),

    # === FUZZY MATCHING TEST ===
    # Wort: Marmelade -> Ersetzung: LECKER

    # Test 1: Strenge Regel (Threshold 0 oder 100 - je nach System)
    # "Score" nutzt (0-100%): 100 = Exakt

]

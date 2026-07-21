# config/maps/koans_deutsch/09_personal_signature/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
#from pathlib import Path as p;import os as o # noqa: E702
#with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:PROJECT_ROOT=p(f.read().strip()) # noqa: E702



#from config import settings


# ============================================================
# Koan 09: Persönliche Signatur – Dynamische Regelinhalte
# ============================================================
#
# LERNZIEL:
#   Regeln können Python-Variablen enthalten – z.B. deinen Namen
#   aus config/settings_local.py
#
# AUFGABE:
#   1. Setze USER_NAME in config/settings_local.py
#   2. Sprich: "viele Grüße" oder "beste Grüße"
#
# ERWARTETES ERGEBNIS:
#   "Mit freundlichen Grüßen, [dein Name]"
#
# NÄCHSTER SCHRITT: Koan 10
# ============================================================

# user_name = getattr(settings, "USER_NAME", "[Name fehlt]")
user_name = "Sebastian"
FUZZY_MAP_pre = [
    # EXAMPLE: viele grüße
    # (f"Mit freundlichen Grüßen, {user_name}\n", r"^(beste grüße|mit freundlichen grüßen)\w*$"),

    # Viele Gruße
    (f"Viele Grüße {user_name}\n", r"^(viele gr.ße|jede gr.ße)$",
    81, {'flags': re.IGNORECASE}),
]

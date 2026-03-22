# config/maps/koans_deutsch/09_personal_signature/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401

from config import settings


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

user_name = getattr(settings, "USER_NAME", "[Name fehlt]")

FUZZY_MAP_pre = [
    (f"Mit freundlichen Grüßen, {user_name}\n", r"^(viele grüße|beste grüße|mit freundlichen grüßen)\w*$"),
]

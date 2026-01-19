# config/maps/koans_deutsch/09_personal_signature/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401

from config import settings
user_name = getattr(settings, "USER_NAME", "[Name fehlt]")

# too<-from
FUZZY_MAP_pre = [
    # EXAMPLE: mfg
    (f"Mit freundlichen Grüßen, {user_name}\n", r"^(mfg|viele grüße|best regards|Mit freundlichen Grüßen|Baum)\w*$"),

    # === FUZZY MATCHING TEST ===
    # Wort: Marmelade -> Ersetzung: LECKER

    # Test 1: Strenge Regel (Threshold 0 oder 100 - je nach System)
    # "Score" nutzt (0-100%): 100 = Exakt



]

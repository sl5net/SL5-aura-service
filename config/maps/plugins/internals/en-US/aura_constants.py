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


# CENTRAL AURA VARIANTS (GERMAN)

# This list combines aura_reg and AURA_VARIANTS.

# It catches noise and misinterpretations of the Vosk model.


# aurasMaple


_variants = (
    r'Aachen|but|a\wra|Ava|amber|fry need|apparatus|era|Also|aura|auras|auras|Aurora|maple|aurore|except|agora|'
    r'drill|need|book|burgess|cora|Dora|doha|doran|doras|your|yours|hey|hoa|high|horror|'
    r'hurrah|k|laura|Lorenz|looser|Nora|although|Oh|ohh|ooh|ear|ears|Opera|Obama|orally|Oprah|apparently|Overlay'
    r'Orange|ora|oradour|ore|ovh|ohhh|o\s+a\s+|ovals|over|prora|smoker|robe|rook|tube|Rohrer|red|'
    r'quiet|rum|samurai|search|more acidic|goals|thora|goals to|uwe|what|law|wizard|zoran|Homer'
)


AURA_VARIANTS = fr'({_variants})'
# Hurray closedOrange search documents

suche_reg = r'\b(search|seek|Schufa|to|book)\b'

# Your documentation

# Words Vosk often hallucinates in silence/noise.

# These lead to a reset of the buffer in the persistent session.

_wake_phantoms = (
    r'a|Munich|pay|Cologne|so support|eat|the disco|so|have|'
    r'morning|see let can|ln|Aachen|next to|offer|above|seek|make|'
    r'no|women away|Alan|good morning|to|next to hugo|find|come|floor|'
    r'Yes|away|fruit|cake|it'
)

WAKE_PHANTOM = [
    "einen", "münchen", "zahlen", "köln", "essen",
    "der disco", "nun", "haben", "morgen", "ln",
    "aachen", "neben", "bieten", "oben", "suchen", "machen", "nein",
    "frauen ab", "alan", "guten morgen", "an", "neben hugo", "finden",
    "kommen", "boden", "ja", "ab", "obst", "kuchen", "es", "Essen"
]

WAKE_PHANTOM_REGEX = fr'({_wake_phantoms})'

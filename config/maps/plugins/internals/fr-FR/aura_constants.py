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


# VARIANTES DE L'AURA CENTRALE (ALLEMAND)

# Cette liste combine aura_reg et AURA_VARIANTS.

# Il capte le bruit et les interprétations erronées du modèle Vosk.


# aurasÉrable


_variants = (
    r'Aix-la-Chapelle|mais|a\wra|Ava|ambre|frire besoin|appareil|ère|Aussi|aura|auras|auras|Aurore|érable|aurore|sauf|agora|'
    r'percer|besoin|livre|bourgeois|Cora|Dora|Doha|doran|doras|ton|le vôtre|Hé|hoah|haut|horreur|'
    r'Hourra|k|laure|Lorenz|plus lâche|Nora|bien que|Oh|ohh|ooh|oreille|oreilles|Opéra|Obama|oralement|Oprah|apparemment|Recouvrir'
    r'Orange|ora|oradour|minerai|oh|ohhh|o\s+a\s+|ovales|sur|prora|fumeur|peignoir|tour|tube|Rohrer|rouge|'
    r'calme|rhum|samouraï|recherche|plus acide|objectifs|Thora|objectifs à|uwe|quoi|loi|magicien|zoran|Homère'
)


AURA_VARIANTS = fr'({_variants})'
# Hourra ferméDocuments de recherche Orange

suche_reg = r'\b(recherche|chercher|Schufa|à|livre)\b'

# Votre documentation

# Mots Vosk hallucine souvent dans le silence/le bruit.

# Ceux-ci entraînent une réinitialisation du tampon dans la session persistante.

_wake_phantoms = (
    r'un|Munich|payer|Eau de Cologne|donc soutien|manger|le disco|donc|avoir|'
    r'matin|voir laisser peut|dans|Aix-la-Chapelle|près de|offre|au-dessus de|chercher|faire|'
    r'Non|femmes loin|Alain|bien matin|à|près de Hugo|trouver|viens|sol|'
    r'Oui|loin|fruit|gâteau|il'
)

WAKE_PHANTOM = [
    "einen", "münchen", "zahlen", "köln", "essen",
    "der disco", "nun", "haben", "morgen", "ln",
    "aachen", "neben", "bieten", "oben", "suchen", "machen", "nein",
    "frauen ab", "alan", "guten morgen", "an", "neben hugo", "finden",
    "kommen", "boden", "ja", "ab", "obst", "kuchen", "es", "Essen"
]

WAKE_PHANTOM_REGEX = fr'({_wake_phantoms})'

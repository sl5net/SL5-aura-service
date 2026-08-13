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


# VARIANTES DEL AURA CENTRAL (ALEMAN)

# Esta lista combina aura_reg y AURA_VARIANTS.

# Capta ruidos y malas interpretaciones del modelo Vosk.


# aurasarce


_variants = (
    r'Aquisgrán|pero|a\wra|ava|ámbar|freír necesidad|aparato|era|También|aura|auras|auras|Aurora|arce|aurora|excepto|ágora|'
    r'perforar|necesidad|libro|diputado|cora|dora|doha|doran|doras|su|tuyo|ey|hola|alto|horror|'
    r'Hurra|k|laura|lorenz|más flojo|nora|a pesar de|Oh|oh|Oh|oreja|orejas|Ópera|obama|oralmente|oprah|aparentemente|Cubrir'
    r'Naranja|ora|orador|mineral|ohh|oh|o\s+a\s+|óvalos|encima|prora|fumador|túnica|torre|tubo|Rohrer|rojo|'
    r'tranquilo|Ron|samurai|buscar|más ácido|objetivos|tóra|objetivos a|uwe|qué|ley|mago|Zoran|Homero'
)


AURA_VARIANTS = fr'({_variants})'
# Hurra cerradoBuscar documentos en naranja

suche_reg = r'\b(buscar|buscar|Schufa|a|libro)\b'

# Tu documentación

# Palabras Vosk a menudo alucina en silencio/ruido.

# Esto conduce a un reinicio del búfer en la sesión persistente.

_wake_phantoms = (
    r'a|Munich|pagar|Colonia|entonces apoyo|comer|el disco|entonces|tener|'
    r'mañana|ver dejar poder|en|Aquisgrán|junto a|oferta|arriba|buscar|hacer|'
    r'No|mujer lejos|alan|bien mañana|a|junto a hugo|encontrar|venir|piso|'
    r'Sí|lejos|fruta|pastel|él'
)

WAKE_PHANTOM = [
    "einen", "münchen", "zahlen", "köln", "essen",
    "der disco", "nun", "haben", "morgen", "ln",
    "aachen", "neben", "bieten", "oben", "suchen", "machen", "nein",
    "frauen ab", "alan", "guten morgen", "an", "neben hugo", "finden",
    "kommen", "boden", "ja", "ab", "obst", "kuchen", "es", "Essen"
]

WAKE_PHANTOM_REGEX = fr'({_wake_phantoms})'

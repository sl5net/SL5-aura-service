
# ZENTRALE AURA-VARIANTEN (DEUTSCH)
# Diese Liste kombiniert aura_reg und AURA_VARIANTS.
# Sie fängt Rauschen und Fehlinterpretationen des Vosk-Modells ab.

# aurasAhorn

_variants = (
    r'aachen|aber|a\wra|ava|ambra|anbraten brauche|Apparat|Ära|Auch|Aura|auras|auren|Aurora|Ahorn|aurore|auer|agora|'
    r'bohrer|brauche|buchen|burgess|cora|dora|doha|doran|doras|eure|eurer|hey|hoa|hoch|horror|'
    r'hurra|k|laura|lorenz|loser|Nora|obwohl|oh|ohh|ouh|ohr|ohren|Opera|obama|oral|Oprah|offenbar|Overlay|'
    r'Orange|ora|oradour|ore|ovh|oha|o\s+a\s+|ovale|over|prora|raucher|robe|roche|rohre|rohrer|rot|'
    r'ruhe|rum|samurai|suche|saurer|tore|thora|tore zu|uwe|woran|jura|zauberer|zoran|homer'
)


AURA_VARIANTS = fr'({_variants})'
# Hurra zugedrücktOrangene suche Dokumenten
suche_reg = r'\b(suche|suchen|schufa|zu|buch)\b'

# Eure Dokumentation
# Wörter, die Vosk oft bei Stille/Rauschen halluziniert.
# Diese führen in der persistenten Session zu einem Reset des Puffers.
_wake_phantoms = (
    r'einen|münchen|zahlen|köln|nun unterstützen|essen|der disco|nun|haben|'
    r'morgen|sehen lassen können|ln|aachen|neben|bieten|oben|suchen|machen|'
    r'nein|frauen ab|alan|guten morgen|an|neben hugo|finden|kommen|boden|'
    r'ja|ab|obst|kuchen|es'
)

WAKE_PHANTOM = [
    "einen", "münchen", "zahlen", "köln", "essen",
    "der disco", "nun", "haben", "morgen", "ln",
    "aachen", "neben", "bieten", "oben", "suchen", "machen", "nein",
    "frauen ab", "alan", "guten morgen", "an", "neben hugo", "finden",
    "kommen", "boden", "ja", "ab", "obst", "kuchen", "es", "Essen"
]

WAKE_PHANTOM_REGEX = fr'({_wake_phantoms})'

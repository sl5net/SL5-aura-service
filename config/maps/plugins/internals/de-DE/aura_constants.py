
# ZENTRALE AURA-VARIANTEN (DEUTSCH)
# Diese Liste kombiniert aura_reg und AURA_VARIANTS.
# Sie fängt Rauschen und Fehlinterpretationen des Vosk-Modells ab.

_variants = (
    r'aachen|aber|anbraten brauche|Apparat|Ära|Auch|Aura|auren|Aurora|aurore|'
    r'bohrer|brauche|buchen|burgess|dora|doras|eure|eurer|hey|hoa|hoch|horror|'
    r'hurra|k|laura|lorenz|loser|Nora|obwohl|oh|ohh|ohr|ohren|Opera|Oprah|'
    r'Orange|ora|ore|ovale|over|prora|raucher|robe|roche|rohre|rohrer|rot|'
    r'ruhe|rum|samurai|suche|tore|tore zu|uwe|woran|Zauberer'
)
AURA_VARIANTS = fr'({_variants})'

suche_reg = r'\b(suche|suchen|zu|buch)\b'

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

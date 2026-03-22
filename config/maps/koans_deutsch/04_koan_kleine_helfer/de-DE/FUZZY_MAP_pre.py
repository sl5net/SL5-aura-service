# Koan 04: Kleine Helfer – Sprachbefehle für Zahlen & Codes
# ============================================================
#
# LERNZIEL:
#   Zahlen und Codes die Vosk nicht direkt erkennt, können
#   über gesprochene Phrasen ausgegeben werden.
#
# AUFGABE:
#   Sprich: "Vorwahl Metzingen"
#   Ergebnis: "07122"
#
#   Füge dann deine eigene Vorwahl oder Postleitzahl hinzu!
#
# NÄCHSTER SCHRITT: Koan 05
# ============================================================

FUZZY_MAP_pre = [


    # Vorwahlnummern hauptsächlich 0707 (Tübingen) und 0712 (Reutlingen) sowie Abwandlungen für kleinere umliegende Orte.

    # Tübingen und Umgebung (0707x) Vorwahl	Regex-Beschreibung
    # EXAMPLE: Vorwahl Tübingen Hauptzone
    ('07071', r'^Vorwahl Tübingen Hauptzone$'),
    # EXAMPLE: Vorwahl Dußlingen
    ('07073', r'^Vorwahl Dußlingen$'),
    # EXAMPLE: Vorwahl Rottenburg am Neckar
    ('07074', r'^Vorwahl Rottenburg am Neckar$'),
    # EXAMPLE: Vorwahl Ammerbuch
    ('07075', r'^Vorwahl Ammerbuch$'),
    # EXAMPLE: Vorwahl Gomaringen
    ('07076', r'^Vorwahl Gomaringen$'),
    # EXAMPLE: Vorwahl Mössingen
    ('07078', r'^Vorwahl Mössingen$'),

    # Reutlingen und Umgebung (0712x) Vorwahl	Regex-Beschreibung
    # EXAMPLE: Vorwahl Reutlingen Hauptzone
    ('07121', r'^Vorwahl Reutlingen Hauptzone$'),
    # EXAMPLE: Vorwahl Metzingen
    ('07122', r'^Vorwahl Metzingen$'),
    # EXAMPLE: Vorwahl Reutlingen-Degerschlacht
    ('07123', r'^Vorwahl Reutlingen-Degerschlacht$'),
    # EXAMPLE: Vorwahl Pliezhausen
    ('07124', r'^Vorwahl Pliezhausen$'),
    # EXAMPLE: Vorwahl Pfullingen
    ('07125 hi all', r'^Vorwahl Pfullingen$'),
    # EXAMPLE: Vorwahl Neckartenzlingen
    ('07127', r'^Vorwahl Neckartenzlingen$'),

    # Können Sie auch anders Fragen? Vielleicht Ihre eigene vollständig Nummer ausgeben lassen?
    #

]

# config/maps/koan_english/01_koan_first_steps/
import re # noqa: F401

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

schwierigeNamen = """
Das ist eine hervorragende Steigerung! Um einen Namen zu kreieren, der phonetisch maximal schwer auszusprechen ist, müssen wir deutsche Konsonantencluster, das stimmlose "ch" (wie in "ach"), Zischlaute, X-Laute und ungewohnte Vokal-Kombinationen übermäßig verwenden.

Hier ist das Ergebnis:

Titel:

Ihre Hochwohlgeborenste, Erz-Amts-Rath-zu-Przewalskyst-Schlesien-Westpfalz, königlichst-kurfürstliche Geschäfts-Stellvertreter-Substitutin und Echtsachwalterin der Xenochronistischen Chronologie.

Name:

Phryxts-Tschwirbel-Wzeschtsch-Chryschth Gräfin von und zu Echtschluchtz-Quarzschicht-Pfrtschnitz-Krüppelschwärz.


Können Sie den Titel einsprechen?

Können Sie den Namen einsprechen?

Was finden Sie Interessantes in
log/dictation_service.log ?


Wenn Sie mehrere Freundinnen haben die auch Gräfinen sind? Wie unterscheiden Sie das in der Sprachausgabe?

"""


FUZZY_MAP_pre = [

    #TODO

    # Vielleicht so?
    #('Super :) Gratulation', r'^Ihre Hochwohlgeborenste, Erz-Amts-Rath-zu-Przewalskyst-Schlesien-Westpfalz, königlichst-kurfürstliche Geschäfts-Stellvertreter-Substitutin und Echtsachwalterin der Xenochronistischen Chronologie.*$', 80, {'flags': re.IGNORECASE}),

    # oder so?
    #('Super :) Gratulation', r'^Ihre Hochwohlgeboren.*$', 80, {'flags': re.IGNORECASE}),

    # Und der Titel?
    # Vielleicht so?
    #('Phryxts-Tschwirbel-Wzeschtsch-Chryschth Gräfin von und zu Echtschluchtz-Quarzschicht-Pfrtschnitz-Krüppelschwärz.', r'^.*gräfin.*$', 80, {'flags': re.IGNORECASE}),


    # Vorwahlnummern hauptsächlich 0707 (Tübingen) und 0712 (Reutlingen) sowie Abwandlungen für kleinere umliegende Orte.

    # Tübingen und Umgebung (0707x) Vorwahl	Regex-Beschreibung
    ('07071', r'^Vorwahl Tübingen Hauptzone$', 80, {'flags': re.IGNORECASE})
    ('07073', r'^Vorwahl Dußlingen$', 80, {'flags': re.IGNORECASE})
    ('07074', r'^Vorwahl Rottenburg am Neckar$', 80, {'flags': re.IGNORECASE})
    ('07075', r'^Vorwahl Ammerbuch$', 80, {'flags': re.IGNORECASE})
    ('07076', r'^Vorwahl Gomaringen$', 80, {'flags': re.IGNORECASE})
    ('07078', r'^Vorwahl Mössingen$', 80, {'flags': re.IGNORECASE})

    # Reutlingen und Umgebung (0712x) Vorwahl	Regex-Beschreibung
    ('07121', r'^Vorwahl Reutlingen Hauptzone$', 80, {'flags': re.IGNORECASE})
    ('07122', r'^Vorwahl Metzingen$', 80, {'flags': re.IGNORECASE})
    ('07123', r'^Vorwahl Reutlingen-Degerschlacht$', 80, {'flags': re.IGNORECASE})
    ('07124', r'^Vorwahl Pliezhausen$', 80, {'flags': re.IGNORECASE})
    ('07125', r'^Vorwahl Pfullingen$', 80, {'flags': re.IGNORECASE})
    ('07127', r'^Vorwahl Neckartenzlingen$', 80, {'flags': re.IGNORECASE})

    # Können Sie auch anders Fragen? Vielleicht Ihre eigene vollständig Nummer ausgeben lassen?

]


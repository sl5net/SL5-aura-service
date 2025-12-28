# config/maps/koans_deutsch/02_koan_listen/de-DE/FUZZY_MAP_pre.py

import re # noqa: F401

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

FUZZY_MAP_pre = [

    #TODO
    #('an', r'^[a-m]+.*$'),
    #('aus', r'^[n-z]+.*$'),

]

schwierigeNamen = """
Das ist eine hervorragende Steigerung! Um einen Namen zu kreieren, der phonetisch maximal schwer auszusprechen ist, müssen wir deutsche Konsonantencluster, das stimmlose "ch" (wie in "ach"), Zischlaute, X-Laute und ungewohnte Vokal-Kombinationen übermäßig verwenden.

Hier ist das Ergebnis:

Titel:

Ihre Hochwohlgeborenste, Erz-Amts-Rath-zu-Przewalskyst-Schlesien-Westpfalz, königlichst-kurfürstliche Geschäfts-Stellvertreter-Substitutin und Echtsachwalterin der Xenochronistischen Chronologie.

Name:

Phryxts-Tschwirbel-Wzeschtsch-Chryschth Gräfin von und zu Echtschluchtz-Quarzschicht-Pfrtschnitz-Krüppelschwärz.

Die phonetische Qual (Zum Zungenbrechen):

Phryxts-Tschwirbel-Wzeschtsch-Chryschth:

Phryxts: Startet mit "Phr" und endet auf eine harte Konsonanten-Kette (xts).

Tschwirbel: Eine Mischung aus tschechisch/polnisch klingenden Lauten.

Wzeschtsch: Eine fast unmöglich flüssig auszusprechende Kette von Zisch- und W-Lauten.

Chryschth: Beginnt mit dem harten Ch und endet auf schth.

Echtschluchtz-Quarzschicht-Pfrtschnitz-Krüppelschwärz:

Echtschluchtz: Zwei harte ch-Laute und tz in Folge.

Quarzschicht: Doppelte harte sch-Laute und ch direkt aufeinander.

Pfrtschnitz: Der Kern der Schwierigkeit: Pfr, tsch, und das rtschn im Zentrum – fast unmöglich ohne Pause auszusprechen.

Krüppelschwärz: Harte pp, sch, w, ärz – eine ungemütliche Mischung.

"""



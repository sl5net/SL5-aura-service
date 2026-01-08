# config/maps/plugins/it-begriffe/de-DE/FUZZY_MAP_pre.py
# file config/maps/plugins/it-begriffe/FUZZY_MAP_pr.py
# Beispiel: https://www.it-begriffe.de/#L
import re # noqa: F401

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - it stops with first full-match. Examples: ^...$ = Full Match = Stop Criterion! 
    # - first is read first imported, lower rules maybe not get read.

    #Mönch CarolinMit CarolinWenn CarolineManjaro Linux
    # EXAMPLE: whatchado
    ('Manjaro Linux', r'^\b(whatchado|Mönch) (Linux|Carolin\w*)(\b)$', 80, {'flags': re.IGNORECASE}),



    # EXAMPLE: Debatte ausgaben
    ('Debug-Ausgaben', r'^(Debatte ausgaben)$', 80, {'flags': re.IGNORECASE}),

    # EXAMPLE: program loaded
    ('Program loaded', r'^(Progra[m]+ loaded)$', 80, {'flags': re.IGNORECASE}),



    # EXAMPLE: Logdatei
    ('Logdatei', r'^(Logdatei|Kochdatei|log-datei)$', 80, {'flags': re.IGNORECASE}),

    # EXAMPLE: Logfile
    ('Logfile', r'^(\b)(Logfile)(\b)$', 80, {'flags': re.IGNORECASE}),

    # EXAMPLE: Relief
    ('release', r'^(\b)(Relief|release|Relief|wer dies)(\b)$', 75, {'flags': re.IGNORECASE}),

#Virtuell in Weibern
#Ritual in Deibel
# virtual in weibel
#Virtuell in weite
#virtuell in white
#Ritual in Weimarvirtual in weimar
#Virtual environment
#virtual in weiß witwen in weimarRitual in Weiß#Virtual environment
#Ritual in Deibelvirtual in weibelVirtuelle in DeibelWird schon in wein
#wird schon in weinWird schwer in warme
#wird schwer in warmeWirtschaft in Weimarwirtschaft in weimarVirtual environment
#witwer in wei mit
#Heiden wird je eine virtuelle Weibe verbindenWird wird es in Deibel
#Bachelorette DeibelVirtuell im WerbenVirtuell in wirbelnWildschweine in räumenVirtual environmentTitan wird hier in einem Ritual Environment verwendet
#virtuell in weivirtuell in räumen
#

    # EXAMPLE: Virtuell
    ('Virtual environment', r'\b(Virtuell|virtual|witwe\w*|witwer|wird schon|wird schwer|wirtschaft|wildschwein)\w* (in |wei |im )?(Weibe|white|weima|metall|wei|warm|wei mit|wirbeln|räumen|beweise|wallet)\w*\b', 75, {'flags': re.IGNORECASE,
            'skip_list': ['LanguageTool'],
    }),


#titan wird hier in einem virtual in weibe verwendet
#Virtual environmentTitan wird hier in einem Ritual Environment mit verbinden
#beiden wird hier in eine virtuelle weibe verwirrt
#titan wird jedem witwe in weibe verwendet
#Titan wird, hier liegtEinen MenschenneinBeiden wird hier deine Witwe salbe zu werdenBeiden wird hier deine Witwe salbe zu wen blöd
#Beiden wird hier in eine virtuelle Weibe verwirrt
#Beiden wird hier in einem ritt für den Leib verbinden
#Titan wird hier in einem virtuellen Weibe verwendet
# titan wird wird in weibel
#Beiden wird hier in einer wird für den falle verwendet
#Weiterhin wird hier in einem virtuell in bei mit verwendet
#Halten wird jedwedem Witwe wird Weibe verwenden
#titan wird hier in einem virtuellen wei metall verwendet
#Zeiten wird hier in einem Witwen in Weimar verbinden
#zeiten wird hier in einem witwen in weimar verbinden
#Scheitern wird hierSkaterTitan wird je in einem Witwer in bei mit verwenden
#titan wird je in einem witwer in wei mit verwenden
#Zeiten wird hier in einem Wildschwein in Weibe verwendet
#ützensagTitan wird hier in einem Ritual Environment mitverwendet

    # EXAMPLE: Brighton
    ('Python', r'^(\b)(Brighton|breit schon|Fallschirm|peitschen)(\b)$', 75, {'flags': re.IGNORECASE}),

    # EXAMPLE: beiden wird hier in einem Virtual environment mitverwendet
    ('Python wird hier in einer Virtual environment verwendet', r'^(beiden wird hier in einem Virtual environment mitverwendet|Beiden wird hier in einer wird für den falle verwendet|Weiterhin wird hier in einem virtuell in bei mit verwendet|Halten wird jedwedem Witwe wird Weibe verwenden|titan wird hier in einem virtual in weibe verwendet|beiden wird hier in einem virtuell in wei mitverwendet)$', 75, {'flags': re.IGNORECASE}),

    # EXAMPLE: sdf b bytes charme b
    ('PyCharm', r'^sdf(\b)(bytes charme)(\b)$', 75, {'flags': re.IGNORECASE}),

    # EXAMPLE: d fahl
    ('default', r'^(\b)(d fahl)(\b)$', 75, {'flags': re.IGNORECASE}),

    # EXAMPLE: Dringen
    ('String', r'^(\b)(Dringen)(\b)$', 75, {'flags': re.IGNORECASE}),


    # EXAMPLE: Kot abschnittt
    ('Code Abschnitt', r'\bKot\s*abschnittt\b', 82, {'flags': re.IGNORECASE}),

    # EXAMPLE: lobt Case
    ('lowerCase', r'\blobt\s*Case\b', 82, {'flags': re.IGNORECASE}),

    # EXAMPLE: stob Button
    ('StopButton', r'\bstob\s*Button\b', 82, {'flags': re.IGNORECASE}),
    # EXAMPLE: lobt Case
    ('lowerCase', r'\blobt\s*Case\b', 82, {'flags': re.IGNORECASE}),

    # EXAMPLE: AutoKey
    ('AutoKey', r'\bAuto k\b', 82, {'flags': re.IGNORECASE}),

    # EXAMPLE: bild prozess
    ('Build Prozess', r'\bbild prozess\b', 82, {'flags': re.IGNORECASE}),

    # EXAMPLE: opensource
    ('opensource', r'\bopensource\b', 75, {'flags': re.IGNORECASE}),

    # EXAMPLE: pipe
    ('|', r'\b(pipe|pipe symbol|paid symbol|treib symbol|Paypal Symbol|pep|prep simba|treib simba|Paypal Simba)\b', 75, {'flags': re.IGNORECASE}),

    # EXAMPLE: pipe
    ('|', r'\b(pipe|pipe|paid|treib|Paypal|pep|prep|treib|Paypal) (symbol|simba|simpel|simbel|schimmer|SIM)\b', 75, {'flags': re.IGNORECASE}),

    # EXAMPLE: at
    ('@', r'\b(at|ed) (symbol|simba|simpel|simbel|schimmer|SIM|shampoo|schimpfwort|Zeichen)\b', 75, {'flags': re.IGNORECASE}),
# ed shampoo denSchätzchen wurdenEr schimpft
#HiPaypalPaid symbolPepWeib SymbolTreib SymbolPythonPaypal SymbolWeibchenbrät SimbaWeibchenPaypal Simbafeit SchimpfTreibt simpelVeit SchimmelPep Schimmer
#Häppchenbei SIMPaypal SIMHalb SIMPep simpel||Plätzchenbacken

 # Logfile-Duden  Logfile-Duden Logfile-Logdatei Nordwärts erreicht Logfile-Logdatei Logfile-Logdatei  Edits Relief Vernissage Kredit Kredit feststellt Wer dies Edit Wer dies




]




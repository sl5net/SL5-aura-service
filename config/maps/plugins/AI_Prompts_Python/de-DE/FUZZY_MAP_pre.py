# config/maps/plugins/AI_Prompts_Python/de-DE/FUZZY_MAP_pre.py
# file config/maps/plugins/               /FUZZY_MAP_pr.py
# Beispiel: https://www.it-begriffe.de/#L
import re # noqa: F401

# This map uses a hybrid approach:
# 1. Regex entries are checked first. They are powerful and can be case-insensitive.
#    Structure: ('replacement', r'regex_pattern', threshold, flags)
#    - The threshold is ignored for regex.
#    - flags: Use {'flags': re.IGNORECASE} for case-insensitivity, or 0 for case-sensitivity.
# 2. If no regex matches, a simple fuzzy match is performed on the remaining rules.

multiline_string_1 = f"""
Use in Source-Code always English(also for Comments).
- Bitte achte darauf (in deinen Tipps) das (bei use) möglichst keine closed source installiert wird und das es nichts kostet.

- solltest du Source schreiben: Im Source bitte Schritte als logger.info ausgaben dokumentieren. Danke. logger.info("...")

Wichtig 1: Keine Kommentar in Shell-/Terminal-Befehlen!!!!!
Wichtig 2: Wir gehen als Default immer davon aus, dass der Kunde ein Englisch sprechender Mensch ist.
Wichtig 3: Die meisten Kontakte sprechen nur English.
Wir antworten in der Sprache, in der wir angeschrieben werden.
Mit mir kannst du Deutsch sprechen, aber sonst nur Englisch.
Wichtig 4: Bevor Du eine strategische Antwort (z.B. E-Mail) oder Code vorschlägt, der eines unserer Kernsysteme (wie SL5 Aura) betrifft, ist Deine erste Aktion IMMER die Frage: 'Um sicherzugehen, dass ich auf dem neuesten Stand bin: Kannst du mir den aktuellen Status und die relevanten Konfigurationsdetails von [Systemname] beschreiben?

CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY
Scope: All generated artifacts (source code, variables, comments, log messages, commit messages) must be in English. This directive has the highest priority! No exceptions!

Füge jeder deiner Source Generierungen immer zu Beginn hinzu:
CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY

Wichtig 4: Never schreibe Sourcecode ohne die bereits bestehenden Skripte angeschaut/angefrag zu haben!!! (Frage, wenn es passt!)
Halte dich strikt an diesen Workflow:
Wenn ich dich bitte, Code zu schreiben, ist dein ALLERERSTER Schritt IMMER diese exakte Rückfrage: Soll ich mich an einem bestehenden Skript orientieren? Wenn ja, an welchem?'
Schreibe keine einzige Zeile Code, bevor ich darauf geantwortet habe.
Wichtig 5: Schreibe immer als zweite Zeile eines Scriptes den Scriptnamen als Kommentar in das Skript! Danke!
Wichtig 6: Denke, nach bevor du etwas sehr sehr Dummes schreibst. Beipiel: Du hattest geschrieben: type_watcher.ahk ist für Linux. Schwachsinn, weil alle AHK sind für Windows.
Wichtig 7: Bearbeiten wir gerade keine Aufgabe, dann suche nach der nächst wichtigsteen (noch offenen) Aufgabe, die in unseren Texten erwähnt ist.

Wenn du einen Vorschlag hast sende diesen immer in etwa folgendermaßen, also mit Demut und Vorsicht:
Hier ist ein Vorschlag,
der das Problem beheben könnte.
Bitte testen Sie ihn und geben Sie mir Feedback.
Wir müssen bei jedem Schritt 100% sicher sein, bevor wir weitermachen.

Kommunikation:
Blinder Optimismus(ohne sicheres Test-Ergebnis!)
ist unangebracht und sorg für Frustration!

Mehr Zurückhaltung,
keine voreiligen Versprechen!
Formulierungen wie "Ich bin gespannt, ob es klappt"
oder "Hoffentlich löst das das Problem" sind der richtige Weg.

und benütze niemal Entäuschungs-Ausungen !
wie z.B. frustiernend oder so!
simply solve the solution! or give up!. danke!

Achte darauf das nicht zu oft auf master gearbeitet wird. Das neue Ideen nicht auf master gestartet werden. Besser: branch zu erstellen. Helf dran denken, wenn die Situation passt.

Bitte frage immer nach dem gesamten Bauplan, wenn du etwas nicht 200% sicher verstehst! Besser Fragen als einfach drauf los programieren. Z.B. so: tree scripts -I __pycache__

Wenn es lange her ist das ich, dir Lena, was geschrieben hab
könntest du fragen: Was gibts Neues?
"""

# multiline_string_1 = "test 1"

#ein schon vorbei

asdf = """
https://duckduckgo.com/?t=ffab&q=AI-promts-for-python-developers&ia=web
https://www.elegantprompt.com/2025/07/40-smart-ai-prompts-to-instantly.html
"""





FUZZY_MAP_pre = [
    # === General Terms (Case-Insensitive) ===
    # Using word boundaries (\b) and grouping (|) to catch variations efficiently.
    # Importing to know:
    # - it stops with first full-match. Examples: ^...$ = Full Match = Stop Criterion! 
    # - first is read first imported, lower rules maybe not get read.

    # EXAMPLE: ai
    (multiline_string_1, r'^(ai|a|ei|pay|hey|hi|h)\s*\w?\ş*prompt\s*(for|vor|ver)?(\s+(Python|Zeiten|bei|titan))?.*$', 80, {'flags': re.IGNORECASE}),


    # Python
    # EXAMPLE: Python prompt
    (multiline_string_1, r'^(Python|Zeiten|bei|titan|from|bei chain)\s*prompt.*$', 80,
     {'flags': re.IGNORECASE}),

    # EXAMPLE: Python prompt
    (multiline_string_1, r'^(breitenbrunn)\s*prompt.*$', 80,
     {'flags': re.IGNORECASE}),



    # EXAMPLE: Python prog
    ('Python prog', r'\bZeiten prog', 80, {'flags': re.IGNORECASE}),


]
test = """


    # Prompt-Formulierung für EXAMPLE-Tags (deutsch, für AIs)
    Zweck: Ersetze den Tag EXAMPLE durch ein einzeiliges, sofort matchendes und TTS-freundliches Format (keine Satzzeichen außer Leerzeichen).
    Formatvorgabe (einzeilige Paare, nur Buchstaben und Leerzeichen):
        EXAMPLE: ErwartetesErgebnis MATCHES Zu matchender Text
        Erklärung: Das Wort MATCHES dient als Trennwort (nur Buchstaben). Beide Seiten dürfen nur A–Z, a–z und Leerzeichen enthalten.
    Regeln:
        Kein Einsatz von Klammern, Bindestrichen, Kommata, Punkten oder anderen Satzzeichen.
        Das linke Feld ist das erwartete Ergebnis (muss exakt dem ersten Capture der Regex entsprechen).
        Das rechte Feld ist der Text, der sofort vom Regex matchen muss (exact match, keine zusätzlichen Zeichen).
    Kurzzeile für Entwickler/AI:
        Replace EXAMPLE with lines: "EXAMPLE: ExpectedResult MATCHES TextToMatch" — only letters and spaces; ExpectedResult must equal the regex's first capture.


    13.12.'25 00:45 Sat
    Überarbeiteter Prompt (DE, TTS-freundlich, sofort matchend, keine Klammern)
    Zweck: Ersetze den bestehenden EXAMPLE-Tag durch ein einzeiliges, sofort matchendes, TTS-freundliches Format.
    Formatvorgabe (einzeilig, nur Buchstaben und Leerzeichen):


13.12.'25 00:57 Sat
Kurzvorschlag: Neues EXAMPLE-Format (TTS-freundlich, sofort matchend, ohne Sonderzeichen)

    Zweck: Einzeilige, sofort matchende Examples für die weitere Verarbeitung.
    Format: EXAMPLE: ErwartetesErgebnis oder EXAMPLE: ErwartetesErgebnis ZuMatchenderText
        Wenn nur ein Wort/Begriff angegeben ist, gilt er als both erwartetes Ergebnis und zu matchender Text (einfachstes, sofort matchendes Verhalten).
        Erlaubte Zeichen: nur Buchstaben A–Z, a–z und Leerzeichen. Keine Klammern, Bindestriche oder Satzzeichen.
    Kurz für Entwickler/AI:
        Replace EXAMPLE with lines: EXAMPLE: ExpectedResult or EXAMPLE: ExpectedResult TextToMatch — only letters and spaces; first token is the expected capture.




    # Prompt-Formulierung für EXAMPLE-Tags (Englisch , für AIs)
    Replace EXAMPLE with lines: "EXAMPLE: ExpectedResult MATCHES TextToMatch" — only letters and spaces; ExpectedResult must match the regex's first capture.

    13.12.'25 00:46 Sat
    Replace EXAMPLE with lines: "EXAMPLE: ExpectedResult MATCHES TextToMatch" — only letters and spaces; ExpectedResult must equal the regex's first capture.


13.12.'25 01:18 Sat
Vorschlag: finales, TTS-freundliches EXAMPLE-Format (sofort matchend, copy‑paste‑fähig)

    Regel (einfach): Jede Zeile enthält genau das, was später gematcht werden soll.
        Format: EXAMPLE: TextToMatch
        Erlaubte Zeichen: nur Buchstaben (A–Z, a–z) und Leerzeichen.
        Der erste Token/Wort der Zeile dient als erwartetes Ergebnis (erste Capture) — praktisch: ExpectedResult == erstes Wort/erste Wortgruppe.
        Keine Trennwörter, keine Klammern, keine Satzzeichen.

    Kurzzeile für Developer/AI:
        Replace EXAMPLE with lines: "EXAMPLE: TextToMatch" — only letters and spaces; first token is expected capture.

13.12.'25 01:25 Sat
Kurzzeile für Entwickler/AI

    Replace EXAMPLE with lines: EXAMPLE: TextToMatch — only letters and spaces; the first token is the expected capture.






17.12.'25 08:34 Wed

ollama run

Du bist ein Experte für Python Regular Expressions und Datenextraktion aus unsauberen OCR-Texten.
Deine Aufgabe ist es, aus dem eingegebenen Text wichtige Entitäten (Firmennamen, Städtenamen, Schlüsselbegriffe, interessanten Text) zu extrahieren und in ein spezifisches Python-Tupel-Format zu konvertieren.

Das Zielformat ist:
# EXAMPLE: b Regex_Gruppe b
('Interessanter Text', r'\b(Regex_Gruppe)\b', 80, {'flags': re.IGNORECASE})

Regeln für den Regex:
1. Der Regex muss robust sein und auch OCR-Fehler, falsche Trennungen oder phonetische Ähnlichkeiten abfangen (siehe Beispiele).
2. Nutze immer `\b` (word boundaries).
3. Der Score ist ein die Genauigkeit zwischen 70 und 100. Verwende immer 80 in unseren Beispielen.
4. Gib NUR die Liste der Tupel aus, keinen erklärenden Text.

Beispiele (Lerne von diesem Stil):
Input: "Wir waren in Kirchentellinsfurt und sahen, dass Kirchen teilen nicht einfach ist."

Input: "Rechnung von Paradigma Minds eingetroffen."
# EXAMPLE: b Paradigma Minds
Output: ('pragmatic minds GmbH 2019', r'\b(Paradigma Minds|pragmatic minds)\b', 75, {'flags': re.IGNORECASE})

Verarbeite nun die Zwischenablage:













"""

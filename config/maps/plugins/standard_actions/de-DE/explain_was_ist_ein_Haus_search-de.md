Diese Zeilen sind Konfigurationseinträge für die **Regel-Engine**.

Jeder Eintrag definiert eine **Regel** (oder einen *Intent*) in einer Tupel-Struktur, die ungefähr so aufgebaut ist:

```
(Ausgabe/Bezeichner, Regular Expression (RegEx) Muster, Einstellungen-Dictionary)
```

Hier ist die Erklärung, was passiert und wofür die Kombination dieser Regeln gut ist:

---

### 1. Regel: Spezifische Markierung/Etikettierung

```python
("was ist ein haus (Begriffsklärung)", r'^.*was ist ein haus$', 
 {
'flags': re.IGNORECASE,
'skip_list': ['LanguageTool','fullMatchStop'],
}),
```

| Element | Was passiert | Nutzen und Zweck |
| :--- | :--- | :--- |
| **`"was ist ein haus (Begriffsklärung)"`** | Dies ist der **Ausgabe-Text** oder der **interne Bezeichner** (Label), der generiert wird, wenn die Regel zutrifft. | **Vorverarbeitung.** Er liefert dem nachfolgenden Prozess einen präziser formulierten Suchbegriff. |
| **`r'^.*was ist ein haus$'`** | Die **Reguläre Expression**. Sie sucht nach der exakten Phrase "was ist ein haus" am Ende der Eingabe. | **Präzises Matching.** Definiert die genaue Benutzereingabe, die diese spezifische Regel auslöst. |
| **`'flags': re.IGNORECASE`** | **Case-Insensitive Match.** Groß- und Kleinschreibung wird ignoriert. | |
| **`'skip_list': ['fullMatchStop']`** | **Dies ist der Schlüssel.** Normalerweise stoppt das System die Regelsuche, sobald eine fullMatch gefunden wird. Durch das Hinzufügen von `fullMatchStop` zur `skip_list` wird dieser **Stopp explizit verhindert**. | **Regelkette/Vorverarbeitung.** Es stellt sicher, dass die Verarbeitung **fortgesetzt** wird und die nächste Regel (die allgemeine Suche) den *markierten* Text verarbeiten kann. |

**Zusammenfassend:** Diese Regel fängt die spezifische Frage ab, **markiert** den resultierenden Text mit der notwendigen **` (Begriffsklärung)`-Ergänzung** und leitet ihn zur weiteren Verarbeitung weiter.

---

### 2. Regel: Allgemeine Ausführung/Suche

```python
('', r'(suche auf wikipedia nach|was sind|was ist|wer ist|wo ist|Wie groß ist)( ein| die| das| der)? (?P<search>.*)', {
'flags': re.IGNORECASE,
'on_match_exec': [CONFIG_DIR / 'wikipedia_local.py']
}),
```

| Element | Was passiert | Nutzen und Zweck |
| :--- | :--- | :--- |
| **`''`** | Der Ausgabetext ist leer. Dies signalisiert, dass die Regel **keine direkte Antwort** liefert, sondern eine Aktion auslöst. | **Dynamische Antwort.** Die eigentliche Antwort wird vom auszuführenden Skript generiert. |
| **`r'(...) (?P<search>.*)'`** | Die **Reguläre Expression für allgemeine Anfragen**. Sie matcht eine Vielzahl von Fragewörtern (`was ist`, `wer ist`, etc.) und fängt den Rest der Eingabe in der **benannten Erfassungsgruppe** (`?P<search>`) ein. | **Generische Abfragen.** Fängt die meisten offenen Fragen ab und extrahiert das eigentliche Suchthema. |
| **`'on_match_exec': [...]`** | Dies ist die **Schlüsselaktion**. Die Regel weist das System an, ein externes Python-Skript (`wikipedia_local.py`) auszuführen. Dieses Skript erhält den erfassten Suchbegriff. | **Externe Funktionalität.** Der Befehl delegiert die Arbeit (die eigentliche Wikipedia-Suche) an das externe Skript. |

---

### Der integrierte Workflow (Der eigentliche Zweck)

Die beiden Regeln arbeiten **sequentiell** zusammen, da die erste Regel den Prozess nicht stoppt:

1.  **Eingabe:** Der Benutzer sagt/tippt: `"was ist ein haus"`.
2.  **Regel 1 trifft zu:** Die Eingabe wird gematcht.
    *   Der Ergebnis-Text wird zu: `"was ist ein haus (Begriffsklärung)"`.
    *   Die Verarbeitung wird **NICHT** gestoppt.
3.  **Regel 2 trifft zu:** Die zweite Regel matcht nun den **markierten Ergebnis-Text** von Regel 1.
    *   Die Regex erfasst den Suchbegriff (`?P<search>`) aus dem **neuen Text**.
    *   Der erfasste Suchbegriff ist: **`haus (Begriffsklärung)`**.
4.  **Aktion:** Das Skript `wikipedia_local.py` wird ausgeführt und führt die Wikipedia-Suche **gezielt** nach dem Begriff **`haus (Begriffsklärung)`** durch.

**Ergebnis:** Durch diese Kaskadierung wird eine einfache, mehrdeutige Eingabe in einen präzisen Suchbefehl **vorverarbeitet**, um direkt auf den Wikipedia-Artikel zur Begriffsklärung zu verweisen und eine allgemeinere Antwort zu verhindern.

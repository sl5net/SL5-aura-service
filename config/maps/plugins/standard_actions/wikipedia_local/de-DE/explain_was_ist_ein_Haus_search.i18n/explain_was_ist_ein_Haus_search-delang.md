# Klärung des genauen Verhaltens des Workflows Ihres Systems:
  
### Erläuterung des integrierten Workflows korrigiert

die erste Regel für **Eingabetransformation** und **Beschriftung**, bevor die letzte Suchaktion durch die zweite Regel ausgeführt wird.

#### 1. Eingabe: „was ist ein haus“

#### 2. Regel 1: Kennzeichnung/Transformation

```python
("was ist ein haus (Begriffsklärung)", r'^.*was ist ein haus$', 90,
 {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool','fullMatchStop']})
```

* **Aktion:** Die Benutzereingabe „was ist ein haus“ wurde erfolgreich abgeglichen.
* **Ergebnis (intern):** Das System generiert die Ausgabe/Beschriftung „was ist ein haus (Begriffsklärung)“.
* **Fortsetzung:** Da „fullMatchStop“ in der „skip_list“ enthalten ist, wird der Regelabgleich **NICHT STOPPT**. Der Prozess wird mit der nächsten Regel fortgesetzt, die den *transformierten* oder *beschrifteten* Inhalt enthält.

#### 3. Regel 2: Allgemeine Aktion/Ausführung

```python
('', r'(suche auf wikipedia nach|was sind|was ist|wer ist|wo ist|Wie groß ist)( ein| die| das| der)? (?P<search>.*)', 90, {
'flags': re.IGNORECASE,
'on_match_exec': [CONFIG_DIR / 'wikipedia_local.py']
})
```

* **Aktion:** Das System stimmt jetzt wahrscheinlich mit dem **aktuellen Ergebnis/Label** aus dem vorherigen Schritt überein, nämlich „was ist ein haus (Begriffsklärung)“ (oder es stimmt mit der ursprünglichen Eingabe überein, aber das ausgeführte Skript priorisiert das transformierte Label).
* **Präfixübereinstimmung:** Das Präfix („was ist“) stimmt immer noch überein.
* **Capture-Gruppe:** Die Capture-Gruppe „(?P<search>.*)“ erfasst den Rest der Zeichenfolge:
* Wenn das System die **Ausgabe von Regel 1 als neue Eingabe** verwendet, erfasst es: **`haus (Begriffsklärung)`** (oder die vollständige transformierte Zeichenfolge, die dann vom Ausführungsskript analysiert wird).
* **Ausführung:** Das Skript „wikipedia_local.py“ wird ausgeführt.

#### 4. Letzte Aktion:

* Das Skript „wikipedia_local.py“ erhält den speziell geänderten Suchbegriff/Label.
* Das Skript führt eine Wikipedia-Suche nach dem beabsichtigten Begriff durch: **`haus (Begriffsklärung)**.

**Abschluss:**

Dieses Setup ist eine elegante Möglichkeit, mehrdeutige oder generische Abfragen zu bearbeiten. Indem die spezifische Regel die Eingabe ändert oder eine gezielte Bezeichnung generiert und dann den Prozess zwingt, mit der allgemeinen Suchregel fortzufahren, stellen Sie sicher, dass die Wikipedia-Suche nicht nach dem generischen „haus“, sondern nach dem spezifischen, eindeutigen Eintrag ausgeführt wird: **`haus (Begriffsklärung)`**.

Dies bestätigt, dass der Ausschluss von „fullMatchStop“ **wesentlich** ist, damit die erste Regel die Abfrage vorverarbeiten und anreichern kann, bevor sie von der allgemeinen Ausführungsregel bearbeitet wird.

(sl5,4.12.'25 12:24 Do)
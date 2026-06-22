# Fuzzy-Map-Makros und Bracket-Logik

Aura unterstützt die Gruppierung mehrerer Vorverarbeitungsregeln in „FUZZY_MAP_pre.py“-Dateien, um sie nacheinander als zusammenhängende Pipeline auszuführen, sobald eine „Startregel“ ausgelöst wird. Dieses Dokument beschreibt die Designphilosophie, Syntax und den Ausführungsablauf dieser Funktion.

## Grundlegende Designprinzipien

1. **Null Redundanz**: Regeln innerhalb einer Gruppe bleiben Standard-Python-Tupel:
`('replacement_text', r'regex_pattern', Schwellenwert, flags_and_options)`
2. **Doppelte Benutzerfreundlichkeit**: Einzelne Regeln innerhalb einer Gruppe sind voll funktionsfähige eigenständige Regeln. Wenn die Gruppe nicht ausgelöst wird, werden sie in der übergeordneten Schleife normal ausgewertet.
3. **Passiver Endmarker**: Das Ende einer Gruppe wird durch einen passiven Regeleintrag definiert, der niemals alleine erfüllt wird. Es fungiert lediglich als Grenzmarkierung für den Parser.
4. **Hybrid-Fallback (Append-on-Non-Match)**: Wenn eine Gruppe aktiv ist, muss jede innere Regel zur Ausgabe beitragen. Wenn der reguläre Ausdruck einer inneren Regel mit dem Text übereinstimmt, findet die normale Ersetzung statt. Wenn er nicht übereinstimmt, wird der Ersatztext mit einem Leerzeichen an den aktuellen Text angehängt.

---

## Syntax und Struktur

Eine Makrogruppe wird definiert, indem eine Reihe von Standardregeln zwischen einer **Startregel** und einer **Endregel** in „FUZZY_MAP_pre.py“ eingeschlossen werden.

### 1. Die Startregel
Die Startregel ist eine Standardregel, die bei Übereinstimmung das Makro auslöst. Es enthält einen „group_start“-Schlüssel in seinem Optionswörterbuch:
```python
('replacement', r'start_pattern', 100, {'group_start': 'unique_group_name'})
```

### 2. Innere Regeln
Innere Regeln sind Standardregeln, die sequentiell nach der Startregel platziert werden. Sie erfordern keine besonderen Metadaten:
```python
('inner_replacement', r'inner_pattern', 100, {})
```

### 3. Die Endregel (Passiver Marker)
Die Endregel hat einen „None“-Ersatz, ein leeres Muster und einen „group_end“-Schlüssel in ihrem Optionswörterbuch:
```python
(None, r'', 100, {'group_end': 'unique_group_name'})
```

---

## Konkretes Beispiel

Hier ist ein praktischer Testfall, der in einer Datei „FUZZY_MAP_pre.py“ definiert ist:

```python
FUZZY_MAP_pre = [
    # Start Rule: Triggers the group 'sandbox_test' when "start sandbox" matches
    ('Sandbox:', r'start\w* sandbox', 100, {'group_start': 'sandbox_test'}),
    
    # Inner Rule 1: Replaces "apfel" with "birne" if present
    ('birne', r'apfel', 100, {}),
    
    # Inner Rule 2: Replaces "banane" if present, otherwise appends "banane"
    ('banane', r'banane', 100, {}),
    
    # End Rule: Passive boundary marker
    (None, r'', 100, {'group_end': 'sandbox_test'}),
]
```

### Ausführungsablaufszenarien:

* **Szenario A (ausgelöstes Makro)**:
* Eingabe: „Sandbox mit Apfel starten“.
* Erwarteter Fluss:
1. Die Startregel stimmt mit „start sandbox“ überein und ersetzt sie durch „Sandbox:“ -> aktueller Text: „Sandbox: mit apfel“.
2. Die Gruppe „sandbox_test“ wird ausgelöst.
3. Wir führen die inneren Regeln rekursiv auf „Sandbox: mit apfel“ aus:
- Innere Regel 1 entspricht „apfel“ und wird durch „birne“ ersetzt -> aktueller Text: „Sandbox: mit birne“.
- Innere Regel 2 stimmt nicht mit „banane“ überein. Da die Gruppe aktiv ist, greift sie auf das Anhängen von „banane“ zurück -> Aktueller Text: „Sandbox: mit birne banane“.
4. Der endgültige Text „Sandbox: mit birne banane“ wird von LanguageTool zurückgegeben und korrigiert.
* Ausgabe: „Sandbox: mit Birne Banane“.

* **Szenario B (nicht ausgelöstes Makro – doppelte Benutzerfreundlichkeit)**:
* Eingabe: „ein apfel und eine kirsche“.
* Erwarteter Fluss:
1. Die Startregel stimmt nicht überein. Die Gruppe „sandbox_test“ bleibt inaktiv.
2. Die Schleife fährt mit der nächsten Regel fort.
3. **Innere Regel 1**: Entspricht „apfel“ und ersetzt es durch „birne“ -> Aktueller Text: „ein birne und eine kirsche“.
4. **Innere Regel 2**: Stimmt nicht überein. Da die Gruppe nicht ausgelöst wurde, verhält sich die Regel wie eine normale eigenständige Regel und **es wird nichts angehängt**.
5. Die Endregel wird ignoriert.
* Ausgabe: „eine birne und eine kirsche“.

---

## Technische Details (Unter der Haube)

* **Isolierte Rekursion**: Wenn eine Gruppe ausgelöst wird, ruft die Engine rekursiv „process_text_in_background“ mit „custom_rules=[inner_rule]“ auf. Dadurch kann jede innere Regel innerhalb eines vollständigen, synchronen Pipeline-Durchlaufs ausgeführt werden.
* **Leistungs- und Stabilitätsgarantien**:
* **Sequenzumgehung**: Innere rekursive Läufe umgehen die Sequenzwarteschlange „chunk_id“, um Deadlocks und Ausführungsverzögerungen zu verhindern.
* **E/A- und TTS-Unterdrückung**: Rekursive Ausführungen unterdrücken das Schreiben von Zwischendateien und TTS-Sprachausgaben und stellen so sicher, dass nur der endgültige stabilisierte Text geschrieben und gesprochen wird.
* **Stabilitätssicherung**: Rekursive Ausführungen werden nach einer Iteration unbedingt unterbrochen, um endlose Stabilitätsschleifen während Fallback-Anhängen zu verhindern.
* **Sichere Beendigung**: Die Stabilitätsprüfung basiert ausschließlich auf der maximalen Anzahl von Iterationen („MAX_ITERATIONS_FOR_SAFETY“), um Endlosschleifen zu verhindern und zeitbasierte Drosselung zu umgehen, die legitime, langsamere Makroausführungen vorzeitig abbrechen könnte.
__CODE_BLOCK_4__
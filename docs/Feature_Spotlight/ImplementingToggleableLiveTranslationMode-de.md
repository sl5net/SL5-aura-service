## Feature Spotlight: Implementierung eines umschaltbaren Live-Übersetzungsmodus

Unser einsteckbares Sprachassistenten-Framework ist auf maximale Flexibilität ausgelegt. In diesem Handbuch wird eine leistungsstarke Funktion demonstriert: ein Live-Übersetzungsmodus, der mit einem einfachen Sprachbefehl ein- und ausgeschaltet werden kann. Stellen Sie sich vor, Sie sprechen mit Ihrem Assistenten auf Deutsch, hören die Ausgabe auf Portugiesisch und kehren dann sofort zum normalen Verhalten zurück.

Dies wird nicht durch eine Änderung der Kern-Engine erreicht, sondern durch eine geschickte Manipulation der Regelkonfigurationsdatei selbst.

### Wie man es benutzt

Um dies einzurichten, müssen Sie Ihrer Datei „FUZZY_MAP_pre.py“ zwei Regeln hinzufügen und die entsprechenden Skripte erstellen.

**1. Die Umschaltregel:** Diese Regel wartet auf den Befehl zum Ein- oder Ausschalten des Übersetzungsmodus.

```python
# Rule to turn the translation mode on or off
    ('', r'^(portugiesisch|übersetzung|übersetzer) (aktivieren|aktiviert|aktiv|einschalten|deaktivieren|ausschalten|toggle|Dogge|doppelt)\b', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),
```
Wenn Sie „Übersetzung einschalten“ sagen, wird das Skript „toggle_translation_mode.py“ ausgeführt.

**2. Die Übersetzungsregel:** Dies ist eine „Catch-All“-Regel, die, wenn sie aktiv ist, jeden Text abgleicht und ihn an das Übersetzungsskript sendet.

```python
    # ANCHOR: The following line is controlled by the toggle script.
    # TRANSLATION_RULE
    ('', r'.+', 5, {'flags': re.IGNORECASE,'on_match_exec': [CONFIG_DIR / 'translate_german_to_portuguese.py']}),
```
Der Schlüssel hier ist der Kommentar „# TRANSLATION_RULE“. Dies fungiert als „Anker“, den das Umschaltskript verwendet, um die darunter liegende Regel zu finden und zu ändern.

### Wie es funktioniert: Die Magie hinter dem Vorhang

Anstatt einen internen Status zu verwenden, bearbeitet diese Methode direkt die Regelzuordnung im Dateisystem. Das Skript „toggle_translation_mode.py“ fungiert als Konfigurationsmanager.

1. **Finden Sie die Regel:** Wenn das Skript ausgelöst wird, liest es den Inhalt von „FUZZY_MAP_pre.py“. Es sucht nach dem eindeutigen Ankerkommentar „# TRANSLATION_RULE“.

2. **Status umschalten:**
* **Zum Deaktivieren:** Wenn die Regelzeile unter dem Anker aktiv ist, fügt das Skript am Anfang der Zeile ein „#“ hinzu, wodurch sie effektiv auskommentiert und deaktiviert wird.
* **Zur Aktivierung:** Wenn die Regelzeile bereits auskommentiert ist, entfernt das Skript sorgfältig das führende „#“ und aktiviert die Regel erneut.

3. **Speichern und neu laden:** Das Skript speichert den geänderten Inhalt zurück in „FUZZY_MAP_pre.py“. Anschließend wird eine spezielle Triggerdatei erstellt (z. B. „RELOAD_RULES.trigger“). Der Hauptdienst sucht ständig nach dieser Triggerdatei. Wenn es angezeigt wird, weiß der Dienst, dass sich seine Konfiguration geändert hat, lädt die gesamte Regelzuordnung neu von der Festplatte und übernimmt die Änderung sofort.

### Designphilosophie: Vorteile und Überlegungen

Dieser Ansatz, die Konfigurationsdatei direkt zu ändern, wurde aufgrund seiner Klarheit und Einfachheit für den Endbenutzer gewählt.

#### Vorteile:

* **Hohe Transparenz:** Der aktuelle Zustand des Systems ist immer sichtbar. Ein kurzer Blick in die Datei „FUZZY_MAP_pre.py“ verrät sofort, ob die Übersetzungsregel aktiv oder auskommentiert ist.
* **Keine Änderungen an der Kern-Engine:** Diese leistungsstarke Funktion wurde implementiert, ohne eine einzige Zeile der Kern-Regelverarbeitungs-Engine zu ändern. Es demonstriert die Flexibilität des Plugin-Systems.
* **Intuitiv für Entwickler:** Das Konzept, einen Teil der Konfiguration durch Auskommentieren zu aktivieren oder zu deaktivieren, ist ein vertrautes, einfaches und vertrauenswürdiges Muster für jeden, der mit Code oder Konfigurationsdateien gearbeitet hat.

#### Überlegungen:

* **Dateisystemberechtigungen:** Damit diese Methode funktioniert, muss der Prozess des Assistenten über Schreibberechtigungen für seine eigenen Konfigurationsdateien verfügen. In manchen Hochsicherheitsumgebungen könnte dies eine Überlegung sein.
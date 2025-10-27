## Neue Plugin-Module erstellen

Unser Framework verwendet ein leistungsstarkes Auto-Discovery-System zum Laden von Regelmodulen. Dadurch ist das Hinzufügen neuer Befehlssätze einfach und sauber, ohne dass jede neue Komponente manuell registriert werden muss. In diesem Leitfaden wird erläutert, wie Sie Ihre eigenen benutzerdefinierten Module erstellen, strukturieren und verwalten.

### Das Kernkonzept: Ordnerbasierte Module

Ein Modul ist einfach ein Ordner im Verzeichnis „config/maps/“. Das System durchsucht dieses Verzeichnis automatisch und behandelt jeden Unterordner als ladbares Modul.

### Schritt-für-Schritt-Anleitung zum Erstellen eines Moduls

Befolgen Sie diese Schritte, um ein neues Modul zu erstellen, um beispielsweise Makros für ein bestimmtes Spiel zu speichern.

**1. Navigieren Sie zum Kartenverzeichnis**
Alle Regelmodule befinden sich im Ordner „config/maps/“ des Projekts.

**2. Erstellen Sie Ihren Modulordner**
Erstellen Sie einen neuen Ordner. Der Name sollte beschreibend sein und Unterstriche anstelle von Leerzeichen verwenden (z. B. „my_game_macros“, „custom_home_automation“).

**3. Sprachunterordner hinzufügen (kritischer Schritt)**
In Ihrem neuen Modulordner müssen Sie Unterordner für jede Sprache erstellen, die Sie unterstützen möchten.

* **Namenskonvention:** Die Namen dieser Unterordner **müssen gültige Sprachcodes sein**. Das System verwendet diese Namen, um die richtigen Regeln für die aktive Sprache zu laden.
* **Korrekte Beispiele:** „de-DE“, „en-US“, „en-GB“, „pt-BR“.
* **Warnung:** Wenn Sie einen nicht standardmäßigen Namen wie „german“ oder „english_rules“ verwenden, ignoriert das System den Ordner entweder oder behandelt ihn als separates, nicht sprachspezifisches Modul.

**4. Fügen Sie Ihre Regeldateien hinzu**
Platzieren Sie Ihre Regeldateien (z. B. „FUZZY_MAP_pre.py“) im entsprechenden Unterordner der Sprache. Der einfachste Einstieg besteht darin, den Inhalt eines vorhandenen Sprachmodulordners zu kopieren und als Vorlage zu verwenden.

### Beispiel einer Verzeichnisstruktur

```
config/
└── maps/
    ├── standard_actions/      # An existing module
    │   ├── de-DE/
    │   └── en-US/
    │
    └── my_game_macros/        # <-- Your new custom module
        └── de-DE/             # <-- Language-specific rules
            └── FUZZY_MAP_pre.py

        ├── __init__.py        # <-- Important: This Empty File must be in every Folders!!
            
```

### Module in der Konfiguration verwalten

Das System ist so konzipiert, dass nur eine minimale Konfiguration erforderlich ist.

#### Module aktivieren (Standard)

Module sind **standardmäßig aktiviert**. Solange ein Modulordner in „config/maps/“ vorhanden ist, wird das System ihn finden und seine Regeln laden. **Sie müssen Ihrer Einstellungsdatei keinen Eintrag hinzufügen, um ein neues Modul zu aktivieren.**

#### Module deaktivieren

Um ein Modul zu deaktivieren, müssen Sie einen Eintrag dafür im Wörterbuch „PLUGINS_ENABLED“ in Ihrer Einstellungsdatei hinzufügen und seinen Wert auf „False“ setzen.

**Beispiel (`config/settings.py`):**
```python
# A dictionary to explicitly control the state of modules.
# The key is the path to the module relative to 'config/maps/'.
PLUGINS_ENABLED = {
    "empty_all": False,

    # This module is explicitly enabled.
    "git": True,

    # This module is also enabled. Second Parameter is per default True. Not False means True.
    # "wannweil": False,

    # This module is explicitly disabled.
    "game": False,

    # This module is disabled by other rule
    "game/game-dealers_choice": True,

    # This module is disabled by other rule
    "game/0ad": True,
}


```
### Wichtige Designhinweise

* **Standardverhalten: Kein Eintrag ist gleich „True“**
Wenn ein Modul nicht im Wörterbuch „PLUGINS_ENABLED“ aufgeführt ist, gilt es standardmäßig als **aktiv**. Durch dieses Design bleibt die Konfigurationsdatei sauber, da Sie nur die Ausnahmen auflisten müssen.

* **Abkürzung für Enabling**
Ihr Konfigurationssystem versteht auch, dass die Auflistung eines Modulschlüssels ohne Wert bedeutet, dass er aktiviert ist. Beispielsweise ist das Hinzufügen von „wannweil“ zum Wörterbuch dasselbe wie das Hinzufügen von „wannweil“: True“. Dies bietet eine praktische Abkürzung zum Aktivieren von Modulen.
(Optional) Für True/False können Sie auch 1/0 verwenden. Dies ist jedoch unüblich und kann die Lesbarkeit beeinträchtigen.

* **Deaktivieren übergeordneter Module:** Das beabsichtigte Verhalten besteht darin, dass die Deaktivierung eines übergeordneten Moduls    sein sollte
Deaktivieren Sie automatisch alle untergeordneten Module und Sprachunterordner. Beispielsweise sollte die Einstellung „standard_actions“: False verhindern, dass sowohl „de-DE“ als auch „en-US“ geladen werden. (27.10.'25 Mo)
  
*   **Ziel**
Ziel ist es, dieses System weiter zu verbessern. Beispielsweise wird eine Möglichkeit geschaffen, die Einstellungen des untergeordneten Moduls auch dann zu berücksichtigen, wenn das übergeordnete Modul deaktiviert ist, oder es werden komplexere Vererbungsregeln eingeführt. (27.10.'25 Mo)

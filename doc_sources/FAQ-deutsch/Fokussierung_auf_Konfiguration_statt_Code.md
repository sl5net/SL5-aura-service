## Die Mächtigkeit der Konfiguration: Keine Programmierung notwendig

Die Stärke des Systems liegt darin, dass es hochkomplexes Verhalten ohne die Notwendigkeit von traditioneller Programmierung ermöglicht.

### 1. Fokussierung auf Konfiguration statt Code

Die gesamte Logik des Systems wird ausschließlich durch die **Konfiguration** der Regel-Tupel (`(Zielwert, Regex-Muster, Fuzzy-Wert, Optionen)`) gesteuert und durch die **physische Position** dieser Regeln in den jeweiligen Dateien (Modul-Reihenfolge und Zeilennummer) priorisiert.

*   **Keine Programmierkenntnisse nötig:** Neue Transformationen oder spezifische Verhaltensweisen erfordern kein Eingreifen in den Kerncode oder die Anwendung komplexer Funktionen, sondern lediglich das Hinzufügen oder Neuanordnen von Konfigurationseinträgen in den Mapping-Dateien.

### 2. Die Rolle von Regulären Ausdrücken (Regex)

Während die grundlegendste Konfiguration ohne Regex möglich ist (z. B. einfache String-Ersetzung bei exaktem Full Match), ermöglicht die Integration von **Regular Expressions (PregReg)** eine enorme Erweiterung der Funktionalität.

*   **Vorteil für einfache Fälle:** Für die meisten Anwendungsfälle, wie das Definieren von Stopp-Kriterien (`^Wort$`) oder einfachen Inklusionsmustern, sind nur elementare Regex-Kenntnisse erforderlich.
*   **Möglichkeit für Experten:** Wer komplexe Muster (Lookaheads wie `(?!Haus)`) nutzen möchte, kann dies tun, um hochspezifische Kontrollmechanismen zu implementieren, ohne die Einfachheit für Gelegenheitsnutzer zu opfern.
*   **Möglichkeit für Experten:** Geräte/Spiele zu steuern ... siehe Plugin **config/maps/plugins/game/0ad/**

**Fazit:** Das System ist darauf ausgelegt, ein maximales Maß an Kontrolle über die Textverarbeitung zu bieten, wobei die **Regel-Daten** die Geschäftslogik definieren und die Kern-Engine lediglich der zuverlässige Interpret und Ausführer dieser Prioritäten und Kaskaden ist.

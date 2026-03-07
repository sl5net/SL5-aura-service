## Die Mächtigkeit der Konfiguration: Keine Programmierung notwendig

Die Stärke des Systems liegt darin, dass es hochkomplexes Verhalten ohne die Notwendigkeit von tradicional Programmierung ermöglicht.

### 1. Configuración de configuración en lugar del código

La logística de los sistemas se gestiona automáticamente mediante la **configuración** de la configuración de rango (`(Zielwert, Regex-Muster, Fuzzy-Wert, Optionen)`) y se administra según la **posición física** de esta configuración en las fechas joyería (Modul-Reihenfolge und Zeilennummer) priorizadas.

* **Keine Programmierkenntnisse nötig:** Nuevas transformaciones o versiones específicas no se pueden introducir en el código Kerncode o en las funciones complejas de configuración, sondern lediglich das Hinzufügen oder Neuanordnen von Konfigurationseinträgen in den Mapping-Dateien.

### 2. Die Rolle von Regulären Ausdrücken (Regex)

Cuando se modifica la configuración básica sin expresiones regulares (por ejemplo, una configuración de cadena sencilla en el examen Full Match), se activa la integración de **Expresiones regulares (PregReg)** una enorme modificación de la función.

* **Vorteil für einfache Fälle:** Para las principales Anwendungsfälle, como las Definieren von Stopp-Kriterien (`^Wort$`) o las einfachen Inklusionsmustern, sind nur elementare Regex-Kenntnisse erforderlich.
* **Möglichkeit für Experten:** Wer komplex Muster (Lookaheads wie `(?!Haus)`) nutzen möchte, kann dies tun, um hochspezifische Kontrollmechanismen zu implementieren, ohne die Einfachheit für Gelegenheitsnutzer zu opfern.
* **Mobiliario para expertos:** Geräte/Spiele zu steuern... siehe Plugin **config/maps/plugins/game/0ad/**

**Fazit:** Das System ist darauf ausgelegt, ein maximales Maß an Kontrolle über die Textverarbeitung zu bieten, wobei die **Regel-Daten** die Geschäftslogik definieren und die Kern-Engine lediglich der zuverlässige Interpret und Ausführer dieser Prioritäten und Kaskaden ist.
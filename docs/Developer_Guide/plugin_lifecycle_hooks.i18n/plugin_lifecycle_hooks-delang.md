# Plugin-Lebenszyklus-Hooks

Aura SL5 unterstützt Lifecycle-Hooks, die es Plugins (Maps) ermöglichen, bestimmte Logik automatisch auszuführen, wenn sich ihr Status ändert.

## Der „on_reload()“-Hook

Die Funktion „on_reload()“ ist eine spezielle optionale Funktion, die Sie in jeder Plugin-Map („.py“) definieren können.

### Verhalten
* **Auslöser:** Diese Funktion wird **unmittelbar nach** dem erfolgreichen Hot-Reload des Moduls ausgeführt (erkannte Dateiänderung + Sprachauslöser).
* **Kontext:** Es wird im Hauptanwendungsablauf ausgeführt.
* **Geltungsbereich:** Es wird **NICHT** beim ersten Systemstart (Kaltstart) ausgeführt. Es ist ausschließlich für *Nachladeszenarien gedacht.

### Anwendungsfälle
* **Sicherheit:** Verschlüsseln oder komprimieren Sie sensible Dateien nach der Bearbeitung automatisch neu.
* **Statusverwaltung:** Zurücksetzen globaler Zähler oder Löschen bestimmter Caches.
* **Benachrichtigung:** Protokollierung spezifischer Debug-Informationen, um zu überprüfen, ob eine Änderung angewendet wurde.

### Technische Details und Sicherheit
* **Fehlerbehandlung:** Die Ausführung ist in einen „try/exclusive“-Block eingeschlossen. Wenn Ihre „on_reload“-Funktion abstürzt (z. B. „DivisionByZero“), wird ein Fehler protokolliert („❌ Fehler beim Ausführen von on_reload...“), aber **führt Aura nicht zum Absturz**.
* **Leistung:** Die Funktion läuft synchron. Vermeiden Sie direkt in dieser Funktion lang andauernde Aufgaben (z. B. große Downloads), da diese die Verarbeitung von Sprachbefehlen kurzzeitig blockieren. Für schwere Aufgaben erstellen Sie einen Thread.

### Beispielcode

__CODE_BLOCK_0__
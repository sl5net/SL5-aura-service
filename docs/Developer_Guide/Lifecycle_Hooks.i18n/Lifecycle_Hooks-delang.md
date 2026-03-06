Aura SL5-Haken: Hinzugefügt

HOOK_PLUGIN_LOAD = 'on_plugin_load'
HOOK_FILE_LOAD = 'on_file_load'
HOOK_RELOAD = 'on_reload'
HOOK_UPSTREAM = 'on_folder_change'

on_folder_change() und
on_reload() zum Auslösen der Logik nach Hot-Reloads. Verwenden Sie dies, um die Ausführung komplexer Pakete mit übergeordneten Skripten wie secure_packer.py zu verketten.

# Entwicklerhandbuch: Plugin-Lebenszyklus-Hooks

Mit Aura SL5 können Plugins (Maps) spezifische „Hooks“ definieren, die automatisch ausgeführt werden, wenn sich der Status des Moduls ändert. Dies ist für erweiterte Arbeitsabläufe wie das **Secure Private Map**-System unerlässlich.

## Der „on_folder_change“-Hook Hook

„on_folder_change“-Hook-Erkennung implementiert. Der Reloader durchsucht nun das Verzeichnis

## Der „on_reload()“-Hook

Die Funktion „on_reload()“ ist eine optionale Funktion, die Sie in jedem Map-Modul definieren können.

### Verhalten
* **Auslöser:** Wird sofort ausgeführt, nachdem ein Modul erfolgreich **im laufenden Betrieb neu geladen wurde** (Dateiänderung + Sprachauslöser).
* **Kontext:** Wird im Hauptanwendungsthread ausgeführt.
* **Sicherheit:** Eingepackt in einen „try/exclusive“-Block. Fehler hier werden protokolliert, führen jedoch **nicht zum Absturz** der Anwendung.

### Nutzungsmuster: Die „Daisy Chain“
Bei komplexen Paketen (wie Private Maps) gibt es oft viele Unterdateien, aber nur ein zentrales Skript („secure_packer.py“) sollte die Logik übernehmen.

Mit dem Hook können Sie die Aufgabe nach oben delegieren:

__CODE_BLOCK_0__
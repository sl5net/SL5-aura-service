# Sicheres Auto-Zip und eingebettete Dokumentation

## Konzept
SL5 Aura überwacht private Ordner, die mit „_“ beginnen (z. B. „_my_confidential_data“).
Wenn Änderungen erkannt werden, erstellt Aura automatisch ein **verschlüsseltes** ZIP-Archiv.

## Kritische Voraussetzung: Verschlüsselungsschlüssel
**Verschlüsselung ist obligatorisch.** Für den Auto-Zip-Vorgang muss unbedingt eine Kennwortdatei in der Verzeichnishierarchie (aktuelle oder übergeordnete Ordner) vorhanden sein.

* **Dateianforderung:** Die Passwortdatei muss mit einem Punkt „.“ beginnen (z. B. „.archive_pass“, „.secret“).
* **Verhalten:** Wenn keine Dot-Datei mit Passwort gefunden wird, wird der Zip-Prozess **blockiert**. Diese Ausfallsicherheit stellt sicher, dass niemals unverschlüsselte Daten verpackt werden.

## Das Muster „Embedded Docs“.
Da das Hot-Reload-System von Aura auf **gültige Python-Dateien** wartet, löst die Aktualisierung einer einfachen „.txt“-Readme-Datei kein erneutes Zip aus.

Verwenden Sie eine **Python-Docstring-Datei**, um Anweisungen für Empfänger einzuschließen (z. B. „So entpacken Sie“) und gleichzeitig sicherzustellen, dass der Auslöser ausgelöst wird.

### Implementierung
Erstellen Sie eine Datei mit dem Namen „README_AUTOZIP.py“ in Ihrem überwachten Ordner.

__CODE_BLOCK_0__
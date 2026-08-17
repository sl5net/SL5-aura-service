Geplant ist im Moment nicht, dass es ohne Passwort auf Ordnern irgendwo oben funktioniert. Passwortdateien müssen mit einem Punkt „.“ beginnen.


# Auto-Zip-Workflow und eingebettete Dokumentation

## Konzept
SL5 Aura überwacht automatisch Ordner, die mit „_“ beginnen (z. B. „_my_application“). Wenn Änderungen erkannt werden, komprimiert Aura den Ordner automatisch in ein ZIP-Archiv.

**Kritische Einschränkung:**
Das „Hot-Reload“- und Überwachungssystem von Aura lauscht gezielt auf Änderungen in **gültigen Python-Dateien**. Eine einfache Aktualisierung einer Textdatei („.txt“) löst den automatischen Zip-Vorgang **nicht** aus.

## Das Muster „Embedded Docs“.
Um Anweisungen für technisch nicht versierte Empfänger (z. B. Personalabteilung, Kunden) einzubinden und gleichzeitig sicherzustellen, dass Aura die Änderung erkennt und die ZIP-Datei aktualisiert, verwenden wir eine **Python-Docstring-Datei**.

Diese Datei ist technisch gesehen ein gültiges Python-Skript (das den Parser von Aura erfüllt), erscheint dem Benutzer jedoch optisch als Standardtextdokument.

### Implementierung
Erstellen Sie eine Datei mit dem Namen „README_AUTOZIP.py“ in Ihrem überwachten Ordner.

**Styleguide:**
1. Verwenden Sie zur Begrüßung „# Documentation“ als erste Zeile (anstelle eines technischen Skriptnamens).
2. Verwenden Sie für den Inhalt einen Docstring in dreifachen Anführungszeichen („“““).
3. Es ist kein weiterer Code erforderlich.

### Beispielcode

__CODE_BLOCK_0__
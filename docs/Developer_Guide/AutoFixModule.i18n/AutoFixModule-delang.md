# Auto-Fix-Modul (Schnellregeleingabemodus)

## Was es tut

Wenn Sie ein einfaches Wort (ohne Anführungszeichen oder Python-Syntax) in eine Map-Datei eingeben
B. „FUZZY_MAP_pre.py“, wandelt das System diese automatisch in eine gültige Regel um.

Dies ist der schnellste Weg, neue Regeln zu erstellen – Sie müssen sich das Format nicht merken.

## Beispiel

Sie geben dies in „FUZZY_MAP_pre.py“ ein:

```
oma
```

Das Auto-Fix-Modul erkennt einen „NameError“ (bloßes Wort, kein gültiges Python)
und wandelt die Datei automatisch um in:

```python
# config/maps/.../de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
# too<-from
FUZZY_MAP_pre = [
    ('oma', 'oma'),
]
```

Bearbeiten Sie nun die Regel so, wie Sie sie tatsächlich benötigen:

```python
('Oma', 'oma'),              # capitalize
('Großmutter', 'oma'),       # synonym
('Thomas Müller', 'thomas'), # from a phone book
```

## Wie es funktioniert

Das Modul „scripts/py/func/auto_fix_module.py“ wird automatisch ausgelöst
wenn Aura beim Laden einer Kartendatei einen „NameError“ erkennt.

Es dann:
1. Fügt den korrekten Dateipfad-Header hinzu
2. Fügt „import re“ hinzu, falls es fehlt
3. Fügt die Listendefinition „FUZZY_MAP_pre = [“ hinzu
4. Wandelt bloße Wörter in Tupel vom Typ „(‚Wort‘, ‚Wort‘)“ um
5. Schließt die Liste mit „]“.

## Regeln und Grenzen

- Funktioniert nur bei Dateien, die kleiner als **1 KB** sind (Sicherheitsgrenze)
- Gilt nur für: „FUZZY_MAP.py“, „FUZZY_MAP_pre.py“, „PUNCTUATION_MAP.py“.
- Die Datei muss in einem gültigen Sprachordner liegen (z. B. „de-DE/“)
- Funktioniert für mehrere Wörter gleichzeitig (z. B. aus einer Telefonbuchliste)

## Bekannte Probleme (nicht vollständig getestet)

> ⚠️ Dieses Modul ist funktionsfähig, aber nicht umfassend getestet. Die folgenden Fälle funktionieren möglicherweise nicht richtig:

- **Zahlen** – „5“ oder „6“ sind keine gültigen Python-Bezeichner, die automatische Korrektur kann sie möglicherweise nicht verarbeiten
- **Sonderzeichen** – Wörter mit „-“, „.“ und Umlauten lösen möglicherweise keinen „NameError“ aus
- **Einträge mit mehreren Wörtern** – „Thomas Mueller“ (mit Leerzeichen) verursacht „SyntaxError“ und nicht „NameError“, sodass die automatische Korrektur möglicherweise nicht ausgelöst wird
- **Komma-getrennte Werte** – „drei, vier“ können unverändert eingefügt werden, ohne ein richtiges Tupel zu werden

Wenn die automatische Korrektur nicht ausgelöst wird, fügen Sie die Regel manuell hinzu:
```python
('replacement', 'input word'),
```

## Der „# too<-from“-Kommentar

Dieser Kommentar wird automatisch als Erinnerung an die Regelrichtung hinzugefügt:

```
too <- from
```

Bedeutung: **Ausgabe** (auch) ← **Eingabe** (von). Der Ersatz steht an erster Stelle.

Für „PUNCTUATION_MAP.py“ ist die Richtung umgekehrt: „# from->too“.

## Masseneintrag aus einer Liste

Sie können mehrere Wörter gleichzeitig einfügen:

```
thomas
maria
berlin
```

Jedes bloße Wort wird zu seiner eigenen Regel:

```python
('thomas', 'thomas'),
('maria', 'maria'),
('berlin', 'berlin'),
```

Bearbeiten Sie dann jede Ersetzung nach Bedarf.

## Datei: „scripts/py/func/auto_fix_module.py“.
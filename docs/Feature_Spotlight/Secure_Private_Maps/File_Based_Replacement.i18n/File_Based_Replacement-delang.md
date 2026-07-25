# FEATURE SPOTLIGHT: Dateibasierte Regelersetzungen

In diesem Dokument wird beschrieben, wie vertrauliche Werte (Passwörter, API-Schlüssel, Token) aufbewahrt werden.
aus dem Quellcode „FUZZY_MAP_pre“ / „FUZZY_MAP“ und dem Git-Verlauf durch Laden der
„Ersatz“-Text zur Laufzeit aus einer separaten Datei, anstatt ihn fest zu codieren.

Dies ist besonders nützlich bei Livestreams oder Bildschirmfreigaben, bei denen die Karte angezeigt wird
Der Quellcode selbst ist möglicherweise sichtbar, die referenzierte Datei jedoch nicht.

---

## 1. Das Konzept

Normalerweise ist das „Ersatz“-Feld einer Regel der wörtliche Ausgabetext:

```python
('my-secret-value', r'^(trigger)$', 85, {'command_flags': re.IGNORECASE})
```

Wenn die dateibasierte Ersetzung aktiviert ist, wird ein „Ersetzungswert“ angezeigt, der mit a beginnt
Das konfigurierte Präfix (standardmäßig „-“ oder „.“) wird stattdessen als **Dateiname** behandelt.
Aura löst diesen Dateinamen relativ zum eigenen Verzeichnis des Plugins auf und liest ihn
Inhalt und verwendet diesen Inhalt als Ersatztext.

```python
('-api_key.txt', r'^(show api key)$', 85, {'command_flags': re.IGNORECASE})
```

Wenn „api_key.txt“ neben „FUZZY_MAP_pre.py“ des Plugins vorhanden ist, ist es (entfernt)
Der Inhalt wird als Ersatz verwendet. Wenn die Datei nicht vorhanden ist, das Literal
Stattdessen wird die Zeichenfolge „-api_key.txt“ zurückgegeben (ausfallsicher: kein versehentliches Auslaufen von
„Datei nicht gefunden“ als verwendbarer Text und kein Absturz).

---

## 2. Einstellungen

Konfiguriert in „config/settings.py“ (oder „config/settings_local.py“ für lokal
überschreibt):

| Einstellung | Geben Sie | ein Standard | Beschreibung |
|---|---|---|---|
| `FILE4REPLACEMENT_USE` | `bool` | „Wahr“ | Hauptschalter für die gesamte Funktion. Bei „Falsch“ wird „Ersatz“ immer wörtlich verwendet. |
| `FILE4REPLACEMENT_ALLOWED_PREFIXES` | `tupel[str]` | `('-', '.')` | „Ersatz“-Werte müssen mit einem dieser Präfixe beginnen, um eine Dateisuche auszulösen. Empty/`None` = Jeder Wert, der nicht mit einem Buchstaben beginnt, wird als potenzieller Dateiname behandelt. |
| `FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL` | `bool` | „Falsch“ | Wenn „True“, erlaubt es das Auflösen von Dateien außerhalb des eigenen Verzeichnisses des Plugins (z. B. absolute Pfade oder „../“-Sequenzen). Siehe Abschnitt „Sicherheit“ weiter unten. |
| `FILE4REPLACEMENT_DENY_PREFIXES` | `tupel[str]` | z.B. `('/etc', '/proc', '/dev', '/var/lib', '/root', 'C:\\Windows', 'C:\\Programme')` | Aufgelöste absolute Pfade, die mit einem dieser Pfade beginnen, werden **immer** abgelehnt, unabhängig von „FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL“. Harte Sicherheitsgrenze für Systemverzeichnisse. |

---

## 3. Pfadauflösung

Die Datei wird wie folgt aufgelöst:

1. Der „source_path“ des Plugins (automatisch vom Kartenlader aufgezeichnet) ist
verbunden gegen „PROJECT_ROOT“ (gelesen aus „SL5NET_AURA_PROJECT_ROOT“)
Umgebungsvariable), um das Verzeichnis des Plugins abzurufen.
2. Der „Ersatz“-Wert wird diesem Verzeichnis hinzugefügt.
3. Sofern „FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL“ nicht „True“ ist, der aufgelöste Pfad
muss im Verzeichnis des Plugins bleiben, sonst wird die Suche abgelehnt.
4. Unabhängig vom oben Gesagten gilt jeder gelöste Pfad, der mit einem Eintrag in beginnt
„FILE4REPLACEMENT_DENY_PREFIXES“ wird immer abgelehnt.
5. Wenn die Datei vorhanden ist, wird ihr entfernter Inhalt zurückgegeben. Ansonsten ist das
Die ursprüngliche Ersatzzeichenfolge wird unverändert zurückgegeben.

---

## 4. Sicherheitshinweise

- Aktivieren Sie „FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL“ nur, wenn Sie das verstehen
Auswirkungen: Es ermöglicht jedem Benutzer, der eine „FUZZY_MAP_pre“-Datei bearbeiten kann (z. B.
über einen Online-Karteneditor), um beliebige Dateien zu lesen, die der Aura-Prozess verarbeiten kann
Zugriff haben und deren Inhalt als Live-Ausgabetext angezeigt wird.
- „FILE4REPLACEMENT_DENY_PREFIXES“ bietet einen Basisschutz gegen
gemeinsame Systemverzeichnisse, auch wenn Pfaddurchquerung erlaubt ist, aber das ist der Fall
ist kein Ersatz für die Einschränkung, wer Kartendateien überhaupt bearbeiten darf.
- Referenzierte Dateien sind reine Textdateien auf der Festplatte. Kombinieren Sie es mit der Datei Ihres Betriebssystems
Berechtigungen, wenn der Inhalt vertraulich ist.

---

## 5. Beispiel

Ein funktionierendes Beispiel-Plugin finden Sie unter „config/maps/plugins/TEST_FILE4REPLACEMENT/“.
und „tools/tests/TEST_FILE4REPLACEMENT.sh“ für ein Testskript, das Übungen durchführt
Sowohl eine Suche im Verzeichnis als auch eine Suche außerhalb des Plugin-Verzeichnisses.

```python
# config/maps/plugins/TEST_FILE4REPLACEMENT/de-DE/FUZZY_MAP_pre.py
FUZZY_MAP_pre = [
    ('.Zebra.txt', r'^(Zebra)$', 85, {'command_flags': re.IGNORECASE}),
]
```

Erstellen Sie dann neben dieser Datei „.Zebra.txt“ mit dem gewünschten Ersetzungstext
Sagen Sie „s Zebra“ (oder geben Sie es über die Konsole ein), um es auszulösen.
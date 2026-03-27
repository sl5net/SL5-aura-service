# Erste Schritte mit SL5 Aura

> **Voraussetzungen:** Sie haben das Setup-Skript abgeschlossen und Ihren Hotkey konfiguriert.
> Wenn nicht, sehen Sie sich [Installation section in README.md](../../README.i18n/README-delang.md#installation) an.

---

## Schritt 1: Ihr erstes Diktat

1. Aura starten (falls noch nicht ausgeführt):
   ```bash
   ./scripts/restart_venv_and_run-server.sh
   ```
Warten Sie auf den Startton – das bedeutet, dass Aura bereit ist.

2. Klicken Sie in ein beliebiges Textfeld (Editor, Browser, Terminal).
3. Drücken Sie Ihren Hotkey, sagen Sie „Hallo Welt“** und drücken Sie den Hotkey erneut.
4. Beobachten Sie, wie der Text erscheint.

> **Nichts passiert?** Überprüfen Sie „log/aura_engine.log“ auf Fehler.
> Allgemeiner Fix für CachyOS/Arch: „sudo pacman -S mimalloc“.

---

## Schritt 2: Schreiben Sie Ihre erste Regel

Der schnellste Weg, eine persönliche Regel hinzuzufügen:

1. Öffnen Sie „config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py“.
2. Fügen Sie eine Regel in „FUZZY_MAP_pre = [...]“ hinzu:
   ```python
   ('Hello World', r'hello world', 0, {'flags': re.IGNORECASE})
   #  ^ output        ^ pattern        ^ threshold (ignored for regex)
   ```
3. **Speichern** – Aura wird automatisch neu geladen. Kein Neustart erforderlich.
4. Diktieren Sie „Hallo Welt“ und sehen Sie zu, wie daraus „Hallo Welt“ wird.

> Die vollständige Regelreferenz finden Sie unter „docs/FuzzyMapRuleGuide.md“.

### Der Oma-Modus (Einsteiger-Shortcut)

Sie kennen Regex noch nicht? Kein Problem.

1. Öffnen Sie eine beliebige leere Datei „FUZZY_MAP_pre.py“ in der Sandbox
2. Schreiben Sie einfach ein einfaches Wort in eine eigene Zeile (keine Anführungszeichen, kein Tupel):
   ```
   raspberry
   ```
3. Speichern – das Auto-Fix-System erkennt das bloße Wort automatisch
wandelt es in einen gültigen Regeleintrag um.
4. Anschließend können Sie den Ersetzungstext manuell bearbeiten.

Dies nennt sich **Oma-Modus** – konzipiert für Benutzer, die ohne Ergebnisse Ergebnisse erzielen möchten
Ich lerne zuerst Regex.

---

## Schritt 3: Lernen Sie mit Koans

Koans sind kleine Übungen, die jeweils ein Konzept vermitteln.
Sie leben in „configmaps/koans deutsch/“ und „configmaps/koans english/“.

Beginnen Sie hier:

| Ordner | Was Sie lernen |
|---|---|
| `00_koan_oma-modus` | Auto-Fix, erste Regel ohne Regex |
| `01_koan_erste_schritte` | Ihre erste Regel, Pipeline-Grundlagen |
| `02_koan_listen` | Arbeiten mit Listen |
| `03_koan_schwierige_namen` | Fuzzy-Matching für schwer erkennbare Namen |
| `04_koan_kleine_helfer` | Nützliche Verknüpfungen |

Jeder Koan-Ordner enthält eine „FUZZY_MAP_pre.py“ mit kommentierten Beispielen.
Kommentieren Sie eine Regel aus, speichern Sie sie, diktieren Sie die Auslösephrase – fertig.

---

## Schritt 4: Gehen Sie weiter

| Was | Wo |
|---|---|
| Vollständige Regelreferenz | `docs/FuzzyMapRuleGuide.md` |
| Erstellen Sie Ihr eigenes Plugin | `docs/CreatingNewPluginModules.md` |
| Führen Sie Python-Skripte über Regeln aus | `docs/advanced-scripting.md` |
| DEV_MODE + Protokollfilter-Setup | `docs/Developer_Guide/dev_mode_setup.md` |
| Kontextbezogene Regeln (`only_in_windows`) | `docs/FuzzyMapRuleGuide.md` |
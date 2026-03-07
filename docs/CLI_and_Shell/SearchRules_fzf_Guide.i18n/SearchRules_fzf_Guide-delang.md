# search_rules.sh – Interaktive Regelsuche mit fzf

> ⚠️ Nur Linux/macOS. Keine Windows-Unterstützung (fzf + xdg-open).

## Was es macht

`search_rules.sh` durchsucht alle Map-Dateien in `config/maps/` interaktiv mit `fzf`.
Treffer können direkt im Editor geöffnet oder auf GitHub angezeigt werden.

## Dateien im Repo

```
scripts/search_rules/search_rules.sh   ← offizielle Version
tools/search_rules.sh                  ← veraltet, hat hardcodierten Pfad-Bug
```

Die Version in `tools/` sollte entfernt oder durch einen Symlink ersetzt werden:
```bash
rm ~/projects/py/STT/tools/search_rules.sh
ln -s ../scripts/search_rules/search_rules.sh ~/projects/py/STT/tools/search_rules.sh
```

## Voraussetzungen

```bash
# fzf installieren (falls nicht vorhanden)
sudo apt install fzf        # Debian/Ubuntu
sudo pacman -S fzf          # Arch
brew install fzf            # macOS
```

## Nutzung

```bash
cd ~/projects/py/STT
bash scripts/search_rules/search_rules.sh
```

## fzf Tastenkürzel

| Geschmack | Aktion |
|---|---|
| Tippen | Suchanfrage eingeben |
| „Eingeben“ | Datei im Editor öffnen (Kate) |
| `Strg+G` | Zeile auf GitHub im Browser öffnen |
| `Strg+Z` | Vorherige Suchanfrage aus History |
| `Strg+Y` | Nächste Suchanfrage aus Geschichte |
| `Strg+P` | Vorheriger History-Eintrag |
| `Strg+N` | Nächster History-Eintrag |
| `Strg+A` | Alle Treffer auswählen |
| `Strg+C` | Abbrechen |
| `Strg+←/→` | Wortweise handeln |
| `Strg+Rücktaste` | Wort löschen (Links) |
| `Strg+Entf` | Wort löschen (rechts) |

## Konfiguration

Am Anfang des Scripts anpassbar:

```bash
PREFERRED_EDITOR="kate"          # Editor für Ctrl+Enter
HISTORY_FILE="$HOME/.search_rules_history"  # Suchverlauf
DEFAULT_QUERY=".py pre # EXAMPLE:"          # Startsuche beim ersten Aufruf
REPO_URL="https://github.com/sl5net/SL5-aura-service/blob/master"
```

## Vorschau-Fenster

Das fzf-Fenster zeigt oben (50%) eine Vorschau des Treffers:
- 5 Zeilen vor und nach dem Match
- Die Treffer-Zeile ist mit `>` markiert
- Zeilennummern werden angezeigt

## Suchverlauf

Die letzte Suchanfrage wird automatisch als Startwert beim nächsten Aufruf verwendet.
Der Verlauf liegt in `~/.search_rules_history`.

## Typische Suchanfragen

```
FUZZY_MAP_pre                    # alle pre-Map Regeln
# TODO                           # auskommentierte Aufgaben
^.*$                             # Fullmatch-Regeln (Pipeline-Stopper)
re.IGNORECASE                    # alle Regex-Regeln mit Flag
koans                            # alle Koan-Dateien
```

## Bekannte Einschränkungen

- Nur Linux/macOS (kein Windows wegen `fzf` und `xdg-open`)
- Editor fest codiert auf „kate“ – für anderen Editor „PREFERRED_EDITOR“ ändern
- Sucht nur in `config/maps/` – nicht im gesamten Repo
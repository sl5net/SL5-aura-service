# search_rules.sh – Interaktive Regelsuche mit fzf

> ⚠️ Nur Linux/macOS. Kein Windows-Support (fzf + xdg-open).

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

| Taste | Aktion |
|---|---|
| Tippen | Suchanfrage eingeben |
| `Enter` | Datei im Editor öffnen (Kate) |
| `Ctrl+G` | Zeile auf GitHub im Browser öffnen |
| `Ctrl+Z` | Vorherige Suchanfrage aus History |
| `Ctrl+Y` | Nächste Suchanfrage aus History |
| `Ctrl+P` | Vorheriger History-Eintrag |
| `Ctrl+N` | Nächster History-Eintrag |
| `Ctrl+A` | Alle Treffer auswählen |
| `Ctrl+C` | Abbrechen |
| `Ctrl+←/→` | Wortweise navigieren |
| `Ctrl+Backspace` | Wort löschen (links) |
| `Ctrl+Delete` | Wort löschen (rechts) |

## Konfiguration

Am Anfang des Scripts anpassbar:

```bash
PREFERRED_EDITOR="kate"          # Editor für Ctrl+Enter
HISTORY_FILE="$HOME/.search_rules_history"  # Suchverlauf
DEFAULT_QUERY=".py pre # EXAMPLE:"          # Startsuche beim ersten Aufruf
REPO_URL="https://github.com/sl5net/SL5-aura-service/blob/master"
```

## Preview-Fenster

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
- Editor hardcoded auf `kate` – für anderen Editor `PREFERRED_EDITOR` ändern
- Sucht nur in `config/maps/` – nicht im gesamten Repo

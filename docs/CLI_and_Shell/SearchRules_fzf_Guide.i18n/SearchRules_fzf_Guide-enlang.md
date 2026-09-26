> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../SearchRules_fzf_Guide.md).*

# search_rules.sh – Interactive rule search with fzf

> ⚠️ Linux/macOS only. No Windows support (fzf + xdg-open).

## What it does

`search_rules.sh` searches all map files in `config/maps/` interactively with `fzf`.
Hits can be opened directly in the editor or viewed on GitHub.

## Files in the repo

```
scripts/search_rules/search_rules.sh   ← offizielle Version
tools/search_rules.sh                  ← veraltet, hat hardcodierten Pfad-Bug
```

The version in `tools/` should be removed or replaced with a symlink:
```bash
rm ~/projects/py/STT/tools/search_rules.sh
ln -s ../scripts/search_rules/search_rules.sh ~/projects/py/STT/tools/search_rules.sh
```

## Requirements

```bash
# fzf installieren (falls nicht vorhanden)
sudo apt install fzf        # Debian/Ubuntu
sudo pacman -S fzf          # Arch
brew install fzf            # macOS
```

## Usage

```bash
cd ~/projects/py/STT
bash scripts/search_rules/search_rules.sh
```

## fzf Keyboard Shortcuts

| Key | Action |
|---|---|
| Type | Enter search query |
| `Enter` | Open file in editor (Kate) |
| `Ctrl+G` | Open line on GitHub in browser |
| `Ctrl+Z` | Previous search request from History |
| `Ctrl+Y` | Next search from History |
| `Ctrl+P` | Previous History Entry |
| `Ctrl+N` | Next History Entry |
| `Ctrl+A` | Select all hits |
| `Ctrl+C` | Cancel |
| `Ctrl+←/→` | Wordwise Navigate |
| `Ctrl+Backspace` | Delete word (left) |
| `Ctrl+Delete` | Delete word (right) |


## Configuration

Customizable at the beginning of the script:

```bash
PREFERRED_EDITOR="kate"          # Editor für Ctrl+Enter
HISTORY_FILE="$HOME/.search_rules_history"  # Suchverlauf
DEFAULT_QUERY=".py pre # EXAMPLE:"          # Startsuche beim ersten Aufruf
REPO_URL="https://github.com/sl5net/SL5-aura-service/blob/master"
```

## Preview Window

The fzf window displays a preview of the match at the top (50%):
- 5 lines before and after the match
- The hit line is marked with `>`
- Line numbers are displayed

## Search History

The last search query is automatically used as the starting value the next time it is called.
The course is located in `~/.search_rules_history`.

## Typical search queries

```
FUZZY_MAP_pre                    # alle pre-Map Regeln
# TODO                           # auskommentierte Aufgaben
^.*$                             # Fullmatch-Regeln (Pipeline-Stopper)
re.IGNORECASE                    # alle Regex-Regeln mit Flag
koans                            # alle Koan-Dateien
```

## Known Limitations

- Only Linux/macOS (no Windows because of `fzf` and `xdg-open`)
- Editor hardcoded to `kate` – change to `PREFERRED_EDITOR` for another editor
- Search only in `config/maps/` – not in the entire repo

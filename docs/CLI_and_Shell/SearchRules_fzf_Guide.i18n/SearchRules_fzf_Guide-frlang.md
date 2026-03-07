# search_rules.sh – Règles interactives avec fzf

> ⚠️ Sous Linux/macOS. Pas de prise en charge Windows (fzf + xdg-open).

## C'était macht

`search_rules.sh` est disponible dans les fichiers Map dans `config/maps/` interactif avec `fzf`.
Je vous invite directement à l'éditeur ou à GitHub.

## Dates dans le dépôt

```
scripts/search_rules/search_rules.sh   ← offizielle Version
tools/search_rules.sh                  ← veraltet, hat hardcodierten Pfad-Bug
```

La version dans `tools/` est simplement disponible ou via un lien symbolique créé :
```bash
rm ~/projects/py/STT/tools/search_rules.sh
ln -s ../scripts/search_rules/search_rules.sh ~/projects/py/STT/tools/search_rules.sh
```

## Vorausetzungs

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

## fzf Tasse de goût

| Goût | Action |
|---|---|
| Tippen | Frais de port gratuits |
| `Entrer` | Datei im Editor öffnen (Kate) |
| `Ctrl+G` | Zeile sur GitHub dans le navigateur ouvert |
| `Ctrl+Z` | Vorherige Suchanfrage aus Histoire |
| `Ctrl+Y` | Nächste Suchanfrage aus Histoire |
| `Ctrl+P` | Vorheriger Histoire-Eintrag |
| `Ctrl+N` | Nächster Histoire-Eintrag |
| `Ctrl+A` | Alle Treffer auswählen |
| `Ctrl+C` | Abbrechen |
| `Ctrl+←/→` | Navigateurs sans fil |
| `Ctrl+Retour arrière` | Moût löschen (liens) |
| `Ctrl+Supprimer` | Moût löschen (droit) |

## Configuration

Suis l'Anfang des Scripts et la barre de passage :

```bash
PREFERRED_EDITOR="kate"          # Editor für Ctrl+Enter
HISTORY_FILE="$HOME/.search_rules_history"  # Suchverlauf
DEFAULT_QUERY=".py pre # EXAMPLE:"          # Startsuche beim ersten Aufruf
REPO_URL="https://github.com/sl5net/SL5-aura-service/blob/master"
```

## Aperçu-Fenster

Das fzf-Fenster zeigt oben (50%) eine Vorschau des Treffers:
- 5 Zeilen vor und nach dem Match
- La Treffer-Zeile est avec le marquage `>`
- Zeilennummern werden angezeigt

## Mise à jour

Le letzte Suchanfrage wird automatisch als Startwert beim nächsten Aufruf verwendet.
Le Verlauf se trouve dans `~/.search_rules_history`.

## Typische Suchanfragen

```
FUZZY_MAP_pre                    # alle pre-Map Regeln
# TODO                           # auskommentierte Aufgaben
^.*$                             # Fullmatch-Regeln (Pipeline-Stopper)
re.IGNORECASE                    # alle Regex-Regeln mit Flag
koans                            # alle Koan-Dateien
```

## Bekannte Inschränkungen

- Pour Linux/macOS (comme Windows avec `fzf` et `xdg-open`)
- Éditeur codé en dur sur `kate` – pour d'autres éditeurs `PREFERRED_EDITOR` également
- Ce n'est pas le cas dans `config/maps/` – n'est pas utilisé dans le Repo
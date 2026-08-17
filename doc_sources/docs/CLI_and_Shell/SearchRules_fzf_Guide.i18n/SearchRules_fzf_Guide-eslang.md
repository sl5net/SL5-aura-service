# search_rules.sh – Regelsuche interactivo con fzf

> ⚠️ En Linux/macOS. Soporte permanente para Windows (fzf + xdg-open).

## Was es macht

`search_rules.sh` muestra todas las fechas de mapas en `config/maps/` interactivamente con `fzf`.
Treffer puede ser elegido directamente en el editor o en GitHub.

## Fecha en el repositorio

```
scripts/search_rules/search_rules.sh   ← offizielle Version
tools/search_rules.sh                  ← veraltet, hat hardcodierten Pfad-Bug
```

La versión en `tools/` se ingresa o se escribe mediante un enlace simbólico:
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

## nuezung

```bash
cd ~/projects/py/STT
bash scripts/search_rules/search_rules.sh
```

## fzf Tastenkürzel

| Sabor | Acción |
|---|---|
| Tippen | Imágenes similares |
| `Entrar` | Datei im Editor öffnen (Kate) |
| `Ctrl+G` | Zeile auf GitHub im Browser activado |
| `Ctrl+Z` | Vorherige Suchanfrage aus Historia |
| `Ctrl+Y` | Nächste Suchanfrage aus Historia |
| `Ctrl+P` | Vorheriger Historia-Eintrag |
| `Ctrl+N` | Nächster Historia-Eintrag |
| `Ctrl+A` | Todos los Treffer auswählen |
| `Ctrl+C` | Abrechen |
| `Ctrl+←/→` | Cómo navegar |
| `Ctrl+Retroceso` | Mosto löschen (enlaces) |
| `Ctrl+Suprimir` | Mosto löschen (derecho) |

## Configuración

Am Anfang des Scripts anpassbar:

```bash
PREFERRED_EDITOR="kate"          # Editor für Ctrl+Enter
HISTORY_FILE="$HOME/.search_rules_history"  # Suchverlauf
DEFAULT_QUERY=".py pre # EXAMPLE:"          # Startsuche beim ersten Aufruf
REPO_URL="https://github.com/sl5net/SL5-aura-service/blob/master"
```

## Vista previa-Fenster

Das fzf-Fenster zeigt oben (50%) eine Vorschau des Treffers:
- 5 veces antes y después del partido
- Die Treffer-Zeile ist mit `>` marcado
- Zeilennummern werden angezeigt

## Suchverlauf

El inicio de la operación se realiza automáticamente cuando se inicia el proceso.
La verificación se encuentra en `~/.search_rules_history`.

## Typische Suchanfragen

```
FUZZY_MAP_pre                    # alle pre-Map Regeln
# TODO                           # auskommentierte Aufgaben
^.*$                             # Fullmatch-Regeln (Pipeline-Stopper)
re.IGNORECASE                    # alle Regex-Regeln mit Flag
koans                            # alle Koan-Dateien
```

## Bekannte Einschränkungen

- En Linux/macOS (no en Windows como `fzf` y `xdg-open`)
- Editor codificado en `kate` – para otros editores `PREFERRED_EDITOR`
- Sucht nur in `config/maps/` – no estoy gesamten Repo
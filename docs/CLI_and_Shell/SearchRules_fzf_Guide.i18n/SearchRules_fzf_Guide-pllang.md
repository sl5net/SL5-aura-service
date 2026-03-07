# search_rules.sh – Interaktywne Regelsuche mit fzf

> ⚠️ Korzystaj z systemu Linux/macOS. Kluczowa obsługa systemu Windows (fzf + xdg-open).

## Was es macht

`search_rules.sh` durchsucht alle Map-Dateien w `config/maps/` interaktiv mit `fzf`.
Treffer może bezpośrednio skontaktować się z redaktorem lub uzyskać dostęp do serwisu GitHub.

## Data w repozytorium

__KOD_BLOKU_0__

Wersja w `tools/` sollte entfernt lub durch einen Symlink ersetzt werden:
__KOD_BLOKU_1__

## Voraussetzungen

__KOD_BLOKU_2__

## Nutzung

__KOD_BLOKU_3__

## fzf Tastenkürzel

| Smak | Akcja |
|---|---|
| Tippena | Wprowadź suchanfrage |
| `Enter` | Datei im Editor öffnen (Kate) |
| `Ctrl+G` | Otwórz GitHub w przeglądarce |
| `Ctrl+Z` | Vorherige Suchanfrage z historią |
| `Ctrl+Y` | Nächste Suchanfrage aus History |
| `Ctrl+P` | Vorheriger Historia-Eintrag |
| `Ctrl+N` | Nächster History-Eintrag |
| `Ctrl+A` | Alle Treffer auswählen |
| `Ctrl+C` | Abbrechen |
| `Ctrl+←/→` | Wortweise nawigacja |
| `Ctrl+Backspace` | Wort löschen (linki) |
| `Ctrl+Usuń` | Brzeczka löschen (rechts) |

## Konfiguracja

Pasek przejścia Am Anfang des Scripts:

__KOD_BLOKU_4__

## Podgląd-Fenster

Das fzf-Fenster zeigt oben (50%) eine Vorschau des Treffers:
- 5 Zeilen vor und nach dem Match
- Die Treffer-Zeile ist mit `>` markert
- Zeilennummern werden angezeigt

## Suchverlauf

Die letzte Suchanfrage wird automatisch als Startwert beim nächsten Aufruf verwendet.
Der Verlauf znajduje się w `~/.search_rules_history`.

## Typowy suchanfragen

__KOD_BLOKU_5__

## Bekannte Einschränungen

- Nur Linux/macOS (w Windowsie są `fzf` i `xdg-open`)
- Edytor zakodowany na stałe auf `kate` – für anderen Editor `PREFERRED_EDITOR` ändern
- Przejdź do `config/maps/` – nie ma ich w repozytorium
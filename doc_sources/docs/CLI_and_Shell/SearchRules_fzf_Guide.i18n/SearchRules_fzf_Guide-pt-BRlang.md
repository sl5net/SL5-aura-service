# search_rules.sh – Registo interativo com fzf

> ⚠️ No Linux/macOS. Kein Windows-Support (fzf + xdg-open).

## Foi es macht

`search_rules.sh` exibe todos os dados do mapa em `config/maps/` interativo com `fzf`.
Treffer pode ser encontrado diretamente no editor ou no GitHub.

## Data no Repo

```
scripts/search_rules/search_rules.sh   ← offizielle Version
tools/search_rules.sh                  ← veraltet, hat hardcodierten Pfad-Bug
```

A versão em `tools/` é inserida ou durante um link simbólico:
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

__CODE_BLOCO_3__

## fzf Tastenkürzel

| Gosto | Ação |
|---|---|
| Tippen | Suchanfrage eingeben |
| `Entrar` | Data da Editora öffnen (Kate) |
| `Ctrl+G` | Zeile no GitHub no navegador desativado |
| `Ctrl+Z` | Vorherige Suchanfrage aus History |
| `Ctrl+Y` | Nächste Suchanfrage aus História |
| `Ctrl+P` | Vorheriger História-Eintrag |
| `Ctrl+N` | História de Nächster-Eintrag |
| `Ctrl+A` | Alle Treffer auswählen |
| `Ctrl+C` | Abbrechen |
| `Ctrl+←/→` | Palavra de navegação |
| `Ctrl+Backspace` | Mosto löschen (links) |
| `Ctrl+Excluir` | Mosto löschen (rechts) |

## Configuração

Anfang des Scripts anpassbar:

```bash
cd ~/projects/py/STT
bash scripts/search_rules/search_rules.sh
```

## Visualização-Fenster

Das fzf-Fenster zeigt oben (50%) eine Vorschau des Treffers:
- 5 Zeilen vor und nach dem Match
- Die Treffer-Zeile é com `>` markiert
- Zeilennummern werden angezeigt

## Suchverlauf

A taxa de transferência será automaticamente iniciada no início da operação.
O Verlauf está em `~/.search_rules_history`.

## Typische Suchanfragen

__CODE_BLOCO_5__

## Bekannte Einschränkungen

- No Linux/macOS (sem Windows com `fzf` e `xdg-open`)
- Editor codificado em `kate` – para outros editores `PREFERRED_EDITOR`
- Sucht nur in `config/maps/` – não está no repositório
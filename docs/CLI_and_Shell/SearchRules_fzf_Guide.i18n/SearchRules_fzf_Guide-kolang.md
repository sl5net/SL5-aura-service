# search_rules.sh – 대화형 Regelsuche mit fzf

> ⚠️ 누르 리눅스/macOS. Kein Windows 지원(fzf + xdg-open).

## 그게 전부였나?

`search_rules.sh`는 `config/maps/` interaktiv mit `fzf`에서 Map-Dateien을 검색합니다.
Treffer können은 GitHub angezeigt werden에서 편집자에게 직접 연락했습니다.

## 다티엔 임 레포

```
scripts/search_rules/search_rules.sh   ← offizielle Version
tools/search_rules.sh                  ← veraltet, hat hardcodierten Pfad-Bug
```

`tools/`의 다이 버전 sollte entfernt oder durch einen Symlink ersetzt werden:
```bash
rm ~/projects/py/STT/tools/search_rules.sh
ln -s ../scripts/search_rules/search_rules.sh ~/projects/py/STT/tools/search_rules.sh
```

## 보라우세춘겐

```bash
# fzf installieren (falls nicht vorhanden)
sudo apt install fzf        # Debian/Ubuntu
sudo pacman -S fzf          # Arch
brew install fzf            # macOS
```

## 누정

```bash
cd ~/projects/py/STT
bash scripts/search_rules/search_rules.sh
```

## fzf Tastenkürzel

| 맛 | 액션 |
|---|---|
| 티펜 | 수찬프라게 에인게벤 |
| `입력` | Datei im Editor öffnen (Kate) |
| `Ctrl+G` | GitHub에서 브라우저 사용 가능 |
| `Ctrl+Z` | Vorherige Suchanfrage aus 연혁 |
| `Ctrl+Y` | Nächste Suchanfrage aus 연혁 |
| `Ctrl+P` | Vorheriger 역사-Eintrag |
| `Ctrl+N` | Nächster 역사-Eintrag |
| `Ctrl+A` | Alle Treffer auswählen |
| `Ctrl+C` | 아브레헨 |
| `Ctrl+←/→` | Wortweise 항해 |
| `Ctrl+백스페이스` | Wort löschen (링크) |
| `Ctrl+삭제` | Wort löschen(rechts) |

## 구성

Am Anfang des Scripts anpassbar:

```bash
PREFERRED_EDITOR="kate"          # Editor für Ctrl+Enter
HISTORY_FILE="$HOME/.search_rules_history"  # Suchverlauf
DEFAULT_QUERY=".py pre # EXAMPLE:"          # Startsuche beim ersten Aufruf
REPO_URL="https://github.com/sl5net/SL5-aura-service/blob/master"
```

## 미리보기 - 펜스터

Das fzf-Fenster zeigt oben (50%) eine Vorschau des Treffers:
- 5 Zeilen vor und nach dem Match
- Die Treffer-Zeile ist mit `>` markiert
- Zeilennummern werden angezeigt

## 슈베라우프

Die letzte Suchanfrage wird automatisch als Startwert beim nächsten Aufruf verwendet.
Der Verlauf는 `~/.search_rules_history`에 있습니다.

## 티피셰 수찬프라겐

```
FUZZY_MAP_pre                    # alle pre-Map Regeln
# TODO                           # auskommentierte Aufgaben
^.*$                             # Fullmatch-Regeln (Pipeline-Stopper)
re.IGNORECASE                    # alle Regex-Regeln mit Flag
koans                            # alle Koan-Dateien
```

## Bekannte Einschränkugen

- Nur Linux/macOS(Windows wegen `fzf` 및 `xdg-open`)
- 편집기는 `kate`로 하드코딩됨 – für anderen 편집기 `PREFERRED_EDITOR` ändern
-`config/maps/`의 Sucht nur – nicht im gesamten Repo
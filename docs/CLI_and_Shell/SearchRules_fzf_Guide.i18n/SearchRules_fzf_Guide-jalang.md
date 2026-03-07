# search_rules.sh – fzf を使用したインタラクティブな規則

> ⚠️ Linux/macOS 以外では使用できません。 Kein Windows サポート (fzf + xdg-open)。

## そうだった

`search_rules.sh` は、`fzf` と対話型の `config/maps/` のすべての Map-Dateien を実行します。
Treffer können は、GitHub を使用して編集者を管理しています。

## ダティエン・イム・レポ

```
scripts/search_rules/search_rules.sh   ← offizielle Version
tools/search_rules.sh                  ← veraltet, hat hardcodierten Pfad-Bug
```

`tools/` 内のバージョンを確認してください。 Symlink ersetzt werden:
```bash
rm ~/projects/py/STT/tools/search_rules.sh
ln -s ../scripts/search_rules/search_rules.sh ~/projects/py/STT/tools/search_rules.sh
```

## フォラウセッツンゲン

```bash
# fzf installieren (falls nicht vorhanden)
sudo apt install fzf        # Debian/Ubuntu
sudo pacman -S fzf          # Arch
brew install fzf            # macOS
```

## ヌツング

```bash
cd ~/projects/py/STT
bash scripts/search_rules/search_rules.sh
```

## fzf タステンキュルツェル

|味 |アクション |
|---|---|
|ティッペン |サカンフラゲ・アインゲベン |
| `入力` |私は編集者です öffnen (Kate) | 編集者です
| `Ctrl+G` | GitHub をブラウザーで使用する方法 |
| `Ctrl+Z` |歴史 | 歴史 | 歴史 |
| `Ctrl+Y` |歴史 | 歴史 | 歴史 |
| `Ctrl+P` | Vorheriger History-Eintrag | 2018
| `Ctrl+N` | Nächster History-Eintrag |
| `Ctrl+A` |すべての Treffer auswählen |
| `Ctrl+C` |アブレヘン |
| `Ctrl+←/→` |ヴォルトヴァイゼ・ナビギレン |
| `Ctrl+Backspace` |ヴォルト・レーシェン (リンク) |
| `Ctrl + 削除` | Wort löschen (レヒツ) |

## 設定

パスバーのスクリプトを読んでいます:

```bash
PREFERRED_EDITOR="kate"          # Editor für Ctrl+Enter
HISTORY_FILE="$HOME/.search_rules_history"  # Suchverlauf
DEFAULT_QUERY=".py pre # EXAMPLE:"          # Startsuche beim ersten Aufruf
REPO_URL="https://github.com/sl5net/SL5-aura-service/blob/master"
```

## プレビュー-フェンスター

Das fzf-Fenster zeigt oben (50%) eine Vorschau des Treffers:
- 5 Zeilen vor und nach dem マッチ
- Die Treffer-Zeile ist mit `>` markiert
- Zeilennummern werden angezeigt

## サッチフェルラウフ

開始時間はすべて自動で開始されます。
`~/.search_rules_history` の詳細情報。

## ティピシェ・スカンフラゲン

```
FUZZY_MAP_pre                    # alle pre-Map Regeln
# TODO                           # auskommentierte Aufgaben
^.*$                             # Fullmatch-Regeln (Pipeline-Stopper)
re.IGNORECASE                    # alle Regex-Regeln mit Flag
koans                            # alle Koan-Dateien
```

## ベカンテ アインシュレンクンゲン

- Linux/macOS 以外 (Windows wegen `fzf` および `xdg-open` など)
- エディターのハードコード化された「kate」 – エディターの「PREFERRED_EDITOR」を参照
- `config/maps/` の内容 – nicht im gesamten Repo
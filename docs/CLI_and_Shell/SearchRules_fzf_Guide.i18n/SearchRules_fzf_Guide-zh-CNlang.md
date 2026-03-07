# search_rules.sh – 交互式 Regelsuche mit fzf

> ⚠️ Nur Linux/macOS。 Kein Windows 支持 (fzf + xdg-open)。

## 这是权力

`search_rules.sh` 包含在 `config/maps/` 中与 `fzf` 交互的所有地图日期。
Treffer 直接由编辑geöffnet 或 GitHub angezeigt werden 编辑。

## 回购协议中的日期

__代码_块_0__

`tools/` 中的版本可以使用符号链接：
__代码_块_1__

## 前言

__代码_块_2__

## 疯狂

__代码_块_3__

## fzf Tastenkürzel

|味道|行动 |
|---|---|
|蒂彭| Suchanfrage eingeben |
| `输入` | Datei im 编辑 öffnen (Kate) |
| `Ctrl+G` | Zeile 在浏览器中使用 GitHub öffnen |
| `Ctrl+Z` | Vorherige Suchanfrage aus 历史 |
| `Ctrl+Y` | Nächste Suchanfrage aus 历史 |
| `Ctrl+P` | Vorheriger 历史-Eintrag |
| `Ctrl+N` | Nächster 历史-Eintrag |
| `Ctrl+A` |全部 | Alle Treffer |
| `Ctrl+C` |阿布雷兴|
| `Ctrl+←/→` |导航 |
| `Ctrl+退格键` |麦芽汁（链接）|
| `Ctrl+删除` | Wort löschen（法律）|

## 配置

Am Anfang des Scripts anpassbar：

__代码_块_4__

## 预览-Fenster

Das fzf-Fenster zeigt oben (50%) eine Vorschau des Treffers：
- 5 场比赛
- Die Treffer-Zeile ist mit `>` markiert
- Zeilennummern werden angezeigt

## 类似的

此操作将自动启动，并自动启动。
Der Verlauf 位于“~/.search_rules_history”中。

## 典型的Suchanfragen

__代码_块_5__

## Bekannte Einschränkungen

- Nur Linux/macOS（主要是 Windows 版本 `fzf` 和 `xdg-open`）
- 编辑器硬编码 auf `kate` – für anderen 编辑器 `PREFERRED_EDITOR` ändern
- Sucht nur 在 `config/maps/` 中 – nicht im gesamten Repo
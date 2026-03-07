# Müll-Abfuhr Erinnerungs-Service（Aura 插件）

该工具自动化了万韦尔的故障排除，基本是官方的 Abfallkalender-PDF。

## 功能
- **PDF 解析**：最直接的终端是 `Abfallterminuebersicht-*.pdf`。
- **桌面-Benachrichtigung**：在 Manjaro 下为可视化警报提供“通知发送”功能。
- **Sprachausgabe**：Nutzt `espeak` für akustische Warnungen（理想，wenn das Handy verlegt ist）。
- **Sicherheits-Check**：Warnt aktiv，wenn das PDF-Jahr abgelaufen ist oder die Datei fehlt。

## 安装和使用
1. **系统 Pakete** (Manjaro)：
__代码_块_0__
2. **Python-Abhängigkeiten** (im Aura-Venv)：
__代码_块_1__

## 自动化 (Systemd)
Der Dienst prüft täglich um 17:00 Uhr sowie 1 Minute nach dem Systemstart, ob am Folgetag Müll abgeholt wird。

**服务-Datei：**
〜/.config/systemd/user/trash_check.service

**定时器-Datei：** `
〜/.config/systemd/user/trash_check.timer

Befehle zum Aktivieren：
__代码_块_2__

## 四季的使用
1. Neues PDF von der Gemeinde Wannweil herunterladen。
2. 在 Ordner `config/maps/plugins/wannweil/de-DE/` ersetzen 中输入日期。
3. Der Service erkennt das new Jahr automatisch am Dateinamen。
4. PDF 会被删除或被删除，并发送系统信息。

## 曼努勒测试
__代码_块_3__
__代码_块_4__
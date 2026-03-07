# Müll-Abfuhr Erinnerungs-Service (Aura プラグイン)

Dieses Tool automatisiert die Erinnerung an Abfalltermine für Wannweil、basierend auf dem offiziellen Abfallkalender-PDF。

## ファンクショネン
- **PDF 解析**: `Abfallterminuebersicht-*.pdf` を使用した最も重要な用語。
- **デスクトップの操作**: マンジャロに対する警告を表示するための「通知送信」。
- **Sprachausgabe**: Nutzt `espeak` für akustische Warnungen (理想的、便利なverlegt ist)。
- **Sicherheits-Check**: 警告アクション、PDF-Jahr abgelaufen ist oder die Datei fehlt。

## インストールと詳細
1. **システム-パケテ** (Manjaro):
   ```bash
   sudo pacman -S libnotify espeak-ng
   ```
2. **Python-Abhängigkeiten** (Aura-Venv):
   ```bash
   # Im Ordner ~/projects/py/STT/
   source .venv/bin/activate
   pip install pdfplumber
   ```

## 自動化 (Systemd)
Der Dienst prüft täglich um 17:00 Uhr sowie 1 Minute nach dem Systemstart, ob am Folgetag Müll abgeholt wird.

**サービスデート:**
~/.config/systemd/user/trash_check.service

**タイマー日付:** `
~/.config/systemd/user/trash_check.timer

活動内容:
```bash
systemctl --user daemon-reload
systemctl --user enable --now trash_check.timer

systemctl --user daemon-reload; systemctl --user enable --now trash_check.timer

```

## ヤーレスヴェクセルのエンプフェルンゲン
1. Neues PDF von der Gemeinde Wannweil herunterladen。
2. オードナーの「config/maps/plugins/wannweil/de-DE/」を設定してください。
3. Der Service erkennt das neue Jahr automatisch am Dateinamen.
4. フォールズは PDF を参照して、システムを参照して送信します。

## マニュラーテスト
```bash
# Testet die Benachrichtigungskette ohne Rücksicht auf das Datum
/.../python3 check_trash.py test
```
__CODE_BLOCK_4__
# Müll-Abfuhr Erinnerungs-Service (Aura 플러그인)

Dieses Tool은 Wannweil에 대한 Abfalltermine을 자동으로 생성하고 Abfallkalender-PDF에 대한 기본 정보를 제공합니다.

## 기능
- **PDF 구문 분석**: Liest Termine은 `Abfallterminuebersicht-*.pdf`로 직접 연결됩니다.
- **Desktop-Benachrichtigung**: Manjaro의 visuelle Alarme에 대한 '알림-보내기'를 사용하세요.
- **Sprachausgabe**: Nutzt `espeak` für akustische Warnungen(이상적, wenn das Handy verlegt ist).
- **Sicherheits-Check**: Warnt aktiv, wenn das PDF-Jahr abgelaufen ist oder die Datei fehlt.

## 설치 및 Voraussetzungen
1. **시스템-파케테**(만자로):
   ```bash
   sudo pacman -S libnotify espeak-ng
   ```
2. **Python-Abhängigkeiten**(임 Aura-Venv):
   ```bash
   # Im Ordner ~/projects/py/STT/
   source .venv/bin/activate
   pip install pdfplumber
   ```

## 자동화(시스템)
Der Dienst prüft täglich um 17:00 Uhr sowie 1 Minute nach dem Systemstart, ob am Folgetag Müll abgeholt wird.

**서비스 날짜:**
~/.config/systemd/user/trash_check.service

**타이머-날짜:** `
~/.config/systemd/user/trash_check.timer

Befehle zum 활성:
```bash
systemctl --user daemon-reload
systemctl --user enable --now trash_check.timer

systemctl --user daemon-reload; systemctl --user enable --now trash_check.timer

```

## Empfehlungen für den Jahreswechsel
1. 새로운 PDF von der Gemeinde Wannweil herunterladen.
2. Die Datei im Ordner `config/maps/plugins/wannweil/de-DE/` ersetzen.
3. Der Service erkennt das neue Jahr automatisch am Dateinamen.
4. Falls das PDF fehlt oder veraltet ist, sendet das System eine tägliche Fehlermeldung.

## 마누엘러 테스트
```bash
# Testet die Benachrichtigungskette ohne Rücksicht auf das Datum
/.../python3 check_trash.py test
```
__CODE_BLOCK_4__
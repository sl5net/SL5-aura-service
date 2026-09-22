> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../check_trash_Anleitung.md).*

# Trash Collection Reminder Service (Aura Plugin)

This tool automates the reminder for waste collection dates for Wannweil, based on the official waste calendar PDF.

## Functions
- **PDF Parsing**: Reads appointments directly from the `Abfallterminuebersicht-*.pdf`.
- **Desktop Notification**: Uses `notify-send` for visual alerts on Manjaro.
- **Voice output**: Uses `espeak` for audio alerts (ideal if the phone is misplaced).
- **Security Check**: Actively warns if the PDF year has expired or the file is missing.

## Installation & Requirements
1. **System Packages** (Manjaro):
   ```bash
   sudo pacman -S libnotify espeak-ng
   ```
2. **Python dependencies** (in the Aura venv):
   ```bash
   # Im Ordner ~/projects/py/STT/
   source .venv/bin/activate
   pip install pdfplumber
   ```

## Automation (Systemd)
The service checks daily at 5:00 PM as well as 1 minute after system startup whether trash will be collected the next day.

**Service File:** 
~/.config/systemd/user/trash_check.service

**Timer file:** `
~/.config/systemd/user/trash_check.timer

Commands to activate:
```bash
systemctl --user daemon-reload
systemctl --user enable --now trash_check.timer

systemctl --user daemon-reload; systemctl --user enable --now trash_check.timer

```

## Recommendations for the Turn of the Year
1. Download new PDF from the municipality of Wannweil.
2. Replace the file in folder `config/maps/plugins/wannweil/de-DE/`.
3. The service automatically recognizes the new year by the file name.
4. If the PDF is missing or outdated, the system sends a daily error message.

## Manual Test
```bash
# Testet die Benachrichtigungskette ohne Rücksicht auf das Datum
/.../python3 check_trash.py test
```
__CODE_BLOCK_1__


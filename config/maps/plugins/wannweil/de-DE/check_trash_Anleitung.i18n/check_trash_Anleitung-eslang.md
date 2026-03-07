# Müll-Abfuhr Erinnerungs-Service (complemento Aura)

Esta herramienta automatiza la configuración de una terminación de fallas para Wannweil, basada en el calendario de caídas oficial-PDF.

## Funciones
- **Análisis de PDF**: Liest Termine direkt aus der `Abfallterminuebersicht-*.pdf`.
- **Desktop-Benachrichtigung**: Nutzt `notify-send` für visuelle Alarme unter Manjaro.
- **Sprachausgabe**: Nutzt `espeak` für akustische Warnungen (ideal, cuando el Handy verlegt ist).
- **Sicherheits-Check**: Warnt aktiv, wenn das PDF-Jahr abgelaufen ist oder die Datei fehlt.

## Instalación y configuración
1. **Sistema-Paquete** (Manjaro):
   ```bash
   sudo pacman -S libnotify espeak-ng
   ```
2. **Python-Abhängigkeiten** (en Aura-Venv):
   ```bash
   # Im Ordner ~/projects/py/STT/
   source .venv/bin/activate
   pip install pdfplumber
   ```

## Automatización (Systemd)
Der Dienst prüft täglich um 17:00 Uhr sowie 1 Minute after dem Systemstart, ob am Folgetag Müll abgeholt wird.

**Fecha de servicio:**
~/.config/systemd/user/trash_check.service

**Fecha del temporizador:** `
~/.config/systemd/user/trash_check.timer

Befehle zum Aktivieren:
```bash
systemctl --user daemon-reload
systemctl --user enable --now trash_check.timer

systemctl --user daemon-reload; systemctl --user enable --now trash_check.timer

```

## Empfehlungen für den Jahreswechsel
1. Neues PDF von der Gemeinde Wannweil herunterladen.
2. Introduzca la fecha en el pedido `config/maps/plugins/wannweil/de-DE/`.
3. El servicio activa automáticamente el nuevo año en la fecha.
4. Falls das PDF fehlt oder veraltet ist, sendet das System eine tägliche Fehlermeldung.

## Prueba de Manueller
```bash
# Testet die Benachrichtigungskette ohne Rücksicht auf das Datum
/.../python3 check_trash.py test
```
__CODE_BLOCK_4__
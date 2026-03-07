# Müll-Abfuhr Erinnerungs-Service (Plugin Aura)

Esta ferramenta automatiza o registro e o término da captura para Wannweil, baseada no calendário de captura oficial-PDF.

## Funções
- **Análise de PDF**: Liest Termine diretamente para `Abfallterminuebersicht-*.pdf`.
- **Desktop-Benachrichtigung**: Nutzt `notify-send` para alarme visual em Manjaro.
- **Sprachausgabe**: Nutzt `espeak` für akustische Warnungen (ideal, quando o Handy é verlegt).
- **Sicherheits-Check**: Warnt ativo, quando o PDF-Jahr abgelaufen ist ou o Datei fehlt.

## Instalação e utilização
1. **Sistema-Pakete** (Manjaro):
   ```bash
   sudo pacman -S libnotify espeak-ng
   ```
2. **Python-Abhängigkeiten** (no Aura-Venv):
   ```bash
   # Im Ordner ~/projects/py/STT/
   source .venv/bin/activate
   pip install pdfplumber
   ```

## Automatização (Systemd)
O dia é iniciado às 17:00 horas, 1 minuto após a inicialização do sistema, até que o Folgetag seja encerrado.

**Data do serviço:**
~/.config/systemd/user/trash_check.service

**Temporizador-Data:** `
~/.config/systemd/user/trash_check.timer

Befehle zum Aktivieren:
```bash
systemctl --user daemon-reload
systemctl --user enable --now trash_check.timer

systemctl --user daemon-reload; systemctl --user enable --now trash_check.timer

```

## Empfehlungen für den Jahreswechsel
1. Neues PDF von der Gemeinde Wannweil herunterladen.
2. A data da ordem `config/maps/plugins/wannweil/de-DE/` é definida.
3. O serviço inicia o novo ano automaticamente em datas.
4. Se o PDF for detectado ou verificado, envie uma mensagem de texto para o sistema.

## Teste Manueller
__CODE_BLOCO_3__
```bash
# Testet die Benachrichtigungskette ohne Rücksicht auf das Datum
/.../python3 check_trash.py test
```
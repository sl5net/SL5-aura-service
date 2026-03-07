# Service de maintenance Müll-Abfuhr (Plugin Aura)

Cet outil automatise la préparation des arrêts d'urgence pour Wannweil, basé sur le calendrier d'arrêts officiel-PDF.

## Fonctions
- **PDF-Parsing** : Liest Termine direkt aus der `Abfallterminuebersicht-*.pdf`.
- **Desktop-Benachrichtigung**: Nutzt `notify-send` pour l'alarme visuelle sous Manjaro.
- **Sprachausgabe** : Nutzt `espeak` für akustische Warnungen (idéal, quand le Handy verlegt ist).
- **Sicherheits-Check** : Warnt aktiv, wenn das PDF-Jahr abgelaufen ist oder die Datei fehlt.

## Installation et configurations
1. **Système-Pakete** (Manjaro) :
   ```bash
   sudo pacman -S libnotify espeak-ng
   ```
2. **Python-Abhängigkeiten** (dans Aura-Venv) :
   ```bash
   # Im Ordner ~/projects/py/STT/
   source .venv/bin/activate
   pip install pdfplumber
   ```

## Automatisation (Systemd)
Le service est prévu à 17h00 pendant 1 minute seulement après le démarrage du système, puis le message est terminé.

**Date de service :**
~/.config/systemd/user/trash_check.service

**Timer-Datei :** `
~/.config/systemd/user/trash_check.timer

Befehle zum Aktivieren:
```bash
systemctl --user daemon-reload
systemctl --user enable --now trash_check.timer

systemctl --user daemon-reload; systemctl --user enable --now trash_check.timer

```

## Empfehlungen für den Jahreswechsel
1. Neues PDF von der Gemeinde Wannweil herunterladen.
2. Les dates dans l'ordre `config/maps/plugins/wannweil/de-DE/` sont terminées.
3. Der Service erkennt das neue Jahr automatisch am Dateinamen.
4. Lorsque le PDF est envoyé ou envoyé, le système envoie un fichier de configuration simple.

## Test de Manueller
```bash
# Testet die Benachrichtigungskette ohne Rücksicht auf das Datum
/.../python3 check_trash.py test
```
__CODE_BLOCK_4__
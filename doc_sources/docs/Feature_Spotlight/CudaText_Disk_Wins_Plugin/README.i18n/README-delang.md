# CudaText-Plugin: „Disk Wins“ (Auto-Neuladen bei externer Änderung erzwingen)

CudaText verfügt über keine integrierte Option, die eine Datei automatisch neu lädt, sobald sie geöffnet wird
Änderungen auf der Festplatte – jeder integrierte Modus „Auf Festplatte geändert“ zeigt immer noch einige an
Art der Eingabeaufforderung (modal oder modallos) vor dem Neuladen
(siehe „ui_notif_confirm“ in „default.json“, Werte „0“–„4“, alle davon
fragen). Dieses Plugin schließt diese Lücke: **Festplatte gewinnt immer**, keine Eingabeaufforderung, nie.

Hier archiviert, damit niemand dafür die CudaText-Plugin-API neu ableiten muss
wieder. Die Quelle der Wahrheit für das Plugin selbst liegt darin
[`cuda_disk_wins/`](.././cuda_disk_wins/) in diesem Ordner.

## Was es tut

- Fragt jede geöffnete, benannte Datei einmal pro Sekunde ab (konfigurierbar über
`TIMER_INTERVAL` in `__init__.py`).
– Wenn sich die mtime einer Datei auf der Festplatte ändert, liest das Plugin sie erneut und ruft auf
`Editor.set_text_all()` — **überschreibt alle nicht gespeicherten Änderungen in der
Editor-Tab, ohne zu fragen**.
- Löscht anschließend das „modified“-Flag („PROP_MODIFIED = False“), sodass die
Die Registerkarte sieht sauber aus, als ob nie etwas auseinandergegangen wäre.
- Best-Effort stellt die Caret-Position und die obere sichtbare Linie danach wieder her
neu laden.
- Fügt zwei Befehle unter „Plugins → Disk Wins“ hinzu:
- „Automatisches Neuladen ein-/ausschalten“.
- „Jetzt prüfen“ (manuelle einmalige Prüfung)

## Warum ein Plugin statt einer Einstellung

CudaTexts eigener Datei-Watcher („ui_notif“) bietet immer nur „Ask“-Verhalten:

| `ui_notif_confirm` | Verhalten |
|--------|--------------------------------------|
| 0 | modallose Eingabeaufforderung, immer |
| 1 | Eingabeaufforderung ohne Modal, wenn Editor geändert oder Rückgängig nicht leer |
| 2 | Eingabeaufforderung ohne Modal, wenn der Editor sie geändert hat |
| 3 | modale Eingabeaufforderung, immer |
| 4 | modale Eingabeaufforderung, wenn der Editor geändert wurde |

Es gibt keinen Wert, der „Automatisch neu laden, keine Aufforderung, weitermachen“ bedeutet.
Daher dieses kleine Plugin, das seine eigene Polling-Schleife ausführt und neu lädt
direkt über die Python-API.

## Installation

```bash
mkdir -p ~/.config/cudatext/py
cp -r cuda_disk_wins ~/.config/cudatext/py/
```

Starten Sie CudaText neu.

**Wichtig:** Deaktivieren Sie dazu auch den eigenen Änderungsbenachrichtigungsdialog von CudaText
es kämpft nicht mit dem Plugin. In
`~/.config/cudatext/settings/user.json`:

```json
{
    "ui_notif": false
}
```

(Entspricht „Optionen → Einstellungen – Benutzerkonfiguration“ in der Benutzeroberfläche.) Starten Sie neu
CudaText nach dieser Änderung erneut.

## Vorbehalte

– Dies ist absichtlich destruktiv: Nicht gespeicherte Editor-Änderungen werden verworfen
stillschweigend, sobald sich die Datei von außen ändert. Das ist das Ganze
Punkt des Plugins – installieren Sie es nicht, wenn Sie es manchmal behalten möchten
lokale Änderungen über externe Änderungen.
- Reagiert nur auf Änderungen in der mtime der Datei; Eingabe im Editor selbst
löst kein Nachladen aus (keine Rückkopplungsschleife).
- Wenn die Datei extern gelöscht wird, unternimmt das Plugin bis dahin nichts
erscheint wieder (kein Absturz, keine wiederholten Neuladeversuche).
- Die Kodierung wird über „PROP_ENC“ gelesen und dem nächstgelegenen Python-Codec zugeordnet;
Erweitern Sie „ENC_MAP“ in „__init__.py“, wenn Sie eine Kodierung verwenden, die noch nicht vorhanden ist
aufgeführt.

## Herkunft

Entwickelt für den „Dateisystemänderungen stets dem nicht gespeicherten Editor vorziehen“.
Puffer, keine Bestätigung“-Anforderung, die beim Einrichten von CudaText besprochen wurde
über `yay -S cudatext-qt6-bin python` auf Arch.
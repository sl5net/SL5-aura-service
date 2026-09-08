# CopyQ macOS-Fehlerbehebung: Unsichtbare GUI und manuelle Hotkey-Konfiguration

Dieses Handbuch befasst sich mit häufigen Problemen, die unter macOS (insbesondere bei Geräten der Apple Silicon M-Serie) auftreten, wenn die grafische Benutzeroberfläche (GUI) von CopyQ nicht angezeigt wird oder globale Tastenkombinationen (z. B. F10) neu zugewiesen werden müssen, ohne auf die GUI zuzugreifen.

---

## 1. Fehlerbehebung bei der unsichtbaren GUI

Unter macOS läuft CopyQ möglicherweise ordnungsgemäß im Hintergrund, bleibt aber aus zwei Hauptgründen optisch verborgen:
- **Koordinaten außerhalb des Bildschirmfensters**: Nach Auflösungsänderungen oder dem Trennen eines externen Monitors behält CopyQ möglicherweise Koordinaten außerhalb des sichtbaren Anzeigebereichs bei.
- **Verstopfung der Menüleistenkerbe**: Bei MacBook-Modellen mit Kamerakerbe verbirgt macOS überschüssige Menüleistensymbole automatisch hinter der Kerbe, wenn das Fach voll ist.

### Lösung: Geometrie- und Kraftanzeige zurücksetzen

Führen Sie die folgenden Befehle im Terminal aus, um Off-Screen-Koordinaten zu löschen und das Fenster in den Vordergrund zu bringen:

```bash
copyq config geometry ""
copyq show
```

Wenn das Fenster immer noch nicht angezeigt wird, schalten Sie seinen Status über die CLI um:

```bash
copyq toggle
```

---

## 2. Manuelles Ändern von Hotkeys mit CudaText

Wenn eine globale Verknüpfung (z. B. „F10“) von einer anderen Anwendung beansprucht oder abgefangen wird, kann die Verknüpfung direkt in der Konfigurationsdatei mit CudaText bearbeitet werden, ohne die CopyQ-GUI zu öffnen.

### Schritt 1: Beenden Sie den CopyQ-Prozess

CopyQ muss vor dem Bearbeiten der Konfigurationsdatei gestoppt werden, um zu verhindern, dass Ihre Änderungen beim Beenden überschrieben werden:

```bash
copyq exit
```

### Schritt 2: Öffnen Sie die Konfiguration in CudaText

Unter macOS werden CopyQ-Befehlsverknüpfungen in „copyq-commands.ini“ gespeichert.

Öffnen Sie die Datei in CudaText:

```bash
cudatext "$HOME/Library/Application Support/copyq/copyq-commands.ini"
```

*Hinweis: Wenn die Datei nicht in „Application Support“ vorhanden ist, öffnen Sie den XDG-Fallback-Speicherort:*

```bash
cudatext "$HOME/.config/copyq/copyq-commands.ini"
```

### Schritt 3: Verknüpfung neu zuweisen

1- Drücken Sie in CudaText „Cmd + F“, um die Suchleiste zu öffnen.
2- Suchen Sie nach „F10“ oder „GlobalShortcut=F10“.
3- Ersetzen Sie „F10“ durch eine verfügbare Tastenkombination (z. B. „F9“ oder „Strg+F10“ oder „Meta+F10“).
4- Speichern Sie die Datei („Cmd + S“) und schließen Sie CudaText („Cmd + Q“).

### Schritt 4: CopyQ neu starten

Starten Sie CopyQ erneut, um die aktualisierte Verknüpfungskonfiguration zu laden:

```bash
open -a CopyQ
```

Die neue globale Verknüpfung ist jetzt aktiv.
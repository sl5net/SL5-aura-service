# CLI-Workflow-Tools-Installationshandbuch

Einige Aktionen im Pfadnavigator-Plugin basieren auf externen Befehlszeilendienstprogrammen, um Fuzzy-Suchen durchzuführen, Dateien aufzulisten und die Zwischenablage zu bearbeiten. Wenn diese Tools fehlen, wird in der Systemkonsole eine Warnung angezeigt.

Nachfolgend finden Sie die Installationsanweisungen für jedes unterstützte Betriebssystem.

## Erforderliche Dienstprogramme

* **`fzf`**: Allzweck-Befehlszeilen-Fuzzy-Finder.
* **`find`** (oder `fd`): Standard-Dienstprogramm zur Dateisuche.
* **Zwischenablage-Tool**: Wird verwendet, um die Ausgabe direkt an die Zwischenablage Ihres Systems weiterzuleiten.
* **Linux:** `xclip` (erfordert X11-Umgebung).
* **macOS:** `pbcopy` (vorinstalliert).
* **Windows:** `clip` (vorinstalliert).
* **`Datei`**: Bestimmt Dateitypen für vollständige Terminalvorschauen.

---

## Installationsanweisungen

### 1. Linux (Arch / Manjaro)
Da Ihr System auf Manjaro läuft, können Sie die benötigten Pakete mit „pacman“ installieren:

```bash
sudo pacman -S fzf findutils xclip file
```



## 1. Schnelle Dateiauswahl (Aura-Befehl)

Die Aktion „path_navigator“ verwendet den folgenden Git-fähigen „fzf“-Befehl. Sein Zweck besteht darin, einen Dateipfad direkt in die Systemzwischenablage auszugeben.

**Befehlslogik:**
– Verwendet „git ls-files“ in einem Git-Repository (schließt ignorierte Dateien aus).
- Fällt auf „find“ zurück. -type f` außerhalb eines Git-Repositorys.
- Gibt den ausgewählten Pfad mit „xclip -selection clipboard“ in die Zwischenablage aus.

## 2. Schnelle Dateiausführung (die „k“-Funktion)

Um die Schleife abzuschließen, wird die benutzerdefinierte Shell-Funktion „k“ verwendet. Diese Funktion übernimmt den Pfad aus der Zwischenablage und öffnet die Datei sofort in „kate“.

### Implementierung

Fügen Sie der Konfigurationsdatei Ihrer Shell die folgende Funktion hinzu (z. B. „~/.bashrc“, „~/.zshrc“):

```bash
# Function to open a file path from the system clipboard in Kate
function k {
    # Check if xclip is available
    if ! command -v xclip &> /dev/null; then
        echo "Error: xclip is required but not installed."
        return 1
    fi
    
    # 1. Get clipboard content
    CLIPBOARD_CONTENT=$(xclip -selection clipboard -o 2>/dev/null)
    
    # Check if clipboard is empty
    if [ -z "${CLIPBOARD_CONTENT}" ]; then
        echo "Error: Clipboard is empty. Nothing to open."
        return 1
    fi

    # 2. Check for multiline content (ensures only a single file path is used)
    LINE_COUNT=$(echo "${CLIPBOARD_CONTENT}" | wc -l)
    
    if [ "${LINE_COUNT}" -gt 1 ]; then
        echo "Error: Clipboard contains ${LINE_COUNT} lines. Only single-line file paths are supported."
        return 1
    fi
    
    # 3. Print the command before execution (User Feedback)
    echo "kate \"${CLIPBOARD_CONTENT}\""
    
    # 4. Final Execution
    # The double quotes around the content handle filenames with spaces correctly.
    # The '&' runs the command in the background, freeing the terminal.
    kate "${CLIPBOARD_CONTENT}" &
}
```

### Nutzung

1. Verwenden Sie den Befehl „path_navigator“ (geben Sie z. B. „search file“ in Ihr Trigger-Tool ein).
2. Suchen Sie die gewünschte Datei und wählen Sie sie aus (z. B. „src/main/config.py“).
3. Geben Sie in Ihrem Terminal „k“ ein und drücken Sie **ENTER**.
4. Die Datei wird sofort in Kate geöffnet.
__CODE_BLOCK_2__
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

### 2. Linux (Debian / Ubuntu / Mint)
Verwenden Sie auf Debian-basierten Systemen „apt“:

```bash
sudo apt update
sudo apt install fzf findutils xclip file
```

### 3. macOS
Verwenden Sie den [Homebrew](https://brew.sh/)-Paketmanager, um die fehlenden Tools zu installieren:

```bash
brew install fzf findutils
# Note: 'pbcopy' and 'file' are native on macOS.
```

### 4. Windows
Wenn Sie Windows verwenden, empfehlen wir die Installation von „fzf“ über [Scoop](https://scoop.sh/) oder [Winget](https://github.com/microsoft/winget-cli):

```powershell
# Using Winget
winget install junegunn.fzf

# Using Scoop
scoop install fzf
```
__CODE_BLOCK_4__
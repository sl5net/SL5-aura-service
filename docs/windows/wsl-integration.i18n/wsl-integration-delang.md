# WSL-Integration (Windows-Subsystem für Linux).

Mit WSL können Sie eine vollständige Linux-Umgebung direkt unter Windows ausführen. Nach der Einrichtung funktioniert die STT-Shell-Integration **identisch mit den Linux Bash- oder Zsh-Anleitungen** – für die Shell-Funktion selbst sind keine Windows-spezifischen Anpassungen erforderlich.

> **Empfohlen für:** Windows-Benutzer, die mit einem Linux-Terminal vertraut sind oder WSL bereits für Entwicklungsarbeiten installiert haben. WSL bietet das zuverlässigste Erlebnis und die geringsten Kompatibilitätskompromisse.

## Voraussetzungen

### WSL installieren (einmalige Einrichtung)

Öffnen Sie PowerShell oder CMD **als Administrator** und führen Sie Folgendes aus:

```powershell
wsl --install
```

Dadurch wird WSL2 standardmäßig mit Ubuntu installiert. Starten Sie Ihren Computer neu, wenn Sie dazu aufgefordert werden.

So installieren Sie eine bestimmte Distribution:

```powershell
wsl --install -d Ubuntu-24.04
# or
wsl --install -d Debian
```

Alle verfügbaren Distributionen auflisten:

```powershell
wsl --list --online
```

### Überprüfen Sie Ihre WSL-Version

```powershell
wsl --list --verbose
```

Stellen Sie sicher, dass in der Spalte „VERSION“ „2“ angezeigt wird. Wenn „1“ angezeigt wird, aktualisieren Sie mit:

```powershell
wsl --set-version <DistroName> 2
```

## Shell-Integration innerhalb der WSL

Sobald WSL ausgeführt wird, öffnen Sie Ihr Linux-Terminal und folgen Sie der **Linux-Shell-Anleitung** für Ihre bevorzugte Shell:

| Schale | Leitfaden |
|-------|-------|
| Bash (WSL-Standard) | [bash-integration.md](../../linux/bash-integration.i18n/bash-integration-delang.md) |
| Zsh | [zsh-integration.md](../../linux/zsh-integration.i18n/zsh-integration-delang.md) |
| Fisch | [fish-integration.md](../../linux/fish-integration.i18n/fish-integration-delang.md) |
| Ksh | [ksh-integration.md](../../linux/ksh-integration.i18n/ksh-integration-delang.md) |
| POSIX sh / Dash | [posix-sh-integration.md](../../linux/posix-sh-integration.i18n/posix-sh-integration-delang.md) |

Für das standardmäßige Ubuntu/Debian-WSL-Setup mit Bash lautet der Schnellpfad:

```bash
nano ~/.bashrc
# Paste the function block from bash-integration.md
source ~/.bashrc
```

## WSL-spezifische Überlegungen

### Zugriff auf Windows-Dateien über die WSL

Ihre Windows-Laufwerke werden unter „/mnt/“ gemountet:

```bash
/mnt/c/   # → C:\
/mnt/d/   # → D:\
```

Wenn sich Ihr Projekt im Windows-Dateisystem befindet (z. B. „C:\Projects\stt“), setzen Sie „PROJECT_ROOT“ auf:

```bash
export PROJECT_ROOT="/mnt/c/Projects/stt"
```

Fügen Sie diese Zeile zu Ihrem „~/.bashrc“ (oder dem Äquivalent für Ihre Shell) **über** der Funktion „s()“ hinzu.

> **Leistungstipp:** Für eine optimale E/A-Leistung sollten Sie die Projektdateien im WSL-Dateisystem (z. B. „~/projects/stt“) und nicht in „/mnt/c/...“ aufbewahren. Der dateisystemübergreifende Zugriff zwischen WSL und Windows ist deutlich langsamer.

### Virtuelle Python-Umgebung innerhalb der WSL

Erstellen und verwenden Sie eine standardmäßige virtuelle Linux-Umgebung innerhalb der WSL:

```bash
cd "$PROJECT_ROOT"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Der Pfad „PY_EXEC“ in der Funktion („$PROJECT_ROOT/.venv/bin/python3“) funktioniert unverändert korrekt.

### Ausführen von „s“ über das Windows-Terminal

[Windows Terminal](https://aka.ms/terminal) ist die empfohlene Methode zur Verwendung von WSL unter Windows. Es unterstützt mehrere Registerkarten, Bereiche und Profile für jede WSL-Verteilung. Installieren Sie es aus dem Microsoft Store oder über:

```powershell
winget install Microsoft.WindowsTerminal
```

Legen Sie Ihre WSL-Distribution als Standardprofil in den Windows-Terminal-Einstellungen fest, um ein möglichst nahtloses Erlebnis zu gewährleisten.

### Docker und Kiwix innerhalb der WSL

Das Kiwix-Hilfsskript („kiwix-docker-start-if-not-running.sh“) erfordert Docker. Installieren Sie Docker Desktop für Windows und aktivieren Sie die WSL 2-Integration:

1. Laden Sie [Docker Desktop](https://www.docker.com/products/docker-desktop/) herunter und installieren Sie es.
2. Aktivieren Sie in Docker Desktop → Einstellungen → Ressourcen → WSL-Integration Ihre WSL-Verteilung.
3. Überprüfen Sie innerhalb der WSL:
   ```bash
   docker --version
   ```

### Aufrufen der WSL-Funktion „s“ unter Windows (optional)

Wenn Sie die Verknüpfung „s“ von einem Windows CMD- oder PowerShell-Fenster aus aufrufen möchten, ohne ein WSL-Terminal zu öffnen, können Sie sie wie folgt umschließen:

```powershell
# PowerShell wrapper
function s { wsl bash -i -c "s $args" }
```

```bat
:: CMD wrapper — save as s.bat on your PATH
@echo off
wsl bash -i -c "s %*"
```

> Das Flag „-i“ lädt eine interaktive Shell, sodass Ihr „~/.bashrc“ (und die Funktion „s“) automatisch als Quelle verwendet werden.

## Merkmale

- **Volle Linux-Kompatibilität**: Alle Unix-Tools („timeout“, „pgrep“, „mktemp“, „grep“) funktionieren nativ – keine Problemumgehungen erforderlich.
- **Dynamische Pfade**: Findet automatisch das Projektstammverzeichnis über die Variable „PROJECT_ROOT“, die in Ihrer Shell-Konfiguration festgelegt ist.
- **Automatischer Neustart**: Wenn das Backend ausgefallen ist, versucht es, „start_service“ und lokale Wikipedia-Dienste auszuführen (Docker muss ausgeführt werden).
- **Intelligente Zeitüberschreitungen**: Versucht zunächst eine schnelle 2-Sekunden-Reaktion und fällt dann auf einen 70-Sekunden-Tiefverarbeitungsmodus zurück.
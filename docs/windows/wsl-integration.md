# WSL (Windows Subsystem for Linux) Integration

WSL lets you run a full Linux environment directly on Windows. Once set up, the STT shell integration works **identically to the Linux Bash or Zsh guides** — no Windows-specific adaptation needed for the shell function itself.

> **Recommended for:** Windows users who are comfortable with a Linux terminal, or who already have WSL installed for development work. WSL provides the most faithful experience and the fewest compatibility compromises.

## Prerequisites

### Install WSL (one-time setup)

Open PowerShell or CMD **as Administrator** and run:

```powershell
wsl --install
```

This installs WSL 2 with Ubuntu by default. Restart your machine when prompted.

To install a specific distribution:

```powershell
wsl --install -d Ubuntu-24.04
# or
wsl --install -d Debian
```

List all available distributions:

```powershell
wsl --list --online
```

### Verify your WSL version

```powershell
wsl --list --verbose
```

Make sure the `VERSION` column shows `2`. If it shows `1`, upgrade with:

```powershell
wsl --set-version <DistroName> 2
```

## Shell Integration Inside WSL

Once WSL is running, open your Linux terminal and follow the **Linux shell guide** for your preferred shell:

| Shell | Guide |
|-------|-------|
| Bash (WSL default) | [bash-integration.md](../linux/bash-integration.md) |
| Zsh | [zsh-integration.md](../linux/zsh-integration.md) |
| Fish | [fish-integration.md](../linux/fish-integration.md) |
| Ksh | [ksh-integration.md](../linux/ksh-integration.md) |
| POSIX sh / Dash | [posix-sh-integration.md](../linux/posix-sh-integration.md) |

For the default Ubuntu/Debian WSL setup with Bash, the quick path is:

```bash
nano ~/.bashrc
# Paste the function block from bash-integration.md
source ~/.bashrc
```

## WSL-Specific Considerations

### Accessing Windows files from WSL

Your Windows drives are mounted under `/mnt/`:

```bash
/mnt/c/   # → C:\
/mnt/d/   # → D:\
```

If your project lives on the Windows filesystem (e.g. `C:\Projects\stt`), set `PROJECT_ROOT` to:

```bash
export PROJECT_ROOT="/mnt/c/Projects/stt"
```

Add this line to your `~/.bashrc` (or the equivalent for your shell) **above** the `s()` function.

> **Performance tip:** For best I/O performance, keep the project files inside the WSL filesystem (e.g. `~/projects/stt`) rather than on `/mnt/c/...`. Cross-filesystem access between WSL and Windows is significantly slower.

### Python virtual environment inside WSL

Create and use a standard Linux virtual environment inside WSL:

```bash
cd "$PROJECT_ROOT"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The `PY_EXEC` path in the function (`$PROJECT_ROOT/.venv/bin/python3`) will work correctly as-is.

### Running `s` from Windows Terminal

[Windows Terminal](https://aka.ms/terminal) is the recommended way to use WSL on Windows. It supports multiple tabs, panes, and profiles for each WSL distribution. Install it from the Microsoft Store or via:

```powershell
winget install Microsoft.WindowsTerminal
```

Set your WSL distribution as the default profile in Windows Terminal settings for the most seamless experience.

### Docker and Kiwix inside WSL

The Kiwix helper script (`kiwix-docker-start-if-not-running.sh`) requires Docker. Install Docker Desktop for Windows and enable WSL 2 integration:

1. Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. In Docker Desktop → Settings → Resources → WSL Integration, enable your WSL distribution.
3. Verify inside WSL:
   ```bash
   docker --version
   ```

### Calling the WSL `s` function from Windows (optional)

If you want to invoke the `s` shortcut from a Windows CMD or PowerShell window without opening a WSL terminal, you can wrap it:

```powershell
# PowerShell wrapper
function s { wsl bash -i -c "s $args" }
```

```bat
:: CMD wrapper — save as s.bat on your PATH
@echo off
wsl bash -i -c "s %*"
```

> The `-i` flag loads an interactive shell so that your `~/.bashrc` (and the `s` function) is sourced automatically.

## Features

- **Full Linux compatibility**: All Unix tools (`timeout`, `pgrep`, `mktemp`, `grep`) work natively — no workarounds needed.
- **Dynamic Paths**: Automatically finds the project root via the `PROJECT_ROOT` variable set in your shell config.
- **Auto-Restart**: If the backend is down, it attempts to run `start_service` and local Wikipedia services (Docker must be running).
- **Smart Timeouts**: Tries a quick 2-second response first, then falls back to a 70-second deep processing mode.

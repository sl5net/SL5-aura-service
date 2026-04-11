# Intégration WSL (sous-système Windows pour Linux)

WSL vous permet d'exécuter un environnement Linux complet directement sur Windows. Une fois configurée, l'intégration du shell STT fonctionne **identiquement aux guides Linux Bash ou Zsh** — aucune adaptation spécifique à Windows n'est nécessaire pour la fonction shell elle-même.

> **Recommandé pour :** Les utilisateurs Windows qui sont à l'aise avec un terminal Linux ou qui ont déjà installé WSL pour les travaux de développement. WSL offre l’expérience la plus fidèle et le moins de compromis de compatibilité.

## Prérequis

### Installer WSL (installation unique)

Ouvrez PowerShell ou CMD **en tant qu'administrateur** et exécutez :

```powershell
wsl --install
```

Cela installe WSL2 avec Ubuntu par défaut. Redémarrez votre machine lorsque vous y êtes invité.

Pour installer une distribution spécifique :

```powershell
wsl --install -d Ubuntu-24.04
# or
wsl --install -d Debian
```

Répertoriez toutes les distributions disponibles :

```powershell
wsl --list --online
```

### Vérifiez votre version WSL

```powershell
wsl --list --verbose
```

Assurez-vous que la colonne « VERSION » affiche « 2 ». S'il affiche « 1 », effectuez la mise à niveau avec :

```powershell
wsl --set-version <DistroName> 2
```

## Intégration Shell dans WSL

Une fois WSL exécuté, ouvrez votre terminal Linux et suivez le **guide du shell Linux** pour votre shell préféré :

| Coquille | Guide |
|-------|-------|
| Bash (WSL par défaut) | [bash-integration.md](../../linux/bash-integration.i18n/bash-integration-frlang.md) |
| Zsh | [zsh-integration.md](../../linux/zsh-integration.i18n/zsh-integration-frlang.md) |
| Poisson | [fish-integration.md](../../linux/fish-integration.i18n/fish-integration-frlang.md) |
| Ksh | [ksh-integration.md](../../linux/ksh-integration.i18n/ksh-integration-frlang.md) |
| POSIX sh/Dash | [posix-sh-integration.md](../../linux/posix-sh-integration.i18n/posix-sh-integration-frlang.md) |

Pour la configuration par défaut d'Ubuntu/Debian WSL avec Bash, le chemin rapide est :

```bash
nano ~/.bashrc
# Paste the function block from bash-integration.md
source ~/.bashrc
```

## Considérations spécifiques à WSL

### Accéder aux fichiers Windows depuis WSL

Vos lecteurs Windows sont montés sous `/mnt/` :

```bash
/mnt/c/   # → C:\
/mnt/d/   # → D:\
```

Si votre projet réside sur le système de fichiers Windows (par exemple `C:\Projects\stt`), définissez `PROJECT_ROOT` sur :

```bash
export PROJECT_ROOT="/mnt/c/Projects/stt"
```

Ajoutez cette ligne à votre `~/.bashrc` (ou l'équivalent pour votre shell) **au-dessus** de la fonction `s()`.

> **Conseil de performances :** Pour de meilleures performances d'E/S, conservez les fichiers de projet dans le système de fichiers WSL (par exemple `~/projects/stt`) plutôt que sur `/mnt/c/...`. L'accès entre systèmes de fichiers entre WSL et Windows est nettement plus lent.

### Environnement virtuel Python dans WSL

Créez et utilisez un environnement virtuel Linux standard dans WSL :

```bash
cd "$PROJECT_ROOT"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Le chemin `PY_EXEC` dans la fonction (`$PROJECT_ROOT/.venv/bin/python3`) fonctionnera correctement tel quel.

### Exécuter `s` depuis le terminal Windows

[Windows Terminal](https://aka.ms/terminal) est la méthode recommandée pour utiliser WSL sous Windows. Il prend en charge plusieurs onglets, volets et profils pour chaque distribution WSL. Installez-le depuis le Microsoft Store ou via :

```powershell
winget install Microsoft.WindowsTerminal
```

Définissez votre distribution WSL comme profil par défaut dans les paramètres du terminal Windows pour l'expérience la plus transparente.

### Docker et Kiwix dans WSL

Le script d'assistance Kiwix (`kiwix-docker-start-if-not-running.sh`) nécessite Docker. Installez Docker Desktop pour Windows et activez l'intégration WSL 2 :

1. Téléchargez et installez [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. Dans Docker Desktop → Paramètres → Ressources → Intégration WSL, activez votre distribution WSL.
3. Vérifiez dans WSL :
   ```bash
   docker --version
   ```

### Appel de la fonction `s` WSL depuis Windows (facultatif)

Si vous souhaitez appeler le raccourci « s » à partir d'une fenêtre Windows CMD ou PowerShell sans ouvrir de terminal WSL, vous pouvez l'encapsuler :

```powershell
# PowerShell wrapper
function s { wsl bash -i -c "s $args" }
```

```bat
:: CMD wrapper — save as s.bat on your PATH
@echo off
wsl bash -i -c "s %*"
```

> L'indicateur `-i` charge un shell interactif afin que votre `~/.bashrc` (et la fonction `s`) soit automatiquement généré.

## Caractéristiques

- **Compatibilité totale avec Linux** : tous les outils Unix (`timeout`, `pgrep`, `mktemp`, `grep`) fonctionnent de manière native — aucune solution de contournement n'est nécessaire.
- **Chemins dynamiques** : recherche automatiquement la racine du projet via la variable `PROJECT_ROOT` définie dans la configuration de votre shell.
- **Auto-Restart** : si le backend est en panne, il tente d'exécuter `start_service` et les services Wikipédia locaux (Docker doit être en cours d'exécution).
- **Smart Timeouts** : essaie d'abord une réponse rapide de 2 secondes, puis revient à un mode de traitement approfondi de 70 secondes.
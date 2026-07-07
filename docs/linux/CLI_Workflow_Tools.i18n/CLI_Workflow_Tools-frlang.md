# Guide d'installation des outils de flux de travail CLI

Certaines actions du plug-in Path Navigator reposent sur des utilitaires de ligne de commande externes pour effectuer des recherches floues, répertorier les fichiers et manipuler le presse-papiers. Si ces outils sont manquants, vous verrez un avertissement dans la console système.

Vous trouverez ci-dessous les instructions d'installation pour chaque système d'exploitation pris en charge.

## Utilitaires requis

* **`fzf`** : Recherche floue en ligne de commande à usage général.
* **`find`** (ou `fd`) : utilitaire standard de recherche de fichiers.
* **Outil Presse-papiers** : utilisé pour diriger la sortie directement vers le presse-papiers de votre système.
* **Linux :** `xclip` (nécessite un environnement X11).
* **macOS :** `pbcopy` (préinstallé).
* **Windows :** `clip` (préinstallé).
* **`file`** : Détermine les types de fichiers pour les aperçus complets du terminal.

---

##Instructions d'installation

### 1. Linux (Arch/Manjaro)
Puisque votre système fonctionne sur Manjaro, vous pouvez installer les packages requis en utilisant `pacman` :

```bash
sudo pacman -S fzf findutils xclip file
```

### 2. Linux (Debian/Ubuntu/Mint)


```bash
sudo apt update
sudo apt install fzf findutils xclip file
```

### 3. macOS
Utilisez le gestionnaire de packages [Homebrew](https://brew.sh/) pour installer les outils manquants :

```bash
brew install fzf findutils
# Note: 'pbcopy' and 'file' are native on macOS.
```

### 4. Fenêtres
Si vous utilisez Windows, nous vous recommandons d'installer `fzf` via [Scoop](https://scoop.sh/) ou [Winget](https://github.com/microsoft/winget-cli) :

```powershell
# Using Winget
winget install junegunn.fzf

# Using Scoop
scoop install fzf
```
__CODE_BLOCK_4__
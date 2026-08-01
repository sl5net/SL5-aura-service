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



## 1. Sélection rapide de fichiers (commande Aura)

L'action `path_navigator` utilise la commande `fzf` compatible Git suivante. Son objectif est d'afficher un chemin de fichier directement dans le presse-papiers du système.

**Logique de commande :**
- Utilise `git ls-files` dans un référentiel Git (exclut les fichiers ignorés).
- Revient à « trouver ». -type f` en dehors d'un référentiel Git.
- Affiche le chemin sélectionné dans le presse-papiers à l'aide de `xclip -selection clipboard`.

## 2. Exécution rapide des fichiers (la fonction 'k')

Pour compléter la boucle, la fonction shell personnalisée « k » est utilisée. Cette fonction prend le chemin du presse-papiers et ouvre instantanément le fichier dans `kate`.

### Mise en œuvre

Ajoutez la fonction suivante au fichier de configuration de votre shell (par exemple, `~/.bashrc`, `~/.zshrc`) :

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

### Utilisation

1. Utilisez la commande `path_navigator` (par exemple, tapez `search file` dans votre outil de déclenchement).
2. Recherchez et sélectionnez le fichier souhaité (par exemple, `src/main/config.py`).
3. Dans votre terminal, tapez « k » et appuyez sur **ENTER**.
4. Le fichier s'ouvre instantanément dans Kate.
__CODE_BLOCK_2__
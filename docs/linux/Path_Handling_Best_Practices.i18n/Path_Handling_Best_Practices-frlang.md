# Répertoire personnel et gestion des chemins multiplateformes

Aura est conçu pour fonctionner sur plusieurs systèmes d'exploitation. Pour garantir que les commandes de navigation du système de fichiers fonctionnent, que vous utilisiez Linux, macOS ou Windows, les chaînes de chemin sont analysées dynamiquement avant d'être enregistrées dans les cartes floues actives.

---

## Logique de normalisation du chemin (`FUZZY_MAP_pre.py`)

La logique de mappage de chemin dynamique s'appuie sur les pratiques standard suivantes :

### 1. Réduction des tildes (POSIX)
Sur les systèmes compatibles POSIX (Linux et macOS), les chemins absolus correspondant au répertoire personnel de l'utilisateur (par exemple, `/home/username/`) sont convertis en chemins relatifs `~` au démarrage. Cela permet de réduire la longueur des chaînes et de rendre les règles générées portables entre différents utilisateurs sur le même système d'exploitation :

```python
# Replaces '/home/username/projects' with '~/projects'
if sys.platform != 'win32' and project_root_str_full.startswith(home_dir_str):
    PROJECT_ROOT_FOR_MAP = project_root_str_full.replace(home_dir_str, '~', 1)
```

### 2. Préservation du chemin absolu (Windows)
Windows n'évalue pas de manière fiable le caractère « ~ » dans les environnements d'invite de commande standard (`cmd.exe`) ou PowerShell. Par conséquent, lorsque le plugin détecte un environnement Windows (`sys.platform == 'win32'`), il préserve le chemin absolu complet (par exemple, `C:\Users\username\...`) pour garantir que l'exécution de la commande n'échoue pas.

### 3. Normalisation des barres obliques (`as_posix()`)
Aura utilise des barres obliques de style POSIX (`/`) en interne pour les cartes de configuration. Le script normalise tous les séparateurs de chemin dépendant du système d'exploitation en utilisant la méthode `pathlib.Path.as_posix()` de Python, qui nettoie automatiquement les barres obliques inverses (`\`) dans les environnements Windows.
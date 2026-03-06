# PLEINS FEUX SUR LES FONCTIONS : Chargement sécurisé de cartes privées et emballage automatique

Ce document décrit l'architecture de gestion des plugins de carte sensibles (par exemple, données client, commandes propriétaires) de manière à permettre l'**édition en direct** tout en appliquant les **meilleures pratiques de sécurité** pour éviter toute exposition accidentelle de Git.

---

## 1. Le concept : la sécurité « Matriochka »

Pour garantir une confidentialité maximale lors de l'utilisation d'outils standard, Aura utilise une stratégie d'imbrication **Matryoshka (Poupée russe)** pour les archives cryptées.

1. **Couche externe :** Un fichier ZIP standard crypté avec **AES-256** (via la commande système `zip`).
* *Apparence :* Contient un seul **un** fichier nommé `aura_secure.blob`.
* *Avantage :* Masque les noms de fichiers et la structure des répertoires aux regards indiscrets.
2. **Couche interne (The Blob) :** Un conteneur ZIP non chiffré à l'intérieur du blob.
* *Contenu :* La structure réelle des répertoires et les fichiers Python.
3. **État de fonctionnement :** Une fois déverrouillés, les fichiers sont extraits dans un dossier temporaire préfixé par un trait de soulignement (par exemple, « _private »).
* *Sécurité :* Ce dossier est strictement ignoré par `.gitignore`.

---

## 2. Flux de travail technique

### A. La barrière de sécurité (démarrage)
Avant de déballer quoi que ce soit, Aura vérifie dans `scripts/py/func/map_reloader.py` les règles `.gitignore` spécifiques.
* **Règle 1 :** `config/maps/**/.*` (Protège les fichiers clés)
* **Règle 2 :** `config/maps/**/_*` (Protège les répertoires de travail)
Si ceux-ci sont manquants, le système **abandonne**.

### B. Déballage (piloté par exception)
1. L'utilisateur crée un fichier de clé (par exemple, « .auth_key.py ») contenant le mot de passe (en texte brut ou en commentaires).
2. Aura détecte ce fichier et le ZIP correspondant (par exemple, « private.zip »).
3. Aura déchiffre le ZIP externe à l'aide de la clé.
4. Aura détecte le « aura_secure.blob », extrait la couche interne et déplace les fichiers vers le répertoire de travail « _private ».

### C. Édition en direct et emballage automatique (The Cycle)
C'est là que le système devient « auto-guérissant » :

1. **Modifier :** Vous modifiez un fichier dans `_private/` et l'enregistrez.
2. **Déclencheur :** Aura détecte le changement et recharge le module.
3. **Lifecycle Hook :** Le module déclenche sa fonction `on_reload()`.
4. **SecurePacker :** Un script (`secure_packer.py`) à la racine du dossier privé exécute :
* Il crée le ZIP interne (structure).
* Il le renomme en `.blob`.
* Il appelle la commande système `zip` pour le chiffrer dans l'archive externe en utilisant le mot de passe du fichier `.key`.

**Résultat :** Votre `private.zip` est toujours à jour avec vos dernières modifications, mais Git ne voit que la modification du fichier ZIP binaire.

---

## 3. Guide de configuration

### Étape 1 : Structure des répertoires
Créez une structure de dossiers comme celle-ci :
```text
config/maps/private/
├── .auth_key.py          # Contains your password (e.g. # MySecretPass)
└── private_maps.zip      # The encrypted archive
```

### Étape 2 : Le fichier de clé (`.auth_key.py`)
Doit commencer par un point.
```python
# MySecretPassword123
# This file is ignored by Git.
```

### Étape 3 : Le script Packer (`secure_packer.py`)
Placez ce script dans votre dossier de carte privé (avant de le compresser initialement). Il gère la logique de chiffrement. assurez-vous que vos cartes appellent ce script via le hook `on_reload`.

### Étape 4 : implémentation du hook
Dans vos fichiers map (`.py`), ajoutez ce hook pour déclencher la sauvegarde à chaque sauvegarde :

```python
# In your private map file
def on_reload():
    # Logic to find and execute secure_packer.py
    # ... (See Developer Guide for snippet)
```

---

## 4. Statut et sécurité de Git

Lorsqu'il est correctement configuré, `git status` affichera **uniquement** :
```text
modified:   config/maps/private/private_maps.zip
```
Le dossier `_private_maps` et le fichier `.auth_key.py` ne sont jamais suivis.
```

---

### 2. Neu: `docs/Developer_Guide/Lifecycle_Hooks.md`

Wir sollten einen Ordner `Developer_Guide` (oder ähnlich) anlegen, um technische Details von allgemeinen Features zu trennen.

```markdown
# Guide du développeur : Hooks du cycle de vie des plugins

Aura SL5 permet aux plugins (Maps) de définir des "Hooks" spécifiques qui s'exécutent automatiquement lorsque l'état du module change. Ceci est essentiel pour les flux de travail avancés tels que le système **Secure Private Map**.

## Le hook `on_reload()`

La fonction `on_reload()` est une fonction facultative que vous pouvez définir dans n'importe quel module Map.

### Comportement
* **Trigger :** Exécuté immédiatement après le **rechargement à chaud** réussi d'un module (modification de fichier + déclencheur vocal).
* **Contexte :** S'exécute dans le thread principal de l'application.
* **Sécurité :** Enveloppé dans un bloc `try/sauf`. Les erreurs ici seront enregistrées mais ne feront **pas planter** l'application.

### Modèle d'utilisation : la « daisy chain »
Pour les packages complexes (comme Private Maps), vous avez souvent de nombreux sous-fichiers, mais un seul script central (`secure_packer.py`) doit gérer la logique.

Vous pouvez utiliser le hook pour déléguer la tâche vers le haut :

```python
# Example: Delegating logic to a parent script
import importlib.util
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def on_reload():
    """
    Searches for 'secure_packer.py' in parent directories and executes it.
    """
    logger.info("🔄 Map modified. Triggering packer...")
    
    current_path = Path(__file__).resolve()
    search_dir = current_path.parent
    packer_script = None

    # Search upwards (max 4 levels)
    for _ in range(4):
        candidate = search_dir / "secure_packer.py"
        if candidate.exists():
            packer_script = candidate
            break
        if search_dir.name in ["maps", "config"]: break
        search_dir = search_dir.parent

    if packer_script:
        try:
            # Dynamic Import & Execution
            spec = importlib.util.spec_from_file_location("packer_dyn", packer_script)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'on_reload'):
                module.on_reload()
        except Exception as e:
            logger.error(f"❌ Failed to run packer: {e}")
```

### Bonnes pratiques
1. **Faites vite :** N'exécutez pas de longues tâches de blocage (comme des téléchargements volumineux) dans le hook principal. Utilisez des fils si nécessaire.
2. **Idempotence :** Assurez-vous que votre hook peut s'exécuter plusieurs fois sans casser des éléments (par exemple, n'ajoutez pas indéfiniment à un fichier, réécrivez-le à la place).
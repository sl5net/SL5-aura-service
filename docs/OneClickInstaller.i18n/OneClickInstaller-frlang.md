# Programme d'installation en 1 clic (installation zéro)

Obtenez **Aura** opérationnel sur votre ordinateur en un seul clic. Aucune connaissance en programmation, commandes de terminal ou configuration manuelle de Python n'est requise.

---

## Zéro prérequis

Vous n'avez **pas** besoin :
- Python pré-installé
- Dépôts Git ou code
- Expérience en ligne de commande ou en terminal

---

## Démarrage rapide

### Méthode 1 : Web One-Liner (le plus rapide et recommandé pour Linux / macOS)
Économise environ 30 secondes de gestion manuelle des fichiers et démarre immédiatement dans votre terminal :

**Linux et macOS :**

```bash
curl -sSL https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.sh | bash
```

**Windows (PowerShell) :**
```bash

# In development - please use Method 2 (standalone binary) for Windows

irm https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.ps1 | iex
```

Méthode 2 : binaire autonome (clic Windows et bureau)

### 2.1 Téléchargez le programme d'installation
Téléchargez le fichier d'installation unique correspondant à votre système d'exploitation à partir de la [dernière version de GitHub] :

- **Windows :** [aura-installer-windows.exe](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-windows.exe.zip)
- **Linux :** [aura-installer-linux](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-linux)
- **macOS :** [aura-installer-macos](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-macos)


### 2.2. Exécutez le programme d'installation

renommer aura-installer-windows.exe.zip en aura-installer-windows.exe

Double-cliquez sur le fichier téléchargé. Une fenêtre de configuration apparaîtra et préparera automatiquement l'environnement.

### 2.3. Commencez à dicter
Une fois terminé, Aura crée un raccourci sur le bureau et commence immédiatement à écouter.

---

## Que se passe-t-il automatiquement ?

Lorsque vous exécutez le programme d'installation, Aura automatiquement :
- Configure le moteur de reconnaissance vocale local et privé.
- Télécharge les modèles vocaux par défaut.
- Configure tous les raccourcis système et lanceurs de bureau nécessaires.

---

## Détails et exigences d'installation

- **Durée de l'installation :** Environ 2 à 3 minutes.
- **Espace disque requis :** Minimum ~1,5 Go (jusqu'à 2,5 Go selon les modèles de langue sélectionnés).
- **Répertoire d'installation :**
- **Linux et macOS :** `~/opt/sl5-aura-service`
- **Windows :** `%LOCALAPPDATA%\sl5-aura-service`

---

## Prochaines étapes

- **Grandma-Mode :** Tapez un seul mot dans votre fichier de règles et regardez Aura créer automatiquement des règles.
- **Apprenez avec Koans :** Explorez les concepts étape par étape dans [Getting Started](../GettingStarted.i18n/GettingStarted-frlang.md).
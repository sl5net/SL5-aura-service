> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../OneClickInstaller.md).*

# Installateur en 1-Clic (Zéro-Configuration)

Mettez **Aura** en marche sur votre machine en un seul clic. Aucune connaissance en programmation, commande terminal ou configuration manuelle de Python n'est requise.

---

## Zéro Prérequis

Vous n'avez **pas** besoin de :
- Python préinstallé
- Git ou dépôts de code
- Expérience en ligne de commande ou terminal

---

## Démarrage rapide

### Méthode 1 : Commande Web en une ligne (Plus rapide et recommandé pour Linux / macOS)
Économise ~30 secondes de manipulation manuelle de fichiers et démarre immédiatement dans votre terminal :

**Linux et macOS :**
#### CodeBerg Web en une ligne
```bash
curl -sSL https://codeberg.org/sl5net/SL5-aura-service/raw/branch/master/web_install.sh | bash
```
ou
#### Ligne unique Web GitHub
```bash
curl -sSL https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.sh | bash
```

**Windows (PowerShell) :**
#### CodeBerg Web en une ligne

```bash
irm https://codeberg.org/sl5net/SL5-aura-service/raw/branch/master/web_install.sh | iex
```
ou
#### Ligne unique Web github
```bash
irm https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.ps1 | iex
```

Méthode 2 : Binaire autonome (Windows et clic sur le bureau)

### 2.1 Télécharger l'installateur
Téléchargez le fichier d'installation unique correspondant à votre système d'exploitation depuis la [Dernière version GitHub] :

- **Windows :** [aura-installer-windows.exe](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-windows.exe.zip)
- **Linux :** [aura-installer-linux](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-linux)
- **macOS :** [aura-installer-macos](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-macos)


### 2.2. Exécuter l'installateur

renommer aura-installer-windows.exe.zip en aura-installer-windows.exe

Double-cliquez sur le fichier téléchargé. Une fenêtre d'installation apparaîtra et préparera automatiquement l'environnement.

### 2.3. Commencer à dicter
Une fois terminé, Aura crée un raccourci sur le bureau et commence à écouter immédiatement.

---

## Que se passe-t-il automatiquement ?

Lorsque vous exécutez l'installateur, Aura fait automatiquement :
- Configure le moteur de reconnaissance vocale local et privé.
- Télécharge les modèles de voix par défaut.
- Configure tous les raccourcis système et les lanceurs de bureau nécessaires.

---

## Détails et exigences d'installation

- **Durée d'installation :** Environ 2 à 3 minutes.
- **Espace disque requis :** Minimum ~1,5 Go (jusqu'à 2,5 Go selon les modèles de langage sélectionnés).
- **Répertoire d'installation :**
  - **Linux & macOS :** `~/opt/sl5-aura-service`
  - **Windows :** `%LOCALAPPDATA%\sl5-aura-service`

---

## Étapes suivantes

- **Mode Grand-mère :** Tapez un seul mot dans votre fichier de règles et regardez Aura créer automatiquement des règles.
- **Apprenez avec des koans :** Explorez les concepts étape par étape dans [Getting Started](../GettingStarted.i18n/GettingStarted-frlang.md).

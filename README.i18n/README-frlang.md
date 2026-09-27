> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../README.md).*

<img src="data/image/logo.svg" align="right" width="150" alt="⬟ SL5 Aura Logo"> 

# ⬟ SL5 Aura – Votre voix. Vos règles

<!-- Stack Overflow & Community Badges -->
[![Stack Overflow](https://img.shields.io/badge/Stack_Overflow-536k+_Reached-F48024?style=for-the-badge&logo=stackoverflow&logoColor=white)](https://stackoverflow.com/users/2891692/sl5net)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Privacy](https://img.shields.io/badge/Privacy-100%25_Local_%26_Offline-2ea44f?style=for-the-badge&logo=keepassxc&logoColor=white)](#)
[![Latency](https://img.shields.io/badge/Latency-0.07s-blueviolet?style=for-the-badge&logo=speedtest&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> Cadre d'assistant vocal 100 % hors ligne, axé sur la confidentialité.  
> Définissez exactement ce que fait votre voix — à partir d’un seul mot  
> jusqu'à des scripts Python complets. Pas de cloud. Aucune donnée ne quitte votre machine.  
> Fonctionne dans le terminal, le navigateur ou en tant que service en arrière-plan — sur Linux, macOS et Windows.

| 👵 Débutant | 🎓 Apprenant | 🧑‍💻 Développeur |
|---|---|---|
| [grandma-mode](../docs/GettingStarted.i18n/GettingStarted-frlang.md#the-oma-modus-beginner-shortcut) : il suffit d'écrire un mot, Aura fait le reste | Apprenez avec des Koans — un concept à la fois | Script complet en Python, plugins, appels d'API |
| 🗄️ Gestion d'État | Trino + orchestration Airflow, fzf, CopyQ, commandes vocales/terminal, interfaces utilisateur de navigateur |

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)

⚡ **~2,87 J** par test (39 tests sans LanguageTool sur >800 cartes @ 0,07 s chaud / 0,36 s froid 🌿 mesuré avec [Eco-CI](https://metrics.green-coding.io/index.html)) · pas de calcul en cloud

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)

⚡ **Suite de tests complète :** 94 tests avec LanguageTool sur plus de 800 cartes @ 0,07 s à chaud / 0,46 s à froid · sans calcul en nuage

<details>
<summary>Démarrage rapide</summary>

## Démarrage rapide

### Option A : Installation en 1 clic et via le Web (Recommandé)

Commande en une ligne ou installateur autonome pour Linux, macOS et Windows :
- **[→ Installer Guide & Direct Downloads](../docs/OneClickInstaller.i18n/OneClickInstaller-frlang.md)**

---

Option B : Installation manuelle (Développeurs / Git)

1. Télécharger ou cloner ce dépôt
2. Exécutez le script d'installation de votre système d'exploitation (voir dossier `setup/`):
   - Linux (Archive/Manjaro): `bash setup/manjaro_arch_setup.sh`
   - Linux (Ubuntu/Debian): `bash setup/ubuntu_setup.sh`
   - Linux (openSUSE): `bash setup/suse_setup.sh`
   - Linux (NixOS): `nix-shell setup/shell.nix` puis `bash setup/nixos_setup.sh`
   ===> Expérimental — non testé par les auteurs, accueil de retour!   
   - MACOS: `bash setup/macos_setup.sh`
   - Windows: `setup/windows11_setup_with_ahk_copyq.bat`
3. Démarrer Aura: `./scripts/restart_venv_and_run-server.sh`
4. Appuyez sur votre touche et parlez — **[full guide →](../docs/GettingStarted.i18n/GettingStarted-frlang.md) * *

---

### Désinstallation
Pour supprimer les services de fond SL5 Aura, les entrées de démarrage automatique et les environnements virtuels :
- **Linux / macOS:** `bash setup/uninstall.sh`
- **Windows (PowerShell):** `powershell -File setup/uninstall.ps1`
*(Vos règles personnalisées dans `config/maps/` sont sécurisées par défaut sauf si vous spécifiez `--purge`). *

---


Exigences du système et compatibilité * *

*   **Windows:** ☐ Entièrement pris en charge (utilise AutoHotkey/PowerShell).
*   **macOS:** -Entièrement pris en charge (utilise AppleScript).
*   **Linux (X11/Xorg):** Entièrement pris en charge.
*   **Linux (Wayland):** Entièrement pris en charge (essai sur KDE Plasma 6 / Wayland).
*   **Linux (CachyOS / Arch-based launning release):** Entièrement pris en charge.
    Nécessite mimalloc (`sudo pacman -S mimalloc`) en raison de la compatibilité glibc 2.43.
*   **Linux (NixOS) :** - Expérimental — configuration communautaire, pas encore testée.
    Si vous essayez, s'il vous plaît ouvrir un problème ou PR avec vos conclusions!    
*   **Linux (Manjaro):** Nouveau : Un hotkey à l'échelle du système ouvre une interface fzf à clavier pour que vous puissiez exécuter les commandes Aura n'importe où sur le bureau (découplé complètement de la fenêtre active). Ce lanceur piloté par hotkey est actuellement mis en œuvre et testé sur Linux (Manjaro); D'autres distributions peuvent fonctionner mais nécessitent la configuration. Voir dans la rubrique [docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.md](../docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.i18n/CopyQ_Shortcut_Super_s-frlang.md)    


    
SL5 Aura est une assistante vocale complète **offline** basée sur **Vosk** (pour la parole au texte) et **LanguageTool** (pour Grammar/Style), avec une option **Local LLM (Ollama) Fallback** pour des réponses créatives et des correspondances floues avancées. Il transforme votre voix en actions et textes précis, conçus pour une personnalisation ultime grâce à un système de règles rechargeables et à un moteur de script dynamique.
    
Traductions: Ce document existe également dans [other languages](https://github.com/sl5net/SL5-aura-service/tree/master/README.i18n).


Note: De nombreux textes sont des traductions générées par machine de la documentation originale en anglais et sont destinés à des conseils généraux seulement. En cas de divergences ou d'ambiguïtés, la version anglaise prévaut toujours. Nous accueillons l'aide de la communauté pour améliorer cette traduction!

</details>

<details>
<summary>Démo</summary>

### 📺 Démonstration du terminal 

[![Terminal Demo](https://github.com/sl5net/SL5-aura-service/raw/master/data/demo_fast.gif)](https://github.com/sl5net/SL5-aura-service/blob/master/data/demo_fast.gif)

> **Conseil :** Pour une meilleure expérience du terminal, consultez [Zsh Integration](../docs/linux/zsh-integration.i18n/zsh-integration-frlang.md).

### 🎥 Tutoriel vidéo
[![SL5 Aura: HowTo crash SL5 Aura?](https://img.youtube.com/vi/BZCHonTqwUw/0.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)

*(Lien alternatif : [skipvids.com](https://skipvids.com/?v=BZCHonTqwUw))*

</details>

<details>
<summary>Caractéristiques principales</summary>

Caractéristiques principales

*   **Offline & Privé:** 100% local. Aucune donnée ne quitte jamais votre machine.
*   ** Moteur de script dynamique :** Allez au-delà du remplacement de texte. Les règles peuvent exécuter des scripts Python personnalisés (`on_match_exec`) pour effectuer des actions avancées comme appeler des API (par exemple, rechercher Wikipédia), interagir avec des fichiers (par exemple, gérer une liste de tâches), ou générer du contenu dynamique (par exemple, un message de messagerie contextuel).
*   **Règles relatives au contenu :** Limiter les règles aux applications spécifiques. En utilisant `only_in_windows`, vous pouvez vous assurer qu'une règle ne déclenche que si un titre de fenêtre spécifique (par exemple, « Terminal », « VS Code » ou « Browser ») est actif. Cela fonctionne multiplateforme (Linux, Windows, macOS).
*  ** Moteur de transformation à haut contrôle :** Implémente un pipeline de traitement hautement personnalisable, piloté par la configuration. La priorité des règles, la détection des commandes et les transformations de texte sont déterminées uniquement par l'ordre séquentiel des règles de la Fuzzy Maps, nécessitant une configuration ** et non un codage**.
*   **Utilisation de la RAM conservatrice :** Gestion intelligente de la mémoire, précharger les modèles seulement si suffisamment de RAM libre est disponible, assurant d'autres applications (comme vos jeux PC) ont toujours la priorité.
*   **Plateforme de choc:** Fonctionne sur Linux, macOS et Windows.
*   **Entièrement automatisé:** Gère son propre serveur LanguageTool (mais vous pouvez aussi utiliser un serveur externe).
*   **Blazing Fast:** La mise en cache intelligente assure des notifications instantanées et un traitement rapide.
*   ** Gestion dynamique de l'État par Trino :** Moteur de configuration de l ' interface
    sépare les paramètres pour `speech`, `terminal` et `web` — changer un sans
    Affecter les autres. Comprend un tableau de bord administratif** en temps réel (port 8084).
</details>

<details>
<summary>Intégrations prêtes à l'emploi</summary>
    
## 🔌 Intégrations prêtes à l'emploi

SL5-Aura est livré avec un vaste écosystème de plus de **100+ plugins préconfigurés**. Voici quelques points forts :

Commande vocale OculiX / SikuliX IDE
SL5-Aura fournit une prise en charge vocale de première classe pour l'IDE **OculiX** et **SikuliX**. Cette intégration vous permet de « parler » votre code d'automatisation.

*   **Voix à extrait:** Dites "cliquez", "attendre" ou "trouver tout", et le service tape instantanément le code Python correct (par exemple `click("image.png")`) dans l'IDE.
*   **Window-Aware:** Le plugin est sensible au contexte ; il ne s'active que lorsque la fenêtre OculiX/SikuliX est focalisée.
*   **Smart English Support:** Optimisé pour `en-US` avec un accent particulier sur les accents non indigènes (par exemple, la phonétique germano-anglaise), assurant une grande précision de reconnaissance pour la communauté mondiale.
*   **Extensible :** Utilise le format `FUZZY_MAP_pre.py` facile à éditer.

> ** État :** Reconnu comme un plugin communautaire par l'équipe OculiX (voir [Issue #204](https://github.com/oculix-org/Oculix/issues/204)).

### Contrôle vocal de l'IDE LibreOffice

### 0 A.D. Contrôle vocal

---

</details>


<details>
<summary>Documentation</summary>

Documentation

🔍 [Interactive Search (Algolia)](https://sl5net.github.io/SL5-aura-service/search_online.html?lang=en)

Pour une référence technique complète, incluant tous les modules et scripts, veuillez consulter notre page de documentation officielle. Il est généré automatiquement et toujours à jour.

👉 [**Go to Documentation sl5net.github.io/SL5-aura-service**](https://sl5net.github.io/SL5-aura-service/)

Pleins feux
- [Interactive Rule Search & Run](../docs/Feature_Spotlight/Interactive_Rule_Search_and_Run.i18n/Interactive_Rule_Search_and_Run-frlang.md) — Recherche de règles `fzf` à double panneau, prévisualisations en direct du contexte, exécution instantanée de la commande via `Enter`/`Ctrl+R` et intégration de l'éditeur via `Ctrl+E`. Prise en charge par un hotkey global (`Super+S`) et plusieurs environnements de recherche dédiés préconfigurés par des commandes vocales.

Statut de construction

[![Linux Manjaro](https://github.com/sl5net/SL5-aura-service/actions/workflows/manjaro_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/manjaro_setup.yml)
[![Linux Ubuntu](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml)
[![Linux Suse](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml)

[![macOS](https://github.com/sl5net/SL5-aura-service/actions/workflows/mac_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml)
[![Windows 11](https://github.com/sl5net/SL5-aura-service/actions/workflows/win11_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml)

[![OculiX Compatible](https://img.shields.io/badge/OculiX-Compatible-blueviolet?style=for-the-badge&logo=python)](https://github.com/oculix-org/Oculix)
<div align="left">
<a href="https://github.com/sl5net/SL5-aura-service/stargazers">
<img src="https://img.shields.io/github/stars/sl5net/SL5-aura-service?style=social" alt="Stargazers">
</a>
<img src="https://img.shields.io/github/license/sl5net/SL5-aura-service" alt="License">
<a href="https://sl5net.github.io/SL5-aura-service/">
<img src="https://img.shields.io/badge/documentation-live-brightgreen" alt="Documentation">
</a>
</div>

</details>

Lisez ceci dans d'autres langues:

[🇬🇧 English](../README.md) | [🇸🇦 العربية](../README.i18n/README-arlang-frlang.md) | [🇩🇪 Deutsch](../README.i18n/README-delang-frlang.md) | [🇪🇸 Español](../README.i18n/README-eslang-frlang.md) | [🇫🇷 Français](../README.i18n/README-frlang.md) | [🇮🇳 हिन्दी](../README.i18n/README-hilang-frlang.md) | [🇯🇵 日本語](../README.i18n/README-jalang-frlang.md) | [🇰🇷 한국어](../README.i18n/README-kolang-frlang.md) | [🇵🇱 Polski](../README.i18n/README-pllang-frlang.md) | [🇵🇹 Português](../README.i18n/README-ptlang-frlang.md) | [🇧🇷 Português Brasil](../README.i18n/README-pt-BRlang-frlang.md) | [🇨🇳 简体中文](../README.i18n/README-zh-CNlang-frlang.md)

---

<details>
<summary>Installation</summary>

Installation

Installation rapide sans modération (Manjaro/Arch Video)
Regardez le processus de configuration complet de 6 minutes :
* **Télécharger : ~3 minutes
* **Setup & Premier départ:** ~3 minutes (y compris l'assistant de bienvenue)

👉 **[SL5 Aura Installation Live-Demo on YouTube](https://www.youtube.com/watch?v=29xiwIW1ZHQ)**


La configuration est un processus en deux étapes:
1.  Téléchargez la dernière version ou master ( https://github.com/sl5net/SL5-aura-service/archive/master.zip ) ou clonez ce dépôt sur votre ordinateur.
2.  Exécutez le script de configuration unique pour votre système d'exploitation.

Les scripts d'installation gèrent tout : dépendances système, environnement Python, et téléchargement des modèles et outils nécessaires (~4GB) directement depuis nos GitHub Releases pour une vitesse maximale.


Pour Linux, macOS et Windows (avec exclusion en option)

Pour économiser de l'espace disque et de la bande passante, vous pouvez exclure les modèles de langage spécifiques (`de`, `en`) ou tous les modèles optionnels (`all`) pendant la configuration. **Les composants de base (LangageTool, cover.176) sont toujours inclus. ****

Ouvrez un terminal dans le répertoire racine du projet et exécutez le script pour votre système :

```bash
# For Ubuntu/Debian, Manjaro/Arch, macOS, or other derivatives
# (Note: Use bash or sh to execute the setup script)

bash setup/{your-os}_setup.sh [OPTION]

# For Arch-based systems (Manjaro, CachyOS, EndeavourOS, etc.):
`bash setup/manjaro_arch_setup.sh`

```sudo pacman -S mimalloc```


# Examples:
# Install everything (Default):
# bash setup/manjaro_arch_setup.sh

# Exclude German models:
# bash setup/manjaro_arch_setup.sh exclude=de

# Exclude all VOSK language models:
# bash setup/manjaro_arch_setup.sh exclude=all

# For Windows in an Admin-Powershell session

setup/windows11_setup.ps1 -Exclude [OPTION]

# Examples:
# Install everything (Default):
# setup/windows11_setup.ps1

# Exclude English models:
# setup/windows11_setup.ps1 -Exclude "en"

# Exclude German and English models:
# setup/windows11_setup.ps1 -Exclude "de,en"

# Or (recommend) - Run the BAT file: 
windows11_setup.bat -Exclude "en"
```

#### Pour Windows
Exécutez le script de configuration avec les privilèges de l'administrateur.

**Installer un outil pour lire et exécuter, p.ex. [CopyQ](https://github.com/hluk/CopyQ) ou [AutoHotkey v2](https://www.autohotkey.com/)**. Ceci est nécessaire pour le text-typing watcher.

L'installation est entièrement automatisée et prend environ **8-10 minutes** lors de l'utilisation de 2 modèles sur un nouveau système.

1. Naviguez dans le dossier `setup`.
2. Double-cliquez sur **`windows11_setup_with_ahk_copyq.bat`**.
   * *Le script invite automatiquement pour les privilèges de l'administrateur. *
   * *Il installe le système de base, les modèles de langue, **AutoHotkey v2**, et **CopyQ**. *
3. Une fois l'installation terminée, **Aura Dictation** lancera automatiquement.

> **Note :** Vous n'avez pas besoin d'installer Python ou Git au préalable; Le script gère tout.

---

#### Installation avancée / personnalisée
Si vous préférez ne pas installer les outils client (AHK/CopyQ) ou si vous voulez économiser de l'espace disque en excluant des langues spécifiques, vous pouvez exécuter le script de base via la ligne de commande:

```powershell
# Core Setup only (No AHK, No CopyQ)
setup/windows11_setup_with_ahk_copyq.bat

# Exclude specific language models (saves space):
# Exclude English:
setup/windows11_setup_with_ahk_copyq.bat -Exclude "en"

# Exclude German and English:
setup/windows11_setup_with_ahk_copyq.bat -Exclude "de,en"
```

---
</details>


<details>
<summary>Utilisation</summary>

Utilisation

Commencez les services

Sur Linux et macOS
Un seul script gère tout. Il démarre le service de dictée principal et le moniteur de fichiers automatiquement dans l'arrière-plan.
```bash
# Run this from the project's root directory
./scripts/restart_venv_and_run-server.sh
```

Sous Windows
Le démarrage du service est un processus manuel en deux étapes *** :

1.  **Démarrer le service principal:** Exécuter `start_aura.bat`. ou commencer à partir de `.venv` le service avec `python3`

Configurez votre hotkey

Pour déclencher la dictée, vous avez besoin d'une touche d'écoute globale qui crée un fichier spécifique. Nous vous recommandons vivement l'outil multiplateforme [CopyQ](https://github.com/hluk/CopyQ).

Notre recommandation: CopyQ

Créez une nouvelle commande dans CopyQ avec un raccourci global.

**Commande pour Linux/macOS:**
```bash
touch /tmp/sl5_record.trigger
```

**Commande pour Windows lors de l'utilisation de [CopyQ](https://github.com/hluk/CopyQ): * *
```js
copyq:
var filePath = 'c:/tmp/sl5_record.trigger';

var f = File(filePath);

if (f.openAppend()) {
    f.close();
} else {
    popup(
        'error',
        'cant read or open:\n' + filePath
        + '\n' + f.errorString()
    );
}
```


**Commande pour Windows lors de l'utilisation de [AutoHotkey](https://AutoHotkey.com): * *
```sh
; trigger-hotkeys.ahk
; AutoHotkey v2 Skript
#SingleInstance Force ; Stellt sicher, dass nur eine Instanz des Skripts läuft

;===================================================================
; Hotkey zum Auslösen des Aura Triggers
; Drücke Strg + Alt + T, um die Trigger-Datei zu schreiben.
;===================================================================
f9::
f10::
f11::
{
    local TriggerFile := "c:\tmp\sl5_record.trigger"
    FileAppend("t", TriggerFile)
    ToolTip("Aura Trigger ausgelöst!")
    SetTimer(() => ToolTip(), -1500)
}
```


3e commence à dicter !
Cliquez dans n'importe quel champ de texte, appuyez sur votre hotkey, et une notification "Listening..." apparaîtra. Parlez clairement, puis arrêtez. Le texte corrigé sera tapé pour vous.

</details>

---


<details>
<summary>Configuration avancée (facultative)</summary>

Configuration avancée (facultative)

Vous pouvez personnaliser le comportement de l'application en créant un fichier de paramètres locaux.

1.  Naviguez dans le répertoire `config/`.
2.  Créez une copie de `config/settings_local.py_Example.txt` et renommez-la en `config/settings_local.py`.
3.  Modifier `config/settings_local.py` (il remplace tout paramètre du fichier principal `config/settings.py`).

Ce fichier `config/settings_local.py` est ignoré par Git par défaut, de sorte que vos modifications personnelles ne seront pas écrasées par des mises à jour.

Structure de connexion et logique

La modularité du système permet une extension robuste via les plugins/répertoires.

Le moteur de traitement adhère strictement à une chaîne prioritaire hiérarchique *** :

1. ** Commande de chargement des modules (haute priorité):** Les règles chargées à partir des paquets de langages de base (de-DE, en-US) ont priorité sur les règles chargées à partir des plugins/répertoires (qui chargent la dernière fois par ordre alphabétique).
    
2. **Arrêté en dossier (priorité micro) :** Dans un fichier de carte donné (FUZZY MAP pre.py), les règles sont traitées strictement par **numéro de ligne** (de haut en bas).
    

Cette architecture garantit la protection des règles du système de base, tandis que les règles spécifiques au projet ou aux contextes (comme celles des commandes CodeIgniter ou des jeux) peuvent être facilement ajoutées en tant qu'extensions de faible priorité via des plug-ins.

</details>

<details>
<summary>Scripts clés pour les utilisateurs de Windows</summary>






## Scripts clés pour les utilisateurs de Windows

Voici une liste des scripts les plus importants pour configurer, mettre à jour et exécuter l'application sur un système Windows.

### Configuration et mise à jour

*   `chmod +x update.sh; ./update.sh`
*   `setup/setup.bat` : Le script principal pour la **configuration initiale unique** de l'environnement.
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `Run powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"`

*   `update.bat` : Exécutez ceci depuis le dossier du projet pour **obtenir le code et les dépendances les plus récents**.

### Exécution de l'application
*   `start_aura.bat` : Un script principal pour **démarrer le service de dictée**.

### Scripts principaux et d'aide
*   `aura_engine.py` : Le service principal Python (généralement démarré par l’un des scripts ci-dessus).
*   `get_suggestions.py` : Un script d'assistance pour des fonctionnalités spécifiques.

</details>



Caractéristiques clés et compatibilité OS

<details>
<summary>Légende pour la compatibilité OS</summary>

Légende pour la compatibilité OS :  
*   **Linux** (par exemple, Arche, Ubuntu)  
    *   **macOS**  
*   **Windows * *  
*   **Android** (pour les fonctionnalités spécifiques au mobile)  

---

</details>



* * * * * * * * * *
    Notre moteur principal pour la reconnaissance de la parole hors ligne et le traitement audio.

    
<details>
<summary>Aura cœur</summary>

**Aura-Core/** 🐧 🍏 🪟  
├─ `aura_engine.py` (Service Python principal orchestrant Aura) 🐧 🍏 🪟  
├┬ **Live Hot-Reload** (Config & Maps) 🐧 🍏 🪟  
│├ **Assurer le chargement de la carte privée (Intégrité-Première)** 🔒  🐧 🍏 🪟  
││ * ** Flux de travail:** Charge les archives ZIP protégées par mot de passe.   
│├ ** Traitement et correction du texte/** groupés par langue (par exemple `de-DE`, `en-US`, ...)   
│├ 1. `normalize_punctuation.py` (standardise la ponctuation post-transcription) 🐧 🍏 🪟  
│├ 2. **Précorrection intelligente** (`FuzzyMap Pre` - [The Primary Command Layer](../docs/CreatingNewPluginModules.i18n/CreatingNewPluginModules-frlang.md)) 🐧 🍏 🪟  
││ * **Exécution de script dynamique: Les règles peuvent déclencher des scripts Python personnalisés (`on_match_exec`) pour effectuer des actions avancées comme les appels API, les E/S de fichiers ou générer des réponses dynamiques.  
││ * **Exécution en cascade:** Les règles sont traitées successivement et leurs effets sont **cumulatifs**. Des règles ultérieures s'appliquent au texte modifié par des règles antérieures.  
││ * **Critère d'arrêt prioritaire le plus élevé:** Si une règle atteint un ** Full Match** (^...$), l'ensemble du pipeline de traitement pour ce jeton s'arrête immédiatement. Ce mécanisme est essentiel à la mise en œuvre de commandes vocales fiables.  
│├ 3. `correct_text_by_languagetool.py` (Intégrates LanguageTool for Grammary/style correction) 🐧 🍏 🪟  
│├ **4. Moteur de règle hiérarchique RegEx avec Ollama AI Fallback * * 🐧 🍏 🪟  
││ * **Contrôle déterministe :** Utilise le moteur de règle RegEx pour une commande précise, hautement prioritaire et un contrôle texte.  
│├ * Plugin de recherche vectorielle** (chargement las) : active la recherche sémantique en connectant les ancrages vectoriaux locaux avec le calque de repli Ollama/LLM 🐧  
││ * **Ollama AI (LLM locale) Retour en arrière :** Fonctionne comme une vérification facultative et peu prioritaire pour les réponses créatives, les questions-réponses et les correspondances Fuzzy avancées** lorsqu'aucune règle déterministe n'est respectée.  
││ * **Situation:** Intégration locale des LLM.
│└ 5. **Intelligent post-corruption** (`FuzzyMap`)**– Raffinement post-LT * * 🐧 🍏 🪟  
││ * Appliquée après LanguageTool pour corriger les sorties spécifiques aux LT. Suivre la même logique de priorité en cascade que la couche de pré-correction.  
││ * *Exécution de script dynamique: Les règles peuvent déclencher des scripts Python personnalisés ([on_match_exec](../docs/advanced-scripting.i18n/advanced-scripting-frlang.md)) pour effectuer des actions avancées comme des appels API, des E/S de fichiers ou générer des réponses dynamiques.  
││ * **Futzy Fallback:** Le **Fuzzy Simility Check** (commandé par un seuil, par exemple, 85%) agit comme la couche de correction des erreurs la plus basse. Il n'est exécuté que si l'ensemble de la règle déterministe/cascading précédente n'a pas réussi à trouver une correspondance (la règle actuelle est fausse), optimisant les performances en évitant les vérifications lentes et floues chaque fois que possible.  
├┬ **Gestion des modèles/**   
│├─ `prioritize_model.py` (Optimise le chargement/déchargement du modèle en fonction de l'utilisation) 🐧 🍏 🪟  
│└─ `setup_initial_model.py` (Configure la configuration du modèle pour la première fois) 🐧 🍏 🪟  
├─ **VAD adaptive Délai * * 🐧 🍏 🪟  
├─ **Chef d'adaptation (démarrage/arrêt)** 🐧 🍏 🪟  
├─ ** Commutateur de langage instantané** (Experimental via le préchargement du modèle) 🐧 🍏         
├─ **Orchestration de flux d'air** (automatisation de flux de travail basée sur le DAG) 🐧 🍏 🪟
│   Nécessite Docker · UI: `http://localhost:8081` 🐧 🍏 🪟  
├─ **Trino State Engine** (configuration de l'interface par discours/terminal/web) 🐧 🍏 🪟
└─  Nécessite Docker · UI Admin: `http://localhost:8084` 🐧 🍏 🪟  

**Utilisations du système/**   
├┬ **Gestion des serveurs d'outils linguistiques/**   
│├─ `start_languagetool_server.py` (Initialise le serveur local LanguageTool) 🐧 🍏 🪟  
│└─ `stop_languagetool_server.py` (Frappe le serveur LanguageTool) 🐧 🍏 
├─ `monitor_mic.sh` (pour utilisation avec casque sans clavier et moniteur) 🐧 🍏 🪟  

### **Gestion des modèles et des paquets * *  
    Outils pour une manipulation robuste des grands modèles de langage.  

**Gestion des modèles/** 🐧 🍏 🪟  
├─ *Robust Model Downloader** (GitHub release chunks) 🐧 🍏 🪟  
├─ `split_and_hash.py` (Utilité pour les propriétaires de repo pour diviser les grands fichiers et générer des somme de contrôle) 🐧 🍏 🪟  
└─ `download_all_packages.py` (Outil pour les utilisateurs finaux pour télécharger, vérifier et réassembler des fichiers multi-parties) 🐧 🍏 🪟  

</details>


<details>
<summary>Aides au développement et au déploiement</summary>

### **Aides au développement et au déploiement * *  
    Scripts pour la configuration d'environnement, les essais et l'exécution de service.  

*Astuce : glogg vous permet d'utiliser des expressions régulières pour rechercher des événements intéressants dans vos fichiers journaux. *     
Veuillez cocher la case à cocher lors de l'installation pour vous associer aux fichiers journaux.    
https://globg.bonnefon.org/     
    
Astuce : Après avoir défini vos modèles régex, lancez `python3 tools/map_tagger.py` pour générer automatiquement des exemples de recherche pour les outils CLI. Voir [Map Maintenance Tools](../docs/Developer_Guide/Map_Maintenance_Tools.i18n/Map_Maintenance_Tools-frlang.md) pour plus de détails. *

Alors peut-être double-cliquez
`log/aura_engine.log`
    
**DevAide/**  
├┬ ** Gestion de l'environnement virtuel/**  
│├ `scripts/restart_venv_and_run-server.sh` (Linux/macOS) 🐧 🍏  
│└ `scripts/restart_venv_and_run-server.ahk` (Windows) 🪟  
├┬ ** Intégration de la dictation à l'échelle du système/*  
│├ Intégration de l'auditeur système Vosk 🐧 🍏 🪟  
│├ `scripts/monitor_mic.sh` (surveillance micro spécifique à Linux) 🐧  
│└ `scripts/type_watcher.ahk` (AutoHotkey écoute le texte reconnu et le tape à l'échelle du système) 🪟  
└─ **CI/CD Automation/**  
    └─ Flux de travail étendus GitHub (installation, test, déploiement de docs) - - - *(Runs sur les actions GitHub)*  

</details>

<details>
<summary>Caractéristiques expérimentales</summary>
    
Caractéristiques expérimentales  
    Caractéristiques en cours d'élaboration ou en projet.  

** Caractéristiques expérimentales/**  
├─ ** ENTRER APRÈS LA DISCRIMINATION REGEX** Exemple de règle d'activation "(ExempleAplicationThatNotExist)" 🐧  
├┬Greffons  
│**Live Lazy-Reload** (*) 🐧 🍏 🪟  
(*Les modifications apportées à l'activation/désactivation du plugin et à leurs configurations sont appliquées lors du prochain traitement sans redémarrage du service.*)  
│ ├ **Commandes de git* (Contrôle de la voix pour l'envoi des commandes git) 🐧 🍏 🪟  
│ ├ **wannweil** (Carte pour l'emplacement Allemagne-Wannweil) 🐧 🍏 🪟  
│ ├ ** Plugin de poker (Projet)** (Contrôle de la voix pour les applications de poker) 🐧 🍏 🪟  
│ └ **0 Plugin A.D. (Projet)** (Contrôle de la voix pour 0 jeu A.D.) 🐧   
├─ **Extrait sonore au début ou à la fin d'une session** (Description en attente) 🐧   
├─ **Speech Output pour déficient visuel** (Description en attente) 🐧 🍏 🪟  
└─ *SL5 Aura Android Prototype** (Pas encore complètement hors ligne) 📱  

---

*(Note: Des distributions Linux spécifiques comme Arch (ARL) ou Ubuntu (UBT) sont couvertes par le symbole général de Linux). Des distinctions détaillées pourraient être abordées dans les guides d'installation *.
</details>

<details>
<summary>Cliquez pour voir la commande utilisée pour générer cette liste de scripts</summary>

```bash
{ find . -maxdepth 1 -type f \( -name "aura_engine.py" -o -name "get_suggestions.py" \) ; find . -path "./.venv" -prune -o -path "./.env" -prune -o -path "./backup" -prune -o -path "./LanguageTool-6.6" -prune -o -type f \( -name "*.bat" -o -name "*.ahk" -o -name "*.ps1" \) -print | grep -vE "make.bat|notification_watcher.ahk"; }
```
</details>

<details>
<summary>Un aperçu graphique de l'architecture</summary>

Aperçu graphique de l'architecture :

![yappi_call_graph](../doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

      
![pydeps -v -o dependencies.svg scripts/py/func/main.py](../doc_sources/dependencies.svg)
</details>

<details>
<summary>Modèles utilisés</summary>

Modèles utilisés :

Recommandation : utiliser les modèles de Mirror https://github.com/sl5net/SL5-aura-service/releases/tag/v02.0.1 (probablement plus rapide)

Ces modèles zippés doivent être enregistrés dans le dossier `models/`

`mv vosk-model-*.zip models/`


Modèle Taille Taux d'erreur mot/vitesse Remarques Licence
| -------------------------------------------------------------------------------------- | ---- | --------------------------------------------------------------------------------------------- | ----------------------------------------- | ---------- |
[vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip)=1.8G=5.69 (librispeech test-clean)<br/>6.05 (tedlium)<br/>29.78 (callcenter)=1 Modèle anglais américain précis
[vosk-model-de-0.21](https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip): 1.9G: 9.83 (Tuda-de test)<br/>24.00 (podcast)<br/>12.82 (cv-test)<br/>12.42 (mls)<br/>33.26 (mtedx): Grand modèle allemand pour la téléphonie et le serveur.

Ce tableau donne un aperçu des différents modèles Vosk, y compris leur taille, le taux d'erreur mot ou la vitesse, les notes et les informations de licence.


- **Modèles de vocabulaire:** [Vosk-Model List](https://alphacephei.com/vosk/models)
- **Outil linguistique:**  
   (6.6) [https://languagetool.org/download/](https://languagetool.org/download/) 

**License de langageOutil:** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---
</details>

Appui au projet
Si vous trouvez cet outil utile, s'il vous plaît envisager de nous acheter un café! Votre soutien contribue à alimenter les améliorations futures.

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)


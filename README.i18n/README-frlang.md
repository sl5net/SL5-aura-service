> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../README.md).*

<img src="data/image/logo.svg" align="right" width="150" alt="⬟ SL5 Aura Logo">

# ⬟ SL5 Aura – Votre Voix. Vos Règles.

<!-- Stack Overflow & Community Badges -->
[![Stack Overflow](https://img.shields.io/badge/Stack_Overflow-536k+_Reached-F48024?style=for-the-badge&logo=stackoverflow&logoColor=white)](https://stackoverflow.com/users/2891692/sl5net)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Privacy](https://img.shields.io/badge/Privacy-100%25_Local_%26_Offline-2ea44f?style=for-the-badge&logo=keepassxc&logoColor=white)](#)
[![Latency](https://img.shields.io/badge/Latency-0.07s-blueviolet?style=for-the-badge&logo=speedtest&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> 100 % hors ligne, cadre d'assistant vocal axé sur la confidentialité.  
> Définissez exactement ce que fait votre voix — à partir d'un seul mot
> aux scripts Python complets. Pas de cloud. Aucune donnée ne quitte votre machine.  
> Fonctionne dans le terminal, le navigateur ou en tant que service en arrière-plan — sur Linux, macOS et Windows.
| 👵 Débutant | 🎓 Apprenant | 🧑‍💻 Développeur |
|---|---|---|
| [grandma-mode](../docs/GettingStarted.i18n/GettingStarted-frlang.md#the-oma-modus-beginner-shortcut) : il suffit d'écrire un mot, Aura fait le reste | Apprenez avec les Koans — un concept à la fois | Script complet en Python, plugins, appels API |
| 🗄️ Gestion d'État | Trino + orchestration Airflow, fzf, CopyQ, commandes vocales/terminal, interfaces utilisateur de navigateur |
[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=261851628)

⚡ **~2,87 J** par test (39 tests without LanguageTool across >800 maps @ 0.07s warm / 0.36s cold 🌿 measured with XMDLINK1X) · pas de calcul en nuage

[![Energy Consumption](https://api.green-coding.io/v1/ci/badge/get?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)](https://metrics.green-coding.io/ci.html?repo=sl5net/SL5-aura-service&branch=master&workflow=350653175)

⚡ **Suite de tests complète :** 94 tests avec LanguageTool sur plus de 800 cartes @ 0,07 s à chaud / 0,46 s à froid · sans calcul en cloud

<details>
XHTMLTAG2Démarrage rapideXHTMLTAG3
## Démarrage rapide
### Option A : Installation en 1 clic & Web Installer (Recommended)

Commande en une ligne ou installateur autonome pour Linux, macOS et Windows :
- **[→ Installer Guide & Direct Downloads](../docs/OneClickInstaller.i18n/OneClickInstaller-frlang.md)**

---
Option B : Installation manuelle (Developers / Git)

1. Télécharger ou cloner ce dépôt
2. Exécutez le script de configuration pour votre OS (see `setup/` folder):
- Linux (Arch/Manjaro): `bash setup/manjaro arch setup.sh`
- Linux (Ubuntu/Debian): `bash setup/ubuntu setup.sh`
- Linux (openSUSE): `bash setup/suse setup.sh`
- Linux (NixOS): `nix-shell setup/shell.nix` puis `bash setup/nixos setup.sh`
===> Expérimental — non testé par les auteurs, retour d'information bienvenue!   
- macOS: `bash setup/macos setup.sh`
- Windows: `setup/windows11 setup with ahk copyq.bat`
3. Démarrer Aura: `./scripts/restart venv and run-server.sh`
4. Appuyez sur votre touche et parlez — **[full guide →](../docs/GettingStarted.i18n/GettingStarted-frlang.md)**

---
### Désinstallation
Pour supprimer les services de fond SL5 Aura, les entrées de démarrage automatique et les environnements virtuels :
- **Linux / macOS:** `bash setup/uninstall.sh`
- **Windows (PowerShell):** `powershell -File setup/uninstall.ps1`
*(Your custom rules in `config/maps/` are kept safe by default unless you specify `--purge`).*

---


Exigences du système et compatibilité**

* **Windows:** * Entièrement pris en charge (uses AutoHotkey/PowerShell).
* **macOS:** -Entièrement pris en charge (uses AppleScript).
* **Linux (X11/Xorg):** Entièrement pris en charge.
* **Linux (Wayland):**  uvre entièrement prise en charge (tested on KDE Plasma 6 / Wayland).
* **Linux (CachyOS / Arch-based rolling release):** Entièrement pris en charge.
Nécessite mimalloc (`sudo pacman -S mimalloc`) en raison de la compatibilité glibc 2.43.
* **Linux (NixOS):** ☐ Expérimental — configuration communautaire, pas encore testée.
Si vous essayez, s'il vous plaît ouvrir un problème ou PR avec vos conclusions!   
* **Linux (Manjaro):** Nouveau : Un hotkey à l'échelle du système ouvre une interface fzf à clavier afin que vous puissiez exécuter les commandes Aura n'importe où sur le bureau (completely decoupled from the active window). Ce lanceur piloté par hotkey est actuellement mis en œuvre et testé sur Linux (Manjaro); d'autres distributions peuvent fonctionner mais nécessitent la configuration . Voir dans la rubrique [docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.md](../docs/Feature_Spotlight/CopyQ_Shortcut_Super_s.i18n/CopyQ_Shortcut_Super_s-frlang.md)   


    
SL5 Aura est un assistant vocal complet **offline** construit sur **Vosk** (for Speech-to-Text) et **LanguageTool** (for Grammar/Style), avec une option **Local LLM (Ollama) Fallback** pour des réponses créatives et des correspondances floues avancées. Il transforme votre voix en actions et textes précis, conçus pour une personnalisation ultime grâce à un système de règles rechargeables et à un moteur de script dynamique.
    
Traductions: Ce document existe également dans [other languages](https://github.com/sl5net/SL5-aura-service/tree/master/README.i18n).


Note: De nombreux textes sont des traductions générées par machine de la documentation originale en anglais et sont destinés à des conseils généraux seulement. En cas de divergences ou d'ambiguïtés, la version anglaise prévaut toujours. Nous accueillons l'aide de la communauté pour améliorer cette traduction!

</details>

<details>
<summary>Demo</summary>
### 📺 Démonstration du terminal

[![Terminal Demo](https://github.com/sl5net/SL5-aura-service/raw/master/data/demo_fast.gif)](https://github.com/sl5net/SL5-aura-service/blob/master/data/demo_fast.gif)

> **Conseil :** Pour une meilleure expérience du terminal, consultez [Zsh Integration](../docs/linux/zsh-integration.i18n/zsh-integration-frlang.md).
### 🎥 Tutoriel Vidéo
[![SL5 Aura: HowTo crash SL5 Aura?](https://img.youtube.com/vi/BZCHonTqwUw/0.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)

*(Alternative link: XMDLINK1X)*

</details>

<details>
<summary>Caractéristiques principales</summary>
Caractéristiques clés

* ** Hors ligne & Privé:** 100% local. Aucune donnée ne quitte jamais votre machine.
* ** Moteur de script dynamique :** Allez au-delà du remplacement de texte. Les règles peuvent exécuter des scripts Python personnalisés (`on_match_exec`) pour effectuer des actions avancées comme appeler les API (e.g., search Wikipedia), interagir avec les fichiers (e.g., manage a to-do list), ou générer du contenu dynamique (e.g., a context-aware email greeting).
* **Règles de Context-Aware:** Limiter les règles aux applications spécifiques. En utilisant `only in windows`, vous pouvez vous assurer qu'une règle ne déclenche que si un titre spécifique de la fenêtre (e.g., "Terminal", "VS Code" or "Browser") est actif. Cela fonctionne en multiplateforme (Linux, Windows, macOS).
* ** Moteur de transformation à haut contrôle :** Implémente un pipeline de traitement hautement personnalisable, piloté par la configuration. La priorité des règles, la détection des commandes et les transformations de texte sont déterminées uniquement par l'ordre séquentiel des règles de la Fuzzy Maps, nécessitant une configuration ** et non un codage**.
* **Utilisation de la RAM conservatrice :** Gestion intelligente de la mémoire, précharger les modèles seulement si suffisamment de RAM libre est disponible, garantissant que les autres applications (like your PC games) ont toujours la priorité.
* **Cross-Platform:** Fonctionne sur Linux, macOS et Windows.
* **Entièrement automatisé:** Gère son propre serveur LanguageTool (but you can also use an external one).
* **Blazing Fast:** La mise en cache intelligente assure des notifications instantanées "Listening..." et un traitement rapide.
* ** Gestion dynamique de l'État par Trino :** Moteur de configuration de l ' interface
sépare les paramètres pour `speech`, `terminal` et `web` - changer un sans
touchant les autres. Comprend un tableau de bord administratif en temps réel** (port 8084).
</details>

<details>
Intégrations prêtes à l'emploi</summary>
    ## 🔌 Intégrations prêtes à l'emploi

SL5-Aura est livré avec un vaste écosystème de plus de **100+ plugins pré-configurés**. Voici quelques points forts :
### OculiX / Contrôle IDE de la voix
SL5-Aura fournit une prise en charge vocale de première classe pour l'IDE **OculiX** et **SikuliX**. Cette intégration vous permet de « parler » votre code d'automatisation.

* **Voix à coupe:** Dites "cliquez", "attendre", ou "trouver tout", et le service tape instantanément le code Python correct (e.g., `click("image.png")`) dans l'IDE.
* **Window-Aware:** Le plugin est sensible au contexte ; il ne s'active que lorsque la fenêtre OculiX/SikuliX est focalisée.
* **Smart English Support:** Optimisé pour "en-US" avec un accent particulier sur les accents non indigènes (e.g., German-English phonetics), assurant une grande précision de reconnaissance pour la communauté mondiale.
* **Extensible :** Utilise le format facile à éditer `FUZZY MAP pre.py`.

> ** État :** Reconnu comme un plugin communautaire par l'équipe OculiX (see XMDLINK0X).
### Contrôle vocal de l'IDE LibreOffice
Contrôle de la voix

---

</details>


<details>
<summary>Documentation</summary>

🔍 [Interactive Search (Algolia)](https://sl5net.github.io/SL5-aura-service/search_online.html?lang=en)
Documentation

Pour une référence technique complète, incluant tous les modules et scripts, veuillez consulter notre page de documentation officielle. Il est généré automatiquement et toujours à jour.

👉 [**Go to Documentation sl5net.github.io/SL5-aura-service**](https://sl5net.github.io/SL5-aura-service/)
Pleins feux
- [Interactive Rule Search & Run](../docs/Feature_Spotlight/Interactive_Rule_Search_and_Run.i18n/Interactive_Rule_Search_and_Run-frlang.md) — Recherche de règles "fzf" à double panneau, prévisualisations en direct du contexte, exécution instantanée de la commande via `Enter`/`Ctrl+R`, et intégration de l'éditeur via `Ctrl+E`. Prise en charge par un clavier (`Super+S`) global et plusieurs environnements de recherche dédiés préconfigurés via des commandes vocales.
### Créer l'état

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

**Lisez ceci dans d'autres langues:**

[🇬🇧 English](../README.md) | [🇸🇦 العربية](../README.i18n/README-arlang-frlang.md) | [🇩🇪 Deutsch](../README.i18n/README-delang-frlang.md) | [🇪🇸 Español](../README.i18n/README-eslang-frlang.md) | [🇫🇷 Français](../README.i18n/README-frlang.md) | [🇮🇳 हिन्दी](../README.i18n/README-hilang-frlang.md) | [🇯🇵 日本語](../README.i18n/README-jalang-frlang.md) | [🇰🇷 한국어](../README.i18n/README-kolang-frlang.md) | [🇵🇱 Polski](../README.i18n/README-pllang-frlang.md) | [🇵🇹 Português](../README.i18n/README-ptlang-frlang.md) | [🇧🇷 Português Brasil](../README.i18n/README-pt-BRlang-frlang.md) | [🇨🇳 简体中文](../README.i18n/README-zh-CNlang-frlang.md)

---

<details>
<summary>Installation</summary>
Installation
Installation rapide sans modération (Manjaro/Arch Video)
Regardez le processus de configuration complet de 6 minutes :
* **Télécharger:** ~3 minutes
* **Setup & Premier départ:** ~3 minutes (including Welcome Wizard)

👉 **[SL5 Aura Installation Live-Demo on YouTube](https://www.youtube.com/watch?v=29xiwIW1ZHQ)**


La configuration est un processus en deux étapes:
1. Téléchargez la dernière version ou maître ( https://github.com/sl5net/SL5-aura-service/archive/master.zip ) ou clonez ce dépôt sur votre ordinateur.
2. Exécutez le script de configuration unique pour votre système d'exploitation.

Les scripts d'installation gèrent tout : dépendances système, environnement Python, et téléchargement des modèles et outils nécessaires (~4GB) directement depuis nos GitHub Releases pour une vitesse maximale.

#### Pour Linux, macOS et Windows (with Optional Language Exclusion)

Pour économiser de l'espace disque et de la bande passante, vous pouvez exclure les modèles de langue spécifiques (`de`, `en`) ou tous les modèles optionnels (`all`) pendant la configuration. **Les composants de base (LanguageTool, lid.176) sont toujours inclus.**

Ouvrez un terminal dans le répertoire racine du projet et exécutez le script pour votre système :

```bash
# For Ubuntu/Debian, Manjaro/Arch, macOS, or other derivatives
# (Note: Use bash or sh to execute the setup script)

bash setup/{your-os}_setup.sh [OPTION]

# For Arch-based systems (Manjaro, CachyOS, EndeavourOS, etc.):
`bash setup/manjaro_arch_setup.sh`

```sudo pacman -S mimalloc```


# Exemples :
# Installez tout (Default) :
# configuration bash/manjaro arch setup.sh

# À l'exclusion des modèles allemands:
# configuration bash/manjaro arch setup.sh exclusion=de

# Exclure tous les modèles de langue VOSK :
# configuration bash/manjaro arch setup.sh exclusion=all

# Pour Windows dans une session Admin-Powershell

configuration/fenêtres11 setup.ps1 - Exclure [OPTION]

# Exemples :
# Installez tout (Default) :
# configuration/fenêtres11 setup.ps1

# Exclure les modèles anglais :
# configuration/fenêtres11 setup.ps1 - Exclure "en"

# À l'exclusion des modèles allemands et anglais:
# configuration/fenêtres11 setup.ps1 - Exclure "de,fr"

# Ou (recommend) - Lancez le fichier BAT:
windows11 setup.bat - Exclure "en"
__CODE_BLOCK_1__#### Pour Windows
Exécutez le script de configuration avec les privilèges de l'administrateur.

**Installer un outil pour lire et exécuter, p.ex. [CopyQ](https://github.com/hluk/CopyQ) ou [AutoHotkey v2](https://www.autohotkey.com/)**. Ceci est nécessaire pour le text-typing watcher.

L'installation est entièrement automatisée et prend environ **8-10 minutes** lors de l'utilisation de 2 modèles sur un nouveau système.

1. Naviguez dans le dossier `setup`.
2. Double-cliquez sur **`windows11 setup with ahk copyq.bat`**.
* * Le script vous demandera automatiquement les privilèges de l'administrateur.
* *Il installe le système de base, les modèles de langue, **AutoHotkey v2**, et **CopyQ**.*
3. Une fois l'installation terminée, **Aura Dictation** sera lancée automatiquement.

> **Note :** Vous n'avez pas besoin d'installer Python ou Git au préalable ; le script gère tout.

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
<summary>Usage</summary>
Utilisation
1. Commencez les services
Sur Linux & macOS
Un seul script gère tout. Il démarre le service de dictée principal et le moniteur de fichiers automatiquement dans l'arrière-plan.
```bash
# Run this from the project's root directory
./scripts/restart_venv_and_run-server.sh
```
Sous Windows
Le démarrage du service est un processus manuel en deux étapes** :

1. **Démarrer le service principal:** Exécuter `start aura.bat`. ou commencer par `.venv` le service avec `python3`
2. Configurez votre hotkey

Pour déclencher la dictée, vous avez besoin d'une touche d'écoute globale qui crée un fichier spécifique. Nous vous recommandons vivement l'outil multiplateforme [CopyQ](https://github.com/hluk/CopyQ).
Notre recommandation: CopyQ

Créez une nouvelle commande dans CopyQ avec un raccourci global.

**Commande pour Linux/macOS:**
```bash
touch /tmp/sl5_record.trigger
```

**Commande pour Windows lorsque vous utilisez [CopyQ](https://github.com/hluk/CopyQ):**
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


**Commande pour Windows lors de l'utilisation de [AutoHotkey](https://AutoHotkey.com):**
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

Commencez à dicter !
Cliquez dans n'importe quel champ de texte, appuyez sur votre hotkey, et une notification "Listening..." apparaîtra. Parlez clairement, puis arrêtez. Le texte corrigé sera tapé pour vous.

</details>

---


<details>
Configuration avancée <summary> (Optional)</summary>
Configuration avancée (Optional)

Vous pouvez personnaliser le comportement de l'application en créant un fichier de paramètres locaux.

1. Naviguez dans le répertoire `config/`.
2. Créer une copie de `config/settings local.py Example.txt` et la renommer en `config/settings local.py`.
3. Modifier `config/settings local.py` (it overrides any setting from the main `config/settings.py` file).

Ce fichier `config/settings local.py` est ignoré par Git par défaut, de sorte que vos modifications personnelles ne seront pas écrasées par des mises à jour.
Structure de connexion et logique

La modularité du système permet une extension robuste via le répertoire plugins/.

Le moteur de traitement adhère strictement à une chaîne prioritaire hiérarchique** :

1. **Ordre de chargement des modules (High Priority):** Les règles chargées à partir des paquets de langages de base (de-DE, en-US) ont priorité sur les règles chargées à partir du répertoire (which load last alphabetically).
    
2. **Décret du dossier (Micro Priority):** Dans un fichier de carte (FUZZY_MAP_pre.py), les règles sont traitées strictement par **numéro de ligne** (top-to-bottom).
    

Cette architecture garantit la protection des règles du système de base, tandis que les règles spécifiques au projet ou aux contextes (like those for CodeIgniter or game controls) peuvent être facilement ajoutées en tant qu'extensions de faible priorité via des plug-ins.

</details>

<details>
Scripts clés pour les utilisateurs de Windows</summary>





## Scripts clés pour les utilisateurs de Windows

Voici une liste des scripts les plus importants pour configurer, mettre à jour et exécuter l'application sur un système Windows.
### Configuration et mise à jour

*   `chmod +x update.sh; ./update.sh`
*   `setup/setup.bat` : Le script principal pour la **configuration initiale unique** de l'environnement.
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `Exécuter powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"`

*   `update.bat` : Exécutez ceci depuis le dossier du projet pour **obtenir le code et les dépendances les plus récents**.
### Exécution de l'application
*   `start_aura.bat` : Un script principal pour **démarrer le service de dictée**.
Les scripts de base et d'aide
* `aura engine.py`: Le service de base Python (usually started by one of the scripts above).
* `get suggestions.py`: Un script d'aide pour des fonctionnalités spécifiques.

</details>


Caractéristiques principales et compatibilité du système d'exploitation

<details>
<summary>Legend pour la compatibilité OS</summary>

Légende pour la compatibilité OS:  
* **Linux** (e.g., Arch, Ubuntu)  
* **macOS**  
* **Windows**  
* **Android** (for mobile-specific features)  

---

</details>


Moteur (Aura)
Notre moteur principal pour la reconnaissance de la parole hors ligne et le traitement audio.

    
<details>
<summary>Aura-Core</summary>
**Aura-Core/**
- `aura engine.py` (Main Python service orchestrating Aura)
*Live Hot-Reload** (Config & Maps)
│Ã **Secure Carte privée Chargement en cours (Integrity-First)**
││ * ** Flux de travail:** Charge les archives ZIP protégées par mot de passe.   
** Traitement de texte et correction/** Groupe par langue ( e.g. `de-DE`, `en-US`, ... )   
│ê 1. `normalize punctuation.py` (Standardizes punctuation post-transcription)
2. **Précorrection intelligente** (`FuzzyMap Pre` - XMDLINK0X)
││ * ** Exécution du script dynamique:** Les règles peuvent déclencher des scripts Python personnalisés (`on_match_exec`) pour effectuer des actions avancées comme les appels API, les E/S de fichiers ou générer des réponses dynamiques.  
││ * **Exécution en cascade:** Les règles sont traitées successivement et leurs effets sont **cumulatifs**. Des règles ultérieures s'appliquent au texte modifié par des règles antérieures.  
││ * **Critère d'arrêt prioritaire le plus élevé:** Si une règle atteint un ** Full Match** (^...$), l'ensemble du pipeline de traitement de ce jeton s'arrête immédiatement. Ce mécanisme est essentiel à la mise en œuvre de commandes vocales fiables.   
│ê 3. `correct text by languagetool.py` (Integrates LanguageTool for grammar/style correction) --
│Ã **4. Hiérarchique RegEx-Rule-Ingéniere avec Ollama AI Fallback**
││ * **Contrôle déterministe:** Utilise RegEx-Rule-Engine pour une commande précise, hautement prioritaire et un contrôle texte.   
│Ã **Greffon de recherche vectorielle** (Lazy loading): Active la recherche sémantique en connectant les éléments d'intégration vectorielle locale avec le calque de repli Ollama/LLM
││ * **Ollama AI (Local LLM) Retour en arrière:** Fonctionne comme une vérification facultative et peu prioritaire pour les réponses créatives, les questions-réponses et les correspondances Fuzzy avancées** lorsqu'aucune règle déterministe n'est respectée.  
││ * **Situation:** Intégration locale des LLM.
5. **Intelligent post-correction** (`FuzzyMap`)**– Raffinement post-LT**
││ * Appliquée après LanguageTool pour corriger les sorties spécifiques aux LT. Suivre la même logique de priorité en cascade que le calque Pré-Correction.  
││ * ** Exécution du script dynamique:** Les règles peuvent déclencher des scripts Python personnalisés (XMDLINK1X) pour effectuer des actions avancées comme les appels API, les E/S de fichiers ou générer des réponses dynamiques.  
││ * **Fuzzy Fallback:** Le **Fuzzy Similarity Check** (controlled by a threshold, e.g., 85%) agit comme le calque de correction d'erreur le plus bas. Il n'est exécuté que si l'ensemble de la règle déterministe/cascading précédente n'a pas réussi à trouver une correspondance (current_rule_matched is False), optimisant les performances en évitant les vérifications lentes et floues dans la mesure du possible.   
**Gestion des modèles/**   
│                                                                                                                                                                                                                                                              
"Setup initial model.py" (Configures the first-time model setup)
**Délai d'adaptation de la VAD**
* *Clé Adaptatif (Start/Stop)**
* ** Commutateur de langues instantanées** (Experimental via model preloading)
Ô – **Orchestration de flux d'air** (DAG-based workflow automation)
│ Nécessite Docker · UI: `http://localhost:8081`
* ** Moteur d'État de Turin** (Interface-aware config per speech/terminal/web)
- Nécessite Docker · UI d'administrateur: `http://localhost:8084`

**Utilisations du système/**   
**Gestion des serveurs d'outils linguistiques/**   
│¬ `start languagetool server.py` (Initializes the local LanguageTool server) --
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
* - `monitor mic.sh` (e.g. for use with Headset without use keyboard and Monitor)
### **Gestion des modèles et des paquets**  
Outils pour une manipulation robuste des grands modèles de langage.  

**Modèle de gestion/**
Téléchargeur de modèles de bust** (GitHub Release chunks)
  `split and hash.py                                                                                                                                                                                                                                                    
* - `download all packages.py ' (Tool for end-users to download, verify, and reassemble multi-part files)

</details>


<details>
<summary>Aides au développement et au déploiement</summary>
### **Aides au développement et au déploiement**  
Scripts pour la configuration d'environnement, les essais et l'exécution de service.   

*Astuce : glogg vous permet d'utiliser des expressions régulières pour rechercher des événements intéressants dans vos fichiers journaux.*   
Veuillez cocher la case à cocher lors de l'installation pour associer avec les fichiers journaux.   
https://globg.bonnefon.org/   
    
*Astuce : Après avoir défini vos modèles regex, exécutez `python3 tools/map tagger.py` pour générer automatiquement des exemples de recherche pour les outils CLI. Voir [Map Maintenance Tools](../docs/Developer_Guide/Map_Maintenance_Tools.i18n/Map_Maintenance_Tools-frlang.md) pour plus de détails.*

Alors peut-être double-cliquez
`log/aura engine.log`
    
**DevHelpers/**  
**Gestion de l'environnement virtuel/**  
│                                                                                                                                                                                                                                                              
"scripts/restart venv and run-server.ahk` (Windows) "  
** Intégration de la dictation à l'échelle du système/**  
│Ã Intégration de vos systèmes-Listener
│English `scripts/monitor mic.sh` (Linux-specific microphone monitoring)
│=scripts/type watcher.ahk=(AutoHotkey listens for recognized text and types it out system-wide)=  
**CI/CD Automation/**  
*(Runs on GitHub Actions)*  

</details>

<details>
<summary>Caractéristiques expérimentales</summary>
    ### **Caractéristiques nouvelles / expérimentales**  
Caractéristiques en cours d'élaboration ou en état provisoire.  

**Caractéristiques expérimentales/**  
* ENTER AFTER DICTATION REGEX** Exemple de règle d'activation "(ExampleAplicationThatNotExist|Pi, your personal AI)"
Plugins  
*Live Lazy-Reload** (*)
(*Changes to Plugin activation/deactivation, and their configurations, are applied on the next processing run without service restart.*)  
│ * Commandes d'agit** (Voice control for send git commands)
│ **wannweil** (Map for Location Germany-Wannweil) --
│ ** Plugin de poche (Draft)** (Voice control for poker applications)
Module (Draft)** (Voice control for 0 A.D. game)
Ô - ** Sortie sonore au début ou à la fin d'une session** (Description pending)
* *Speech Output pour les malvoyants** (Description pending)
**SL5 Aura Android Prototype** (Not fully offline yet)

---

*(Note: Specific Linux distributions like Arch (ARL) ou Ubuntu (UBT) sont couverts par le symbole général de Linux. Des distinctions détaillées pourraient être incluses dans les guides d'installation.*
</details>

<details>
<summary>Cliquez pour voir la commande utilisée pour générer cette liste de script</summary>

```bash
{ find . -maxdepth 1 -type f \( -name "aura_engine.py" -o -name "get_suggestions.py" \) ; find . -path "./.venv" -prune -o -path "./.env" -prune -o -path "./backup" -prune -o -path "./LanguageTool-6.6" -prune -o -type f \( -name "*.bat" -o -name "*.ahk" -o -name "*.ps1" \) -print | grep -vE "make.bat|notification_watcher.ahk"; }
```
</details>

<details>
<summary>A aperçu graphique de l'architecture</summary>
### Un aperçu graphique de l'architecture :

![yappi_call_graph](../doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

      
![pydeps -v -o dependencies.svg scripts/py/func/main.py](../doc_sources/dependencies.svg)
</details>

<details>
Modèles utilisés <summary></summary>
## Modèles utilisés :

Recommandation : utiliser les modèles de Mirror https://github.com/sl5net/SL5-aura-service/releases/tag/v02.0.1 (probably faster)

Ces modèles zippés doivent être enregistrés dans le dossier "modèles/`

`mv vosk-modèle-*.zip modèles/`

Modèle Taille Taux d'erreur mot/vitesse Remarques Licence
| -------------------------------------------------------------------------------------- | ---- | --------------------------------------------------------------------------------------------- | ----------------------------------------- | ---------- |
[vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) (en anglais) 1.8G (en anglais) 5.69 (librispeech test-clean)<br/>6.05 (tedlium)<br/>29.78 (callcenter) (en anglais) Exacerbe generic US English model (en anglais) Apache 2.0 (en anglais)
[vosk-model-de-0.21](https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip)=1.9G=9.983 (Tuda-de test)<br/>24.00 (podcast)<br/>12.82 (cv-test)<br/>12.42 (mls)<br/>33.26 (mtedx)=1 Grand modèle allemand pour la téléphonie et le serveur
Ce tableau donne un aperçu des différents modèles Vosk, y compris leur taille, le taux d'erreur mot ou la vitesse, les notes et les informations de licence.


- **Modèles Vosk:** [Vosk-Model List](https://alphacephei.com/vosk/models)
- **Outil de langue:**  
   (6.6) [https://languagetool.org/download/](https://languagetool.org/download/) 

**License de langageOutil:** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---
</details>
## Appuyer le projet
Si vous trouvez cet outil utile, s'il vous plaît envisager de nous acheter un café! Votre soutien contribue à alimenter les améliorations futures.

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)

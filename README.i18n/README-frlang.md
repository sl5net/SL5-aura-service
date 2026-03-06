# Voix hors ligne à l'échelle du système vers des commandes ou du texte, système enfichable

**⚠️ Configuration système requise et compatibilité**

* **Windows :** ✅ Entièrement pris en charge (utilise AutoHotkey/PowerShell).
* **macOS :** ✅ Entièrement pris en charge (utilise AppleScript).
* **Linux (X11/Xorg) :** ✅ Entièrement pris en charge.
* **Linux (Wayland) :** ✅ Entièrement pris en charge.


Bienvenue au service SL5 Aura ! Ce document fournit un aperçu rapide de nos fonctionnalités clés et de leur compatibilité avec le système d'exploitation.

Aura n'est pas seulement un transcripteur ; il s'agit d'un puissant moteur de traitement hors ligne qui transforme votre voix en actions et en texte précis.

Il s'agit d'un **assistant vocal hors ligne** complet, basé sur **Vosk** (pour la synthèse vocale) et **LanguageTool** (pour la grammaire/le style), proposant désormais un **Local LLM (Ollama) Fallback** en option pour des réponses créatives et une correspondance floue avancée. Il est conçu pour une personnalisation ultime grâce à un système de règles enfichable et un moteur de script dynamique.

  
Traductions : Ce document existe également en [other languages](https://github.com/sl5net/SL5-aura-service/tree/master/docs).


Remarque : De nombreux textes sont des traductions générées automatiquement de la documentation originale en anglais et sont uniquement destinés à des conseils généraux. En cas de divergences ou d'ambiguïtés, la version anglaise prévaut toujours. Nous apprécions l’aide de la communauté pour améliorer cette traduction !


[![SL5 Aura (v0.16.1): HowTo crash SL5 Aura? -  seeh Hierarchical and Recursive Rule Engine](https://img.youtube.com/vi/d98ml86u68g/maxresdefault.jpg)](https://www.youtube.com/watch?v=BZCHonTqwUw)
( https://www.youtube.com/watch?v=BZCHonTqwUw ou https://skipvids.com/?v=BZCHonTqwUw )

## Principales fonctionnalités

* **Hors ligne et privé :** 100 % local. Aucune donnée ne quitte votre machine.
* **Moteur de script dynamique :** Allez au-delà du remplacement de texte. Les règles peuvent exécuter des scripts Python personnalisés (`on_match_exec`) pour effectuer des actions avancées telles que l'appel d'API (par exemple, rechercher sur Wikipédia), interagir avec des fichiers (par exemple, gérer une liste de tâches) ou générer du contenu dynamique (par exemple, un message d'accueil par e-mail contextuel).
* **Règles contextuelles :** Restreindre les règles à des applications spécifiques. En utilisant `only_in_windows`, vous pouvez garantir qu'une règle ne se déclenche que si un titre de fenêtre spécifique (par exemple, "Terminal", "VS Code" ou "Navigateur") est actif. Cela fonctionne sur plusieurs plates-formes (Linux, Windows, macOS).
* **Moteur de transformation à contrôle élevé :** implémente un pipeline de traitement hautement personnalisable et basé sur la configuration. La priorité des règles, la détection des commandes et les transformations de texte sont déterminées uniquement par l'ordre séquentiel des règles dans les cartes floues, nécessitant une **configuration, pas un codage**.
* **Utilisation conservatrice de la RAM :** Gère intelligemment la mémoire, en préchargeant les modèles uniquement si suffisamment de RAM libre est disponible, garantissant ainsi que les autres applications (comme vos jeux PC) ont toujours la priorité.
* **Multiplateforme :** Fonctionne sous Linux, macOS et Windows.
* **Entièrement automatisé :** Gère son propre serveur LanguageTool (mais vous pouvez également en utiliser un externe).
* **Blazing Fast :** La mise en cache intelligente garantit des notifications instantanées « Écoute … » et un traitement rapide.

##Documents

Pour une référence technique complète, y compris tous les modules et scripts, veuillez visiter notre page de documentation officielle. Il est généré automatiquement et toujours à jour.

[**Go to Documentation >>**](https://sl5net.github.io/SL5-aura-service/)


### État de la construction
[![Linux Manjaro](https://img.shields.io/badge/Manjaro-Tested-27ae60?style=for-the-badge&logo=manjaro)](https://youtu.be/D9ylPBnP2aQ)
[![Linux Ubuntu](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml)
[![Linux Suse](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml)
[![macOS](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml)
[![Windows 11](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml)

[![Documentation](https://img.shields.io/badge/documentation-live-brightgreen)](https://sl5net.github.io/SL5-aura-service/)

**Lisez ceci dans d'autres langues :**

[🇬🇧 English](../README.md) | [🇸🇦 العربية](docs/README/README-arlang.md) | [🇩🇪 Deutsch](docs/README/README-delang.md) | [🇪🇸 Español](docs/README/README-eslang.md) | [🇫🇷 Français](docs/README/README-frlang.md) | [🇮🇳 हिन्दी](docs/README/README-hilang.md) | [🇯🇵 日本語](docs/README/README-jalang.md) | [🇰🇷 한국어](docs/README/README-kolang.md) | [🇵🇱 Polski](docs/README/README-pllang.md) | [🇵🇹 Português](docs/README/README-ptlang.md) | [🇧🇷 Português Brasil](docs/README/README-pt-BRlang.md) | [🇨🇳 简体中文](docs/README/README-zh-CNlang.md)

---







##Installation

La configuration est un processus en deux étapes :
1. Téléchargez la dernière version ou master ( https://github.com/sl5net/SL5-aura-service/archive/master.zip ) ou clonez ce référentiel sur votre ordinateur.
2. Exécutez le script d'installation unique pour votre système d'exploitation.

Les scripts d'installation gèrent tout : les dépendances du système, l'environnement Python et le téléchargement des modèles et outils nécessaires (~ 4 Go) directement depuis nos versions GitHub pour une vitesse maximale.


#### Pour Linux, macOS et Windows (avec exclusion de langue facultative)

Pour économiser de l'espace disque et de la bande passante, vous pouvez exclure des modèles de langage spécifiques (`de`, `en`) ou tous les modèles facultatifs (`all`) lors de l'installation. **Les composants de base (LanguageTool, lid.176) sont toujours inclus.**

Ouvrez un terminal dans le répertoire racine du projet et exécutez le script pour votre système :

```bash
# For Ubuntu/Debian, Manjaro/Arch, macOS, or other derivatives
# (Note: Use bash or sh to execute the setup script)

bash setup/{your-os}_setup.sh [OPTION]

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

# Or (recommend) - Start des BAT: 
windows11_setup.bat -Exclude "en"
```

#### Pour Windows
Exécutez le script d'installation avec les privilèges d'administrateur.

**Installez un outil pour lire et exécuter, par ex. [CopyQ](https://github.com/hluk/CopyQ) ou [AutoHotkey v2](https://www.autohotkey.com/)**. Ceci est requis pour l’observateur de saisie de texte.

L'installation est entièrement automatisée et prend environ **8 à 10 minutes** lors de l'utilisation de 2 modèles sur un nouveau système.

1. Accédez au dossier « setup ».
2. Double-cliquez sur **`windows11_setup_with_ahk_copyq.bat`**.
* *Le script demandera automatiquement les privilèges d'administrateur.*
* *Il installe le système principal, les modèles de langage, **AutoHotkey v2** et **CopyQ**.*
3. Une fois l'installation terminée, **Aura Dictation** se lancera automatiquement.

> **Remarque :** Vous n'avez pas besoin d'installer Python ou Git au préalable ; le script gère tout.

---

#### Installation avancée/personnalisée
Si vous préférez ne pas installer les outils clients (AHK/CopyQ) ou souhaitez économiser de l'espace disque en excluant des langues spécifiques, vous pouvez exécuter le script principal via la ligne de commande :

```powershell
# Core Setup only (No AHK, No CopyQ)
setup\windows11_setup.bat

# Exclude specific language models (saves space):
# Exclude English:
setup\windows11_setup.bat -Exclude "en"

# Exclude German and English:
setup\windows11_setup.bat -Exclude "de,en"
```


---

## Utilisation

### 1. Démarrez les services

#### Sous Linux et macOS
Un seul script gère tout. Il démarre automatiquement le service de dictée principal et l'observateur de fichiers en arrière-plan.
```bash
# Run this from the project's root directory
./scripts/restart_venv_and_run-server.sh
```

#### Sous Windows
Le démarrage du service est un **processus manuel en deux étapes** :

1. **Démarrez le service principal :** Exécutez `start_aura.bat`. ou démarrez à partir de `.venv` le service avec `python3`

### 2. Configurez votre raccourci clavier

Pour déclencher la dictée, vous avez besoin d'un raccourci clavier global qui crée un fichier spécifique. Nous recommandons fortement l'outil multiplateforme [CopyQ](https://github.com/hluk/CopyQ).

#### Notre recommandation : CopyQ

Créez une nouvelle commande dans CopyQ avec un raccourci global.

**Commande pour Linux/macOS :**
```bash
touch /tmp/sl5_record.trigger
```

**Commande pour Windows lors de l'utilisation de [CopyQ](https://github.com/hluk/CopyQ) :**
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


**Commande pour Windows lors de l'utilisation de [AutoHotkey](https://AutoHotkey.com) :**
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



Cliquez dans n'importe quel champ de texte, appuyez sur votre touche de raccourci et une notification "Écoute..." apparaîtra. Parlez clairement, puis faites une pause. Le texte corrigé sera tapé pour vous.

---


## Configuration avancée (facultatif)

Vous pouvez personnaliser le comportement de l'application en créant un fichier de paramètres local.

1. Accédez au répertoire `config/`.
2. Créez une copie de `config/settings_local.py_Example.txt` et renommez-la en `config/settings_local.py`.
3. Modifiez `config/settings_local.py` (il remplace tout paramètre du fichier principal `config/settings.py`).

Ce fichier `config/settings_local.py` est (peut-être) ignoré par Git, donc vos modifications personnelles ne seront (peut-être) pas écrasées par les mises à jour.

### Structure et logique du plug-in

La modularité du système permet une extension robuste via le répertoire plugins/.

Le moteur de traitement adhère strictement à une **Chaîne de priorités hiérarchique** :

1. **Ordre de chargement des modules (haute priorité) :** Les règles chargées à partir des modules linguistiques principaux (de-DE, en-US) ont priorité sur les règles chargées à partir du répertoire plugins/ (qui se chargent en dernier par ordre alphabétique).
  
2. **Ordre dans le fichier (micro-priorité) :** Dans tout fichier de carte donné (FUZZY_MAP_pre.py), les règles sont traitées strictement par **numéro de ligne** (de haut en bas).
  

Cette architecture garantit que les règles de base du système sont protégées, tandis que les règles spécifiques au projet ou sensibles au contexte (comme celles de CodeIgniter ou des contrôles de jeu) peuvent être facilement ajoutées en tant qu'extensions de faible priorité via des plug-ins.
## Scripts clés pour les utilisateurs Windows

Voici une liste des scripts les plus importants pour configurer, mettre à jour et exécuter l'application sur un système Windows.

### Configuration et mise à jour
* `setup/setup.bat` : Le script principal pour la **configuration initiale unique** de l'environnement.
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `Exécutez PowerShell -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"`

* `update.bat` : exécutez-les à partir du dossier Projet **obtenez le dernier code et les dernières dépendances**.

### Exécution de l'application
* `start_aura.bat` : Un script principal pour **démarrer le service de dictée**.

### Scripts de base et d'assistance
* `aura_engine.py` : le service Python principal (généralement démarré par l'un des scripts ci-dessus).
* `get_suggestions.py` : Un script d'assistance pour des fonctionnalités spécifiques.




## 🚀 Principales fonctionnalités et compatibilité du système d'exploitation

Légende de compatibilité du système d'exploitation :   
* 🐧 **Linux** (par exemple, Arch, Ubuntu)  
* 🍏 **macOS**  
* 🪟 **Windows**  
* 📱 **Android** (pour les fonctionnalités spécifiques aux mobiles)  

---

### **Moteur principal de synthèse vocale (Aura)**
Notre principal moteur de reconnaissance vocale et de traitement audio hors ligne.

  
**Aura-Core/** 🐧 🍏 🪟  
├─ `aura_engine.py` (service Python principal orchestrant Aura) 🐧 🍏 🪟  
├┬ **Live Hot-Reload** (Configuration et cartes) 🐧 🍏 🪟  
│├ **Chargement sécurisé de la carte privée (intégrité d'abord)** 🔒 🐧 🍏 🪟  
││ * **Workflow :** Charge les archives ZIP protégées par mot de passe.   
│├ **Traitement et correction de texte/** Regroupés par langue ( par exemple `de-DE`, `en-US`, ... )   
│├ 1. `normalize_punctuation.py` (Standardise la ponctuation après la transcription) 🐧 🍏 🪟  
│├ 2. **Pré-correction intelligente** (`FuzzyMap Pre` - [The Primary Command Layer](../docs/CreatingNewPluginModules.i18n/CreatingNewPluginModules-frlang.md)) 🐧 🍏 🪟  
││ * **Exécution de script dynamique :** Les règles peuvent déclencher des scripts Python personnalisés (on_match_exec) pour effectuer des actions avancées telles que des appels d'API, des E/S de fichiers ou générer des réponses dynamiques.  
││ * **Exécution en cascade :** Les règles sont traitées séquentiellement et leurs effets sont **cumulatifs**. Les règles ultérieures s'appliquent au texte modifié par les règles antérieures.  
││ * **Critère d'arrêt de priorité la plus élevée :** Si une règle obtient une **Correspondance complète** (^...$), l'ensemble du pipeline de traitement pour ce jeton s'arrête immédiatement. Ce mécanisme est essentiel pour implémenter des commandes vocales fiables.  
│├ 3. `correct_text_by_lingualtool.py` (Intègre LanguageTool pour la correction de grammaire/style) 🐧 🍏 🪟  
│├ **4. Moteur de règles RegEx hiérarchique avec Ollama AI Fallback** 🐧 🍏 🪟  
││ * **Contrôle déterministe :** utilise RegEx-Rule-Engine pour un contrôle précis et prioritaire des commandes et du texte.  
││ * **Ollama AI (Local LLM) Fallback :** Sert de vérification facultative et de faible priorité pour les **réponses créatives, les questions et réponses et la correspondance floue avancée** lorsqu'aucune règle déterministe n'est respectée.  
││ * **Statut :** Intégration LLM locale.
│└ 5. **Post-correction intelligente** (`FuzzyMap`)** – Raffinement post-LT** 🐧 🍏 🪟
││ * Appliqué après LanguageTool pour corriger les sorties spécifiques à LT. Suit la même logique stricte de priorité en cascade que la couche de pré-correction.  
││ * **Exécution de script dynamique :** Les règles peuvent déclencher des scripts Python personnalisés ([on_match_exec](../docs/advanced-scripting.i18n/advanced-scripting-frlang.md)) pour effectuer des actions avancées telles que des appels d'API, des E/S de fichiers ou générer des réponses dynamiques.  
││ * **Fuzzy Fallback :** Le **Fuzzy Similarity Check** (contrôlé par un seuil, par exemple 85 %) agit comme la couche de correction d'erreurs la plus basse priorité. Elle n'est exécutée que si l'exécution complète de la règle déterministe/en cascade précédente n'a pas réussi à trouver une correspondance (current_rule_matched est False), optimisant ainsi les performances en évitant les vérifications floues lentes autant que possible.  
├┬ **Gestion des modèles/**   
│├─ `prioritize_model.py` (Optimise le chargement/déchargement du modèle en fonction de l'utilisation) 🐧 🍏 🪟  
│└─ `setup_initial_model.py` (Configure la première configuration du modèle) 🐧 🍏 🪟  
├─ **Délai d'expiration VAD adaptatif** 🐧 🍏 🪟  
├─ **Raccourci clavier adaptatif (Démarrer/Arrêter)** 🐧 🍏 🪟  
└─ **Changement de langue instantané** (expérimental via le préchargement du modèle) 🐧 🍏   

**Utilitaires système/**   
├┬ **Gestion du serveur LanguageTool/**   
│├─ `start_lingualtool_server.py` (Initialise le serveur LanguageTool local) 🐧 🍏 🪟  
│└─ `stop_lingualtool_server.py` (Arrête le serveur LanguageTool) 🐧 🍏
├─ `monitor_mic.sh` (par exemple pour une utilisation avec un casque sans utiliser le clavier ni le moniteur) 🐧 🍏 🪟  

### **Gestion des modèles et des packages**  
Outils pour une gestion robuste des grands modèles de langage.  

**Gestion de modèles/** 🐧 🍏 🪟  
├─ **Téléchargeur de modèles robuste** (morceaux de la version GitHub) 🐧 🍏 🪟  
├─ `split_and_hash.py` (Utilitaire permettant aux propriétaires de dépôts de diviser des fichiers volumineux et de générer des sommes de contrôle) 🐧 🍏 🪟  
└─ `download_all_packages.py` (outil permettant aux utilisateurs finaux de télécharger, vérifier et réassembler des fichiers en plusieurs parties) 🐧 🍏 🪟  


### **Aide au développement et au déploiement**  
Scripts pour la configuration de l'environnement, les tests et l'exécution des services.  

*Astuce : glogg vous permet d'utiliser des expressions régulières pour rechercher des événements intéressants dans vos fichiers journaux.*   
Veuillez cocher la case lors de l'installation pour l'associer aux fichiers journaux.    
https://translate.google.com/translate?hl=en&sl=en&tl=fr&u=https://glogg.bonnefon.org/     
  
*Conseil : après avoir défini vos modèles d'expression régulière, exécutez « python3 tools/map_tagger.py » pour générer automatiquement des exemples consultables pour les outils CLI. Voir [Map Maintenance Tools](../docs/Developer_Guide/Map_Maintenance_Tools.i18n/Map_Maintenance_Tools-frlang.md) pour plus de détails.*

Alors peut-être double-cliquez
`log/aura_engine.log`
  
  
**DevHelpers/**  
├┬ **Gestion de l'environnement virtuel/**  
│├ `scripts/restart_venv_and_run-server.sh` (Linux/macOS) 🐧 🍏  
│└ `scripts/restart_venv_and_run-server.ahk` (Windows) 🪟  
├┬ **Intégration de dictée à l'échelle du système/**  
│├ Intégration Vosk-System-Listener 🐧 🍏 🪟  
│├ `scripts/monitor_mic.sh` (surveillance des microphones spécifiques à Linux) 🐧  
│└ `scripts/type_watcher.ahk` (AutoHotkey écoute le texte reconnu et le tape dans tout le système) 🪟  
└─ **Automation CI/CD/**  
└─ Workflows GitHub étendus (installation, tests, déploiement de documents) 🐧 🍏 🪟 *(S'exécute sur les actions GitHub)*  

### **Fonctionnalités à venir/expérimentales**  
Fonctionnalités actuellement en cours de développement ou à l'état de projet.  

**Fonctionnalités expérimentales/**  
├─ **ENTER_AFTER_DICTATION_REGEX** Exemple de règle d'activation "(ExampleAplicationThatNotExist|Pi, votre IA personnelle)" 🐧  
├┬Plugins  
│╰┬ **Live Lazy-Reload** (*) 🐧 🍏 🪟  
(*Les modifications apportées à l'activation/désactivation du plug-in et à leurs configurations sont appliquées lors de la prochaine exécution du traitement sans redémarrage du service.*)  
│ ├ **commandes git** (Contrôle vocal pour envoyer des commandes git) 🐧 🍏 🪟  
│ ├ **wannweil** (Carte de localisation Allemagne-Wannweil) 🐧 🍏 🪟  
│ ├ **Poker Plugin (Draft)** (Contrôle vocal pour les applications de poker) 🐧 🍏 🪟  
│ └ **0 A.D. Plugin (Draft)** (Commande vocale pour le jeu 0 A.D.) 🐧   
├─ **Sortie sonore au démarrage ou à la fin d'une session** (Description en attente) 🐧   
├─ **Sortie vocale pour les malvoyants** (Description en attente) 🐧 🍏 🪟  
└─ **Prototype Android SL5 Aura** (Pas encore entièrement hors ligne) 📱  

---

*(Remarque : des distributions Linux spécifiques comme Arch (ARL) ou Ubuntu (UBT) sont couvertes par le symbole général Linux 🐧. Des distinctions détaillées peuvent être couvertes dans les guides d'installation.)*









<détails>
<summary>Cliquez pour voir la commande utilisée pour générer cette liste de scripts</summary>

```bash
{ find . -maxdepth 1 -type f \( -name "aura_engine.py" -o -name "get_suggestions.py" \) ; find . -path "./.venv" -prune -o -path "./.env" -prune -o -path "./backup" -prune -o -path "./LanguageTool-6.6" -prune -o -type f \( -name "*.bat" -o -name "*.ahk" -o -name "*.ps1" \) -print | grep -vE "make.bat|notification_watcher.ahk"; }
```
</détails>


### regardez graphiquement ce qu'il y a derrière :

![yappi_call_graph](doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png "doc_sources/DeveloperGuide_Generating_ServiceCallGraph/yappi_call_graph_stripped.svg_20251024_010459.png")

  
![pydeps -v -o dependencies.svg scripts/py/func/main.py](../doc_sources/dependencies.svg)


# Modèles utilisés :

Recommandation : utilisez les modèles de Mirror https://github.com/sl5net/SL5-aura-service/releases/tag/v0.2.0.1 (probablement plus rapide)

Ces modèles zippés doivent être enregistrés dans le dossier `models/`

`mv vosk-model-*.zip modèles/`


| Modèle | Taille | Taux d'erreur de mot/Vitesse | Remarques | Licence |
| ---------------------------------------------------------------------------- | ---- | --------------------------------------------------------------------------------------------- | ----------------------------------------- | ---------- |
| [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) | 1,8G | 5,69 (librispeech test-clean)<br/>6,05 (tedlium)<br/>29,78 (centre d'appels) | Modèle générique précis en anglais américain | Apache2.0 |
| [vosk-model-de-0.21](https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip) | 1,9G | 9,83 (Tuda-de test)<br/>24,00 (podcast)<br/>12,82 (cv-test)<br/>12,42 (mls)<br/>33,26 (mtedx) | Grand modèle allemand de téléphonie et de serveur | Apache2.0 |

Ce tableau donne un aperçu des différents modèles Vosk, y compris leur taille, leur taux d'erreur de mots ou leur vitesse, leurs notes et leurs informations de licence.


- **Modèles Vosk :** [Vosk-Model List](https://alphacephei.com/vosk/models)
- **LanguageTool :**  
(6.6) [https://languagetool.org/download/](https://languagetool.org/download/)

**Licence de LanguageTool :** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---

## Soutenez le projet
Si vous trouvez cet outil utile, pensez à nous offrir un café ! Votre soutien contribue à alimenter les améliorations futures.

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)
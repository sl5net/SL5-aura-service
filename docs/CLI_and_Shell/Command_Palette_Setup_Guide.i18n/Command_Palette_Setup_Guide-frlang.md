# Guide de recherche de palette de commandes et de carte

Ce guide explique comment configurer et utiliser la **Palette de commandes** à l'échelle du système et indépendante de l'emplacement pour SL5 Aura. Il vous permet de rechercher de manière interactive dans vos règles de carte, de voir des aperçus d'exécution en direct à partir du cache SQLite local et de saisir instantanément la sortie sélectionnée sur votre curseur actif.

## Prérequis

Assurez-vous que les services et outils d’arrière-plan suivants sont installés et actifs :
1. **`fzf`** (Fuzzy Finder)
2. **CopyQ** (Clipboard Manager, utilisé pour l'orchestration globale des raccourcis clavier)
3. **`type_watcher.sh`** (démon de saisie en arrière-plan Aura)

---

## Configuration du raccourci global CopyQ

Pour lancer la palette de commandes instantanément depuis n'importe quelle fenêtre active (par exemple, votre navigateur ou éditeur de texte), configurez un raccourci clavier global dans CopyQ :

1. Ouvrez **CopyQ** et appuyez sur « F6 » (ou accédez à **Commands** / **Befehle**).
2. Cliquez sur **Ajouter** (Remarque) et nommez-le « Aura Command Palette ».
3. Définissez le **raccourci global** souhaité (par exemple, « Meta+S » ou « Ctrl+Alt+S »).
4. Définissez le **Type** sur « Command » (Befehl).
5. Collez le code JavaScript suivant dans la zone de commande :

__CODE_BLOCK_0__
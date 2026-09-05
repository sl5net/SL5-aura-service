# Exécution de 0 A.D. avec Aura Voice Control sur des systèmes à faible RAM (Linux Mint)

Ce guide documente la configuration et l'optimisation de la mémoire pour exécuter la commande vocale **sl5net Aura** avec **0 A.D.** sur du matériel Linux Mint existant ou à mémoire limitée.

## Profil matériel et système cible
- **Appareil** : Lenovo ThinkPad T520 (ordinateur portable)
- **CPU** : Intel Core i7-2620M (Dual-Core à 2,70 GHz - 3,40 GHz)
- **Mémoire** : 5,67 Go de RAM
- **Swap** : échange effectif de 4 Gio
- **Système d'exploitation** : Linux Mint 21.3 Virginia (64 bits)
- **Environnement de bureau** : Cinnamon 6.0.5 (serveur d'affichage X11)
- **Cible d'application** : 0 après J.-C. (Empires ascendants)

## Gestion et architecture de la mémoire
Sur les systèmes avec ≤ 6 Gio de RAM, l'exécution d'un environnement de bureau lourd, un jeu RTS 3D (0 A.D.) et la reconnaissance vocale nécessitent simultanément une protection stricte de la mémoire :

1. **Priorité du modèle vocal Vosk** :
- Utilise `vosk-model-small-de` (ou un langage équivalent) pour une faible empreinte mémoire (~ 300-500 Mo).
- La rétention du modèle Vosk est prioritaire pour garantir la réactivité des commandes en temps réel pendant le jeu.

2. **Expulsion automatique de LanguageTool** :
- Le processus Java de LanguageTool peut consommer environ 1,34 Gio RSS.
- Lorsque la RAM disponible descend en dessous de « CRITICAL_THRESHOLD_MB » (2,0 Gio), le « model_manager » d'Aura met immédiatement fin à LanguageTool pour libérer environ 1,3 Gio de RAM pour le jeu.
- Un temps de recharge de 5 minutes (`set_lingual_tool_cooldown`) empêche LanguageTool de redémarrer et de détruire la mémoire pendant le jeu actif.

## Commandes de vérification
Pour inspecter la mémoire système et les états des processus :
__CODE_BLOCK_0__
# Dépannage CopyQ macOS : interface graphique invisible et configuration manuelle des raccourcis clavier

Ce guide aborde les problèmes courants rencontrés sur macOS (en particulier les appareils Apple Silicon M-series) où l'interface graphique (GUI) CopyQ n'apparaît pas ou où les raccourcis globaux (tels que F10) doivent être réaffectés sans accéder à l'interface graphique.

---

## 1. Dépannage de l'interface graphique invisible

Sur macOS, CopyQ peut fonctionner correctement en arrière-plan tout en restant visuellement masqué pour deux raisons principales :
- **Coordonnées de la fenêtre hors écran** : suite à des changements de résolution ou à la déconnexion d'un moniteur externe, CopyQ peut conserver les coordonnées en dehors de la zone d'affichage visible.
- **Obstruction de l'encoche de la barre de menu** : sur les modèles de MacBook dotés d'une encoche pour l'appareil photo, macOS masque automatiquement les icônes de barre de menu en excès derrière l'encoche lorsque le plateau est plein.

### Solution : Réinitialiser l'affichage de la géométrie et de la force

Exécutez les commandes suivantes dans le terminal pour effacer les coordonnées hors écran et amener la fenêtre au premier plan :

```bash
copyq config geometry ""
copyq show
```

Si la fenêtre n'apparaît toujours pas, changez son état via CLI :

```bash
copyq toggle
```

---

## 2. Modification manuelle des raccourcis clavier à l'aide de CudaText

Lorsqu'un raccourci global (tel que « F10 ») est réclamé ou intercepté par une autre application, le raccourci peut être modifié directement dans le fichier de configuration à l'aide de CudaText sans ouvrir l'interface graphique de CopyQ.

### Étape 1 : Terminez le processus CopyQ

CopyQ doit être arrêté avant de modifier le fichier de configuration pour éviter qu'il n'écrase vos modifications à la fin :

```bash
copyq exit
```

### Étape 2 : Ouvrez la configuration dans CudaText

Sur macOS, les raccourcis des commandes CopyQ sont stockés dans `copyq-commands.ini`.

Ouvrez le fichier dans CudaText :

```bash
cudatext "$HOME/Library/Application Support/copyq/copyq-commands.ini"
```

*Remarque : si le fichier n'existe pas dans « Application Support », ouvrez l'emplacement de secours XDG :*

```bash
cudatext "$HOME/.config/copyq/copyq-commands.ini"
```

### Étape 3 : Réaffecter le raccourci

1- Dans CudaText, appuyez sur `Cmd + F` pour ouvrir la barre de recherche.
2- Recherchez `F10` ou `GlobalShortcut=F10`.
3- Remplacez « F10 » par un raccourci disponible (par exemple, « F9 » ou « Ctrl+F10 » ou « Meta+F10 »).
4- Enregistrez le fichier (`Cmd + S`) et fermez CudaText (`Cmd + Q`).

### Étape 4 : Redémarrez CopyQ

Redémarrez CopyQ pour charger la configuration de raccourci mise à jour :

```bash
open -a CopyQ
```

Le nouveau raccourci global sera désormais actif.

(mis à jour : 8.9.'26 08:01 mar)
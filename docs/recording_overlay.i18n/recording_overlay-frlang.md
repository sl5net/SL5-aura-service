# Superposition d'enregistrement (affichage à l'écran)

La superposition d'enregistrement fournit un indicateur visuel immédiat et multiplateforme de l'état de la dictée. Il fonctionne indépendamment des démons de notification du bureau et des filtres « Ne pas déranger », affichant l'état directement sur l'écran principal.

## Exemples visuels

| En bas à gauche (`bl`) | En haut à droite (`tr`) |
| :---: | :---: |
| ![Top-Right Overlay 1](../images/recording_overlay_1.png) | ![Top-Right Overlay 2](../images/recording_2.png) |
| *Se fond dans les panneaux sombres et les barres d'état système* | *Contraste élevé sur des fenêtres claires ou complexes* |

## États

- **Enregistrement (`🔴`)** : Un cercle rouge vif avec un contour en surbrillance (`#e62222` sur `#181818`) signale un enregistrement audio actif.
- **Inactif**:
- `hidden` (par défaut) : La fenêtre est complètement retirée, libérant de l'espace sur le bureau pour une interaction normale.
- `pentagon` : affiche un subtil badge de pentagone géométrique (`⬟`) en mode veille.

##Configuration

Les paramètres sont gérés dans `config/settings.py` :

```python
# Enable/disable on-screen overlay
RECORDING_OVERLAY_ENABLED = True

# Keep window always on top without borders
RECORDING_OVERLAY_TOPMOST = True

# Placement: "tr" (top-right) or "bl" (bottom-left)
RECORDING_OVERLAY_POSITION = "tr"

# Inactivity mode: "hidden" or "pentagon"
RECORDING_OVERLAY_IDLE_MODE = "hidden"

# Window dimension in pixels
RECORDING_OVERLAY_SIZE = 36
```

## Architecture

- Construit à l'aide de la bibliothèque standard Python (`tkinter`), ne nécessitant aucune dépendance C externe.
- S'exécute dans un thread démon en arrière-plan avec une gestion des événements de file d'attente thread-safe.
- Détecte dynamiquement le moniteur principal dans les environnements multi-écrans.

(s, 10.9.'26 14:41 jeu.)
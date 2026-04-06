[![SikuliX](https://raw.githubusercontent.com/oculix-org/SikuliX1/master/Support/sikulix-red.png)](https://sikulix.github.io)
# Framework d'automatisation visuelle optimisé par Computer Vision
**Si vous pouvez le voir, vous pouvez l'automatiser.**

SikuliX est désormais activement maintenu sous [**oculix-org**](https://github.com/oculix-org), avec le plein accord de son créateur d'origine [**RaiMan**](https://github.com/RaiMan).

## Qu'est-ce que SikuliX
SikuliX utilise la **vision par ordinateur** (optimisée par [OpenCV](https://opencv.org/)) pour identifier et interagir avec tout ce qui est visible sur votre écran, sous **Windows**, **macOS** et **Linux**.

Il localise les éléments de l'interface graphique grâce à la **reconnaissance d'image**, puis les pilote avec des actions simulées de la souris et du clavier. Aucun accès au code source, au DOM ou aux API internes requis.

## Plugin Aura
Ce plugin vous permet de dicter les commandes SikuliX vocalement pendant que l'IDE SikuliX est au point.

| Commande vocale (de) | Sortie |
|---|---|
| "cliquez" | `cliquez("image.png")` |
| "double clic" | `doubleClick("image.png")` |
| "droit droit" | `rightClick("image.png")` |
| "verte" | `attendre("image.png", 10)` |

Les commandes ne sont actives que lorsqu'une fenêtre SikuliX (`sikulixide`, `SikuliX`, `Sikuli`) est focalisée.

## Ressources
- [Get SikuliX ready to use](https://raimans-sikulix.gitbook.io/untitled/)
- [SikuliX Documentation](https://sikulix-2014.readthedocs.io/en/latest/index.html)
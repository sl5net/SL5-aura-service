## Utilitaires de projet : séparateur et téléchargeur de fichiers

Ce référentiel comprend deux puissants scripts Python conçus pour gérer la distribution et le téléchargement de fichiers volumineux via les versions GitHub.

1. **`split_and_hash.py`** : un utilitaire permettant aux propriétaires de référentiels de diviser des fichiers volumineux en parties plus petites et de générer un manifeste de somme de contrôle complet et vérifiable.
2. **`download_all_packages.py`** : un outil robuste permettant aux utilisateurs finaux de télécharger, vérifier et réassembler automatiquement ces fichiers en plusieurs parties, garantissant l'intégrité des données du début à la fin.

---

### 1. Script de fractionnement de fichiers et de génération de somme de contrôle (`split_and_hash.py`)

Ce script est destiné au **mainteneur du référentiel**. Il prépare des fichiers volumineux pour la distribution sur des plates-formes telles que GitHub Releases, qui ont des limites de taille de fichier individuelles.

#### But

L'objectif principal est de prendre un seul gros fichier (par exemple, `vosk-model-de-0.21.zip`) et d'effectuer deux actions critiques :
1. Divisez le fichier en une série de parties plus petites et numérotées.
2. Générez un fichier manifeste unique et complet (`.sha256sums.txt`) qui contient les sommes de contrôle pour **à la fois le fichier original complet et chaque partie individuelle**.

Ce manifeste complet est la clé pour garantir une intégrité des données à 100 % pour l'utilisateur final.

#### Principales fonctionnalités

* **Partage standardisé :** Divise les fichiers en morceaux de 100 Mo (configurables dans le script).
* **Nom cohérent :** Crée des pièces avec un préfixe `Z_` (par exemple, `Z_vosk-model-de-0.21.zip.part.aa`). Le préfixe « Z_ » garantit un tri et une manipulation appropriés dans divers systèmes.
* **Manifeste d'intégrité complet :** Le fichier `.sha256sums.txt` généré est structuré pour une fiabilité maximale. Il comprend :
* Le hachage SHA256 du **fichier original complet**.
* Le hachage SHA256 de **chaque pièce** créée.

#### Utilisation pour une version de GitHub

1. Placez le gros fichier (par exemple, `vosk-model-de-0.21.zip`) dans un répertoire avec le script `split_and_hash.py`.
2. Exécutez le script depuis votre terminal :
    ```bash
    python split_and_hash.py <your-large-file.zip>
    ```
3. Le script générera tous les fichiers `Z_...part.xx` et le fichier `...sha256sums.txt` correspondant.
4. Lors de la création d'une nouvelle version de GitHub, téléchargez **tous** les fichiers générés : les fichiers de pièce et le fichier manifeste unique.
5. Répétez ce processus pour chaque fichier volumineux que vous souhaitez distribuer.

---

### 2. Téléchargeur et vérificateur automatisé de packages (`download_all_packages.py`)

Ce script est destiné à l'**utilisateur final**. Il fournit une solution simple, à une seule commande, pour télécharger et réassembler de manière fiable tous les packages proposés dans la version GitHub.

#### But

Il automatise le processus autrement complexe et sujet aux erreurs consistant à télécharger des dizaines de parties de fichiers, à vérifier chacune d'entre elles et à les réassembler correctement. Il utilise les manifestes de somme de contrôle fournis dans la version pour garantir que le fichier final assemblé est une copie parfaite et non corrompue de l'original.

#### Principales fonctionnalités

* **Découverte automatique :** Le script se connecte à l'API GitHub pour rechercher automatiquement tous les « packages » disponibles dans la version en recherchant les fichiers `.sha256sums.txt`. Aucune configuration manuelle des noms de fichiers n'est nécessaire.
* **Processus axé sur l'intégrité :** Pour chaque package, il télécharge *d'abord* le fichier manifeste pour obtenir la liste des pièces requises et leurs sommes de contrôle correctes.
* **Vérification pièce par pièce :** Il télécharge une partie à la fois et vérifie immédiatement son hachage SHA256.
* **Réessai automatique en cas de corruption :** Si une partie téléchargée est corrompue (le hachage ne correspond pas), le script la supprime automatiquement et la télécharge à nouveau, garantissant ainsi un téléchargement propre.
* **Réassemblage intelligent :** Une fois que toutes les parties d'un package sont téléchargées et vérifiées, il les fusionne dans le bon ordre alphabétique (`.aa`, `.ab`, `.ac`...) pour reconstruire le gros fichier d'origine.
* **Vérification finale :** Après le réassemblage, il calcule le hachage SHA256 du fichier final complet et le vérifie par rapport au hachage maître trouvé dans le manifeste. Cela fournit une confirmation de bout en bout du succès.
* **Résilient et tolérant :** Le script est robuste contre les incohérences de dénomination mineures, telles que `Z_` contre `z_`, garantissant une expérience utilisateur fluide.
* **Nettoyage automatisé :** Une fois qu'un package est créé et vérifié avec succès, le script supprime les fichiers de pièces téléchargés pour économiser de l'espace disque.

#### Prérequis

L'utilisateur doit avoir Python et les bibliothèques `requests` et `tqdm` installés. Ils peuvent être installés avec pip :
```bash
pip install requests tqdm
```

#### Utilisation

1. Téléchargez le script `download_all_packages.py`.
2. Exécutez-le depuis le terminal sans argument :
    ```bash
    python download_all_packages.py
    ```
3. Le script s'occupera du reste, affichant des barres de progression et des messages d'état. Une fois terminé, l'utilisateur disposera de tous les fichiers ZIP finaux et vérifiés, prêts à être utilisés dans le même répertoire.
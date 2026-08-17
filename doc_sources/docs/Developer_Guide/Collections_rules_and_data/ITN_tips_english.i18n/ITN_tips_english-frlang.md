Le terme technique est **normalisation de texte inverse (ITN)**.

Si vous le recherchez, vous trouverez d’énormes collections de règles et de données.

Voici les meilleures ressources pour remplir des cartes sans tout saisir vous-même :

### 1. Collections de règles ITN (le « gold standard »)
* **[itnpy](https://github.com/barseghyanartur/itnpy) :** Un outil Python simple et déterministe conçu dans ce but précis. Il utilise des fichiers CSV pour convertir les mots prononcés en caractères écrits (chiffres, devises, dates). Vous pouvez copier les CSV presque 1:1 dans votre carte.

* **[NVIDIA NeMo ITN](https://github.com/NVIDIA/NeMo) :** Très puissant. Ils ont d’énormes fichiers de grammaire pour presque toutes les langues. Vous y trouverez des listes d'unités de mesure, de titres et de formats de date.

### 2. Sources de données pour la ponctuation et la casse
* **[Vosk recasepunc](https://github.com/benob/recasepunc) :** Il s'agit de l'outil standard pour Vosk. Il utilise des modèles, mais le code source contient souvent des listes d'abréviations et de noms propres pouvant être extraits.

* **[Google Text Normalization Dataset](https://github.com/rwsproat/text-normalization-data) :** Un énorme ensemble de données (créé pour un défi Kaggle) contenant des millions d'exemples sur la façon dont la langue parlée est convertie en langue écrite.

### 3. Bibliothèques « Aide à la dictée »
* **[num2words](https://github.com/savoirfairelinux/num2words) :** Si vous avez besoin d'un mappage de numéros, vous pouvez trouver des listes de « un » à « un million » ici.
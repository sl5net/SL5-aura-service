der Fachbegriff est la **normalisation de texte inverse (ITN)**.

Wenn du danach suchst, findest du riesige Sammlungen von Regeln und Daten.

Voici les meilleures ressources pour remplir Maps, sans tout vous-même :

### 1. ITN-Regel-Sammlungen (Der "Goldstandard")
* **[itnpy](https://github.com/barseghyanartur/itnpy):** Un outil Python déterministe créé pour cette tâche. Il s'agit d'un CSV-Dateien, un gesprochene Wörter in geschriebene Zeichen (Zahlen, Währungen, Daten) zu verwandeln. Les CSV peuvent être rapides 1:1 dans votre copie de carte.

* **[NVIDIA NeMo ITN](https://github.com/NVIDIA/NeMo) :** Sehr mächtig. Vous avez des dates de grammaire rapides pour tous les textes. Dort findest du Listen für Maßeinheiten, Titel und Datumsformate.

### 2. Datenquellen pour la ponctuation et la casse
* **[Vosk recasepunc](https://github.com/benob/recasepunc) :** Il s'agit de l'outil standard pour Vosk. Es nutzt zwar Modelle, aber im Quellcode finden sich oft Listen für Abkürzungen und Eigennamen, die man extrahieren kann.

* **[Google Text Normalization Dataset](https://github.com/rwsproat/text-normalization-data) :** Une date plus récente (pour un défi Kaggle créé), der Millionen von Beispielen enthält, comme la langue gesprochene (`parlée`) dans la langue geschriebene (`écrit`) umgewandelt wird.

### 3. Bibliothèque « Diktat-Helfer »
* **[num2words](https://github.com/savoirfairelinux/num2words) :** Lorsque le Zahlen-Mapping est disponible, vous pouvez vous diriger ici vers l'écoute pour "un" jusqu'à "un million" généré.
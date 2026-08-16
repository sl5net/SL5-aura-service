der Fachbegriff ist **Normalización de texto inverso (ITN)**.

Wenn du danach suchst, findest du riesige Sammlungen von Regeln und Daten.

Aquí se encuentran los mejores recursos, para completar los mapas, sin incluir todos los consejos:

### 1. ITN-Regel-Sammlungen (Der "Goldstandard")
* **[itnpy](https://github.com/barseghyanartur/itnpy):** Una herramienta determinista de Python propiamente dicha para este espacio. Es nutzt CSV-Dateien, um gesprochene Wörter in geschriebene Zeichen (Zahlen, Währungen, Daten) zu verwandeln. Los CSV pueden copiarse rápidamente 1:1 en cada mapa.

* **[NVIDIA NeMo ITN](https://github.com/NVIDIA/NeMo):** Sehr mächtig. Sie haben riesige Grammatik-Dateien für fast alle Sprachen. Dort findest du Listen für Maßeinheiten, Titel and Datumsformate.

### 2. Fechas de puntuación y mayúsculas y minúsculas
* **[Vosk recasepunc](https://github.com/benob/recasepunc):** Esta es la herramienta estándar para voz. Es nutzt zwar Modelle, aber im Quellcode finden sich oft Listen für Abkürzungen und Eigennamen, die man extrahieren kann.

* **[Google Text Normalization Dataset](https://github.com/rwsproat/text-normalization-data):** Ein riesiger Datensatz (für eine Kaggle-Challenge erstellt), der Millionen von Beispielen enthält, wie gesprochene Sprache (`hablado`) in geschriebene (`escrito`) umgewandelt wird.

### 3. Biblioteca "Diktat-Helfer"
* **[num2words](https://github.com/savoirfairelinux/num2words):** Cuando se activa Zahlen-Mapping, puede escuchar aquí "eins" bis "eine Million" generados.
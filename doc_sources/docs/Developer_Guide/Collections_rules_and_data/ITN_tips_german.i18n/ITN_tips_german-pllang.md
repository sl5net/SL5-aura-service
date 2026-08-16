der Fachbegriff ist **Odwrotna normalizacja tekstu (ITN)**.

Wenn du danach suchst, findest du riesige Sammlungen von Regeln und Daten.

Hier sind die besten Ressourcen, um Maps zu befüllen, ohne alles selbst zu tippen:

### 1. ITN-Regel-Sammlungen (Der „Goldstandard”)
* **[itnpy](https://github.com/barseghyanartur/itnpy):** Umożliwia deterministyczne narzędzie Python-Tool dla diesen Zweck. Es nutzt CSV-Dateien, um gesprochene Wörter in geschriebene Zeichen (Zahlen, Währungen, Daten) zu verwandeln. Można szybko kopiować CSV 1:1 w kopiowaniu map.

* **[NVIDIA NeMo ITN](https://github.com/NVIDIA/NeMo):** Sehr mächtig. Sie haben riesige Grammatik-Dateien für fast alle Sprachen. Dort findest du Listen für Maßeinheiten, Titel und Datumsformate.

### 2. Data dla interpunkcji i wielkości liter
* **[Vosk recasepunc](https://github.com/benob/recasepunc):** Jest to standardowe narzędzie dla Vosk. Es nutzt zwar Modelle, aber im Quellcode finden sich często Listen für Abkürzungen und Eigennamen, die man extrahieren kann.

* **[Google Text Normalization Dataset](https://github.com/rwsproat/text-normalization-data):** Ein riesiger Datensatz (für eine Kaggle-Challenge erstellt), der Millionen von Beispielen enthält, wie gesprochene Sprache („mówione”) in geschriebene („pisane”) umgewandelt wird.

### 3. Bibliotheken „Diktat-Helfer”.
* **[num2words](https://github.com/savoirfairelinux/num2words):** Wenn du Zahlen-Mapping brauchst, możesz dir hier die Listen für „eins” bis „eine Million” generieren lassen.
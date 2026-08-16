der Fachbegriff ist **Inverse Text Normalization (ITN)**. 

Wenn du danach suchst, findest du riesige Sammlungen von Regeln und Daten.

Hier sind die besten Ressourcen, um Maps zu befüllen, ohne alles selbst zu tippen:

### 1. ITN-Regel-Sammlungen (Der "Goldstandard")
*   **[itnpy](https://github.com/barseghyanartur/itnpy):** Ein einfaches, deterministisches Python-Tool genau für diesen Zweck. Es nutzt CSV-Dateien, um gesprochene Wörter in geschriebene Zeichen (Zahlen, Währungen, Daten) zu verwandeln. Die CSVs kannst du fast 1:1 in deine Map kopieren.

*   **[NVIDIA NeMo ITN](https://github.com/NVIDIA/NeMo):** Sehr mächtig. Sie haben riesige Grammatik-Dateien für fast alle Sprachen. Dort findest du Listen für Maßeinheiten, Titel und Datumsformate.

### 2. Datenquellen für Punctuation & Case
*   **[Vosk recasepunc](https://github.com/benob/recasepunc):** Das ist das Standard-Tool für Vosk. Es nutzt zwar Modelle, aber im Quellcode finden sich oft Listen für Abkürzungen und Eigennamen, die man extrahieren kann.

*   **[Google Text Normalization Dataset](https://github.com/rwsproat/text-normalization-data):** Ein riesiger Datensatz (für eine Kaggle-Challenge erstellt), der Millionen von Beispielen enthält, wie gesprochene Sprache (`spoken`) in geschriebene (`written`) umgewandelt wird.

### 3. "Diktat-Helfer" Bibliotheken
*   **[num2words](https://github.com/savoirfairelinux/num2words):** Wenn du Zahlen-Mapping brauchst, kannst du dir hier die Listen für „eins“ bis „eine Million“ generieren lassen.


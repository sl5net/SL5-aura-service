Der Fachbegriff lautet **Inverse Text Normalization (ITN)**.

Wer danach sucht, findet riesige Sammlungen an Regeln und Daten.

Hier sind die besten Ressourcen zum Ausfüllen von Karten, ohne alles selbst eingeben zu müssen:

### 1. ITN-Regelsammlungen (der „Goldstandard“)
* **[itnpy](https://github.com/barseghyanartur/itnpy):** Ein einfaches, deterministisches Python-Tool, das genau für diesen Zweck entwickelt wurde. Es verwendet CSV-Dateien, um gesprochene Wörter in geschriebene Zeichen (Zahlen, Währungen, Datumsangaben) umzuwandeln. Sie können die CSVs nahezu 1:1 in Ihre Karte kopieren.

* **[NVIDIA NeMo ITN](https://github.com/NVIDIA/NeMo):** Sehr mächtig. Sie haben riesige Grammatikdateien für fast alle Sprachen. Dort finden Sie Listen für Maßeinheiten, Titel und Datumsformate.

### 2. Datenquellen für Interpunktion und Groß-/Kleinschreibung
* **[Vosk recasepunc](https://github.com/benob/recasepunc):** Dies ist das Standardtool für Vosk. Es werden Modelle verwendet, der Quellcode enthält jedoch häufig Listen mit Abkürzungen und Eigennamen, die extrahiert werden können.

* **[Google Text Normalization Dataset](https://github.com/rwsproat/text-normalization-data):** Ein riesiger Datensatz (erstellt für eine Kaggle-Herausforderung), der Millionen von Beispielen dafür enthält, wie gesprochene Sprache in geschriebene Sprache umgewandelt wird.

### 3. „Diktierhilfs“-Bibliotheken
* **[num2words](https://github.com/savoirfairelinux/num2words):** Wenn Sie eine Zahlenzuordnung benötigen, finden Sie hier Listen für „eins“ bis „eine Million“.
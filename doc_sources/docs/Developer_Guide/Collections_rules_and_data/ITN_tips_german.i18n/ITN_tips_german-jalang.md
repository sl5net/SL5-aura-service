**逆テキスト正規化 (ITN)** が Fachbegriff です。

Wenn du danach suchst, findest du riesige Sammlungen von Regeln und Daten.

Hier sind die besten Ressourcen, um Maps zu befüllen, ohne alles selbst zutippen:

### 1. ITN-Regel-Sammlungen (「ゴールドスタンダード」)
* **[itnpy](https://github.com/barseghyanartur/itnpy):** Zweck 用の Python ツールを使用して決定します。 CSV-Dateien を参照してください。Zahlen、Währungen、Daten の geschriebene Zeichen の guesprochene Wörter zu verwandeln です。 Die CSVs kannst du fast 1:1 in deine Map kopieren.

* **[NVIDIA NeMo ITN](https://github.com/NVIDIA/NeMo):** 機能。 Grammatik-Dateien für fast alle Sprachen を参照してください。メインハイテン、タイトルとデータ形式を聞いてください。

### 2. 句読点と大文字小文字の区別
* **[Vosk recasepunc](https://github.com/benob/recasepunc):** Vosk の標準ツールです。 Es Nutzt zwar Modelle, aber im Quellcode finden sich offt Listen für Abkürzungen und Eigenname, die man extrahieren kann.

* **[Google Text Normalization Dataset](https://github.com/rwsproat/text-normalization-data):** Ein riesiger Datensatz (für eine Kaggle-Challenge erstellt), der Millionen von Beispielen enthält, wie gesprochene Sprache (`spoken`) in geschriebene (`Written`) umgewandelt wird。

### 3.「ディクタット・ヘルファー」図書館
* **[num2words](https://github.com/savoirfairelinux/num2words):** Wenn du Zahlen-Mapping brauchst、kannst du dir hier die の「eins」と「eine Million」の生成を聞いてください。
der Fachbegriff ist **逆文本规范化 (ITN)**。

Wenn du danach suchst，findest du riesige Sammlungen von Regeln und Daten。

如果您有最好的资源，请使用地图，请注意以下几点：

### 1. ITN-Regel-Sammlungen（“黄金标准”）
* **[itnpy](https://github.com/barseghyanartur/itnpy):** 是 Zweck 的决定论 Python 工具。 Es nutzt CSV-Dateien, um gesprochene Wörter in geschriebene Zeichen (Zahlen, Währungen, Daten) zu verwandeln. CSV 在 deine Map kopieren 中以 1:1 的速度快速进行。

* **[NVIDIA NeMo ITN](https://github.com/NVIDIA/NeMo)：** Sehr mächtig。请参阅快速语言的语法日期。 Dort findest du Listen für Maßeinheiten、标题和数据格式。

### 2. 标点符号和大小写的日期
* **[Vosk recasepunc](https://github.com/benob/recasepunc)：** 这是 Vosk 的标准工具。 Es nutzt zwar Modelle, aber im Quellcode finden sich oft Listen für Abkürzungen und Eigennamen, die man extrahieren kann.

* **[Google Text Normalization Dataset](https://github.com/rwsproat/text-normalization-data):** Ein riesiger Datensatz (für eine Kaggle-Challenge erstellt), der Millionen von Beispielen enthält, wie gesprochene Sprache (`spoken`) in geschriebene (`writing`) umgewandelt wird.

### 3.“Diktat-Helfer”图书馆
* **[num2words](https://github.com/savoirfairelinux/num2words):** Wenn du Zahlen-Mapping brauchst，可以在下面聆听“eins” bis “eine Million” Generieren lassen。
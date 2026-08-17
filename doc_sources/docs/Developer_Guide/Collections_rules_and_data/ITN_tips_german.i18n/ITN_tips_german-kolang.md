der Fachbegriff ist **역 텍스트 정규화(ITN)**.

Wenn du danach suchst, findest du riesige Sammlungen von Regeln und Daten.

Hier sind die besten Ressourcen, um Maps zu befüllen, ohne alles selbst zutippen:

### 1. ITN-Regel-Sammlungen(Der "Goldstandard")
* **[itnpy](https://github.com/barseghyanartur/itnpy):** Zweck을 위한 Python 도구가 결정적으로 결정되었습니다. Es nutzt CSV-Dateien, um gesprochene Wörter in geschriebene Zeichen(Zahlen, Währungen, Daten) zu verwandeln. 지도 복사에서 CSV를 1:1로 빠르게 확인하세요.

* **[NVIDIA NeMo ITN](https://github.com/NVIDIA/NeMo):** Sehr mächtig. Sie haben riesige Grammatik-Dateien für fast alle Sprachen. Dort findest du Listen für Maßeinheiten, Titel und Datumsformate.

### 2. 구두점 및 대소문자에 대한 날짜
* **[Vosk recasepunc](https://github.com/benob/recasepunc):** Das ist das Standard-Tool for Vosk. Es nutzt zwar Modelle, aber im Quellcode finden sich oft Listen für Abkürzungen und Eigennamen, die man extrahieren kann.

* **[Google Text Normalization Dataset](https://github.com/rwsproat/text-normalization-data):** Ein riesiger Datensatz (für eine Kaggle-Challenge erstellt), der Millionen von Beispielen enthält, wie gesprochene Sprache (`spoken`) in geschriebene (`writing`) umgewandelt wird.

### 3. "Diktat-Helfer" 비블리오테켄
* **[num2words](https://github.com/savoirfairelinux/num2words):** Wenn du Zahlen-Mapping brauchst, kannst du dir hier die Listen für "eins" bis "eine Million" generieren lassen.
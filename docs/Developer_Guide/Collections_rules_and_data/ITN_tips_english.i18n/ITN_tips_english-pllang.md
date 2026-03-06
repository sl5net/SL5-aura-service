Termin techniczny to **Odwrotna normalizacja tekstu (ITN)**.

Jeśli go wyszukasz, znajdziesz ogromne zbiory reguł i danych.

Oto najlepsze zasoby do wypełniania map bez wpisywania wszystkiego samodzielnie:

### 1. Zbiór reguł ITN („złoty standard”)
* **[itnpy](https://github.com/barseghyanartur/itnpy):** Proste, deterministyczne narzędzie Pythona zaprojektowane właśnie do tego celu. Wykorzystuje pliki CSV do konwersji mówionych słów na znaki pisane (cyfry, waluty, daty). Możesz skopiować pliki CSV prawie 1:1 na swoją mapę.

* **[NVIDIA NeMo ITN](https://github.com/NVIDIA/NeMo):** Bardzo mocny. Mają ogromne pliki gramatyczne dla prawie wszystkich języków. Znajdziesz tam listy jednostek miar, tytułów i formatów dat.

### 2. Źródła danych dotyczące interpunkcji i wielkości liter
* **[Vosk recasepunc](https://github.com/benob/recasepunc):** To standardowe narzędzie dla Voska. Używa modeli, ale kod źródłowy często zawiera listy skrótów i nazw własnych, które można wyodrębnić.

* **[Google Text Normalization Dataset](https://github.com/rwsproat/text-normalization-data):** Ogromny zbiór danych (stworzony na potrzeby wyzwania Kaggle) zawierający miliony przykładów konwersji języka mówionego na język pisany.

### 3. Biblioteki „Pomocnik dyktowania”.
* **[num2words](https://github.com/savoirfairelinux/num2words):** Jeśli potrzebujesz mapowania liczb, tutaj znajdziesz listy od „jednego” do „jednego miliona”.
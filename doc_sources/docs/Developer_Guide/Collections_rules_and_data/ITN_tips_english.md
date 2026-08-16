The technical term is **Inverse Text Normalization (ITN)**. 

If you search for it, you will find huge collections of rules and data.

Here are the best resources for filling maps without typing everything yourself:

### 1. ITN rule collections (the “gold standard”)
*   **[itnpy](https://github.com/barseghyanartur/itnpy):** A simple, deterministic Python tool designed for this very purpose. It uses CSV files to convert spoken words into written characters (numbers, currencies, dates). You can copy the CSVs almost 1:1 into your map.

* **[NVIDIA NeMo ITN](https://github.com/NVIDIA/NeMo):** Very powerful. They have huge grammar files for almost all languages. There you will find lists for units of measurement, titles, and date formats.

### 2. Data sources for punctuation & case
* **[Vosk recasepunc](https://github.com/benob/recasepunc):** This is the standard tool for Vosk. It uses models, but the source code often contains lists of abbreviations and proper names that can be extracted.

*   **[Google Text Normalization Dataset](https://github.com/rwsproat/text-normalization-data):** A huge dataset (created for a Kaggle challenge) containing millions of examples of how spoken language is converted into written language.

### 3. “Dictation helper” libraries
* **[num2words](https://github.com/savoirfairelinux/num2words):** If you need number mapping, you can find lists for “one” to “one million” here.


> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../ITN_tips_german.md).*

The technical term is **Inverse Text Normalization (ITN)**.

If you search for it, you will find huge collections of rules and data.

Here are the best resources to fill maps without typing everything yourself:

ITN Rule Collections (The "Gold Standard")
*   **[itnpy](https://github.com/barseghyanartur/itnpy):** A simple, deterministic Python tool for this purpose. It uses CSV files to turn spoken words into written characters (numbers, currencies, data). You can copy the CSVs almost 1:1 into your map.

*   **[NVIDIA NeMo ITN](https://github.com/NVIDIA/NeMo):** Very powerful. They have huge grammar files for almost all languages. There you will find lists for units, titles and date formats.

### Data sources for Punctuation & Case
*   **[Vosk recasepunc](https://github.com/benob/recasepunc):** This is the standard tool for Vosk. It uses models, but the source code often contains lists of abbreviations and proper names that can be extracted.

*   **[Google Text Normalization Dataset](https://github.com/rwsproat/text-normalization-data):** A huge data set (created for a Kaggle challenge) that contains millions of examples of how spoken language (`spoken`) is converted to written (`written`).

### 3. "Dictation Helper" Libraries
*   **[num2words](https://github.com/savoirfairelinux/num2words):** If you need number mapping, you can generate the lists here for 'one' to 'one million'.


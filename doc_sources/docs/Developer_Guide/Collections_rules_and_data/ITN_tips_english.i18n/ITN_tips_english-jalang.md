技術用語は **逆テキスト正規化 (ITN)** です。

検索すると、膨大なルールとデータのコレクションが見つかります。

すべてを自分で入力せずにマップを埋めるための最適なリソースは次のとおりです。

### 1. ITN ルール コレクション (「ゴールド スタンダード」)
* **[itnpy](https://github.com/barseghyanartur/itnpy):** まさにこの目的のために設計された、シンプルで決定的な Python ツール。 CSV ファイルを使用して、話し言葉を文字 (数字、通貨、日付) に変換します。 CSV をほぼ 1:1 でマップにコピーできます。

* **[NVIDIA NeMo ITN](https://github.com/NVIDIA/NeMo):** 非常に強力です。ほぼすべての言語に対応する巨大な文法ファイルがあります。そこには、測定単位、タイトル、日付形式のリストがあります。

### 2. 句読点と大文字小文字のデータ ソース
* **[Vosk recasepunc](https://github.com/benob/recasepunc):** これは Vosk の標準ツールです。モデルを使用しますが、ソース コードには、抽出できる略語や固有名のリストが含まれることがよくあります。

* **[Google Text Normalization Dataset](https://github.com/rwsproat/text-normalization-data):** 話し言葉が書き言葉にどのように変換されるかを示す数百万の例を含む巨大なデータセット (Kaggle チャレンジ用に作成)。

### 3.「ディクテーションヘルパー」ライブラリ
* **[num2words](https://github.com/savoirfairelinux/num2words):** 数値マッピングが必要な場合は、ここで「1」から「100 万」までのリストを見つけることができます。
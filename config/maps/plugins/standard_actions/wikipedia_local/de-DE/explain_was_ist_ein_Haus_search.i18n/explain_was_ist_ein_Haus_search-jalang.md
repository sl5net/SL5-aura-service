# システムのワークフローの正確な動作を明確にします。
  
### 統合ワークフローの説明を修正

最後の検索アクションが 2 番目のルールによって実行される前に、**入力変換** と **ラベル付け** の最初のルールが実行されます。

#### 1. 入力:「was ist ein haus」

#### 2. ルール 1: ラベル付け/変換

```python
("was ist ein haus (Begriffsklärung)", r'^.*was ist ein haus$', 90,
 {'flags': re.IGNORECASE, 'skip_list': ['LanguageTool','fullMatchStop']})
```

* **アクション:** ユーザー入力 `"was ist ein haus"` は正常に照合されました。
* **結果 (内部):** システムは出力/ラベル `"was ist ein haus (Begriffsklärung)"` を生成します。
* **続き:** `fullMatchStop` が `skip_list` にあるため、ルールのマッチングは **停止しません**。プロセスは次のルールに進み、*変換された* または *ラベルが付けられた* コンテンツを運びます。

#### 3. ルール 2: 一般的なアクション/実行

```python
('', r'(suche auf wikipedia nach|was sind|was ist|wer ist|wo ist|Wie groß ist)( ein| die| das| der)? (?P<search>.*)', 90, {
'flags': re.IGNORECASE,
'on_match_exec': [CONFIG_DIR / 'wikipedia_local.py']
})
```

* **アクション:** システムは、前のステップの **現在の結果/ラベル** (「was ist ein haus (Begriffsklärung)」) と一致する可能性があります (または、元の入力と一致しますが、実行されたスクリプトは変換されたラベルを優先します)。
* **プレフィックス一致:** プレフィックス (`was ist`) は依然として一致します。
* **キャプチャ グループ:** キャプチャ グループ `(?P<search>.*)` は文字列の残りの部分をキャプチャします。
* システムが **ルール 1 出力を新しい入力**として使用する場合、**`haus (Begriffsklärung)`** (または、実行スクリプトによって解析される完全な変換された文字列) をキャプチャします。
* **実行:** `wikipedia_local.py` スクリプトが実行されます。

#### 4. 最終アクション:

* `wikipedia_local.py` スクリプトは、特別に変更された検索語/ラベルを受け取ります。
* スクリプトは、目的の用語 **`haus (Begriffsklärung)`** の Wikipedia 検索を実行します。

**結論：**

この設定は、あいまいなクエリまたは一般的なクエリを処理するための洗練された方法です。特定のルールで入力を変更するか対象のラベルを生成してから、プロセスを一般的な検索ルールに継続させることにより、Wikipedia 検索が一般的な「ハウス」ではなく、曖昧さのない特定のエントリ: **`haus (Begriffsklärung)`** に対して実行されるようになります。

これは、最初のルールが汎用実行ルールによって作用される前にクエリを前処理して強化できるようにするために、`fullMatchStop` の除外が**必須**であることを確認します。

(sl5,4.12.'25 12:24 木)
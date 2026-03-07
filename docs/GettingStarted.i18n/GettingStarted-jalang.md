# SL5 Aura の入門

## SL5 オーラとは何ですか?

SL5 Aura は、音声をテキスト (STT) に変換し、構成可能なルールを適用して出力をクリーンアップ、修正、変換するオフラインファーストの音声アシスタントです。

GUI なしで動作します。すべてが CLI またはコンソール経由で実行されます。

## 仕組み

```
Microphone → Vosk (STT) → Maps (Pre) → LanguageTool → Maps (Post) → Output
```

1. **Vosk** があなたのスピーチを生のテキストに変換します
2. **Pre-Maps** は、スペルチェックの前にテキストをクリーンアップして修正します。
3. **LanguageTool** は文法とスペルを修正します
4. **ポストマップ**は最終的な変換を適用します
5. **出力** は最終的なクリーン テキスト (およびオプションで TTS) です。

## あなたの最初の一歩

### 1. オーラを開始する
```bash
python main.py
```

### 2. コンソール入力によるテスト
「s」と入力し、その後にテキストを入力します。
```
s hello world
```

### 3. ルールの動作を確認する
`config/maps/koans_deutsch/01_koan_erste_schritte/de-DE/FUZZY_MAP_pre.py` を開きます

内部のルールのコメントを解除して、再度テストします。何が起こるのですか？

## ルールを理解する

ルールは、`FUZZY_MAP_pre.py` または `FUZZY_MAP.py` という Python ファイルの `config/maps/` に存在します。

ルールは次のようになります。
```python
('Hello World', r'\bhello world\b', 0, {'flags': re.IGNORECASE})
#   ^output        ^pattern          ^threshold  ^case-insensitive
```

**出力**が最初に表示されます。ルールによって何が生成されるかがすぐにわかります。

ルールは **上から下**に処理されます。最初の完全一致 (`^...$`) はすべてを停止します。

## 公案 – 実践による学習

Koan は、`config/maps/koans_deutsch/` および `config/maps/koans_english/` にある小さな演習です。

各公案は 1 つの概念を教えています。

|幸庵 |トピック |
|---|---|
| 01_koan_erste_schritte | 01_koan_erste_schritte最初のルール、完全一致、パイプライン停止 |
| 02_koan_listen |リスト、複数のルール |
| 03_koan_schwierige_name |難しい名前、発音の一致 |

Koan 01 から始めて、徐々にレベルを上げてください。

## ヒント

- `FUZZY_MAP_pre.py` のルールはスペル チェックの **前** に実行されます – STT エラーの修正に適しています
- `FUZZY_MAP.py` のルールはスペル チェックの **後** に実行されます – 書式設定に適しています
- 変更前にバックアップ ファイル (`.peter_backup`) が自動的に作成されます
- `peter.py` を使用して AI に公案を自動的に実行させます
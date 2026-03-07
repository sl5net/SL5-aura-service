# FUZZY_MAP ルールガイド

## ルールの形式

```python
('replacement', r'regex_pattern', threshold, {'flags': re.IGNORECASE})
```

|ポジション |名前 |説明 |
|---|---|---|
| 1 |交換 |ルールが | に一致した後の出力テキスト
| 2 |パターン |照合する正規表現またはあいまい文字列 |
| 3 |しきい値 |正規表現ルールでは無視されます。あいまい一致に使用 (0 ～ 100) |
| 4 |フラグ |大文字と小文字を区別しない場合は `{'flags': re.IGNORECASE}`、大文字と小文字を区別する場合は `0` |

## パイプライン ロジック

- ルールは **トップダウン** で処理されます
- **すべて**の一致ルールが適用されます (累積)
- **完全一致** (`^...$`) はパイプラインを即座に停止します
- 前のルールが後のルールより優先されます。

## 一般的なパターン

### 単一の単語 (単語境界) に一致します
```python
('Python', r'\bpython\b', 0, {'flags': re.IGNORECASE})
```

### 複数のバリアントを照合する
```python
('OpenAI', r'\bopen\s*ai\b', 0, {'flags': re.IGNORECASE})
```

### Fullmatch – パイプラインを停止します
```python
('hello koan', r'^.*$', 0, {'flags': re.IGNORECASE})
```
⚠️ これは **すべて** に一致します。パイプラインはここで止まります。以前のルールが引き続き優先されます。

### 入力の先頭と一致する
```python
('Note: ', r'^notiz\b', 0, {'flags': re.IGNORECASE})
```

### フレーズと完全に一致
```python
('New York', r'\bnew york\b', 0, {'flags': re.IGNORECASE})
```

## ファイルの場所

|ファイル |フェーズ |説明 |
|---|---|---|
| `FUZZY_MAP_pre.py` |事前言語ツール |スペルチェックの前に適用される |
| `FUZZY_MAP.py` |ポスト言語ツール |スペルチェック後に適用される |
| `PUNCTUATION_MAP.py` |事前言語ツール |句読点の規則 |

## ヒント

- **一般**ルールの前に**特定**ルールを置く
- `^...$` 完全一致は、以降のすべての処理を停止したい場合にのみ使用してください。
- `FUZZY_MAP_pre.py` はスペルチェック前の修正に最適です
- Aura コンソールの「テスト入力」を使用してルールをテストします。
- バックアップは `.peter_backup` として自動的に作成されます

## 例

```python
FUZZY_MAP_pre = [
    # Correct a common STT mistake
    ('Raspberry Pi', r'\braspberry\s*pie?\b', 0, {'flags': re.IGNORECASE}),

    # Expand abbreviation
    ('zum Beispiel', r'\bzb\b', 0, {'flags': re.IGNORECASE}),

    # Stop pipeline for testing
    # ('test koan', r'^.*$', 0, {'flags': re.IGNORECASE}),
]
```
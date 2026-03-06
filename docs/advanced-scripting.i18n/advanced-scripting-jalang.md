# 高度なルール アクション: Python スクリプトの実行

このドキュメントでは、カスタム Python スクリプトを実行して単純なテキスト置換ルールの機能を拡張する方法について説明します。この強力な機能を使用すると、動的な応答の作成、ファイルの操作、外部 API の呼び出し、複雑なロジックの実装を音声認識ワークフロー内で直接行うことができます。

## 中心となる概念: `on_match_exec`

テキストを単に置き換えるのではなく、パターンが一致した場合に 1 つ以上の Python スクリプトを実行するようにルールに指示できるようになりました。これは、「on_match_exec」キーをルールのオプション辞書に追加することによって行われます。

スクリプトの主な仕事は、一致に関する情報を受け取り、アクションを実行し、新しいテキストとして使用される最終文字列を返すことです。

### ルールの構造

スクリプト アクションを含むルールは次のようになります。

```python
# In your map file (e.g., config/maps/.../de-DE/my_rules.py)
from pathlib import Path

# It's best practice to define the directory path once at the top
CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    (
        None,  # The replacement string is often None, as the script generates the final text.
        r'what time is it', # The regex pattern to match.
        95, # The confidence threshold.
        {
            'flags': re.IGNORECASE,
            # The new key: a list of script files to execute.
            'on_match_exec': [CONFIG_DIR / 'get_current_time.py']
        }
    ),
]
```
**重要なポイント:**
- `on_match_exec` 値は **list** である必要があります。
- スクリプトはマップ ファイルと同じディレクトリに配置されるため、パスを定義するには `CONFIG_DIR / 'script_name.py'` が推奨される方法です。

---

## 実行可能スクリプトの作成

システムがスクリプトを使用するには、次の 2 つの単純なルールに従う必要があります。
1. 有効な Python ファイル (例: 「my_script.py」) である必要があります。
2. `execute(match_data)` という名前の関数が含まれている必要があります。

### `execute(match_data)` 関数

これは、すべての実行可能スクリプトの標準エントリ ポイントです。ルールが一致すると、システムは自動的にこの関数を呼び出します。

- **`match_data` (dict):** 一致に関するすべてのコンテキストを含む辞書。
- **戻り値 (str):** 関数は文字列を返す必要があります**。この文字列が新しく処理されたテキストになります。

### `match_data` ディクショナリ

この辞書は、メイン アプリケーションとスクリプトの間の橋渡しとなります。これには次のキーが含まれています。

* `'original_text'` (str): 現在のルールからの置換が適用される「前の」フルテキスト文字列。
* `'text_after_replacement'` (文字列): ルールの基本置換文字列が適用された「後」、ただしスクリプトが呼び出される「前」のテキスト。 (置換が「なし」の場合、これは「original_text」と同じになります)。
* `'regex_match_obj'` (re.Match): 公式の Python 正規表現一致オブジェクト。これは、**キャプチャ グループ**にアクセスする場合に非常に強力です。 `match_obj.group(1)`、`match_obj.group(2)`などを使用できます。
* `'rule_options'` (dict): スクリプトをトリガーしたルールの完全なオプション辞書。

---

## 例

### 例 1: 現在時刻の取得 (動的応答)

このスクリプトは、時刻に基づいてパーソナライズされた挨拶を返します。

**1.ルール (マップ ファイル内):**
```python
(None, r'\b(what time is it|uhrzeit)\b', 95, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'get_current_time.py']
}),
```

**2.スクリプト (`get_current_time.py`):**
```python
from datetime import datetime
import random

def execute(match_data):
    """Returns a friendly, time-aware response."""
    now = datetime.now()
    hour = now.hour
    time_str = now.strftime('%H:%M')

    if hour < 12:
        greeting = "Good morning!"
    elif hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"
    
    responses = [
        f"{greeting} It's currently {time_str}.",
        f"Right now, the time is {time_str}. Hope you're having a great day!",
    ]
    return random.choice(responses)
```
**使用法：**
> **入力:** 「今何時ですか」
> **出力:** 「こんにちは! 現在 14:30 です。」

### 例 2: 単純な計算機 (キャプチャ グループの使用)

このスクリプトは、正規表現からのキャプチャ グループを使用して計算を実行します。

**1.ルール (マップ ファイル内):**
```python
(None, r'calculate (\d+) (plus|minus) (\d+)', 98, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'calculator.py']
}),
```

**2.スクリプト (`calculator.py`):**
```python
def execute(match_data):
    """Performs a simple calculation based on regex capture groups."""
    try:
        match_obj = match_data['regex_match_obj']
        
        num1 = int(match_obj.group(1))
        operator = match_obj.group(2).lower()
        num2 = int(match_obj.group(3))

        if operator == "plus":
            result = num1 + num2
        elif operator == "minus":
            result = num1 - num2
        else:
            return "I didn't understand that operator."
            
        return f"The result is {result}."
    except (ValueError, IndexError):
        return "I couldn't understand the numbers in your request."
```
**使用法：**
> **入力:** 「55 プラス 10 を計算します」
> **出力:** 「結果は 65 です。」

### 例 3: 永続的なショッピング リスト (ファイル I/O)

この例では、ユーザーの元のテキストを検査することで 1 つのスクリプトで複数のコマンド (追加、表示) を処理する方法と、ファイルに書き込むことでデータを保持する方法を示します。

**1.ルール (マップ ファイル内):**
```python
# Rule for adding items
(None, r'add (.*) to the shopping list', 95, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'shopping_list.py']
}),

# Rule for showing the list
(None, r'show the shopping list', 95, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'shopping_list.py']
}),
```

**2.スクリプト (`shopping_list.py`):**
```python
from pathlib import Path

LIST_FILE = Path(__file__).parent / "shopping_list.txt"

def execute(match_data):
    """Manages a shopping list stored in a text file."""
    original_text = match_data['original_text'].lower()
    
    # --- Add Item Command ---
    if "add" in original_text:
        item = match_data['regex_match_obj'].group(1).strip()
        with open(LIST_FILE, "a", encoding="utf-8") as f:
            f.write(f"{item}\n")
        return f"Okay, I've added '{item}' to the shopping list."
    
    # --- Show List Command ---
    elif "show" in original_text:
        if not LIST_FILE.exists() or LIST_FILE.stat().st_size == 0:
            return "The shopping list is empty."
        with open(LIST_FILE, "r", encoding="utf-8") as f:
            items = f.read().strip().splitlines()
        
        item_str = ", ".join(items)
        return f"On the list you have: {item_str}."
        
    return "I'm not sure what to do with the shopping list."
```
**使用法：**
> **入力 1:** 「買い物リストに牛乳を追加」
> **出力 1:** 「はい、買い物リストに「牛乳」を追加しました。」
>
> **入力 2:** 「買い物リストを表示」
> **出力 2:** 「リストには牛乳があります。」

---

## ベストプラクティス

- **スクリプトごとに 1 つのジョブ:** スクリプトを単一のタスクに集中させます (例: `calculator.py` は計算のみを実行します)。
- **エラー処理:** アプリケーション全体がクラッシュするのを防ぐために、スクリプトのロジックを常に `try...excel` ブロックで囲みます。 `excel` ブロックからわかりやすいエラー メッセージを返します。
- **外部ライブラリ:** 外部ライブラリ (`requests` や `wikipedia-api` など) を使用できますが、それらが Python 環境にインストールされていることを確認する必要があります (`pip install <library-name>`)。
- **セキュリティ:** この機能はあらゆる Python コードを実行できることに注意してください。信頼できるソースからのスクリプトのみを使用してください。
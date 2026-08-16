# ルール属性: `only_in_windows` および `exclude_windows`

これら 2 つの属性は、**どのアクティブなウィンドウでルールの起動を許可する** かを制御します。
これらはルールの「オプション」辞書内で定義され、**正規表現パターンのリスト**を受け入れます。
現在のアクティブなウィンドウのタイトル (`_active_window_title`) と照合されます。

---

## `only_in_windows`

このルールは、アクティブなウィンドウのタイトルが指定されたパターンの**少なくとも 1 つ**に一致する場合にのみ実行されます。
他のウィンドウはすべて無視されます。

**使用例:** ルールを特定のアプリケーションに制限します。


> このルールは、Firefox または Chromium がアクティブなウィンドウである場合にのみ**実行されます。

---

## `exclude_windows`

このルールは、アクティブなウィンドウのタイトルが指定されたパターンの**少なくとも 1 つ**と一致しない限り**実行されます。
一致するウィンドウはスキップされます。

**使用例:** 特定のアプリケーションのルールを無効にします。

例

```py
Targets
    Occurrences of 'exclude_windows' in Project with mask '*pre.py'
Found occurrences in Project with mask '*pre.py'  (3 usages found)
    Usage in string constants  (3 usages found)
        STT  (3 usages found)
            config/maps/plugins/z_fallback_llm/de-DE  (3 usages found)
                FUZZY_MAP_pre.py  (3 usages found)
                    90 'exclude_windows': [r'element',r'firefox', r'chrome', r'brave'],
                    105 'exclude_windows': [r'element',r'firefox', r'chrome', r'brave'],
                    119 'exclude_windows': [r'element',r'firefox', r'chrome', r'brave',r'doublecmd'],

```



照合では **大文字と小文字は区別されません**。Python **正規表現**が使用されます。

---

＃＃ まとめ

|属性 |次の場合に発火します... |
|-----------------|--------------------------------------------|
| `Windows のみ` |ウィンドウ タイトルが **パターンの 1 つと一致します** |
| `除外_windows` |ウィンドウ タイトル **どのパターンにも一致しません** |

---

## も参照

- `scripts/py/func/process_text_in_background.py` — 行 ~1866 および ~1908
- `scripts/py/func/get_active_window_title.py` — ウィンドウタイトルの取得方法
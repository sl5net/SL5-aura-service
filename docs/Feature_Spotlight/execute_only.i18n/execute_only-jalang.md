# ルール属性: `execute_only` (実験的、7.7.'26 火曜日)

「execute_only」属性は、入力テキストを変更または置換せずに外部スクリプトのみをトリガーするルール用に設計された実験的な構成オプションです。

＃＃ 概要
- **タイプ:** `bool` (例: `True` または `False`)
- **主な使用例:** 通常、外部スクリプトを実行するために「on_match_exec」と組み合わせて使用されます。

## 仕組みと現在の動作
- **速度の最適化:** (数ミリ秒のみ) テキストの後処理ルーチンとテキスト置換ルーチンをバイパスし、トリガーされたアクションの即時実行を高速化します。
- **除外/フォールスルーの副作用なし:** `execute_only` を `True` に設定しても、他の一致ルールが同じ入力テキストを評価することは **妨げられません**。
- **フローの停止:** 後続のルールによる同じ入力テキストの処理を停止する必要がある場合は、現在、実行フローを手動で終了する必要があります (トリガーされたスクリプトまたはルールセット ハンドラーの最後で例外をスローするなど)。

## 設定例

```python
# EXAMPLE: gather metal
('gather metal',
 r'^(gather\s*)?(met\w+|mat\w+|metall|mit|zitat|metal|matcha|günther)$',
 85,
 {
     'command_flags': re.IGNORECASE,
     'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
     'on_match_exec': [CONFIG_DIR / '..' / '0ad_actions.py'],
     'execute_only': True, # Experimental: Fast execution, does not halt the rule-chain.
 }),
```
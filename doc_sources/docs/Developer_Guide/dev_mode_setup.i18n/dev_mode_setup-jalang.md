# DEV_MODE セットアップガイド

＃＃ 問題



現在（21.3.'26 Sat）、ログ記録のルールが変更されました。マンジャロでは問題なかった。

「DEV_MODE = 1」がアクティブな場合、Aura は 1 秒あたり数百のログエントリを生成します
複数のスレッドから。これにより、「SafeStreamToLogger」がデッドロックする可能性があります。
最初のディクテーショントリガー後にオーラがハングします。

## 修正: LOG_ONLY フィルターを使用する

`DEV_MODE = 1` で開発する場合は、次のログ フィルターも設定する必要があります**。
`config/filters/settings_local_log_filter.py`

### DEV_MODE の最小限の作業フィルター:
```python
LOG_ONLY = [
    r"Successfully",
    r"CRITICAL",
    r"📢📢📢 #",
    r"Title",
    r"window",
    r":st:",
]
LOG_EXCLUDE = []
```

## settings_local.py のワンライナー
このコメントを DEV_MODE 設定の横にリマインダーとして追加します。
```python
DEV_MODE = 1  # ⚠️ Requires LOG_ONLY filter! See docs/dev_mode_setup.md
```

＃＃ 根本的な原因
`SafeStreamToLogger` は、`threading.Lock` を使用して標準出力の書き込みを保護します。
ログ負荷が高い (DEV_MODE) 場合、ロック競合によりシステムでデッドロックが発生する
積極的なスレッド スケジューリングを使用します (例: 新しいカーネル/glibc を備えた CachyOS)。
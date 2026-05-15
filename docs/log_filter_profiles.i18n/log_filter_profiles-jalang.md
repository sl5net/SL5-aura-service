# ログフィルタープロファイル

アクティブなログ フィルタは常に `config/filters/settings_local_log_filter.py` です。

## プロファイル

事前定義されたプロファイルは `config/filters/.backlock/` に保存されます。

|プロフィール |説明 |
|---|---|
| `first_run` |最小限の出力 — エラーとステータスのみ。初回起動時に自動的に適用されます。 |
| `普通` |日常使いに最適なスタンダードフィルター。 |

## プロファイルを手動で切り替える

```bash
cp config/filters/.backlock/first_run/settings_local_log_filter.py config/filters/settings_local_log_filter.py
cp config/filters/.backlock/normal/settings_local_log_filter.py config/filters/settings_local_log_filter.py
```

## カスタム プロファイルを追加する

1. `config/filters/.backlock/my_profile/` の下に新しいフォルダーを作成します。
2. 既存の「settings_local_log_filter.py」をそこにコピーし、必要に応じて編集します
3. 上のように「cp」で適用します。

## プロファイルの自動切り替え

最初の起動時に、Aura は `log/` ディレクトリがまだ存在しないことを検出し、
`first_run` プロファイルをアクティブなフィルターとして自動的にコピーします。
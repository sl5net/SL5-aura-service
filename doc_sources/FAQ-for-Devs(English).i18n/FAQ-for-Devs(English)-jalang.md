# 正規表現ルール

重要: 正規表現を正しい順序で適用してください。

最初に複合 (より一般的な) 正規表現を使用し、次に特殊な正規表現を適用する必要があります。

その理由は、短い特殊な正規表現が最初に実行されると、より大きな複合正規表現に必要な文字列の一部と一致する可能性があるためです。これにより、後で複合正規表現が一致するものを見つけることができなくなります。
(S. 20.10.'25 18:37 Mon)

# Linux/Mac

サービスを自動的に開始したい場合は、次のように追加します。
~/projects/py/STT/scripts/restart_venv_and_run-server.sh
自動スタートに。

インターネット接続がある場合にのみサービスを開始します。
次に、 settings_local.py に設定します。
SERVICE_START_OPTION = 1


## エンターを追加
設定するとき
config/settings_local.py/AUTO_ENTER_AFTER_DICTATION_REGEX_APPS
1 に Enter を追加します。

設定するとき
tmp/sl5_auto_enter.flag
1 に Enter を追加します。

tmp/sl5_auto_enter.flag はサービス起動時に上書きされます。
tmp/sl5_auto_enter.flag は、他のスクリプトを使用すると解析しやすくなり、読み取りが少し速くなります。

無効化には他の番号を使用してください
(S.13.9.'25 16:12 Sat)
Aura SL5 フック: 追加

HOOK_PLUGIN_LOAD = 'on_plugin_load'
HOOK_FILE_LOAD = 'on_file_load'
HOOK_RELOAD = 'リロード時'
HOOK_UPSTREAM = 'フォルダ変更時'

on_folder_change() と
on_reload() は、ホットリロード後にロジックをトリガーします。これを使用して、複雑なパッケージの secure_packer.py などの親スクリプトを「デイジーチェーン」実行します。

# 開発者ガイド: プラグインのライフサイクル フック

Aura SL5 allows plugins (Maps) to define specific "Hooks" that are executed automatically when the module's state changes.これは、**Secure Private Map** システムのような高度なワークフローには不可欠です。

## `on_folder_change` フック フック

`on_folder_change` フック検出を実装しました。リローダーがディレクトリをスキャンアップするようになりました

## `on_reload()` フック

`on_reload()` 関数は、任意の Map モジュールで定義できるオプションの関数です。

＃＃＃ 行動
* **トリガー:** モジュールが正常に **ホットリロード** (ファイル変更 + 音声トリガー) された直後に実行されます。
* **コンテキスト:** メイン アプリケーション スレッド内で実行されます。
* **安全性:** `try/excel` ブロックでラップされています。ここでのエラーはログに記録されますが、アプリケーションは**クラッシュしません**。

### 使用パターン: 「デイジーチェーン」
複雑なパッケージ (プライベート マップなど) の場合、多くのサブファイルがあることがよくありますが、ロジックを処理する必要があるのは 1 つの中央スクリプト (`secure_packer.py`) だけです。

フックを使用してタスクを上に委任できます。

__CODE_BLOCK_0__
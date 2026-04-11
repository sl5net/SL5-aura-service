# SL5 Aura のトラブルシューティング

## クイック診断

常にここから始めてください:

```bash
# Check the main log:
tail -50 log/aura_engine.log

# Is Aura running?
pgrep -a -f aura_engine.py

# Is the file watcher running?
pgrep -a type_watcher
```

---

## 問題: Aura が起動しない

**症状:** 起動音が鳴らず、`pgrep` にプロセスが表示されません。

**ログを確認してください:**
```bash
tail -30 log/aura_engine.log
```

**一般的な原因:**

|ログにエラーがあります |修正 |
|---|---|
| `モジュールが見つかりませんエラー` |セットアップ スクリプトを再度実行します: `bash setup/manjaro_arch_setup.sh` |
| `'objgraph' という名前のモジュールはありません` | `.venv` が再作成されました — 再インストール: `pip install -r required.txt` |
| `アドレスはすでに使用されています` |古いプロセスを強制終了します: `pkill -9 -f aura_engine` |
| `モデルが見つかりません` |セットアップを再実行して欠落しているモデルをダウンロードする |
| `pygame.mixer は利用できません` |以下の「起動時に音が出ない」を参照してください。

---

## 問題: 起動時に音が出ない (pygame.mixer)

**症状:** `pygame.mixer` に関する警告またはエラーが表示されません。オーラが始まる
しかし音は鳴りません。

**原因:** システムの pygame ビルドにはオーディオ サポートまたは SDL2 が含まれていません。
オーディオライブラリがありません。

**Arch/Manjaro を修正:**
```bash
sudo pacman -S sdl2_mixer
pip install pygame-ce --upgrade
```

**Ubuntu/Debian での修正:**
```bash
sudo apt install libsdl2-mixer-2.0-0
pip install pygame-ce --upgrade
```

Aura は音声なしでも動作し続けます。これは致命的なエラーではありません。

---

## 問題: 最初のディクテーション後に Aura がクラッシュする

**症状:** 一度動作すると、その後静かに動作しなくなります。

**標準エラー出力を確認してください:**
```bash
cat /tmp/aura_stderr.log | tail -30
```

**「セグメンテーション違反」または「ダブルフリー」が表示された場合:**

これは、glibc 2.43 以降 (CachyOS、新しい Arch) を搭載したシステムの既知の問題です。

```bash
sudo pacman -S mimalloc
```

mimalloc がインストールされている場合、開始スクリプトによって自動的に使用されます。アクティブであることを確認します。起動時に次のように表示されるはずです。
```
Info: Using mimalloc for improved memory management (/usr/lib/libmimalloc.so).
```

---

## 問題: トリガーキーが何も起こりません

**症状:** ホットキーを押しても何も起こりません。音もテキストも表示されません。

**ファイル ウォッチャーが実行されているかどうかを確認します:**
```bash
pgrep -a type_watcher
```

何も表示されない場合は、Aura を再起動します。
```bash
./scripts/restart_venv_and_run-server.sh
```

**トリガー ファイルが作成されているかどうかを確認します:**
```bash
ls -la /tmp/sl5_record.trigger
```

ファイルが作成されない場合は、ホットキーが機能しません。以下を参照してください。

---

## 問題: Wayland でホットキーが機能しない

**症状:** CopyQ がインストールされ構成されているが、ホットキーを押すと、
Wayland セッションでは何もありません。

**原因:** CopyQ グローバル ホットキーは、これがないと Wayland で確実に機能しません。
追加の構成。これは、KDE Plasma、GNOME、その他に影響します。
Wayland コンポジター。

### オプション 1: KDE システム設定 (KDE Plasma に推奨)

1. **システム設定→ショートカット→カスタムショートカット**を開きます
2. **Command/URL** タイプの新しいショートカットを作成します。
3. コマンドを次のように設定します。
   ```bash
   touch /tmp/sl5_record.trigger
   ```
4. 好みのキーの組み合わせを割り当てます (例: 「F9」または「Ctrl+Alt+Space」)。

### オプション 2: dotool (任意の Wayland コンポジターで動作します)

```bash
# Install dotool:
sudo pacman -S dotool        # Arch/Manjaro
# or
sudo apt install dotool      # Ubuntu (if available)
```

次に、デスクトップのショートカット マネージャーを使用して以下を実行します。
```bash
touch /tmp/sl5_record.trigger
```

### オプション 3: ydotool

```bash
sudo pacman -S ydotool
sudo systemctl enable --now ydotool
```

次に、実行するショートカットを設定します。
```bash
touch /tmp/sl5_record.trigger
```

### オプション 4: GNOME (dconf / GNOME 設定を使用)

1. **[設定] → [キーボード] → [カスタム ショートカット]** を開きます。
2. 次のコマンドを使用して新しいショートカットを追加します。
   ```bash
   touch /tmp/sl5_record.trigger
   ```
3. キーの組み合わせを割り当てます

### オプション 5: Wayland 修正を含む CopyQ

一部の Wayland コンポジターでは、次のコマンドで開始すると CopyQ が動作します。
```bash
QT_QPA_PLATFORM=xcb copyq
```

これにより、CopyQ はグローバル ホットキーをサポートする XWayland を使用するようになります。

---

## 問題: テキストは表示されるが修正されない

**症状:** ディクテーションは機能しますが、すべてが小文字のままで、文法が修正されません。

**LanguageTool が実行されているかどうかを確認してください:**
```bash
curl -s http://127.0.0.1:8082/v2/languages | head -5
```

これによりエラーが返された場合は、LanguageTool が実行されていません。オーラが起動するはずです
自動的に — LanguageTool に関連するエラーのログを確認します。

```bash
grep -i "languagetool\|LT\|8082" log/aura_engine.log | tail -10
```

**LanguageTool ログを確認してください:**
```bash
cat log/languagetool_server.log | tail -20
```

---

## 問題: DEV_MODE で Aura がハングする

**症状:** 「DEV_MODE = 1」の場合、最初のトリガー後に Aura がハングして停止します。
応答しています。

**原因:** 複数のスレッドからの大量のログにより、ログ システムに過負荷がかかります。

**修正:** `config/filters/settings_local_log_filter.py` にログ フィルターを追加します。

```python
LOG_ONLY = [
    r"Successfully",
    r"CRITICAL",
    r"📢📢📢 #",
    r"window_title",
    r":st:",
]
LOG_EXCLUDE = []
```

ファイルを保存します — Aura はフィルターを自動的に再読み込みします。再起動は必要ありません。

---

## 問題: plugins.zip が際限なく増大する / CPU 使用率が高い

**症状:** CPU が 100%、ファンがフルスピードで動作し、「plugins.zip」が止まらずに成長します。

**原因:** セキュア パッカーが無限ループでファイルを再パッケージ化しています。

**修正:** `.blob` ファイルと `.zip` ファイルがタイムスタンプ スキャンから除外されていることを確認します。
86 行目あたりの「scripts/py/func/secure_packer_lib.py」を確認してください。

```python
if file.startswith('.') or file.endswith('.pyc') or file.endswith('.blob') or file.endswith('.zip'):
    continue
```

この行が欠落している場合は追加してください。

---

## 問題: ルールが起動しない

**症状:** トリガー フレーズを入力しても、ルールは何も実行しません。

**チェックリスト:**

1. ルールは正しいファイルにありますか? (`FUZZY_MAP_pre.py` = LanguageTool の前、
`FUZZY_MAP.py` = 後)
2. マップファイルは保存されていますか? Aura は保存時にリロードされます。ログを確認してください。
「正常にリロードされました」。
3. パターンは Vosk が実際に転写したものと一致しますか?ログを確認してください
生の文字起こし:
   ```bash
   grep "Yielding chunk" log/aura_engine.log | tail -5
   ```
4. 「only_in_windows」が設定されており、間違ったウィンドウがアクティブになっていますか?
5. より一般的なルールが最初に一致しますか?ルールは上から下に処理されます —
一般的なルールの前に特定のルールを置きます。

---

## バグレポートのためのログの収集

問題を報告するときは、次のことを含めてください。

```bash
# Last 100 lines of main log:
tail -100 log/aura_engine.log

# Crash output:
cat /tmp/aura_stderr.log

# System info:
uname -a
python3 --version
```

投稿先: [GitHub Issues](https://github.com/sl5net/SL5-aura-service/issues)
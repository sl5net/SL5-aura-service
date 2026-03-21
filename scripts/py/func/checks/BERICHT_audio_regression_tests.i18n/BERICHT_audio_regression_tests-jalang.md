# SL5 Aura – オーディオ回帰テスト: ステータスベリヒト

**日付:** 2026-03-14  
**日付:** `scripts/py/func/checks/test_youtube_audio_regression.py`

---

## 1. ひどいことだった

Ein テストシステムのデータ:
1. YouTube ビデオのオーディオ セグメントを参照 (`yt-dlp` + `ffmpeg` 経由)
2. ダッセルベの YouTube トランスクリプトのセグメントの一部 (`youtube-transcript-api` 経由)
3. Vosk トランスクリビアートによる Das Audio
4. **Aura-Pipeline** のオプションの実行 (`process_text_in_background`)
5. Die Word Error Rate (WER) zwischen Aura-Output および YouTube-Transcript berechnet
6. `pytest` ごとに automatischer Regressionstest läuft を実行

すべてのダウンロード (`scripts/py/func/checks/fixtures/youtube_clips/`)、フォルゲテスト シュネル ラウフェン。

---

## 2.ダテイエン

|ダテイ |ツベック |
|---|---|
| `scripts/py/func/checks/test_youtube_audio_regression.py` |ハウプテストダテイ |
| `scripts/py/func/checks/fixtures/youtube_clips/*.wav` | Gecachte オーディオクリップ |
| `scripts/py/func/checks/fixtures/youtube_clips/*.transcript.json` |ゲカフテ転写物 |
| `scripts/py/func/checks/fixtures/youtube_clips/.gitignore` | Git を使用したキャッシュ |
| `conftest.py` (リポジトリルート) | pytest の PYTHONPATH を設定します。

---

## 3. テストモード

### モード A – Vosk のみ (ベースライン)
```python
YoutubeAudioTestCase(
    test_id       = "mein_test_vosk",
    video_id      = "XXXXXXXXXXX",
    start_sec     = 10,
    end_sec       = 25,
    language      = "de-DE",
    wer_threshold = 0.40,
)
```
Vosk-Qualität のテスト。ケイン・オーラ。シュネル。

### モジュール B – Volle Aura-Pipeline、WER-Vergleich
```python
YoutubeAudioTestCase(
    test_id            = "mein_test_aura",
    video_id           = "XXXXXXXXXXX",
    start_sec          = 10,
    end_sec            = 25,
    language           = "de-DE",
    wer_threshold      = 0.35,   # strenger — Aura soll besser sein als Vosk
    test_aura_pipeline = True,
)
```
Schickt Vosk は、FuzzyMap Pre → LanguageTool → FuzzyMap Post による出力を行います。

### Modus C – Volle Aura-Pipeline、正確な出力
```python
YoutubeAudioTestCase(
    test_id            = "befehl_terminal_oeffnen",
    video_id           = "XXXXXXXXXXX",
    start_sec          = 42,
    end_sec            = 45,
    language           = "de-DE",
    test_aura_pipeline = True,
    expected_output    = "terminal öffnen",  # Aura muss genau das ausgeben
)
```
Für Segmente wo ein bekannter Befehl gesprochen wird。シャーフスターテスト。

---

## 4. 奇妙な出来事だった — ニヒトだった

|だった |ゲテステト？ |
|---|---|
| Vosk STT-Qualität | ✅ |
| FuzzyMap Pre-Regeln | ✅ (ウェン・オーラ・レフト) |
| LanguageTool-Korekturen | ✅ (ウェン LT レフト) |
|レーゲルン後のファジーマップ | ✅ (ウェン・オーラ・レフト) |
|キーボード出力 (AutoHotkey/CopyQ) | ❌ bewusst — OS-Ebene、keine Logik |
| Vosk-Modell-Loading | ❌ — 最も美しい出力データ、新しいモデルを取得 |

`tts_output_*.txt` を使用した出力を一時的に取得します — ターミナルを使用してオーラを生成します。

---

## 5.スタートビフェール

### Normaler Testlauf (Aura muss bereits laufen):
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | grep -E "PASSED|FAILED|SKIPPED|WER|YT ref|Vosk   |Aura   :|Test   :"
```

### Mit vollem ログ:
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | tee /tmp/aura_test.log
```

### 最高のテスト:
```bash
# Nur Aura-Tests
.venv/bin/pytest ... -k "aura"

# Nur Vosk-Baseline
.venv/bin/pytest ... -k "not aura"

# Einen spezifischen Test
.venv/bin/pytest ... -k "sl5_demo_de_v1"
```

### Aura + LT の最初の開始:
```bash
./scripts/restart_venv_and_run-server.sh &
sleep 60
curl -s http://localhost:8010/v2/languages | head -c 50   # prüfen ob LT läuft
```

---

## 6. Wichtige の設定

### Sprachcodes — zwei verschiedene Systeme!

|システム |コード |バイシュピール |
|---|---|---|
|ヴォスク・モデル・オードナー |で | `models/vosk-model-de-0.21` |
| Aura FuzzyMap-Ordner | オーラファジーマップオードナー`脱DE` | `config/maps/.../de-DE/` |
| YouTube トランスクリプト API |で | `api.fetch(..., 言語=["de"])` |

**Lösung im Code:** ` language="de-DE"` が設定されています。コードの自動化:
- Für Vosk: `"de-DE"` → `"de"` (`-` を分割)
- YouTube の場合: `"de-DE"` → `"de"` (`-` を分割)
- Für Aura: `"de-DE"` ダイレクト

### 自動翻訳機能のテスト:
```bash
# Backup wiederherstellen (deaktiviert Auto-Translator):
cp config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py.off.backup.py \
   config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py
```
英語のテキスト — das verfälscht den WER。

---

## 7. ベカンテ・プロブレマーレとローズンゲン

|問題 |ウルサッシュ |ロソン |
|---|---|---|
| `SKIPPED` ソフト | YouTube-トランスクリプト nicht gefunden | `api.list('video_id')` を使用して詳細を確認する |
| 「スキップ」ナッハオーディオ | Vosk-Modell ニヒト ゲフンデン | ` language.split("-")[0]` コードでのフォールバック |
| `FUZZY_MAP_pre ルールが 0 個見つかりました` |ファルッシャー オーラのスプラッハコード | `"de-DE"` statt `"de"` verwenden |
| `接続が拒否されました 8010` | LT ニヒト ゲスタート |オーラは最初から始まり、60 年代は終わり |
| `zsh: 終了しました` | X11-Watchdog killt Prozess | `SDL_VIDEODRIVER=dummy` バージョン; Watchdog-Schwellenwert erhöhen |
| YouTube `>>` マーカー | Zweitsprecher im 転写 | `re.sub(r'>>', '', text)` — `>>` を参照してください。
| `属性エラー: get_transcript` | youtube-transcript-api v1.x | `api = YouTubeTranscriptApi(); api.fetch(...)` statt クラッセンメソッド |
|キャッシュの内容を確認する テキスト | Alter Lauf mit kaputtem Regex | `rm fixtures/youtube_clips/*.transcript.json` |

---

## 8. エルゲブニッセ・ビス・ジェッツト

### ビデオ: `sOjRNICiZ7Q` (ドイツ語)、セグメント 5 ～ 20 秒

```
YT ref : Das ist jetzt der ultimative Test. Meer gewinnt die Spracherkennung...
Vosk   : meine zehn finger technik war ich will jetzt hier...
Aura   : meine 10 finger technik war ich will jetzt hier...
WER    : 71.4%
```

**ベオバッハトゥンゲン:**
- オーラハット・アイネ・レーゲル・アンゲウェンデット：`ゼーンフィンガー`→`10フィンガー`✅
- LT-Status während dieses Laufs undlar — Verbindung wurde verweigert
- Hoher WER liegt am Segment: YouTube-トランスクリプト beginnt mit Wörtern die Vosk nicht hört (Sprecher noch nicht am Mikro)
- **Empfehlung:** セグメント verschieben auf einen Bereich wo klar gesprochen wird

---

## 9. 帝国のシュリッテ

1. **Besseres Segment wählen** — `ffplay` は、新しいゲームを見つけるのに役立ちます
2. **LT-Status im Test prüfen** — `curl http://localhost:8010/v2/langages` のテスト
3. **Modus C テストのヒント** — セグメントを確認する (`expected_output`)

---
---

# SL5 Aura – オーディオ回帰テスト: ステータス レポート

**日付:** 2026-03-14  
**ファイル:** `scripts/py/func/checks/test_youtube_audio_regression.py`

---

## 1. 構築されたもの

次のようなテスト システム:
1. YouTube ビデオからオーディオ セグメントをダウンロードします (`yt-dlp` + `ffmpeg` 経由)
2. 同じセグメントの自動生成された YouTube トランスクリプトを取得します (`youtube-transcript-api` 経由)
3. Vosk を通じて音声を文字に起こします。
4. オプションで、**完全な Aura パイプライン** (`process_text_in_background`) を通じて結果を渡します。
5. Aura 出力と YouTube トランスクリプト間の Word Error Rate (WER) を計算します。
6. 「pytest」経由で自動回帰テストとして実行します。

すべてのダウンロードはキャッシュされるため (`scripts/py/func/checks/fixtures/youtube_clips/`)、その後の実行は高速になります。

---

## 2. ファイル

|ファイル |目的 |
|---|---|
| `scripts/py/func/checks/test_youtube_audio_regression.py` |メインテストファイル |
| `scripts/py/func/checks/fixtures/youtube_clips/*.wav` |キャッシュされたオーディオ クリップ |
| `scripts/py/func/checks/fixtures/youtube_clips/*.transcript.json` |キャッシュされたトランスクリプト |
| `scripts/py/func/checks/fixtures/youtube_clips/.gitignore` | Git からキャッシュを除外する |
| `conftest.py` (リポジトリのルート) | pytest の PYTHONPATH を設定します。

---

## 3. テストモード

### モード A – Vosk のみ (ベースライン)
```python
YoutubeAudioTestCase(
    test_id       = "my_test_vosk",
    video_id      = "XXXXXXXXXXX",
    start_sec     = 10,
    end_sec       = 25,
    language      = "de-DE",
    wer_threshold = 0.40,
)
```
Vosk の品質のみをテストします。オーラがない。速い。

### モード B – フル Aura パイプライン、WER 比較
```python
YoutubeAudioTestCase(
    test_id            = "my_test_aura",
    video_id           = "XXXXXXXXXXX",
    start_sec          = 10,
    end_sec            = 25,
    language           = "de-DE",
    wer_threshold      = 0.35,   # stricter — Aura should improve on Vosk
    test_aura_pipeline = True,
)
```
Vosk 出力を FuzzyMap Pre → LanguageTool → FuzzyMap Post 経由で送信します。

### モード C – 完全な Aura パイプライン、正確な出力一致
```python
YoutubeAudioTestCase(
    test_id            = "command_open_terminal",
    video_id           = "XXXXXXXXXXX",
    start_sec          = 42,
    end_sec            = 45,
    language           = "de-DE",
    test_aura_pipeline = True,
    expected_output    = "terminal öffnen",   # Aura must produce exactly this
)
```
既知の音声コマンドを含むセグメントの場合。最も厳しいテストモード。

---

## 4. 何がテストされるのか、何がテストされないのか

|何を |テスト済み? |
|---|---|
| Vosk STT の品質 | ✅ |
| FuzzyMap 事前ルール | ✅ (Aura 実行時) |
|言語ツールの修正 | ✅（LT走行時） |
| FuzzyMap 投稿ルール | ✅ (Aura 実行時) |
|キーボード出力 (AutoHotkey/CopyQ) | ❌ 意図的 — OS レベル、ロジックなし |
| Vosk モデルのリロード | ❌ — Aura は出力ファイルを読み取り、モデルをリロードしません。

出力は一時ディレクトリの `tts_output_*.txt` から読み取られます。これは、Aura がターミナルからではなく内部的に行うのとまったく同じです。

---

## 5. 開始コマンド

### 通常のテストの実行 (Aura がすでに実行されている必要があります):
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | grep -E "PASSED|FAILED|SKIPPED|WER|YT ref|Vosk   |Aura   :|Test   :"
```

### 完全なログの場合:
```bash
SDL_VIDEODRIVER=dummy \
AURA_LT_URL=http://localhost:8010/v2 \
  .venv/bin/pytest scripts/py/func/checks/test_youtube_audio_regression.py -v -s \
  2>&1 | tee /tmp/aura_test.log
```

### 特定のテストのみ:
```bash
# Only Aura tests
.venv/bin/pytest ... -k "aura"

# Only Vosk baseline
.venv/bin/pytest ... -k "not aura"

# One specific test
.venv/bin/pytest ... -k "sl5_demo_de_v1"
```

### まず Aura + LT を開始します。
```bash
./scripts/restart_venv_and_run-server.sh &
sleep 60
curl -s http://localhost:8010/v2/languages | head -c 50   # verify LT is up
```

---

## 6. 重要な構成

### 言語コード — 2 つの異なるシステム!

|システム |コード |例 |
|---|---|---|
| Vosk モデル フォルダー |で | `models/vosk-model-de-0.21` |
| Aura FuzzyMap フォルダー | `脱DE` | `config/maps/.../de-DE/` |
| YouTube トランスクリプト API |で | `api.fetch(..., 言語=["de"])` |

**コードでの解決策:** ` language="de-DE"` を設定します。コードは以下を自動的に処理します。
- Vosk の場合: `"de-DE"` → `"de"` (`-` で分割)
- YouTube の場合: `"de-DE"` → `"de"` (`-` で分割)
- Aura の場合: `"de-DE"` を直接

### テストの前に自動翻訳を無効にします。
```bash
cp config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py.off.backup.py \
   config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py
```
そうしないと、Aura がドイツ語のテキストを英語に翻訳します。これにより、WER 測定が破損します。

---

## 7. 既知の問題と解決策

|問題 |原因 |修正 |
|---|---|---|
|すぐに「スキップ」します。 YouTube トランスクリプトが見つかりません |利用可能な言語を確認するには、`api.list('video_id')` を呼び出します。
|音声後の「SKIPPED」 | Vosk モデルが見つかりません |コード内の ` language.split("-")[0] ` フォールバック |
| `FUZZY_MAP_pre ルールが 0 個見つかりました` |間違った言語コードが Aura に渡されました | 「de」ではなく「de-DE」を使用してください。
| `接続が拒否されました 8010` | LT が開始されていません |最初に Aura を起動し、60 秒待ちます。
| `zsh: 終了しました` | X11 ウォッチドッグがプロセスを強制終了します。 `SDL_VIDEODRIVER=dummy` を使用します。ウォッチドッグしきい値を上げる |
| YouTube `>>` マーカー |トランスクリプトの 2 番目の講演者 | `re.sub(r'>>', '', text)` — `>>` のみを削除し、単語を保持します。
| `属性エラー: get_transcript` | youtube-transcript-api v1.x | `api = YouTubeTranscriptApi(); を使用します。 api.fetch(...)` |
|キャッシュに空のテキストが含まれています |正規表現が壊れている古い実行 | `rm fixtures/youtube_clips/*.transcript.json` |

---

## 8. これまでの結果

### ビデオ: `sOjRNICiZ7Q` (ドイツ語)、セグメント 5 ～ 20 秒

```
YT ref : Das ist jetzt der ultimative Test. Meer gewinnt die Spracherkennung...
Vosk   : meine zehn finger technik war ich will jetzt hier...
Aura   : meine 10 finger technik war ich will jetzt hier...
WER    : 71.4%
```

**所見:**
- アウラはルールを適用しました：「ゼーンフィンガー」→「10フィンガー」✅
- この実行中の LT ステータスが不明瞭 — 接続が拒否されました
- WER が高いのはセグメントの選択によるものです: YouTube のトランスクリプトは Vosk が聞き取れない単語で始まります (スピーカーがまだマイクを向いていない)
- **推奨:** セグメントを明瞭な音声のセクションに移動します。

---

## 9. 推奨される次のステップ

1. **より適切なセグメントを選択します** — `ffplay` を使用して、音声が明瞭な正確な秒を見つけます
2. **テスト前に LT ステータスを確認します** — 実行前に `curl http://localhost:8010/v2/langages`
3. **モード C テストを追加** — 既知の音声コマンド (`expected_output`) を含むセグメント
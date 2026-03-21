# Abschlussbericht: SL5 Aura – エンドツーエンド テストのトリガー

**日付:** 2026-03-15  
**日付:** `scripts/py/func/checks/test_trigger_end_to_end.py`

---

## 1. 計画を立てる

問題は次のとおりです:
**Bei manchen Aufnahmen fehlt das letzte Wort im Output.**

テスト結果:
1. Eine WAV-Datei als virginles Mikrofon einspeisen
2. `touch /tmp/sl5_record.trigger` によるオーラが開始される — Betrieb で得られる情報
3. Mit zweitem トリガーストッパー
4. YouTube トランスクリプトの出力を保存する
5. フェストステレン・オブ・アイン・ワート・アム・エンデ・フェルト

---

## 2. 間違っていた ✅

- オーラ レアギルト アウフ デン トリガー コレクト
- LT läuft und ist erreichbar (`http://127.0.0.1:8082`)
- `_wait_for_output()` `tts_output_*.txt` を見つける
- `_fetch_yt_transcript_segment()` の参照テキストの修正
- Der grundlegende Testaufbau ist Solide und funktioniert konzeptionell

---

## 3. 問題 🔴

### カーンの問題: `manage_audio_routing` に関する問題

Beim Session-Start ruft Aura インターン auf:
```python
manage_audio_routing(SYSTEM_DEFAULT)
```

最新の機能:
```python
subprocess.run(["pactl", "unload-module", "module-loopback"], capture_output=True)
subprocess.run(["pactl", "unload-module", "module-null-sink"], capture_output=True)
```

**Sie löscht jeden Sink den wir vorher erstellt haben.**

Danach erstellt sie keinen neuen Sink weil `mode == 'SYSTEM_DEFAULT'` (nicht `MIC_AND_DESKTOP`)。

### ヴェルシュテ・レスンゲン

|ヴァーサッチ |問題 |
|---|---|
| PulseAudio 仮想ソース erstellen | PipeWire は `module-virtual-source` を無視します。
| `settings_local.py` auf `MIC_AND_DESKTOP` setzen | Datei wurde mit mehrfachen Einträgen Korrumpiert |
|マルキエルテン オーバーライド ブロックとエンデ シュライベン |オーラの設定を変更し、トリガーを変更します。
| `_create_mic_and_desktop_sink()` 直接テスト | 「manage_audio_routing」を使用してセッションを開始する |
| `pw-ループバック` | Erscheint als ソース aber Aura hört nicht darauf |

### Warum `settings_local.py` nicht funktioniert をオーバーライドします

`dynamic_settings.py` は、日付と日付を表示します — 間隔をあけてください。 Der Trigger kommt zu Schnell nach dem Schreiben。オーラは「SYSTEM_DEFAULT」を使用してセッションを開始しました。

オーサーデム: Aura `MIC_AND_DESKTOP` を選択し、Sink erst beim **nächsten** Session-Start — nicht sofort を選択します。

---

## 4. モーグリッシェ・レースングスウェーゲ

### オプション A — 設定を変更する
```python
_set_audio_input_device("MIC_AND_DESKTOP")
time.sleep(5.0)   # statt 1.5s — mehr Zeit für dynamic_settings reload
TRIGGER_FILE.touch()
```
Risiko: Nicht zuverlässig、timing-abhängig。

### オプション B — 新しい設定を開始する
```python
_set_audio_input_device("MIC_AND_DESKTOP")
subprocess.run(["./scripts/restart_venv_and_run-server.sh"])
time.sleep(60)   # warten bis LT bereit
TRIGGER_FILE.touch()
```
Nachteil: 1 分間テストしてください。アベル・ツフェルレッシグ。

### オプション C — `manage_audio_routing` を直接テストする
```python
from scripts.py.func.manage_audio_routing import manage_audio_routing
manage_audio_routing("MIC_AND_DESKTOP", logger=null_logger)
```
シンクが存在し、トリガーが設定され、セッション開始時に `is_mic_and_desktop_sink_active() == True` が実行され、`manage_audio_routing` がセットアップされます。

Das ist wahrscheinlich die **sauberste Lösung**。

### オプション D — `process_text_in_background` の指示 (キーントリガー)
`test_youtube_audio_regression.py` の詳細 — パイプラインの Vosk 出力ダイレクト、トリガー メカニズムの詳細。 Dann testet man die Pipeline aber nicht das Abschneiden des letzten Wortes。

### オプション E — `run_mode_override=TEST` を開始する Aura
Falls Aura einen Test-Modus hat der das Audio-Routing überspringt.

---

## 5. エンプフェールング

**オプション C** 最高のプロビレン — インポート テスト マシン:

```bash
python3 -c "from scripts.py.func.manage_audio_routing import manage_audio_routing; print('OK')"
```

機能に関する情報:
```python
from scripts.py.func.manage_audio_routing import manage_audio_routing

manage_audio_routing("MIC_AND_DESKTOP", logger=null_logger)
time.sleep(0.5)
TRIGGER_FILE.touch()
```

Dann erkennt Aura beim Session-Start `is_mic_and_desktop_sink_active() == True` と Sink in Ruhe を実行します。

---

## 6. テストは langfristig Bringt でした

Sobald er läuft、カンマン:
- `SPEECH_PAUSE_TIMEOUT` テスト (1.0、2.0、4.0 秒) と、完全に終了するまでの時間
- `transcribe_audio_with_フィードバック.py` パラメータの最適化
- オーディオ処理に関する回帰分析
- Beweisen dass ein Fix wirklich hilft

---

---



**日付:** 2026-03-15  
**ファイル:** `scripts/py/func/checks/test_trigger_end_to_end.py`

---

## 1. 計画

既知の問題を調査するための実際のエンドツーエンド テスト:
**一部の録音では、出力で最後の単語が切り取られます。**

テストでは次のことを行う必要があります。
1. WAV ファイルを仮想マイクとしてフィードします。
2. 実際の使用法とまったく同じように、「touch /tmp/sl5_record.trigger」経由で Aura を開始します。
3. 2 番目のトリガーで停止します
4. 出力と YouTube トランスクリプトを比較する
5.末尾に単語が欠けているかどうかを検出する

---

## 2. 達成されたこと ✅

- Aura はトリガーに正しく反応します
- LT が実行中であり、到達可能です (`http://127.0.0.1:8082`)
- `_wait_for_output()` は `tts_output_*.txt` ファイルを見つけます
- `_fetch_yt_transcript_segment()` は参照テキストを正しくフェッチします
- 基本的なテスト構造がしっかりしていて、概念的に動作します

---

## 3. 未解決の問題 🔴

### 核心的な問題: `manage_audio_routing` がすべてを上書きする

セッション開始時に、Aura は内部的に以下を呼び出します。
```python
manage_audio_routing(SYSTEM_DEFAULT)
```

この関数はまず次のことを行います。
```python
subprocess.run(["pactl", "unload-module", "module-loopback"], capture_output=True)
subprocess.run(["pactl", "unload-module", "module-null-sink"], capture_output=True)
```

**事前に作成したシンクはすべて削除されます。**

次に、「mode == 'SYSTEM_DEFAULT'」 (「MIC_AND_DESKTOP」ではない) であるため、新しいシンクは作成されません。

### 試みられた解決策

|試み |問題 |
|---|---|
| PulseAudio 仮想ソースの作成 | PipeWire は「module-virtual-source」を無視します。
| `settings_local.py` を `MIC_AND_DESKTOP` に設定します。ファイルが複数のエントリで破損しました。
|マークされたオーバーライド ブロックをファイルの最後に書き込む | Aura は、トリガーが起動する前に設定を十分に速くリロードしません。
| `_create_mic_and_desktop_sink()` をテストで直接実行 |セッション開始時に `manage_audio_routing` によって削除されました |
| `pw-ループバック` |ソースとして表示されますが、Aura はそれを聞きません |

---

## 4. 推奨される次のステップ

トリガーの前にテストから直接「manage_audio_routing」を呼び出します。

```python
from scripts.py.func.manage_audio_routing import manage_audio_routing

manage_audio_routing("MIC_AND_DESKTOP", logger=null_logger)
time.sleep(0.5)
TRIGGER_FILE.touch()
```

Aura はセッションを開始するときに `is_mic_and_desktop_sink_active()` をチェックします。`True` の場合、セットアップをスキップし、シンクをそのままにしておきます。これが最もクリーンな解決策です。

---

## 5. このテストにより長期的に何が可能になるか

実行したら:
- `SPEECH_PAUSE_TIMEOUT` 値 (1.0、2.0、4.0s) をテストし、単語のカットオフを検出します
- `transcribe_audio_with_フィードバック.py` パラメータを最適化します。
- オーディオ処理が変更されたときの回帰を捕捉する
- 修正が実際に機能することを証明する
# AUDIO_DIAGNOSTICS_EN.md

# Aura の Linux オーディオ診断


### 1. デバイスの識別
Python 環境で認識されるすべてのオーディオ デバイスを一覧表示します。
```bash
./.venv/bin/python3 -m sounddevice > /tmp/aura_devices.txt && kate /tmp/aura_devices.txt
```
* **確認すべき点:** マイクの **インデックス番号** と **ハードウェア ID (hw:X,Y)** に注意してください。

### 2. ハードウェアを使用しているのは誰ですか?
「デバイスがビジー」または「タイムアウト」エラーが発生した場合は、現在オーディオ ハードウェアをロックしているプロセス (PID) を確認します。
```bash
fuser -v /dev/snd/*
```
* **ヒント:** 「pipewire」または「wireplumber」が表示される場合は、サウンド サーバーがデバイスを管理しています。 PCM デバイス上で直接「python3」または「obs」PID が表示される場合は、他のデバイスがブロックされている可能性があります。

### 3. リアルタイム監視 (PipeWire)
システムが PipeWire (最新の Manjaro では標準) を使用している場合、これがライブ診断に最適なツールです。
```bash
pw-top
```
* **注意すべき点:** 「ERR」列でドロップアウトがないか確認し、Aura (16000Hz) と OBS (48000Hz) が CPU にリサンプリング過負荷を引き起こしていないことを確認します。

### 4. オーディオイベントのモニタリング
マイクがミュートされているとき、ミュートが解除されているとき、または新しいストリームが作成されたときに、ライブ アップデートを表示します。
```bash
pactl subscribe
```
* **使用方法:** これを実行して、Aura を起動します。すぐに多くの「削除」イベントが表示される場合は、プロセスがクラッシュしているか拒否されています。

### 5. ハードウェアバイパステスト
マイクが生のハードウェア レベルで動作するかどうかをテストします (PulseAudio/PipeWire をバイパスします)。これにより、5 秒間の音声が録音されます。
```bash
# Replace hw:1,0 with your device index
arecord -D hw:1,0 -f S16_LE -r 16000 -d 5 /tmp/test.wav && vlc /tmp/test.wav
```
* **結果:** これが機能しても Aura が機能しない場合、問題はハードウェアではなく、サウンドサーバーの設定にあります。

### 6. 緊急リセット
オーディオ システムが停止している場合:
```bash
systemctl --user restart pipewire wireplumber
# Or for older PulseAudio systems:
pulseaudio -k
```


**より簡単なワークフローのヒント:**

`/tmp/diagnose.txt && kate /tmp/diagnose.txt` を参照してください。 🌵🚀
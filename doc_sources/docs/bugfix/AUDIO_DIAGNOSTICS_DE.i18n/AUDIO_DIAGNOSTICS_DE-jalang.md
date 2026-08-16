# ドイツ語版: `AUDIO_DIAGNOSTICS_DE.md`

# Aura の Linux オーディオ診断

Aura Service に関するさまざまな情報をオーディオとコンフリクトで確認できます (タイムアウト、「デバイス ビジー」、またはサンプル レートとコンフリクト)。 Diese Befehle ヘルフェン バイ デア フェラーシュケ。

### 1. 識別情報を取得する
Python に関する音声言語に関する情報は次のとおりです。
```bash
./.venv/bin/python3 -m sounddevice > /tmp/aura_devices.txt && kate /tmp/aura_devices.txt
```
* **Ziel:** は **インデックス番号** と **ハードウェア ID (hw:X,Y)** でマイクロフォンを定義します。

### 2. 死んだのはハードウェアですか?
Wenn Fehler は、「デバイス ビジー」または「タイムアウト」を原因として、ハードウェア ブロック問題 (PID) に関する問題を解決しています。
```bash
fuser -v /dev/snd/*
```
* **ヒント:** Wenn `pipewire` または `wireplumber` erscheint, verwaltet der Sound-Server das Gerät。 「python3」または「obs」の PID は、PCM を使用してブロックされたものを直接管理します。デン・ズグリフ・ファ・アンデレ。

### 3. エクスツァイト監視 (PipeWire)
PipeWire が開発した最新の Manjaro システム ツール:
```bash
pw-top
```
* **Ziel:** Prüfe die Spalte `ERR` auf Fehler und stelle sicher、dass Aura (16000Hz) und OBS (48000Hz) keine CPU-Überlastung durch Resampling verursachen。

### 4. オーディオイベントの説明
Verfolge ライブ、Mikrofone の最新のストリーミング:
```bash
pactl subscribe
```
* **アンウェンドゥン:** スターテは死に、オーラは消えます。 `削除` を実行すると、システムの変更を行うためのイベントが実行されます。

### 5. ハードウェアダイレクトテスト
ハードウェア エベント機能 (PulseAudio/PipeWire を含む) のマイクロフォンをテストします。 Nimmt 5 Sekunden auf:
```bash
# Ersetze hw:1,0 durch deinen Geräte-Index
arecord -D hw:1,0 -f S16_LE -r 16000 -d 5 /tmp/test.wav && vlc /tmp/test.wav
```
* **問題:** ウェンは、ハードウェアとサウンド サーバーの構成に問題があり、問題が発生しました。

### 6. Notfall-リセット
Falls のオーディオ システム コンポーネント:
```bash
systemctl --user restart pipewire wireplumber
# Oder für ältere PulseAudio-Systeme:
pulseaudio -k
```

---

**ワークフローに関するヒント:** Kate zu betrachten の Ausgaben direkt、hänge einfach `> /tmp/diagnose.txt && kate /tmp/diagnose.txt` と Befehl an を参照してください。 🌵🚀
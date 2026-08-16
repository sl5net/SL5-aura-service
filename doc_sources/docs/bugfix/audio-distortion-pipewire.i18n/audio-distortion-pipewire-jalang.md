# バグ修正: オーディオの歪みと PipeWire ハング (Linux)

このドキュメントでは、**SL5-aura-service** を OBS、AnyDesk、または高周波 TTS ストリームなどの他のメディア アプリケーションと一緒に使用するときに発生する可能性のある音声の歪み (「klirren」)、ロボット音声アーティファクト、およびシステム オーディオのハングを解決する方法について説明します。

＃＃ 症状
- 音声出力/入力音が歪んだり、金属的、または「耳障り」な音になります。
- システム オーディオがハングし、「PulseAudio への接続を確立しています」または「お待ちください」というメッセージが表示されます。
- 高 CPU 負荷または同時ストリーム使用後の合計オーディオ損失。
- ジャーナル ログには、「spa.alsa: hw:X: snd_pcm_status error: No such device」が表示されます。

＃＃ 根本的な原因
Manjaro やその他の最新の Linux ディストリビューションでは、**PipeWire** がオーディオを管理します。歪みは通常、次のような原因で発生します。
1. **バッファ アンダーラン:** 同時ストリーム間の競合 (例: TTS/OBS の実行中にオーディオをキャプチャする AnyDesk)。
2. **サンプルレートの不一致:** 44.1kHz と 48kHz の間で頻繁に切り替わります。
3. **USB タイミングの問題:** バス負荷が高いため、USB ヘッドセット (Plantronics/Poly など) が一時的に切断されます。

---

## ソリューション

### 1. 即時回復 (「核」リセット)
オーディオ スタックがフリーズまたは歪んでいる場合は、オーディオ関連のプロセスをすべて強制終了します。すぐに自動再起動されます。

```bash
# Force kill PipeWire and its PulseAudio compatibility layer
killall -9 pulseaudio pipewire pipewire-pulse
```

### 2. 防止と安定性の設定

#### AnyDesk オーディオを無効にする
AnyDesk は頻繁にオーディオ デバイスに接続しようとし、ハードウェアの競合を引き起こします。
- **アクション:** AnyDesk 設定 -> **オーディオ** を開き、**「オーディオの送信」** と **「オーディオの再生」** を無効にします。

#### PipeWire サンプル レートを修正 (推奨)
TTS 再生中のリサンプリング アーティファクトを避けるために、PipeWire を強制的に 48kHz に維持します。

1. 設定ディレクトリを作成します: `mkdir -p ~/.config/pipewire`
2. デフォルトの設定をコピーします: `cp /usr/share/pipewire/pipewire.conf ~/.config/pipewire/`
3. `~/.config/pipewire/pipewire.conf` を編集し、次のように設定します。
   ```conf
   default.clock.rate = 48000
   ```
4. サービスを再起動します。
   ```bash
   systemctl --user restart pipewire pipewire-pulse wireplumber
   ```

---

## 3. ポストプロダクションリカバリ (FFmpeg)
セッションを録音し、オーディオが歪んでいる (「クリリング」) 場合は、次の `ffmpeg` フィルター チェーンを使用してファイルを修復します。

### 推奨される修復コマンド
このコマンドは、ビデオを再エンコードせずに、デクリッパー、ノイズ リダクション、およびローパス フィルターを適用して高周波デジタル アーティファクトを除去します。

テスト済みで非常に良好です:

```bash
ffmpeg -i input_video.mp4 
    -af "adeclip, afftdn, lowpass=f=5000, volume=1.5" \
    -c:v copy reparatur_output.mp4  
```

(テストされていません):

```bash
ffmpeg -i input_video.mp4 \
  -af "adeclip, afftdn, lowpass=f=3500, volume=1.8" \
  -c:v copy repaired_audio_output.mp4
```



テストされていません:
```bash
ffmpeg -i input_video.mp4 -af "arnndn=m=cb.rnnn, lowpass=f=5000" -c:v copy ki_reparatur.mp4
```




**フィルターの内訳:**
- `adeclip`: デジタル クリッピング スパイクを丸めます。
- `afftdn`: FFT ベースのデジタル ノイズを低減します。
- `lowpass=f=3500`: 最も「クリアリング」が発生する 3.5kHz を超える周波数をカットします (音声をよりクリアに/より暖かくします)。
- `volume=1.8`: フィルタリング中のボリューム損失を補正します。
- `-c:v copy`: 元のビデオ品質を維持します (非常に高速)。

---

## デバッグツール
開発中にオーディオの健全性をリアルタイムで監視するには:
- `pw-top`: リアルタイムエラー(ERR列)とバッファステータスを表示します。
- `journalctl --user -u Pipewire`: ハードウェアの切断をチェックします。
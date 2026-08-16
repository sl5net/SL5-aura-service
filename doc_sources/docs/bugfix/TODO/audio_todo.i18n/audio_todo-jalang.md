'25.12.31 18:25 水

継続的な実行と ToDo リストの作成:

### ドキュメント: 「統合オーディオ入力」(マイク + デスクトップ) のバージョン
**ステータス:** Pausiert (概念実証が存在し、非常に安定/パフォーマンス)。

**エルファールンゲン / 調査結果:**
* **ルーティング:** PipeWire/PulseAudio は、Python-Stream (ALSA-Bridge) の物理的な標準マイクロフォン (Stream-Restore-Logik) を制御します。
* **パフォーマンス:** Die Verarbeitung von RMS、VAD und Vosk in einem engen Loop、kombiniert mit externen `pactl`-Aufrufen、führ zu hoher CPU-Last (Lüfterdrehen)。
* **信号:** トロッツ コレクテム デバイス インデックスは、RMS ペーゲル フォン ~1.7 で頻繁に作成され、ALSA と PipeWire のマッピングに関する誤った情報が含まれていました。

---

### ToDo リスト (将来のスプリント)
1. **[ ] WirePlumber 統合:** ネイティブの PipeWire-Rules (「スクリプト」) を実行し、「pactl」フックを使用して永続的なストリームを実行します。
2. **[ ] パフォーマンスの最適化:** Den Audio-Loop entlasten (z.B. RMS の詳細なチェックや VAD パラメーターの最適化)。
3. **[ ] ネイティブ モノラル シンク:** 16kHz のモノラル シンク システムを使用した、リサンプリングの最終的なシンク システムです。
4. **[ ] 堅牢なデバイス マッピング:** アドレスを指定した「サウンドデバイス」名でのモニターシンクの検出方法が安定しています。

---

### `config/settings.py` を更新します
```python
# config/settings.py

# AUDIO_INPUT_DEVICE = None 
# PLANNED: UNIFIED_AUDIO_INPUT (Mic + Desktop Sound)
# Current status: Experimental. Requires stable PipeWire routing and CPU optimization.
# AUDIO_INPUT_DEVICE = 'UNIFIED_AUDIO_INPUT' 
```

**[EN] 概要:**
仮想「ヌルシンク」を使用してマイクとデスクトップオーディオをマージしようとしました。 PipeWire のストリーム復元によりルーティングが不安定でした。高い CPU 負荷が観察されました。将来の反復のためにロジックが文書化されました。

Ich bin gespannt, ob wir bei einem späteren Ver such mit einer Performanteren Lösung (vielleicht direkt über PipeWire-Schnittstellen) Erfolg haben! Erledigt für heute。
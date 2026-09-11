# 録音オーバーレイ (オンスクリーン表示)

録音オーバーレイは、ディクテーションのステータスを即座にクロスプラットフォームで視覚的に示すインジケーターを提供します。これはデスクトップ通知デーモンや「応答不可」フィルターとは独立して動作し、主画面に状態を直接表示します。

## 視覚的な例

|左下 (`bl`) |右上 (`tr`) |
| :---: | :---: |
| ![Top-Right Overlay 1](../images/recording_overlay_1.png) | ![Top-Right Overlay 2](../images/recording_2.png) |
| *暗いパネルやシステム トレイに溶け込みます* | *明るい窓または複雑な窓上での高コントラスト* |

## 州

- **録音 (`🔴`)**: 輪郭が強調表示された鮮やかな赤い円 (`#181818` の `#e62222`) は、アクティブなオーディオ録音を示します。
- **アイドル**:
- `hidden` (デフォルト): ウィンドウが完全に閉じられ、デスクトップのスペースが通常の操作のために解放されます。
- `pentagon`: アイドル モード中に微妙な幾何学模様の五角形バッジ (`⬟`) を表示します。

＃＃ 構成

設定は `config/settings.py` で管理されます。

```python
# Enable/disable on-screen overlay
RECORDING_OVERLAY_ENABLED = True

# Keep window always on top without borders
RECORDING_OVERLAY_TOPMOST = True

# Placement: "tr" (top-right) or "bl" (bottom-left)
RECORDING_OVERLAY_POSITION = "tr"

# Inactivity mode: "hidden" or "pentagon"
RECORDING_OVERLAY_IDLE_MODE = "hidden"

# Window dimension in pixels
RECORDING_OVERLAY_SIZE = 36
```

＃＃ 建築

- Python 標準ライブラリ (`tkinter`) を使用して構築されており、外部 C 依存関係は必要ありません。
- スレッドセーフなキュー イベント処理を使用して、バックグラウンド デーモン スレッドで実行します。
- マルチディスプレイ環境でプライマリ モニターを動的に検出します。

(s、10.9.'26 14:41 木)
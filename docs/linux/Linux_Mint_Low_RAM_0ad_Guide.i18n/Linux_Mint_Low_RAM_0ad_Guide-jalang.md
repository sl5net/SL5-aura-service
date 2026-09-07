# 低 RAM システムで Aura Voice Control を使用して 0 A.D. を実行する (Linux Mint)

このガイドでは、レガシーまたはメモリに制約のある Linux Mint ハードウェア上で **0 A.D.** とともに **sl5net Aura** 音声コントロールを実行するためのセットアップとメモリの最適化について説明します。

## ターゲットのハードウェアとシステム プロファイル
- **デバイス**: Lenovo ThinkPad T520 (ラップトップ)
- **CPU**: Intel Core i7-2620M (デュアルコア @ 2.70GHz - 3.40GHz)
- **メモリ**: 5.67 GiB RAM
- **スワップ**: 4 GiB の実効スワップ
- **オペレーティング システム**: Linux Mint 21.3 Virginia (64 ビット)
- **デスクトップ環境**: Cinnamon 6.0.5 (X11 ディスプレイ サーバー)
- **適用対象**: 西暦 0 年 (帝国のアセンダント)

## メモリ管理とアーキテクチャ
RAM が 6 GiB 以下のシステムでは、重いデスクトップ環境、3D RTS ゲーム (西暦 0 年)、および音声認識を同時に実行するには、厳密なメモリ保護が必要です。

1. **Vosk 音声モデルの優先度**:
- 低いメモリ フットプリント (約 300 ～ 500 MB) のために `vosk-model-small-de` (または同等の言語) を使用します。
- Vosk モデルの保持は、ゲームプレイ中のリアルタイムのコマンド応答性を確保するために優先されます。

2. **LanguageTool の自動エビクション**:
- LanguageTool の Java プロセスは、最大 1.34 GiB RSS を消費する可能性があります。
- 利用可能な RAM が「CRITICAL_THRESHOLD_MB」 (2.0 GiB) を下回ると、Aura の「model_manager」は LanguageTool を直ちに終了し、ゲーム用に最大 1.3 GiB の RAM を解放します。
- 5 分間のクールダウン (`set_ language_tool_cooldown`) により、LanguageTool がアクティブなゲームプレイ中に再起動してメモリをスラッシングするのを防ぎます。

## 検証コマンド
システム メモリとプロセスの状態を検査するには、次の手順を実行します。
# メモリとスワップの使用状況を確認する
```bash
free -h
```

# LanguageTool プロセスがエビクトされているかどうかを確認する
```bash
ps aux | grep -i "[l]anguagetool"
```
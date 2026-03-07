# 開発者ガイド: サービスコールグラフの生成

このドキュメントでは、長時間実行される「aura_engine.py」の視覚的なコールグラフを生成するための堅牢でスレッドセーフな方法について説明します。 `yappi` プロファイラー (マルチスレッド サポート用) と `gprof2dot` を視覚化に使用します。

### 前提条件

必要なツールがグローバルまたは仮想環境にインストールされていることを確認してください。

```bash
# Required Python libraries for profiling
pip install yappi gprof2dot

# Required system library for visualization
# Linux: sudo apt install graphviz 
```

### ステップ 1: プロファイリング用にサービスを変更する

「yappi」プロファイラーを手動で起動し、中断（「Ctrl+C」）時にプロファイリングデータを正常に保存するには、「aura_engine.py」スクリプトを変更する必要があります。

**「aura_engine.py」の主な変更点:**

1. **インポートとシグナル ハンドラー:** `yappi` をインポートし、`yappi.stop()` と `stats.save(...)` を呼び出すための `generate_graph_on_interrupt` 関数 (以前に実装したとおり) を定義します。
2. **開始/停止:** `yappi.start()` と `signal.signal(signal.SIGINT, ...)` を `if __name__ == "__main__":` ブロック内に追加して、`main(...)` の実行をラップします。

### ステップ 2: サービスの実行とデータの収集

変更したスクリプトを直接実行し、スレッド化された関数 (LanguageTool 修正など) を含むすべてのコア関数が確実に呼び出されるように、十分な時間 (10 ～ 20 秒など) データを処理します。

```bash
# Execute the service directly (do NOT use the pycallgraph wrapper)
python3 aura_engine.py
```

**Ctrl+C** を 1 回押して、シグナル ハンドラーをトリガーします。これにより、プロファイラーが停止し、生データが次の場所に保存されます。

`\mathbf{yappi\_profile\_data.prof`

### ステップ 3: ビジュアル グラフの生成とフィルタリング

`gprof2dot` を使用して、生の `pstats` データを SVG 形式に変換します。 `--include` や `--threshold` などの高度なフィルタリング オプションは特定の環境ではサポートされていない可能性があるため、基本的な **`--strip`** フィルタを使用してパス情報をクリーンアップし、システム内部の混乱を軽減します。

**視覚化コマンドを実行します:**

```bash
python3 -m gprof2dot -f pstats yappi_profile_data.prof --strip | dot -Tsvg -o yappi_call_graph_stripped.svg
```

### ステップ 4: ドキュメント作成 (手動トリミング)

結果の `yappi_call_graph_stripped.svg` (または `.png`) ファイルは大きくなりますが、すべてのスレッドを含む完全な実行フローが正確に含まれています。

ドキュメント化の目的で、**画像を手動でトリミング**して中央ロジック (10 ～ 20 個のコア ノードとその接続) に焦点を当て、リポジトリ ドキュメント用に焦点を当てた読みやすいコール グラフを作成します。

### アーカイブ

変更した構成ファイルと最終的なコール グラフの視覚化は、ドキュメント ソース ディレクトリにアーカイブする必要があります。

|アーティファクト |場所 |
| :--- | :--- |
| **変更されたサービス ファイル** | `doc_sources/profiling/aura_engine_profiling_base.py` |
| **最終的なトリミングされた画像** | `doc_sources/profiling/core_logic_call_graph.svg` |
| **生のプロファイリング データ** | *(オプション: 最終リポジトリのドキュメントから除外する必要があります)* |


![yappi_call_graph](../yappi_call_graph_stripped.svg_20251024_010459.png "yappi_call_graph_stripped.svg_20251024_010459.png")
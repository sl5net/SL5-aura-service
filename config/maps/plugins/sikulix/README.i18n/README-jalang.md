[![SikuliX](https://raw.githubusercontent.com/oculix-org/SikuliX1/master/Support/sikulix-red.png)](https://sikulix.github.io)
# コンピューター ビジョンを活用したビジュアル オートメーション フレームワーク
**それが見えるなら、自動化できます。**

SikuliX は現在、元の作成者 [**RaiMan**](https://github.com/RaiMan) の完全な同意を得て、[**oculix-org**](https://github.com/oculix-org) の下で積極的に保守されています。

## SikuliX とは
SikuliX は **コンピューター ビジョン** ([OpenCV](https://opencv.org/) を利用) を使用して、**Windows**、**macOS**、**Linux** の画面上に表示されるものを識別し、操作します。

**画像認識**を通じて GUI 要素を特定し、シミュレートされたマウスとキーボードの操作でそれらを駆動します。ソース コード、DOM、内部 API へのアクセスは必要ありません。

## オーラプラグイン
このプラグインを使用すると、SikuliX IDE がフォーカスされているときに SikuliX コマンドを音声で指示できます。

|音声コマンド (de) |出力 |
|---|---|
| 「クリック」 | `click("image.png")` |
| 「ドッペルクリック」 | `doubleClick("image.png")` |
| "レヒツクリック" | `rightClick("image.png")` |
| 「ワルテ」 | `wait("image.png", 10)` |

コマンドは、SikuliX ウィンドウ (`sikulixide`、`SikuliX`、`Sikuli`) がフォーカスされている場合にのみアクティブになります。

＃＃ リソース
-[Get SikuliX ready to use](https://raimans-sikulix.gitbook.io/untitled/)
- [SikuliX Documentation](https://sikulix-2014.readthedocs.io/en/latest/index.html)
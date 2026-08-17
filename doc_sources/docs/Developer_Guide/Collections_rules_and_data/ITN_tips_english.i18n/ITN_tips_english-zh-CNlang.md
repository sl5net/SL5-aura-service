技术术语是**逆文本标准化（ITN）**。

如果你搜索它，你会发现大量的规则和数据。

以下是无需亲自输入所有内容即可填充地图的最佳资源：

### 1. ITN 规则集合（“黄金标准”）
* **[itnpy](https://github.com/barseghyanartur/itnpy)：** 一个简单的、确定性的 Python 工具，专为此目的而设计。它使用 CSV 文件将口语单词转换为书面字符（数字、货币、日期）。您可以将 CSV 几乎 1:1 复制到地图中。

* **[NVIDIA NeMo ITN](https://github.com/NVIDIA/NeMo)：** 非常强大。他们拥有几乎所有语言的巨大语法文件。在那里您可以找到测量单位、标题和日期格式的列表。

### 2.标点符号和大小写的数据源
* **[Vosk recasepunc](https://github.com/benob/recasepunc)：** 这是 Vosk 的标准工具。它使用模型，但源代码通常包含可以提取的缩写和专有名称列表。

* **[Google Text Normalization Dataset](https://github.com/rwsproat/text-normalization-data)：** 一个巨大的数据集（为 Kaggle 挑战创建），包含数百万个关于如何将口语转换为书面语言的示例。

### 3.“听写助手”库
* **[num2words](https://github.com/savoirfairelinux/num2words):** 如果您需要数字映射，您可以在此处找到“一”到“一百万”的列表。
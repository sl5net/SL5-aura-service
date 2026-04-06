[![SikuliX](https://raw.githubusercontent.com/oculix-org/SikuliX1/master/Support/sikulix-red.png)](https://sikulix.github.io)
# 由计算机视觉提供支持的视觉自动化框架
**如果你能看到它，你就可以自动化它。**

SikuliX 现在在 [**oculix-org**](https://github.com/oculix-org) 下积极维护，并得到其原始创建者 [**RaiMan**](https://github.com/RaiMan) 的完全同意。

## SikuliX 是什么
SikuliX 使用**计算机视觉**（由 [OpenCV](https://opencv.org/) 提供支持）来识别屏幕上可见的任何内容并与之交互 - 跨 **Windows**、**macOS** 和 **Linux**。

它通过**图像识别**定位 GUI 元素，然后通过模拟鼠标和键盘操作来驱动它们。无需访问源代码、DOM 或内部 API。

## 光环插件
该插件可让您在 SikuliX IDE 处于焦点状态时通过语音听写 SikuliX 命令。

|语音命令（德）|输出|
|---|---|
| “点击”| `点击("image.png")` |
| “双重舔”| `doubleClick("image.png")` |
| “rechtsklick”| `rightClick("image.png")` |
| “疣”| `等待("image.png", 10)` |

仅当 SikuliX 窗口（`sikulixide`、`SikuliX`、`Sikuli`）聚焦时命令才处于活动状态。

＃＃ 资源
- [Get SikuliX ready to use](https://raimans-sikulix.gitbook.io/untitled/)
- [SikuliX Documentation](https://sikulix-2014.readthedocs.io/en/latest/index.html)
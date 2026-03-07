# 开发人员指南：生成服务调用图

本文档描述了用于生成长期运行的“aura_engine.py”的可视化调用图的稳健、线程安全的方法。我们使用“yappi”分析器（用于多线程支持）和“gprof2dot”进行可视化。

### 先决条件

确保您已在全局或虚拟环境中安装了必要的工具：

__代码_块_0__

### 第 1 步：修改分析服务

必须修改“aura_engine.py”脚本以手动启动“yappi”分析器并在中断时正常保存分析数据（“Ctrl+C”）。

**`aura_engine.py` 中的主要更改：**

1. **导入和信号处理程序：** 导入 `yappi` 并定义 `generate_graph_on_interrupt` 函数（如之前实现的）以调用 `yappi.stop()` 和 `stats.save(...)`。
2. **开始/停止：** 在 `if __name__ == "__main__":` 块中添加 `yappi.start()` 和 `signal.signal(signal.SIGINT, ...)` 来包装 `main(...)` 的执行。

### 第 2 步：运行服务并收集数据

直接运行修改后的脚本，并允许其处理数据足够的时间（例如 10-20 秒），以确保调用所有核心函数，包括线程函数（如 LanguageTool 校正）。

__代码_块_1__

按 **Ctrl+C** 一次即可触发信号处理程序。这将停止分析器并将原始数据保存到：

`\mathbf{yappi\_profile\_data.prof`

### 步骤 3：生成和过滤可视化图表

我们使用“gprof2dot”将原始“pstats”数据转换为 SVG 格式。由于我们的特定环境可能不支持“--include”和“--threshold”等高级过滤选项，因此我们使用基本的“--strip”过滤器来清理路径信息并减少系统内部的混乱。

**执行可视化命令：**

__代码_块_2__

### 步骤 4：文档（手动裁剪）

生成的“yappi_call_graph_stripped.svg”（或“.png”）文件会很大，但它准确地包含完整的执行流程，包括所有线程。

出于文档目的，**手动裁剪图像**以重点关注中央逻辑（10-20 个核心节点及其连接），从而为存储库文档创建重点突出且可读的调用图。

### 归档

修改后的配置文件和最终的调用图可视化应存档在文档源目录中：

|神器|地点 |
| :--- | :--- |
| **修改后的服务文件** | `doc_sources/profiling/aura_engine_profiling_base.py` |
| **最终裁剪图像** | `doc_sources/profiling/core_logic_call_graph.svg` |
| **原始分析数据** | *（可选：应从最终存储库文档中排除）* |


![yappi_call_graph](../yappi_call_graph_stripped.svg_20251024_010459.png "yappi_call_graph_stripped.svg_20251024_010459.png")
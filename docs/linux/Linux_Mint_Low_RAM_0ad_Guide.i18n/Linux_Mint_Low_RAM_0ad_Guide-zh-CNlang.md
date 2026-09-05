# 在低 RAM 系统上使用 Aura 语音控制运行 0 A.D. (Linux Mint)

本指南记录了在旧版或内存受限的 Linux Mint 硬件上运行 **sl5net Aura** 语音控制以及 **0 A.D.** 的设置和内存优化。

## 目标硬件和系统配置文件
- **设备**：Lenovo ThinkPad T520（笔记本电脑）
- **CPU**：英特尔酷睿 i7-2620M（双核 @ 2.70GHz - 3.40GHz）
- **内存**：5.67 GiB RAM
- **交换**：4 GiB 有效交换
- **操作系统**：Linux Mint 21.3 Virginia（64 位）
- **桌面环境**：Cinnamon 6.0.5（X11 显示服务器）
- **应用目标**：公元 0 年（帝国崛起）

## 内存管理和架构
在 RAM ≤ 6 GiB 的系统上，同时运行繁重的桌面环境、3D RTS 游戏（0 A.D.）和语音识别需要严格的内存保护：

1. **Vosk 语音模型优先级**：
- 使用“vosk-model-small-de”（或等效语言）来实现低内存占用（~300-500 MB）。
- Vosk 模型保留优先，以确保游戏过程中的实时命令响应。

2. **自动语言工具驱逐**：
- LanguageTool 的 Java 进程可以消耗约 1.34 GiB RSS。
- 当可用 RAM 降至“CRITICAL_THRESHOLD_MB” (2.0 GiB) 以下时，Aura 的“model_manager”会立即终止 LanguageTool，为游戏释放约 1.3 GiB RAM。
- 5 分钟的冷却时间 (`set_language_tool_cooldown`) 可防止 LanguageTool 在游戏进行期间重新启动并破坏内存。

## 验证命令
检查系统内存和进程状态：
__代码_块_0__
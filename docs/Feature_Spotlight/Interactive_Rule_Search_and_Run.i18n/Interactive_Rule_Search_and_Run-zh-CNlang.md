# 交互式规则搜索和运行

这个焦点强调了交互式规则搜索和执行系统，桥接语音命令、实时导航和即时执行。

## 核心特性
[1] **双窗格实时搜索（`fzf`）：** 左窗格过滤规则文件；右窗格通过“preview_rule.py”显示行上下文预览。
[2] **即时执行（`Enter` / `Ctrl+R`）：** 通过后台的 `run_palette_command.py` 立即运行提取的目标命令。
[3] **直接编辑 (`Ctrl+E`)：** 直接在目标行启动编辑器（使用 `@line` 的 CudaText，使用 `--line` 的 Kate/VS Code）。
[4] **浮动窗口热键：** 绑定到“Super+S”，以实现快速、桌面集成的工作区工作流程。
[5] **语音命令支持：** 许多语音命令在“search_rules.sh”中预先配置搜索模式，以实现快速、有针对性的查找。

## 跨平台支持
- **Linux Bash (`run_rule.sh` / `search_rules.sh`)：** 具有历史记录跟踪和剪贴板操作 (`Ctrl+X` / `Ctrl+A`) 的全功能实现。
- **Windows PowerShell (`search_rules.ps1`)：** 提供轻量级终端搜索功能的配套工具。

![Interactive Rule Search Console](.././assets/interactive_rule_search_20260727_155546.png)

![Interactive Rule Search Console](.././assets/interactive_rule_search_wie_wetter_heute20260727.png)

![Interactive Rule Search Console](.././assets/interactive_rule_search_20260814.png)
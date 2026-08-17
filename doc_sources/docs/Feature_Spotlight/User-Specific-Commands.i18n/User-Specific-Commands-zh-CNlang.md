# 用户特定的语音命令

Aura 允许您定义**仅对您**（或特定团队成员）有效的自定义命令。这可以防止其他用户触发个人快捷方式或实验性功能。

＃＃ 设置

您可以在任何映射文件中应用这些规则，例如“FUZZY_MAP_pre.py”（原始输入）或“FUZZY_MAP.py”（校正后）。

目标文件：`config/maps/plugins/internals/de-DE/FUZZY_MAP_pre.py`

### 代码示例

将此块添加到文件末尾：

__代码_块_0__
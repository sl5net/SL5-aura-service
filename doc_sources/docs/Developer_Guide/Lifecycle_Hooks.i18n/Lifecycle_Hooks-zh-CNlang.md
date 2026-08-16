Aura SL5 挂钩：已添加

HOOK_PLUGIN_LOAD = 'on_plugin_load'
HOOK_FILE_LOAD = 'on_file_load'
HOOK_RELOAD = 'on_reload'
HOOK_UPSTREAM = 'on_folder_change'

on_folder_change() 和
on_reload() 在热重载后触发逻辑。使用它来“菊花链”执行父脚本，例如复杂包的 secure_packer.py。

# 开发人员指南：插件生命周期挂钩

Aura SL5 允许插件（地图）定义特定的“钩子”，当模块状态发生变化时自动执行。这对于**安全私人地图**系统等高级工作流程至关重要。

## `on_folder_change` 钩子 Hook

实现了“on_folder_change”钩子检测。重新加载器现在扫描目录

## `on_reload()` 钩子

`on_reload()` 函数是一个可选函数，您可以在任何 Map 模块中定义。

＃＃＃ 行为
* **触发：**模块成功**热重载**后立即执行（文件修改+语音触发）。
* **上下文：** 在主应用程序线程内运行。
* **安全：** 包裹在 `try/ except` 块中。此处的错误将被记录，但不会导致应用程序崩溃。

### 使用模式：“菊花链”
对于复杂的包（例如私有地图），您通常有许多子文件，但只有一个中央脚本（“secure_packer.py”）应该处理逻辑。

您可以使用钩子向上委托任务：

__代码_块_0__
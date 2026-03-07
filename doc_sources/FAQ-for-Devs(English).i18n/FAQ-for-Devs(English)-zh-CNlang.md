# 正则表达式规则

重要提示：请按正确的顺序应用正则表达式。

您必须首先使用复合（更通用）正则表达式，然后应用专用正则表达式。

原因是，如果较短的专用正则表达式首先运行，它可能会匹配对于较大的复合正则表达式至关重要的字符串部分。这将使复合正则表达式随后无法找到其匹配项。
(S. 20.10.'25 18:37 星期一)

# Linux/Mac

如果你想自动启动服务可以添加：
〜/projects/py/STT/scripts/restart_venv_and_run-server.sh
到自动启动。

仅在有互联网连接时启动服务：
然后在settings_local.py中设置：
SERVICE_START_OPTION = 1


## 添加回车
当你设置
config/settings_local.py/AUTO_ENTER_AFTER_DICTATION_REGEX_APPS
到 1 后，它会添加 Enter。

当你设置
tmp/sl5_auto_enter.flag
到 1 后，它会添加 Enter。

当您启动服务时，tmp/sl5_auto_enter.flag将被覆盖。
tmp/sl5_auto_enter.flag 可能更容易用其他脚本为您解析，并且读取速度可能会更快一些。

使用其他号码禁用
(S. 13.9.'25 16:12 星期六)
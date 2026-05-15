# 记录过滤器配置文件

活动日志过滤器始终是“config/filters/settings_local_log_filter.py”。

## 个人资料

预定义的配置文件存储在`config/filters/.backlock/`中：

|简介 |描述 |
|---|---|
| `第一次运行` |最小输出 - 仅错误和状态。首次启动时自动应用。 |
| `正常` |适合日常使用的标准过滤器。 |

## 手动切换配置文件

__代码_块_0__

## 添加自定义配置文件

1. 在 `config/filters/.backlock/my_profile/` 下创建一个新文件夹
2. 将现有的 `settings_local_log_filter.py` 复制到其中并根据您的需要进行编辑
3.如上所示使用`cp`应用它

## 自动配置文件切换

首次启动时，Aura 检测到 `log/` 目录尚不存在，并且
自动将“first_run”配置文件复制为活动过滤器。
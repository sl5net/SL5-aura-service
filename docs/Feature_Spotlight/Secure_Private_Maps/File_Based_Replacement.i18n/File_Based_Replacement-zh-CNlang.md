# 特色聚焦：基于文件的规则替换

本文档描述了如何保留敏感值（密码、API 密钥、令牌）
通过加载`FUZZY_MAP_pre`/`FUZZY_MAP`源代码和Git历史记录
在运行时从单独的文件中替换文本，而不是对其进行硬编码。

这在直播或屏幕共享期间特别有用，其中地图
源代码本身可能是可见的，但引用的文件不是可见的。

---

## 1. 概念

通常，规则的“替换”字段是文字输出文本：

__代码_块_0__

启用基于文件的替换后，以
配置的前缀（默认为“-”或“.”）被视为**文件名**。
Aura 解析相对于插件自己目录的文件名，读取其
内容，并使用该内容作为替换文本。

__代码_块_1__

如果插件的“FUZZY_MAP_pre.py”旁边存在“api_key.txt”，则其（已删除）
内容用作替换。如果文件不存在，则文字
相反，返回字符串“-api_key.txt”（故障安全：不会意外泄漏
“找不到文件”作为可用文本，并且没有崩溃）。

---

## 2. 设置

在 `config/settings.py` （或本地的 `config/settings_local.py`）中配置
覆盖）：

|设置|类型 |默认|描述 |
|---|---|---|---|
| `FILE4REPLACMENT_USE` | `布尔` | '真实' |整个功能的主开关。如果“False”，则始终按字面意思使用“replacement”。 |
| `FILE4REPLACMENT_ALLOWED_PREFIXES` | `元组[str]` | `('-', '.')` | “替换”值必须以这些前缀之一开头才能触发文件查找。空/`无` = 任何不以字母开头的值都被视为潜在的文件名。 |
| `FILE4REPLACMENT_ALLOW_PATH_TRAVERSAL` | `布尔` | ‘假’|如果为“True”，则允许解析插件自己的目录之外的文件（例如绝对路径或“../”序列）。请参阅下面的安全部分。 |
| `FILE4REPLACMENT_DENY_PREFIXES` | `元组[str]` |例如`('/etc', '/proc', '/dev', '/var/lib', '/root', 'C:\\Windows', 'C:\\Program Files')` |无论“FILE4REPLACMENT_ALLOW_PATH_TRAVERSAL”如何，以其中任何一个开头的解析绝对路径都会被拒绝。针对系统目录的硬安全边界。 |

---

## 3. 路径解析

文件解析如下：

1.插件的`source_path`（由地图加载器自动记录）是
加入“PROJECT_ROOT”（从“SL5NET_AURA_PROJECT_ROOT”读取
环境变量）来获取插件的目录。
2. `replacement` 值被加入到该目录中。
3. 除非`FILE4REPLACMENT_ALLOW_PATH_TRAVERSAL`为`True`，否则解析的路径
必须保留在插件的目录中，否则查找将被拒绝。
4. 无论上述情况如何，任何以以下条目开头的已解析路径
`FILE4REPLACMENT_DENY_PREFIXES` 始终被拒绝。
5. 如果文件存在，则返回其剥离的内容。否则，
原始“替换”字符串原样返回。

---

## 4. 安全说明

- 仅当您了解以下内容时才启用“FILE4REPLACMENT_ALLOW_PATH_TRAVERSAL”
含义：它允许任何可以编辑“FUZZY_MAP_pre”文件的用户（例如
通过在线地图编辑器）读取 Aura 进程可以读取的任意文件
访问，并将其内容显示为实时输出文本。
- `FILE4REPLACMENT_DENY_PREFIXES` 提供了针对
即使允许路径遍历，公共系统目录也是如此，但它是
不能替代限制谁可以编辑地图文件。
- 引用的文件是磁盘上的纯文本。与您的操作系统文件合并
如果内容敏感。

---

## 5. 示例

有关工作示例插件，请参阅“config/maps/plugins/TEST_FILE4REPLACMENT/”，
和用于练习的测试脚本的“tools/tests/TEST_FILE4REPLACEMENT.sh”
目录内查找和插件目录外查找。

__代码_块_2__

使用所需的替换文本在此文件旁边创建“.Zebra.txt”，然后
说出（或通过控制台输入）“s Zebra”来触发它。
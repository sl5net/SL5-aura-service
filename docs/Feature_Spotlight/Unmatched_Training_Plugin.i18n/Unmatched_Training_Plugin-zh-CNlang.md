# 无与伦比的训练插件 (`a_collect_unmatched_training`)

＃＃ 目的

该插件自动收集无法识别的语音输入并添加它们
作为模糊映射正则表达式的新变体。这使得系统能够“自我训练”
随着时间的推移，通过从无与伦比的识别结果中学习。

## 它是如何工作的

1.“FUZZY_MAP_pre.py”中的“COLLECT_UNMATCHED”包罗万象的规则在以下情况下触发：
没有其他规则与语音输入匹配。
2. 通过“on_match_exec”使用匹配的文本调用“collect_unmatched.py”。
3. 文本被添加到“unmatched_list.txt”（以竖线分隔）。
4. `FUZZY_MAP_pre.py` 中的正则表达式会自动使用新变体进行扩展。

## 禁用插件

当您收集了足够的训练数据后，可以通过以下任一方式禁用此插件：

- 在光环设置中停用它
- 从“maps”目录中删除插件文件夹
- 使用无效名称重命名文件夹（例如添加空格：`a_collect unmatched_training`）

## 文件结构
__代码_块_0__

＃＃ 笔记

该插件在运行时修改“FUZZY_MAP_pre.py”。确保承诺
定期更新文件以保存收集的训练数据。
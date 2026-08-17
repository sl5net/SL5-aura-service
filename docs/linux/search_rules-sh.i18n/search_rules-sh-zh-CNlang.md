除了许多搜索选项之外，您的开发环境中可能还有全文搜索，您还可以使用：

脚本/search_rules/search_rules.sh

这允许您在现有地图、源代码或文档中进行搜索。然后你可以打开你在你最喜欢的编辑器中找到的和平或在github上打开它或者...请根据需要配置脚本。

MAPS_DIR 可通过位置参数或环境变量进行配置

脚本保留其硬编码默认值，但允许覆盖：

- 优先级：1) 第一个位置参数 ($1)，2) 现有 MAPS_DIR 环境变量，
3) 硬编码默认“$SL5NET_AURA_PROJECT_ROOT/config/maps”。
- 提高了 CI、本地覆盖和测试的灵活性，无需编辑脚本。
- 添加引用和目录存在检查，以便在路径无效时提前失败。

用法示例：
- ./search_rules.sh 使用默认值
- ./search_rules.sh ./docs 使用提供的路径
- MAPS_DIR=/env/maps ./search_rules.sh

这在使配置显式化的同时保留了向后兼容性。

还有一个适用于 Windows PC 的版本（在此文件夹中）可以做一些更少的事情：search_rules.ps1


(s, 28.3.'26 23:07 星期六)
## 创建新的插件模块 ( docs/CreatingNewPluginModules.md )

我们的框架使用强大的自动发现系统来加载规则模块。这使得添加新命令集变得简单而干净，无需手动注册每个新组件。本指南解释了如何创建、构建和管理您自己的自定义模块。

### 核心概念：基于文件夹的模块

模块只是 `config/maps/` 目录中的一个文件夹。系统自动扫描该目录并将每个子文件夹视为可加载模块。

### 创建模块的分步指南

按照以下步骤创建新模块，例如，保存特定游戏的宏。

**1.导航至地图目录**
所有规则模块都位于项目的“config/maps/”文件夹中。

**2.创建您的模块文件夹**
创建一个新文件夹。名称应该具有描述性，并使用下划线而不是空格（例如“my_game_macros”、“custom_home_automation”）。

**3.添加语言子文件夹（关键步骤）**
在新模块文件夹中，您必须为要支持的每种语言创建子文件夹。

* **命名约定：** 这些子文件夹的名称 **必须是有效的语言区域代码**。系统使用这些名称来加载活动语言的正确规则。
* **正确示例：** `de-DE`、`en-US`、`en-GB`、`pt-BR`
* **警告：** 如果您使用“german”或“english_rules”等非标准名称，系统将忽略该文件夹或将其视为单独的、非特定于语言的模块。

**4.添加您的规则文件**
将您的规则文件（例如“FUZZY_MAP_pre.py”）放入适当的语言子文件夹中。最简单的开始方法是复制现有语言模块文件夹的内容以用作模板。

### 目录结构示例

__代码_块_0__

### 管理配置中的模块

该系统被设计为需要最少的配置。

#### 启用模块（默认）

模块**默认启用**。只要`config/maps/`中存在模块文件夹，系统就会找到它并加载其规则。 **您无需向设置文件添加条目即可启用新模块。**

#### 禁用模块

要禁用模块，您必须在设置文件的“PLUGINS_ENABLED”字典中为其添加一个条目，并将其值设置为“False”。

（可选）对于 True/False，您也可以使用 1/0。然而，这种情况并不常见，并且会降低可读性。

**示例（`config/settings.py`）：**
__代码_块_1__
### 重要的设计说明

* **默认行为：没有条目等于“True”**
如果模块未在“PLUGINS_ENABLED”字典中列出，则默认情况下将其视为**活动**。这种设计使配置文件保持干净，因为您只需要列出例外情况。

* **启用的简写**
您的配置系统还知道列出没有值的模块密钥意味着它已启用。例如，将 `"wannweil"` 添加到字典中与添加 `"wannweil": True` 相同。这为启用模块提供了方便的简写。
X空格符X
（可选）对于 True/False，您也可以使用 1/0。然而，这种情况并不常见，并且会降低可读性。

* **禁用父模块：** 预期的行为是禁用父模块应该   
自动禁用其所有子模块和语言子文件夹。例如，设置 `"standard_actions": False` 应阻止加载 `de-DE` 和 `en-US`。 (25 年 10 月 27 日星期一)
X空格符X
*   **目标**
目标是进一步增强该系统。例如，提供一种即使父模块被禁用也能尊重子模块设置的方法，或者引入更复杂的继承规则。 (25 年 10 月 27 日星期一)


X空格符X
X空格符X
X空格符X
t1- Es ist in der Tat wesentzerfreundlicher und komfortabler, die Steuerung über die Sprachbefehle direct in diesem Dokumentationsabschnitt hervorzuheben [1]。

t2- Wir erweitern den Entwurf um eine klare Beschreibung der Tastenbzw。 Sprachsteuerungsbefehle（即“Aura，Lernmodus einschalten / ausschalten”）和erklären kurz，即“toggle_learning.py”das Aus- und Einkommentieren automatisiert [2]。


### 启用学习模式（无与伦比的训练）

为了让您的自定义模块在“Lernmodus”（学习模式）处于活动状态时自动学习无法识别的短语，您可以在“FUZZY_MAP_pre”列表的**最底部**附加一个包罗万象的规则。

当文件中没有其他特定规则匹配时，此规则将调用不匹配的训练插件：

__代码_块_2__

训练插件使用“f'{str(__file__)}'”来定位您的文件，并自动将无法识别的短语附加到第一个可用的规则组（例如您的主命令组）。

#### 通过语音命令切换学习模式

管理此功能的最舒适方法是通过内置语音命令，而不是手动编辑文件：

* **启用：** 说 *“Aura，学习模式开启”* 或 *“Aura，Lernmodus starten”*。
* **要禁用：** 说 *“Aura，学习模式关闭”* 或 *“Aura，Lernmodus stoppen”*。

这些命令在幕后触发“toggle_learning.py”，它会自动注释或取消注释活动地图文件中的所有行。
X空格符X
X空格符X
X空格符X
X空格符X
*提示：定义正则表达式模式后，运行“python3 tools/map_tagger.py”以自动生成 CLI 工具的可搜索示例。有关详细信息，请参阅 [Map Maintenance Tools](../../Developer_Guide/Map_Maintenance_Tools-zh-CNlang.md)。*
# SL5 Aura 入门

> **先决条件：** 您已完成设置脚本并配置热键。
> 如果没有，请参阅 [Installation section in README.md](../../README.i18n/README-zh-CNlang.md#installation)。

---

## 第 1 步：你的第一次听写

1. 启动 Aura（如果尚未运行）：
__代码_块_0__
等待启动声音 — 这意味着 Aura 已准备就绪。



4. 观察文本出现。

> **什么也没发生？** 检查 `log/aura_engine.log` 是否有错误。
> CachyOS/Arch 的常见修复：`sudo pacman -S mimalloc`

---

## 第 2 步：写下你的第一条规则

添加个人规则的最快方法：

1. 打开 `config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py`
2. 在 `FUZZY_MAP_pre = [...]` 中添加一条规则：
__代码_块_1__
3. **保存** — Aura 自动重新加载。无需重新启动。
4. 口述“hello world”并看着它变成“Hello World”。

> 请参阅“docs/FuzzyMapRuleGuide.md”以获取完整的规则参考。

### Oma-Modus（初学者快捷方式）

还不知道正则表达式？没问题。

1. 在沙箱中打开任何空的`FUZZY_MAP_pre.py`
2. 在自己的行上只写一个简单的单词（没有引号，没有元组）：
__代码_块_2__
3. 保存 — Auto-Fix 系统检测到裸字并自动
将其转换为有效的规则条目。
4. 然后您可以手动编辑替换文本。

这被称为 **Oma-Modus** — 专为那些想要在没有任何信息的情况下获得结果的用户而设计。
首先学习正则表达式。

---

## 第三步：与公案一起学习

公案是一些小练习，每个练习都教授一个概念。
它们位于 `configmaps/koans deutsch/` 和 `configmaps/koans english/` 中。

从这里开始：

|文件夹|你学到了什么 |
|---|---|
| `00_koan_oma-modus` |自动修复，无需正则表达式的第一条规则 |
| `01_koan_erste_schritte` |您的第一条规则，管道基础知识 |
| `02_koan_listen` |使用列表 |
| `03_koan_schwierige_namen` |难以识别的名字的模糊匹配 |
| `04_koan_kleine_helfer` |有用的快捷键|

每个 koan 文件夹都包含一个带有注释示例的“FUZZY_MAP_pre.py”。
取消注释规则、保存、口述触发短语 — 完成。

---

## 步骤 4：更进一步

|什么 |哪里 |
|---|---|
|完整规则参考| `docs/FuzzyMapRuleGuide.md` |
|创建您自己的插件 | `docs/CreatingNewPluginModules.md` |
|从规则运行 Python 脚本 | `docs/advanced-scripting.md` |
| DEV_MODE + 日志过滤器设置 | `docs/Developer_Guide/dev_mode_setup.md` |
|上下文感知规则（`only_in_windows`）| `docs/FuzzyMapRuleGuide.md` |
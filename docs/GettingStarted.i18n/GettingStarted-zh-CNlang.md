# SL5 Aura 入门

## SL5 Aura 是什么？

SL5 Aura 是一款离线优先的语音助手，可将语音转换为文本 (STT) 并应用可配置的规则来清理、纠正和转换输出。

它无需 GUI 即可工作 – 一切都通过 CLI 或控制台运行。

## 它是如何工作的

__代码_块_0__

1. **Vosk** 将您的语音转换为原始文本
2. **预映射** 在拼写检查之前清理并更正文本
3. **LanguageTool** 修复语法和拼写
4. **Post-Maps** 应用最终转换
5. **输出**是最终的干净文本（以及可选的 TTS）

## 你的第一步

### 1.启动光环
__代码_块_1__

### 2. 使用控制台输入进行测试
输入“s”，然后输入您的文本：
__代码_块_2__

### 3. 查看正在运行的规则
打开 `config/maps/koans_deutsch/01_koan_erste_schritte/de-DE/FUZZY_MAP_pre.py`

取消里面规则的注释并再次测试。会发生什么？

## 理解规则

规则位于名为“FUZZY_MAP_pre.py”或“FUZZY_MAP.py”的 Python 文件中的“config/maps/”中。

规则如下所示：
__代码_块_3__

**输出**首先出现 - 您立即看到规则产生的内容。

规则是**从上到下**处理的。第一个完全匹配 (`^...$`) 停止了一切。

## 公案 – 边做边学

Koans 是 `config/maps/koans_deutsch/` 和 `config/maps/koans_english/` 中的小练习。

每个公案都教导一个概念：

|公案|主题 |
|---|---|
| 01_koan_erste_schritte | 01_koan_erste_schritte第一条规则，完全匹配，管道停止 |
| 02_koan_听 |列表，多个规则|
| 03_koan_schwierige_namen | 03_koan_schwierige_namen难名字、拼音|

从 Koan 01 开始，逐步升级。

＃＃ 尖端

- `FUZZY_MAP_pre.py` 中的规则在拼写检查之前运行 – 有助于修复 STT 错误
- `FUZZY_MAP.py` 中的规则在拼写检查之后运行 – 有利于格式化
- 任何更改之前都会自动创建备份文件（`.peter_backup`）
- 使用“peter.py”让人工智能自动完成公案
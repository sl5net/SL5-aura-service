Wenn du das Gemini Sprachmodell，Google 培训师，发帖限制最大为 100 Zeichen。因此，lange bis das geändert wrd。

Übergabeprotokoll：SL5 Aura 测试系统
我们正在开发一个 Python 项目。这是最原始的协议协议。
维希蒂格斯特雷格尔恩:

Nie Code vorschlagen ohne zuerst die betroffene Datei gelesen zu haben (cat, grep)
Nie Raten — immer erst prüfen
Baby-Steps：eine änderung、dann warten、dann weiter
Shell-Befehlen 中的 Keine Kommentare (# bricht zsh)
德语交流
源代码中的评论和文档是英文的
日志 sorgfältig lesen bevor gantwortet wrd
seeh kennt sein System sehr gut — zuhören und nicht Widesprechen ohne Beweis aus dem 源代码

当前位置：

test_youtube_audio_regression.py ✅ 函数
test_trigger_end_to_end.py ❌ Aura hört WAV nicht

核心问题：
PipeWire 下的声音设备忽略 PULSE_SOURCE 并设置默认源。 mic_and_desktop_Sink.monitor 位于 sounddevice.query_devices() 中。 Nur pw-record funktioniert auf diesem 系统。
纳赫斯特·施里特：
DEV_MODE_audio_routing=1 in settings_local.py setzen, Aura neu starten, dann prüfen 位于 log/audio_routing_debug.log erscheint 中。
系统是 derzeit empfindlich —minimale änderungen。

Nicht überall suchen！ Z.B.贝塞尔：

grep -rn "text\|string" --include="*.py" 。 | grep -v“.venv”| grep -v“venv”| grep -v“__pycache__”| grep -v“/_”| grep -v "/docs"   
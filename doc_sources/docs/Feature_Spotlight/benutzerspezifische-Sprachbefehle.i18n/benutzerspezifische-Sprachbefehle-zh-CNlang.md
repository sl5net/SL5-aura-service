# Benutzerspezifische Sprachbefehle

Aura erlaubt es dir，eigene Befehle zu definieren，die **nur für dich** (oder bestimmte Teammitglieder) aktiv sind。死后，私人 Kürzel 或 Test-Befehle bei anderen Benutzern ausgelöst werden。



Die Anpassung erfolgt direkt in einer Regel-Datei (z.B. `FUZZY_MAP_pre.py` bzw. `FUZZY_MAP.py` Regeln die erst nach der Sprach-Korrektur ausgeführt werden)：

### 代码-Beispiel

Füge am Ende der Datei folgenden Block hinzu：

__代码_块_0__
从scripts.py.func.define_current_user导入define_current_user

# 1. bin 是吗？
当前用户, _ = 确定当前用户()

如果当前用户在 ['misterx'] 中：
我的用户规则 = [
# 格式：（Antwort/Aktion、Regex-Muster、Min-Genauigkeit、Optionen）
(f"你好{当前用户}"，r'^(hello|hi)$')
]
FUZZY_MAP_pre.extend(MY_USER_RULES)

__代码_块_1__
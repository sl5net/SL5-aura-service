# 💡 功能聚焦：插件的持久缓存

## 💾 性能和稳定性的缓存维护

该系统具有中心性、持久性缓存机制（`simple_plugin_cache`）、外部 API-Aufrufe（例如 Wetter、Übersetzungen 等）等。 Der Cache ist **持久**，d.h.请重新启动 Haupt-Services 服务。

**Ziel：** Reduzierung der Netzwerklast 和 Failover auf die letzte bekannte Antwort bei einem API-Ausfall。

---

### 1. 缓存活动（Der Standardfall）

在缓存中的功能，请使用“get_cached_result”和“set_cached_result”导入功能。

#### 1.1 导入和配置

Fügen Sie diese Zeilen zu Ihrem Plugin-Skript hinzu (z.B. `weather.py`):

__代码_块_0__

#### 1.2 在“执行”块中缓存逻辑

请参阅以下代码：**Prüfen**、**Ausführen** 和 **Speichern**。

__代码_块_1__

---

### 2. Spezielle Caching-Fälle

#### A. Permanentes 缓存（Ewiger Cache）

Wenn ein Ergebnis niemals ablaufen soll（z.B. eine API-URL，die sich nicht ändert），lassen Sie den `ttl_seconds` 参数 einfach weg。

__代码_块_2__

#### B. Wichtige Hinweise zum `key_args`

`key_args` 参数必须是 **Tupel** sein 和 alle Werte enthalten，die das Ergebnis der Funktion beeinflussen (z.B. `('Berlin', 'de')`)。

**Der Mechanismus wandelt automatisch `pathlib.Path`-Objekte in Strings um, bevor der Cache-Schlüssel Generiert wird, um Probleme zu vermeiden.**
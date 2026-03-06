# 💡 Omówienie funkcji: trwałe buforowanie wtyczek

## 💾 Cache-Nutzung zur Steigerung der Performance und Ausfallsicherheit

System ten jest zintegrowany, trwały mechanizm pamięci podręcznej (`simple_plugin_cache`), zewnętrzny interfejs API (np. Wetter, Übersetzungen itp.) beschleunigt i reduziert. Der Cache jest **trwały**, d.h. er bleibt auch nach einem Neustart des Haupt-Services erhalten.

**Ziel:** Reduzierung der Netzwerklast and Failover auf letzte bekannte Antwort bei API-Ausfall.

---

### 1. Aktywacja buforowania (Der Standardfall)

Możesz użyć funkcji `get_cached_result` i `set_cached_result` importowania.

#### 1.1 Import i konfiguracja

Fügen Sie diese Zeilen zu Ihrem Plugin-Skript hinzu (z.B. `weather.py`):

__KOD_BLOKU_0__

#### 1.2 Buforowanie-Logik w `execute`-Block

Sie müssen den Code in drei Blöcke unterteilen: **Prüfen**, **Ausführen** i **Speichern**.

__KOD_BLOKU_1__

---

### 2. Spezielle Caching-Fälle

#### A. Trwałe buforowanie (pamięć podręczna Ewigera)

Wenn ein Ergebnis niemals ablaufen soll (z.B. eine API-URL, die sich nicht ändert), lassen Sie den `ttl_sekundy` Parametr einfach weg.

__KOD_BLOKU_2__

#### B. Wichtige Hinweise zum `key_args`

Der `key_args` Parametr muss ein **Tupel** sein und alle Werte enthalten, die das Ergebnis der Funktion beeinflussen (z.B. `('Berlin', 'de')`).

**Der Mechanismus wandelt automatisch `pathlib.Path`-Objekte in Strings um, bevor der Cache-Schlüssel generiert wird, um Probleme zu vermeiden.**
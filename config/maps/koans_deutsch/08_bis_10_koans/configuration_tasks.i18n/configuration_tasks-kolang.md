구성-Koans

### 1. Koan 08: Die Schalter-Zentrale(플러그인 활동)
**기본 정보:** 자세히 알아보려면 'settings.py'에서 새로운 기능(플러그인)을 찾아보세요.

* **Aufgabe:** "Aktiviere das Wikipedia-Plugin, indem du den Wert von `False` auf `True` änderst."
* **Nutzen:** Verstehen, dass Aura 모듈러 ist.

### 2. Koan 09: Dein digitales Namensschild(변수)
**Lerneffekt:** Eigene Daten in der Konfiguration Hinterlegen, die von Plugins genutzt werden.
* **Aufgabe:** "'USER_NAME' 변수에 Trage deinen eigenen Namen이 있습니다."
* **Nutzen:** 플러그인 können dann Sätze schreiben wie "Mit freundlichen Grüßen, [Dein Name]".

```py
from config import settings
user_name = getattr(settings, "USER_NAME", "[Name fehlt]")
```

### 3. 고안 10: 게둘드 비트! (파우젠-자이텐)
**Lerneffekt:** Die Spracherkennung an das eigene Sprechtempo anpassen.
* **Aufgabe:** "Erhöhe den `SPEECH_PAUSE_TIMEOUT`, damit Aura länger wartet, bevor sie deinen Satz verarbeitet."
* **Nutzen:** Besonders wenn sie in Ruhe nachdenken.
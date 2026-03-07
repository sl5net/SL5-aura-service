Configurações-Koans

### 1. Koan 08: Die Schalter-Zentrale (plugins ativados)
**Efeitos importantes:** Aprenda mais sobre como usar as novas funções (plugins) do `settings.py`.

* **Aufgabe:** "Ative o plug-in da Wikipedia, indem o valor de `False` em `True` änderst."
* **Nutzen:** Verstehen, dass Aura modular ist.

### 2. Koan 09: Dein digitales Namensschild (Variáveis)
**Lerneffekt:** Eigene Daten in der Konfiguration hinterlegen, die von Plugins genutzt werden.
* **Aufgabe:** "Trage deinen eigenen Namen in the Variable `USER_NAME` ein."
* **Nutzen:** Plugins podem ser listados como "Mit freundlichen Grüßen, [Dein Name]".

```py
from config import settings
user_name = getattr(settings, "USER_NAME", "[Name fehlt]")
```

### 3. Koan 10: Geduld bitte! (Pausen-Zeiten)
**Lerneffekt:** Die Spracherkennung an das eigene Sprechtempo anpassen.
* **Aufgabe:** "Erhöhe den `SPEECH_PAUSE_TIMEOUT`, damit Aura länger wartet, bevor sie deinen Satz verarbeitet."
* **Nutzen:** Besonders wenn sie in Ruhe nachdenken.
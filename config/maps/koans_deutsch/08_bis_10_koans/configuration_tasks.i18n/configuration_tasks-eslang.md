Configuraciones-Koans

### 1. Koan 08: Die Schalter-Zentrale (Activación de complementos)
**Lerneffekt:** Teilnehmer lernen, wie sie in der `settings.py` nuevas funciones (complementos) gratuitas.

* **Aufgabe:** "Activa el complemento de Wikipedia, indem du den Wert von `False` auf `True` änderst".
* **Nutzen:** Verstehen, dass Aura modular ist.

### 2. Koan 09: Dein digitales Namensschild (Variable)
**Lerneffekt:** Eigene Daten in der Konfiguration Hinterlegen, die von Plugins genutzt werden.
* **Aufgabe:** "Trage deinen eigenen Namen in the Variable `USER_NAME` ein."
* **Números:** Los complementos pueden seleccionarse como "Mit freundlichen Grüßen, [Dein Name]".

```py
from config import settings
user_name = getattr(settings, "USER_NAME", "[Name fehlt]")
```

### 3. Koan 10: ¡Geduld bitte! (Pausen-Zeiten)
**Lerneffekt:** Die Spracherkennung an das eigene Sprechtempo anpassen.
* **Aufgabe:** "Erhöhe den `SPEECH_PAUSE_TIMEOUT`, damit Aura langer wartet, bevor sie deinen Satz verarbeitet."
* **Nutzen:** Besonders wenn sie in Ruhe nachdenken.
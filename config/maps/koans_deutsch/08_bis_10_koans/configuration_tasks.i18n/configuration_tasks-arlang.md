تكوينات Koans

### 1. الجزء 08: Die Schalter-Zentrale (المكونات الإضافية النشطة)
**تأثير التعلم:** يمكنك التعلم من خلال `settings.py` الوظائف الجديدة (المكونات الإضافية).

* **Aufgabe:** "قم بتفعيل ملحق ويكيبيديا الإضافي، مما يعني أنك تعلمت أن `False` على `True` änderst."
                             * **Nutzen:** Verstehen، dass Aura modular ist.

              ### 2. القرآن 09: Dein digitales Namensschild (Variablen)
**التعلم:** البيانات الذاتية في التكوين الخلفي هي التي يتم تطويرها بواسطة المكونات الإضافية.
* **Aufgabe:** "قم بمسح الأسماء الذاتية في المتغير `USER_NAME`."
* **Nutzen:** يمكن كتابة المكونات الإضافية مثل "Mit freundlichen Grüßen, [Dein Name]".

```py
from config import settings
user_name = getattr(settings, "USER_NAME", "[Name fehlt]")
```

            ### 3.الجزء 10: جيدولد بايت! (باوسن زيتن)
        **تعلم:** Die Spracherkennung an das eigene Sprechtempo anpassen.
* **Aufgabe:** "Erhöhe den `SPEECH_PAUSE_TIMEOUT`، مع استمرار الهالة لفترة أطول، قبل أن تظل ثابتًا."
                         * **Nutzen:** Besonders wenn sie in Ruhe nachdenken.
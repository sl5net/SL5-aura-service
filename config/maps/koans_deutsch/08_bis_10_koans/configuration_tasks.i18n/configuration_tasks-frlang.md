Configurations-Koans

### 1. Koan 08 : Die Schalter-Zentrale (Plugins activés)
**Effets d'apprentissage :** Apprenez-en davantage, comme dans les nouvelles fonctions (plugins) gratuites de `settings.py`.

* **Aufgabe:** "Activer le plugin Wikipédia, indépendamment de la valeur de `False` auf `True`."
* **Nutzen :** Verstehen, l'artiste modulaire Aura.

### 2. Koan 09 : Dein digitales Namensschild (Variablen)
**Lerneffekt :** Les données propres dans l'arrière-plan de la configuration sont générées par les plugins.
* **Aufgabe:** "Trage votre propre nom dans la variable `USER_NAME` dans un."
* **Nutzen:** Les plugins peuvent être consultés comme "Mit freundlichen Grüßen, [Dein Name]".

```py
from config import settings
user_name = getattr(settings, "USER_NAME", "[Name fehlt]")
```

### 3. Koan 10 : Geduld mord ! (Pause-Zeiten)
**Lerneffekt :** Die Spracherkennung an das eigene Sprechtempo anpassen.
* **Aufgabe:** "Vous pouvez utiliser `SPEECH_PAUSE_TIMEOUT`, mais Aura est plus longue, avant que votre satz soit planifié."
* **Nutzen :** Besonders wenn sie in Ruhe nachdenken.
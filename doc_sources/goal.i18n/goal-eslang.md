## Objetivo: el modelo de "sesión de dictado"

### Unser Ziel (alemán): Die "Diktier-Sitzung"

Un disparador inicia un **"Diktier-Sitzung"**, las tres fases son las siguientes:

1. **Fase inicial (Warten auf Sprache):**
* Después del disparo del sistema.
* Cuando **no** se activa la tecla Spracheingabe, finalice la sesión asignada después de `PRE_RECORDING_TIMEOUT` (por ejemplo, 12 s).

2. **Fase activa (Continuierliches Diktieren):**
* Sobald die erste Spracheingabe erkannt wird, wechselt die Sitzung in den aktiven Modus.
* Immer wenn VOSK eine Sprechpause erkennt y un Textblock liefert (por ejemplo, un Satz), wird este Block **sofort** zur Verarbeitung (LanguageTool, etc.) weitergegeben y als Text ausgegeben.
* Die Aufnahme läuft währenddessen **nahtlos weiter**. Die Sitzung wartet auf den nächsten Satz.

3. **Fase final (Ende der Sitzung):**
* Die gesamte Sitzung endet nur, wenn eine dieser beiden Bedingungen erfüllt ist:
* Der Nutzer bleibt für die Dauer des `SPEECH_PAUSE_TIMEOUT` (z.B. 1-2s) completo todavía.
* Der Nutzer detuvo la posición manual según Trigger.

**Zusammengefasst:** Eine Sitzung, viele sofortige Textausgaben. Die Sitzung bleibt aktiv, bis der Nutzer eine langere Pause macht oder sie manually beendet.


### **Objetivo: el modelo de "sesión de dictado"**

Un único activador inicia una **"Sesión de dictado"**, que consta de tres fases:
1. **Fase de inicio (esperando discurso):**
* Después del disparo, el sistema comienza a escuchar.
* Si **no se detecta voz**, toda la sesión finaliza después del `PRE_RECORDING_TIMEOUT` (por ejemplo, 12 segundos).
2. **Fase Activa (Dictado Continuo):**
* Tan pronto como se detecta la primera entrada de voz, la sesión cambia al modo activo.
* Cada vez que VOSK detecta una pausa y entrega un fragmento de texto (por ejemplo, una oración), este fragmento se pasa **inmediatamente** al proceso de procesamiento (LanguageTool, etc.) y se genera como texto.
* La grabación continúa **sin interrupciones** en segundo plano, esperando la siguiente declaración.
3. **Fase de Terminación (Finalización de la Sesión):**
* Toda la sesión termina solo cuando se cumple una de dos condiciones:
* El usuario permanece completamente en silencio durante el `SPEECH_PAUSE_TIMEOUT` (por ejemplo, 1-2 segundos).
* El usuario detiene manualmente la sesión mediante el disparador.
**En resumen:** Una sesión, múltiples salidas de texto inmediatas. La sesión permanece activa hasta que el usuario hace una pausa larga o la finaliza manualmente.
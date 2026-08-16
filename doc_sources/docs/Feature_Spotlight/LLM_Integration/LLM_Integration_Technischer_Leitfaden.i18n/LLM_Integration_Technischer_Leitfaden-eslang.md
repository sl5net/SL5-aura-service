# 🧠 SL5 Aura: integración completa de LLM sin conexión

**Estado:** Produktionsbereit
**Motor:** Ollama (Llama 3.2 3B)
**Latencia:** Sofort (<0,1 s en caché) / ~20 s (generación de CPU)

## 1. La filosofía "Architekt & Praktikant"
Aura nutzt ein Hybrid-Modell, um **Präzision** und **Flexibilität** zu vereinen:
* **Der Architekt (RegEx/Python):** Deterministicsche, sofortige Ausführung für Systembefehle ("Browser öffnen", "Lauter").
* **Der Praktikant (Lokales LLM):** Übernimmt unscharfe Anfragen, Zusammenfassungen und Allgemeinwissen. Wird nur aktiv, wenn keine strikte Regel greift.

---

## 2. Performance-Architektur

Para tener un LLM local sobre CPU normales (sin GPU) para machen, establezcamos una **estrategia de 3 estrategias**:

### Estudio 1: Der "Instant Modus" (Schlagworte)
* **Activador:** Palabras como "Instant", "Schnell", "Sofort".
* **Lógica:** Umgeht das LLM komplett. Vergleicht Schlagworte der Eingabe direkt mit der SQLite-Datenbank.
* **Latencia:** **< 0,05 s**

### Paso 2: La caché inteligente (SQLite)
* **Lógica:** Cuando se indica el mensaje (SHA256). Si desea anfragar un Ollama, se guardará `llm_cache.db`.
* **Característica "Variación activa":** Además, hay una actualización de caché generada por el sistema manchmal (20 % de probabilidad) proactiva una *nueva* variante de respuesta. Ziel: ~5 Variantes pro Frage für mehr Lebendigkeit.
* **Función "Semantic Hashing":** Bei langen Fragen (>50 Zeichen) extrahiert das LLM zuerst Keywords (por ejemplo, "installation anleitung") y hasht diese. Entonces werden "¿Wie installiere ich es?" y "Installationshilfe bitte" también son idénticos.
* **Latencia:** **~0,1 s**

### Estudio 3: La generación de API (alternativa)
* **Lógica:** Si no existe caché, usaremos la API de Ollama (`http://localhost:11434/api/generate`).
* **Optimización:**
* **Límites estrictos:** `num_predict=60` zwingt das Modell, nach ca. 40 Wörtern zu stoppen.
* **Tubería de entrada:** Große Texte (README) werden über STDIN übergeben, um Argumenten-Limits des Betriebssystems zu umgehen.
* **Latencia:** **~15-25s** (abhängig von CPU)

---

## 3. Conexión a tierra del sistema (antialucinaciones)

Los LLM genéricos incluyen GUI (botones, menús). Wir injizieren bei jedem Aufruf das strikte **`AURA_TECH_PROFILE`**:

1. **No tiene GUI:** Aura es un dispositivo CLI sin cabeza.
2. **No hay archivos de configuración:** La lógica no es código Python, no `.json`/`.xml`.
3. **Activador:** Control externo activado por Dateisystem-Events (`touch /tmp/sl5_record.trigger`), no sobre API.
4. **Instalación:** Dauert real 10-20 Min wegen 4GB Modelldownloads (verhindert falsche Versprechen).

---

## 4. El puente del portapapeles (seguridad de Linux)

Los fondos interiores (systemd) no pueden utilizarse en zonas de seguridad a menudo en el interior (X11/Wayland).
* **Lesung:** Un escrito en la sesión de usuario (`clipboard_bridge.sh`) escribe el contenido en una fecha de disco RAM (`/tmp/aura_clipboard.txt`).
* **Aura:** Liest diese Datei und umgeht so alle Rechte-Probleme.

---

## 5. Selbst-Lernen (Calentamiento de caché)

Trabajamos con el script `warm_up_cache.py`:
1. Es liest die `README.md` des Projekts.
2. Es beauftragt das LLM, sich wahrscheinliche User-Fragen auszudenken.
3. Es estellt estas Fragen an Aura, um die Datenbank zu befüllen automatisch.
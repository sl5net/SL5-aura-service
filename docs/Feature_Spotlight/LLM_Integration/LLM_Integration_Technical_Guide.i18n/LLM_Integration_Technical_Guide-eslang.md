# 🧠 SL5 Aura: integración avanzada de LLM sin conexión

**Estado:** Listo para producción
**Motor:** Ollama (Llama 3.2 3B)
**Latencia:** Instantánea (<0,1 s en caché) / ~20 s (generación en CPU)

## 1. La Filosofía del "Arquitecto y Pasante"
Aura opera en un modelo híbrido para equilibrar la **precisión** y la **flexibilidad**:
* **The Architect (RegEx/Python):** Ejecución instantánea y determinista de comandos del sistema (por ejemplo, "Abrir navegador", "Subir volumen").
* **El pasante (LLM local):** Maneja consultas confusas, resúmenes y conocimientos generales. Solo se activa si no hay coincidencias de reglas estrictas ni se utilizan palabras clave específicas.

---

## 2. Arquitectura de rendimiento

Para que un LLM local se pueda utilizar en CPU estándar sin aceleración de GPU, implementamos una **Estrategia de rendimiento de 3 capas**:

### Capa 1: El "modo instantáneo" (palabras clave)
* **Desencadenante:** Palabras como "Instant", "Schnell", "Sofort".
* **Lógica:** Omite el LLM por completo. Compara las palabras clave ingresadas por el usuario con la base de datos SQLite local mediante la intersección establecida.
* **Latencia:** **< 0,05 s**

### Capa 2: La caché inteligente (SQLite)
* **Lógica:** Cada mensaje tiene un hash (SHA256). Antes de preguntarle a Ollama, revisamos `llm_cache.db`.
* **Función "Variación activa":** Incluso si existe un acierto en caché, el sistema a veces (20% de probabilidad) genera una *nueva* variante para aprender diferentes frases para la misma pregunta. Idealmente, almacenamos ~5 variantes por pregunta.
* **Función "Hashing semántico":** Para preguntas largas (>50 caracteres), utilizamos el LLM para extraer palabras clave primero (por ejemplo, "guía de instalación") y aplicar hash a ellas en lugar de la oración completa. Esto coincide con "¿Cómo lo instalo?" con "Instrucciones de instalación por favor".
* **Latencia:** **~0,1 s**

### Capa 3: La generación de API (alternativa)
* **Lógica:** Si no existe ningún caché, llamamos a la API de Ollama (`http://localhost:11434/api/generate`).
* **Optimización:**
* **Límites estrictos:** `num_predict=60` obliga al modelo a detenerse después de ~40 palabras.
* **Tubería de entrada:** Los textos grandes (README) se pasan a través de STDIN para evitar los límites de argumentos del sistema operativo.
* **Latencia:** **~15-25s** (dependiente de la CPU)

---

## 3. Conexión a tierra del sistema (antialucinaciones)

Los LLM genéricos tienden a inventar elementos GUI (botones, menús). Inyectamos un estricto **`AURA_TECH_PROFILE`** en cada mensaje del sistema:

1. **Sin GUI:** Aura es un servicio CLI sin cabeza.
2. **Sin archivos de configuración:** La lógica es código Python, no `.json`/`.xml`.
3. **Disparadores:** El control externo funciona mediante la creación de archivos (`touch /tmp/sl5_record.trigger`), no mediante API.
4. **Instalación:** Tarda entre 10 y 20 minutos debido a las descargas del modelo de 4 GB (evita la mentira "Se instala en 3 segundos").

---

## 4. El puente del portapapeles (seguridad de Linux)

Los servicios en segundo plano (systemd) no pueden acceder al portapapeles de X11/Wayland directamente debido al aislamiento de seguridad.
* **Solución:** Un script de sesión de usuario (`clipboard_bridge.sh`) refleja el contenido del portapapeles en un archivo de disco RAM (`/tmp/aura_clipboard.txt`).
* **Aura:** Lee este archivo, omitiendo todos los problemas de permisos.

---

## 5. Autoaprendizaje (calentamiento de caché)

Proporcionamos un script `warm_up_cache.py`.
1. Lee el proyecto `README.md`.
2. Le pide al LLM que invente posibles preguntas de los usuarios sobre el proyecto.
3. Simula estas preguntas contra Aura para prellenar la base de datos.
# 🧠 Modo híbrido SL5 Aura: integración local de LLM

**Estado:** Experimental / Estable
**Tecnología:** Ollama (Llama 3.2) + Subproceso Python
**Privacidad:** 100% sin conexión

## El concepto: "Arquitecto y pasante"

Tradicionalmente, Aura se basa en reglas deterministas (RegEx): rápidas, precisas y predecibles. Este es el **"Arquitecto"**. Sin embargo, a veces el usuario quiere preguntar algo "confuso" o creativo, como *"Cuéntame un chiste"* o *"Resume este texto"*.

Aquí es donde entra en juego el **Complemento LLM local** (el **"Pasante"**):
1. **Aura (RegEx)** primero verifica todos los comandos estrictos ("Encender luces", "Abrir aplicación").
2. Si no se detecta nada que coincida con **Y**/ **O** con una palabra desencadenante específica (por ejemplo, "Aura ..."), se activa la regla alternativa.
3. El texto se envía a un modelo de IA local (Ollama).
4. La respuesta se desinfecta y se envía mediante TTS o escritura de texto.

---

## 🛠 Requisitos previos

El complemento requiere una instancia en ejecución de [Ollama](https://ollama.com/) que funcione localmente en la máquina.

```bash
# Installation (Arch/Manjaro)
sudo pacman -S ollama
sudo systemctl enable --now ollama

# Download model (Llama 3.2 3B - only ~2GB, very fast)
ollama run llama3.2
```

---

## 📂 Estructura y orden de carga

El complemento se coloca intencionalmente en la carpeta `z_fallback_llm`.
Dado que Aura carga complementos **alfabéticamente**, este nombre garantiza que la regla LLM se cargue **al final**. Sirve como "red de seguridad" para comandos no reconocidos.

**Ruta:** `config/maps/plugins/z_fallback_llm/de-DE/`

### 1. El mapa (`FUZZY_MAP_pre.py`)

Usamos una **puntuación alta (100)** y una palabra desencadenante para obligar a Aura a ceder el control del guión.

```python
import re
from pathlib import Path
CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    # Trigger: "Aura" + any text
    ('ask_ollama', r'^\s*(Aura|Aurora|Laura)\s+(.*)$', 100, {
        'flags': re.IGNORECASE,
        # 'skip_list': ['LanguageTool'], # Optional: Performance boost
        'on_match_exec': [CONFIG_DIR / 'ask_ollama.py']
    }),
]
```

### 2. El controlador (`ask_ollama.py`)

Este script se comunica con la CLI de Ollama.
**Importante:** Contiene una función `clean_text_for_typing`. Los resultados sin procesar de LLM a menudo contienen emojis (😂, 🚀) o caracteres especiales que pueden bloquear herramientas como `xdotool` o sistemas TTS heredados.

```python
# Snippet from ask_ollama.py
def execute(match_data):
    # ... (Regex group extraction) ...
    
    # System prompt for short answers
    system_instruction = "Answer in German. Max 2 sentences. No emojis."
    
    # Subprocess call (blocks briefly, note the timeout!)
    cmd = ["ollama", "run", "llama3.2", full_prompt]
    result = subprocess.run(cmd, capture_output=True, ...)

    # IMPORTANT: Sanitize output for system stability
    return clean_text_for_typing(result.stdout)
```

---

## ⚙️ Opciones de personalización

### Cambiando el gatillo
Modifique la expresión regular en `FUZZY_MAP_pre.py` si no desea utilizar "Aura" como palabra de activación.
* Ejemplo de un verdadero Catch-All (todo lo que Aura no sabe): `r'^(.*)$'` (Precaución: ¡Ajuste la puntuación!)

### Intercambiando el modelo
Puedes cambiar fácilmente el modelo en `ask_ollama.py` (por ejemplo, a `mistral` para una lógica más compleja, aunque requiere más RAM).
```python
cmd = ["ollama", "run", "mistral", full_prompt]
```

### Aviso del sistema (Persona)
Puedes darle personalidad a Aura ajustando `system_instruction`:
> "Eres un asistente sarcástico de una película de ciencia ficción".

---

## ⚠️ Limitaciones conocidas

1. **Latencia:** La primera solicitud después del arranque puede tardar entre 1 y 3 segundos mientras el modelo se carga en la RAM. Las solicitudes posteriores son más rápidas.
2. **Conflictos:** Si la expresión regular es demasiado amplia (`.*`) sin una estructura de carpetas adecuada, podría tragarse los comandos estándar. El orden alfabético (`z_...`) es imprescindible.
3. **Hardware:** Requiere aprox. 2 GB de RAM libres para Llama 3.2.
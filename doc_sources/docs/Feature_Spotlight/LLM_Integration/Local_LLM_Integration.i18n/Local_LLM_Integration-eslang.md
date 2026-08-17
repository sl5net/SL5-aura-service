# 🧠 Modo híbrido SL5 Aura: LLM local e integración del portapapeles

**Estado:** Estable
**Tecnología:** Ollama (Llama 3.2) + Arquitectura File Bridge
**Privacidad:** 100% sin conexión

## El concepto: "Arquitecto y pasante"

Tradicionalmente, Aura se basa en reglas deterministas (RegEx): rápidas y precisas. Este es el **"Arquitecto"**.
El **Complemento LLM local** actúa como **"Pasante"**: maneja solicitudes confusas, resume textos y responde preguntas generales.

## 🛠 Arquitectura: El puente del portapapeles

Debido a restricciones de seguridad en Linux (Wayland/X11), los procesos en segundo plano (como Aura) a menudo no pueden acceder directamente al portapapeles. Resolvimos esto con una **Arquitectura de Puente**:

1. **El proveedor (sesión de usuario):** Un pequeño script de shell (`clipboard_bridge.sh`) se ejecuta en la sesión del usuario. Observa el portapapeles y refleja su contenido en un archivo temporal (`/tmp/aura_clipboard.txt`).
2. **El consumidor (Aura):** El complemento de Python lee este archivo. Dado que el acceso a archivos es universal, se evitan los problemas de permisos.

---

## 🚀 Guía de configuración

### 1. Instalar Ollama
```bash
sudo pacman -S ollama xclip wl-clipboard
sudo systemctl enable --now ollama
ollama run llama3.2
```

### 2. Configurar el script del puente
Crea `~/clipboard_bridge.sh` y hazlo ejecutable:

```bash
#!/bin/bash
# Mirrors clipboard to a file in RAM
FILE="/tmp/aura_clipboard.txt"
while true; do
    if command -v wl-paste &> /dev/null; then
        wl-paste --no-newline > "$FILE" 2>/dev/null
    else
        xclip -selection clipboard -o > "$FILE" 2>/dev/null
    fi
    sleep 1.5
done
```

**Importante:** ¡Agregue este script al inicio automático de su sistema!

### 3. Lógica del complemento (`ask_ollama.py`)

El script se encuentra en `config/maps/plugins/z_fallback_llm/de-DE/`.
* **Activador:** Detecta palabras como "Computadora", "Aura", "Portapapeles", "Resumen".
* **Memoria:** Mantiene un `conversation_history.json` para recordar el contexto (por ejemplo, "¿Qué acabo de preguntar?").
* **Ingeniería rápida:** Prioriza los datos actuales del portapapeles sobre el contexto de la conversación histórica para evitar alucinaciones.

---

## 📝 Ejemplos de uso

1. **Resumir texto:**
* *Acción:* Copie un correo electrónico largo o un texto de sitio web (Ctrl+C).
* *Comando de voz:* "Computadora, resume el texto en el portapapeles".

2. **Traducción/Análisis:**
* *Acción:* Copie un fragmento de código.
* *Comando de voz:* "Computadora, ¿qué hace el código en el portapapeles?"

3. **Chat general:**
* *Comando de voz:* "Computadora, cuéntame un chiste sobre programadores".

4. **Restablecer memoria:**
* *Comando de voz:* "Computadora, olvídate de todo". (Borra el historial JSON).
  
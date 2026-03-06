# 🧠 Modo Híbrido SL5 Aura: Integração LLM Local

**Status:** Experimental/Estável
**Tecnologia:** Ollama (Llama 3.2) + Subprocesso Python
**Privacidade:** 100% off-line

## O Conceito: "Arquiteto e Estagiário"

Tradicionalmente, o Aura depende de regras determinísticas (RegEx) – rápidas, precisas e previsíveis. Este é o **"Arquiteto"**. Porém, às vezes o usuário quer perguntar algo "confuso" ou criativo, como *"Conte-me uma piada"* ou *"Resuma este texto"*.

É aqui que entra o **Plugin LLM Local** (o **"Estagiário"**):
1. **Aura (RegEx)** primeiro verifica todos os comandos estritos ("Acender luzes", "Abrir aplicativo").
2. Se nada corresponder a **AND**/ **OU** uma palavra acionadora específica (por exemplo, "Aura ...") for detectada, a regra de fallback será ativada.
3. O texto é enviado para um modelo de IA local (Ollama).
4. A resposta é higienizada e emitida via TTS ou digitação de texto.

---

## 🛠 Pré-requisitos

O plugin requer uma instância em execução do [Ollama](https://ollama.com/) operando localmente na máquina.

```bash
# Installation (Arch/Manjaro)
sudo pacman -S ollama
sudo systemctl enable --now ollama

# Download model (Llama 3.2 3B - only ~2GB, very fast)
ollama run llama3.2
```

---

## 📂 Estrutura e ordem de carregamento

O plugin é colocado intencionalmente na pasta `z_fallback_llm`.
Como o Aura carrega os plug-ins **em ordem alfabética**, essa nomenclatura garante que a regra LLM seja carregada **por último**. Serve como uma “rede de segurança” para comandos não reconhecidos.

**Caminho:** `config/maps/plugins/z_fallback_llm/de-DE/`

### 1. O mapa (`FUZZY_MAP_pre.py`)

Usamos uma **pontuação alta (100)** e uma palavra-gatilho para forçar Aura a entregar o controle ao script.

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

### 2. O manipulador (`ask_ollama.py`)

Este script se comunica com a CLI do Ollama.
**Importante:** Ele contém uma função `clean_text_for_typing`. As saídas LLM brutas geralmente contêm emojis (😂, 🚀) ou caracteres especiais que podem travar ferramentas como `xdotool` ou sistemas TTS legados.

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

## ⚙️ Opções de personalização

### Alterando o gatilho
Modifique o RegEx em `FUZZY_MAP_pre.py` se não quiser usar "Aura" como palavra de ativação.
* Exemplo de um verdadeiro pega-tudo (tudo que Aura não sabe): `r'^(.*)$'` (Cuidado: ajuste a pontuação!)

### Trocando o modelo
Você pode facilmente trocar o modelo em `ask_ollama.py` (por exemplo, para `mistral` para uma lógica mais complexa, embora exija mais RAM).
__CODE_BLOCO_3__

### Prompt do sistema (persona)
Você pode dar personalidade ao Aura ajustando o `system_instruction`:
> "Você é um assistente sarcástico de um filme de ficção científica."

---

## ⚠️ Limitações conhecidas

1. **Latência:** A primeira solicitação após a inicialização pode levar de 1 a 3 segundos enquanto o modelo é carregado na RAM. As solicitações subsequentes são mais rápidas.
2. **Conflitos:** Se o RegEx for muito amplo (`.*`) sem uma estrutura de pastas adequada, ele poderá engolir comandos padrão. A ordem alfabética (`z_...`) é essencial.
3. **Hardware:** Requer aprox. 2 GB de RAM grátis para Llama 3.2.
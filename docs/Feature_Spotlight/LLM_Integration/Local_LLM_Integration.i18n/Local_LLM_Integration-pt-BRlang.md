# 🧠 Modo híbrido SL5 Aura: LLM local e integração com área de transferência

**Status:** Estável
**Tecnologia:** Ollama (Llama 3.2) + Arquitetura File Bridge
**Privacidade:** 100% off-line

## O Conceito: "Arquiteto e Estagiário"

Tradicionalmente, o Aura depende de regras determinísticas (RegEx) – rápidas e precisas. Este é o **"Arquiteto"**.
O **Plugin LLM Local** atua como o **"Estagiário"**: Ele lida com solicitações difusas, resume textos e responde a perguntas gerais.

## 🛠 Arquitetura: a ponte da área de transferência

Devido a restrições de segurança no Linux (Wayland/X11), processos em segundo plano (como Aura) muitas vezes não conseguem acessar a área de transferência diretamente. Resolvemos isso com uma **Arquitetura Bridge**:

1. **O Provedor (Sessão do Usuário):** Um pequeno script de shell (`clipboard_bridge.sh`) é executado na sessão do usuário. Ele observa a área de transferência e espelha seu conteúdo em um arquivo temporário (`/tmp/aura_clipboard.txt`).
2. **O Consumidor (Aura):** O plugin Python lê este arquivo. Como o acesso aos arquivos é universal, os problemas de permissão são contornados.

---

## 🚀 Guia de configuração

### 1. Instale o Ollama
```bash
sudo pacman -S ollama xclip wl-clipboard
sudo systemctl enable --now ollama
ollama run llama3.2
```

### 2. Configure o script Bridge
Crie `~/clipboard_bridge.sh` e torne-o executável:

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

**Importante:** Adicione este script à inicialização automática do sistema!

### 3. Lógica do plug-in (`ask_ollama.py`)

O script está localizado em `config/maps/plugins/z_fallback_llm/de-DE/`.
* **Acionador:** Detecta palavras como "Computador", "Aura", "Área de Transferência", "Resumo".
* **Memória:** Mantém um `conversation_history.json` para lembrar o contexto (por exemplo, "O que acabei de perguntar?").
* **Prompt Engineering:** Prioriza os dados atuais da área de transferência em relação ao contexto histórico da conversa para evitar alucinações.

---

## 📝 Exemplos de uso

1. **Resuma o texto:**
* *Ação:* Copie um e-mail longo ou texto de site (Ctrl+C).
* *Comando de voz:* "Computador, resuma o texto na área de transferência."

2. **Tradução/Análise:**
* *Ação:* Copie um trecho de código.
* *Comando de voz:* "Computador, o que o código na área de transferência faz?"

3. **Bate-papo Geral:**
* *Comando de voz:* "Computador, conte-me uma piada sobre programadores."

4. **Redefinir memória:**
* *Comando de voz:* "Computador, esqueça tudo." (Limpa o histórico JSON).
  
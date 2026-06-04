# UI de administração do Aura

A UI Admin permite visualizar e alterar as configurações do Aura em seu navegador com custo zero de recursos ociosos. O servidor do painel não é executado na inicialização; ele é iniciado sob demanda somente quando solicitado.

## Como abrir (sob demanda)

Você pode iniciar e abrir o Painel do administrador dinamicamente usando qualquer um dos três métodos a seguir:

### 1. Comando de voz
Basta falar em seu microfone:
* *"administração da aura"

### 2. Terminal / Comando do Console
Se você estiver trabalhando no terminal, execute este comando para acionar o inicializador diretamente:
```bash
s aura administration
```

*⚠️ **Nota da plataforma para usuários de Windows/macOS:** O wrapper de comando curto `s` é configurado principalmente para ambientes Linux. Por favor, leia o documento para isso. Se você estiver executando o Windows ou macOS, o comando `s` pode não funcionar imediatamente. Consulte nossa documentação oficial de configuração da CLI para saber como configurar e implementar o alias de comando `s` para o seu sistema operacional.*


### 3. Atalho na área de trabalho
Para criar um ícone na área de trabalho específico da plataforma, execute este script de configuração uma vez:
```bash
python scripts/py/chat/install_shortcut.py
```
Em seguida, basta clicar duas vezes no ícone **Aura Admin Dashboard** em sua área de trabalho.

---

## Acesso direto ao navegador
Depois que o servidor for iniciado por meio de qualquer um dos métodos sob demanda acima, você poderá acessar a interface diretamente no seu navegador a qualquer momento:

http://localhost:8084

*(Sinta-se à vontade para adicionar este link aos favoritos em seu navegador!)*

---

## O que você pode fazer

- Veja o status da tradução para cada interface (fala, terminal, web).
- Habilite ou desabilite a tradução por interface.
- Escolha o idioma de destino (inglês, francês, espanhol, etc.).

## Interfaces

| Interface | Descrição |
|-----------|-----------------------------------|
| discurso | Entrada de voz (microfone) |
| terminal | Linha de comando (comando `s`) |
| rede | Bate-papo na web Streamlit (porta 8831) |

## Exemplo

Para traduzir apenas usuários da web para o inglês — deixe a fala e o terminal desativados, habilite a web com o idioma `en`.
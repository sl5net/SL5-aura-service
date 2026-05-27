# UI de administração do Aura

A UI Admin permite visualizar e alterar as configurações do Aura em seu navegador.

## Abrir

http://localhost:8084

## O que você pode fazer

- Veja o status da tradução para cada interface (fala, terminal, web)
- Habilitar ou desabilitar tradução por interface
- Escolha o idioma de destino (inglês, francês, espanhol, etc.)

## Interfaces

| Interface | Descrição |
|-----------|-----------------------------------|
| discurso | Entrada de voz (microfone) |
| terminal | Linha de comando (comando `s`) |
| rede | Bate-papo na web Streamlit (porta 8831) |

## Exemplo

Para traduzir apenas usuários da web para o inglês – deixe a fala e o terminal desligados,
habilite a web com o idioma `en`.
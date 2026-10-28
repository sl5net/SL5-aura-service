> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../matrix_threema_relay.md).*

# Element ↔ Threema Beta GUI Relay

Um pequeno daemon que espelha mensagens entre **Element Desktop** (Matrix) e
**Threema Beta** (o cliente Threema para desktop) no Linux/X11 dirigindo ambos
Windows como um usuário faria: atalhos de teclado, a área de transferência e alguns cliques do mouse.

Sem API, sem tokens, sem bibliotecas extras de Python. Apenas ferramentas de linha de comando padrão do X11.

## O que faz

| Direção | O que acontece |
|---|---|
| **Element → Threema** | A última mensagem *que você* escreveu no Element é lida e, se for nova, colada no Threema Beta e enviada. |
| **Threema → Element** | A última mensagem *recebida* do chat aberto do Threema é copiada pelo menu de contexto e, se for nova, colada no Element e enviada. |

Uso típico: ditar ou digitar em uma sala do Element (por exemplo, com o Aura's)
reconhecimento de fala para texto) e fazer com que o texto chegue em um chat do Threema, e ver o
As respostas do Threema aparecem na mesma sala do Element.

Ambas as janelas devem estar abertas, conectadas e mostrando o chat/sala que você deseja retransmitir.

# # Proteção de alça

Um espelho ingénuo de duas vias faria saltar todas as mensagens para trás e para a frente para sempre. O relé
previne isto com uma história de curta duração (`relay_history.py`):

1. Cada texto que o relé adiante é lembrado **antes** é enviado, por 180 segundos.
2. Se um texto aparece do outro lado que está nesta história, é nosso próprio
   echo: é marcado como visto mas ** não** reencaminhado novamente.
3. Um texto que é novo * e * desconhecido é uma mensagem genuína e é transmitido.

Os textos são comparados com o espaço em branco colapsado, por isso as diferenças entre linhas e
copiar/colar não derrotar o guarda. Porque as entradas morrem, você pode enviar o
O mesmo texto (por exemplo, "ok") novamente após a janela ter passado.

Na inicialização a última mensagem atual de cada lado é lida como uma linha de base ** e é
* não * reencaminhado. Apenas mensagens que chegam após o início são transmitidas.

## Requisitos

- Linux com **X11** (`echo $XDG_SESSION_TYPE` deve imprimir `x11`). Wayland não é suportado.
- `xdotool`, `xclip`, `wmctrl` e `xset` (opcional, usado para desativar o protetor de tela)
- Element Desktop (classe WM `element.Element`)
- Threema Beta (classe WM `threema beta.Threema Beta`, por exemplo, o Flatpak
  `ch.threema.threema-desktop`)
- Python 3 com o virtualenv do projeto
- `zsh` para o script de calibração única

# # Configuração: calibração única

Threema Beta desenha seu próprio menu de contexto que não pode ser operado com o teclado,
assim o relé clica em "Copiar Mensagem" com o mouse em posições em relação ao
Janela Threema. Medi-os uma vez:

```zsh
scripts/py/func/threema/threema-relay.zsh calibrate
```

O script pede três posições do mouse, cada uma com uma contagem regressiva (não toque no
Teclado, não mover ou redimensionar a janela:

1. ** Clique com o botão direito** a última mensagem *vindo* (uma bolha no lado esquerdo) e deixe
   O menu está aberto.
2. Mova o mouse, sem clicar, para **"Copy Message"**.
3. Mova o mouse para o campo de entrada **mensagem**.

O resultado é armazenado em `~/.config/threema-relay.conf`:

A chave significa que
|---|---|
O `FX` Posição de clique horizontal como uma fração da largura da janela
□ `BOTTOM` □ Clique na posição, pixels acima da borda inferior da janela
`DX`, `DY` Offset from the click point to "Copy Message"
`INPUT_FX`, `INPUT_BOTTOM`
* `DELAY_MENU`, `DELAY_COPY` * Espera opcional em segundos (por omissão 0,30 / 0,20)

Verifique a calibração com uma nova mensagem recebida como a última na conversa:

```zsh
scripts/py/func/threema/threema-relay.zsh test
```

Ele imprime o texto copiado sem encaminhá-lo. A calibração depende da janela
geometria: se você alterar muito o tamanho da janela do Threema, calibre novamente.

## Uso

Da raiz do repositório:

```zsh
PYTHONPATH=. .venv/bin/python3 scripts/py/func/threema/matrix_threema_relay.py
```

Opções:

| Opção | Efeito |
|---|---|
| `--poll SECONDS` | Intervalo da pesquisa (padrão `2.0`) |
| `--no-threema-to-element` | Elemento apenas de retransmissão → Threema |
| `--no-element-enter` | Cole mensagens do Threema no campo de entrada do Element, mas **não** as envie (modo de teste seguro) |

Pare com `Ctrl+C`.

Primeira execução recomendada: use `--no-element-enter`, envie uma mensagem para si mesmo no Threema
e verifique se ele aparece no campo de entrada do Element. Em seguida, execute sem a opção.

Exemplo de registro:

```
[INFO] Initial Element baseline: 'Test'
[INFO] Initial Threema baseline: 'kaa'
[INFO] New Element message -> Threema: 'Hallo Welt'
[INFO] New Threema message -> Element: 'müsli'
[INFO] Element shows our own relayed text - not sending back.
```

# # Como funciona

```
every poll interval
├─ Element:  focus window (wmctrl) → Up, Ctrl+A, Ctrl+C, Escape (xdotool) → read clipboard (xclip)
│            new + unknown  → paste into Threema + Return, remember text
│            new + known    → echo, ignore
└─ Threema:  focus window → right-click last incoming bubble → click "Copy Message"
                          → click input field (restores focus) → read clipboard
             new + unknown  → paste into Element (+ Return), remember text
             new + known    → echo, ignore
```

- * Subir* no compositor do Element edita a sua última mensagem; * Ctrl+A / Ctrl+C* copia
  ele e *Escape* deixam o modo de edição. É por isso que apenas ** seu próprio** último elemento
  A mensagem é transmitida para Threema.
- Para Threema a ** string sentinel** é colocado na área de transferência primeiro. Se ainda estiver
  depois disso, nada foi copiado (por exemplo, porque a sua própria mensagem é
  Última e o clique não atingiu nenhuma bolha) e a tentativa é ignorada.

## Arquivos

□ Ficheiro
|---|---|
□ `matrix_threema_relay.py` □ Loop principal, CLI, lógica de decisão (`classify_candidate`)
`read_last_element_message.py` Leia a última mensagem do próprio elemento
O `send_to_threema_window.py` cola o texto em Threema Beta
`read_last_threema_message.py` Leia a última mensagem de Threema, calibração de cargas
O `send_to_element_window.py` cola o texto no elemento
`relay_history.py`
□ `threema-relay.zsh` • Calibração e ferramenta de teste manual (`calibrate`, `test`)
`test_threema_relay.py`

Execute os testes com:

```zsh
PYTHONPATH=. .venv/bin/python3 -m unittest scripts.py.func.threema.test_threema_relay
```

# # Limitações

- **O relé usa o foco do mouse e teclado. *** Durante cada enquete os Threema e
  Elemento Windows são focados e o mouse salta brevemente (é restaurado). Não
  digite enquanto uma pesquisa é executada, ou use um `--poll` mais longo.
- Sobrepõe a área de transferência em todas as pesquisas.
- **A última mensagem em Threema:** quando sua própria mensagem é a última no Threema
  Chat, uma resposta que chegou pouco antes de ser vista.
- ** Apenas a última mensagem** é lida por pesquisa. Se várias mensagens chegarem dentro de uma
  intervalo, só o mais novo é retransmitido.
- ** Apenas texto. As imagens, arquivos, reações e edições não são transmitidas.
- ** Um par de chat.** Qualquer bate-papo/quarto aberto em cada janela é usado.
- ** Um rascunho no campo de entrada do Element** será combinado com o próximo colar
  Mensagem.
- ** Apenas X11. Wayland bloqueia entradas sintéticas e mudanças de foco de janela.
- O relé desativa o protetor de tela X11 e o DPMS no início (`xset s off -dpms`);
  Ficam desligados até os reactivares ou voltarem a entrar.

## Solução de Problemas

Sintomas Provável causa / correção
|---|---|
• `Threema window ... not found` • Verifique `xdotool search --class "Threema Beta"` e `xprop WM_CLASS` (clique na janela).
O `Nothing copied` / no Threema → Elemento O `calibrate`; execute o `test` com uma mensagem recebida como a última. Aumentar `DELAY_MENU`/`DELAY_COPY` na configuração em uma máquina lenta.
O texto chega em Threema, mas não é enviado em campo de entrada não focado; verifique `INPUT_FX`/`INPUT_BOTTOM` da calibração.
O texto de Threema aparece no elemento mas não é enviado O relé foi iniciado com `--no-element-enter`.
Números decimais como o `0,9353` na configuração □ Escrito por uma versão de script mais antiga sob uma localidade alemã. O código Python os aceita; Calibrando novamente com o script atual escreve pontos. □

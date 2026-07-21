# Notas: problema de chave travada type_watcher.sh (dotool)

## Sintoma
Logo após a reinicialização do Manjaro, no primeiro ditado após `sl5net Aura`
iniciado automaticamente, um único caractere travou e se repetiu infinitamente
(por exemplo, "n" repetido centenas de vezes) até que a tecla de disparo fosse pressionada
novamente como uma solução alternativa manual.

Observado uma vez em 21/07/2026 ~09:44 (terça), texto: "Die Ideen niemand wird
mais gefragt, aber es soll trotzdem genauso sein wie...nnnnn...".

## Linha do tempo (comprovada por meio de registros)
- 09:29:17 - `type_watcher.sh` iniciado (log/type_watcher.log)
- 09:41:56 - ditado "ideen niemand wird mehr gefragt..." recebido
(log/aura_engine.log, Tópico-13/14)
- 09:42:03 - processamento finalizado do texto (`melhor pontuação difusa: 0%`),
presumivelmente escrito em um arquivo `tts_output_*.txt`
- ~09:42:04-09:42:09 - `type_watcher.sh` travou (inferido: watchdog
o intervalo da pesquisa é de 5s, veja abaixo)
- 09:42:09 - registro de cão de guarda (log/type_watcher_keep_alive.log):
"WATCHDOG: 'type_watcher.sh' não está em execução. Iniciando agora."
- 09:42:13 - `type_watcher.sh` reiniciado (log/type_watcher.log)
- Nenhuma entrada `typed content of ...` para o arquivo "ideen niemand..." foi
já encontrado em log/type_watcher.log - a digitação desse específico
o texto nunca foi concluído/registrado.

## Status da causa raiz
- CONFIRMADO: `type_watcher.sh` travou entre o final do texto
processamento (09:42:03) e o watchdog detectando que não está em execução
(09:42:09). O watchdog (`type_watcher_keep_alive.sh`) só mata
e reinicia em uma mudança de carimbo de data/hora do arquivo de configuração (`ts1`/`ts2`,
confirmado inalterado neste incidente) ou reinicia automaticamente quando
`pgrep -f "type_watcher.sh"` não encontra nenhum processo - ou seja, isso foi muito
provavelmente uma falha automática, não uma morte externa.
- HIPÓTESE (não comprovada): `set -euo pipefail` (type_watcher.sh linha 5)
fez com que o script fosse encerrado em algum código de saída diferente de zero dentro do
pipeline, possivelmente enquanto o pipe `dotool` de `do_type()` (linha 125) foi
meio do caminho. Se o processo bash morrer durante o streaming para `dotool`,
o daemon `dotoold` separado (que continua rodando de forma independente)
pode ser deixado com uma chave em um estado "para baixo" sem nenhuma correspondência "para cima"
recebido, causando repetição de chave no nível do sistema operacional.
- AINDA NÃO PROVADO: o comando/linha exato que causou o valor diferente de zero
saia em `set -euo pipefail`. Nenhum stderr do acidente
O processo `type_watcher.sh` foi capturado (o watchdog o chama
sem qualquer redirecionamento de saída, `type_watcher_keep_alive.sh` linha 79).
- A chave afetada NÃO era sempre o mesmo caractere em diferentes
ocorrências deste bug (relatório do usuário: anteriormente "t" também).

## Já investigado e descartado
- Não é uma reinicialização acionada por alteração de configuração (confirmada pelo usuário: config
inalterado e a verificação `ts1_old != ts1_new` registraria "Configuração alterada").
- Não é uma inicialização automática duplicada de `type_watcher.sh` sobreposta a
em si (apenas uma entrada "Hello from Watcher" precedeu a falha).
- A chamada `dotool type` de `do_type()` é atômica por invocação e não
não envia a chave por caractere para baixo/para cima - descartando `type_watcher.sh`
lógica do aplicativo como fonte direta de uma chave travada sob condições normais
operação (sem travamento).

## Correção já aplicada (substituição/mitigação, não correção de causa raiz)
Ambos `cleanup()` em `type_watcher.sh` e `do_cleanup()` em
`keep-keys-up.sh` lançou anteriormente apenas teclas modificadoras (shift, ctrl,
alt, etc.) via `dotool`/`xdotool`. Isso não fez nada por um regular preso
chave (letra, número, pontuação).

- `type_watcher.sh`: `cleanup()` agora envia `dotool key <nome>:up` para
todas as letras, números e teclas comuns de pontuação/espaço em branco, não
apenas modificadores.
- `type_watcher.sh`: `INPUT_METHOD` agora é exportado após a detecção, então
outros scripts podem ver qual backend (`dotool` / `xdotool`) está ativo.
- `keep-keys-up.sh`: `do_cleanup()` ganhou um branch `dotool` (usando o
verbo `keyup`, sem atraso por tecla, para desempenho) ativo somente quando
`INPUT_METHOD=dotool`, espelhando a chamada `xdotool keyup` existente
para modificadores.

Isso não corrige a falha subjacente de `type_watcher.sh`; isso só
garante que, se a falha acontecer novamente, uma tecla presa será liberada
a próxima passagem de limpeza (`--cleanup`, chamada após cada `do_type()`, e
através do manipulador `trap cleanup EXIT INT TERM`) em vez de repetir
indefinidamente até um pressionamento manual da tecla do gatilho.

## Próximas etapas se isso acontecer novamente
- Capture stderr de `type_watcher.sh` em caso de falha. Atualmente
A linha 79 `type_watcher_keep_alive.sh` chama sem redirecionamento, então
qualquer mensagem de erro do bash é perdida (vai para o próprio watchdog
stdout/stderr, onde quer que seja direcionado pelo mecanismo de inicialização automática).
- Considere um modo de depuração, por ex. `bash -x scripts/type_watcher/type_watcher.sh
2 >> log/type_watcher_debug.log`, alternado por meio de um env var como
`TYPE_WATCHER_DEBUG=1`, para capturar a linha exata com falha no próximo
colidir.
- Verifique o que inicia `type_watcher_keep_alive.sh` na inicialização do Manjaro
(arquivo autostart `.desktop`, unidade systemd `--user`, etc.) e se
seu stdout/stderr é capturado em qualquer lugar.
- Se for reproduzível, teste se a falha está correlacionada com
`dotoold` ainda inicializando logo após a inicialização (veja o `sleep 0.1`
na linha 8 de type_watcher.sh e no loop de inicialização `dotoold` nas linhas
102-110).
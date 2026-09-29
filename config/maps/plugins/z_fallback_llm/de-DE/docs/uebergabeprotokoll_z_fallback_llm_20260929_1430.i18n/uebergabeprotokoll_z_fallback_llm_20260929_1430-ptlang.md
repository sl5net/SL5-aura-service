> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../uebergabeprotokoll_z_fallback_llm_20260929_1430.md).*

# Protocolo de entrega: z_fallback_llm, Entrada CLI não fornece uma piada

Situação: 29-09-2026

# # 1- Tarefa (compreensão, ainda não confirmada por você com "sim")

Estado real: A entrada CLI é exatamente "computador exatamente contar duas piadas". Não aparece nenhuma piada.

Estado-alvo: A resposta LLM aparece diretamente no console, não em um arquivo de log.

Não faz parte da tarefa: reconstruir registro, encurtar ou estender linhas de log, alterar o comportamento do cache. O desvio de cache ("brincadeira" na entrada) é deliberadamente escolhido desta forma.

O seguidor deve primeiro combinar este entendimento com você e esperar por seu "sim".

# # 2 Ambiente

Manjaro Linux, ZSH, Branch feature/fallback-llm-lazy-install.

Ollama está disponível em http://localhost:11434 (Binário /usr/bin/olama). Modelos disponíveis: llama3.2:último, qwen3:8b.

O teste Ollama por cacho com modelo lhama3.2, stream:false, num predict:100 e as palavras stop fornecem uma resposta válida ("Por que o computador foi ao médico?") Porque ele tinha um vírus! Ollama, nome do modelo, palavras de parada e limite de token não são, portanto, a causa. O prompt de teste foi mais curto do que o prompt real de ask ollama.py (sem função do sistema, gradiente e sufixo aura).

Configuração:

```
config/settings_local.py
```

Chave: PLUGINAS ENABLED = {"z fallback llm": 1}. Acesso via DynamicSettings().PLUGINAS ENABLED.get("z fallback llm", Falso).

Instalador de pacotes existente:

```
scripts/py/func/ensure_package.py
```

## 3- Sequência de cadeia (verificada a partir de seções de código)

Regras:

```
config/maps/plugins/z_fallback_llm/de-DE/FUZZY_MAP_pre.py
```

Regra 1 tem prioridade 10 e requer `{aura1}` plus mode word (normal, lento, fluxo, lento, preciso, completo). A regra 2 tem prioridade 100 e exige um dos gatilhos aura, aurora, laura, dora, era, hurra, prora ou computador, em seguida, um espaço e qualquer texto. Ambos chamam perguntar ollama.py. Ambos excluem janelas como Firefox, Chrome, Brave e Element.

Desenho:

```
config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py
```

`execute()` toma o último grupo Regex como entrada e o torna pequeno. Para "brincar" na entrada, `bypass_cache = True` é definido, a verificação de cache é ignorada. Isto é seguido pela solicitação Ollama com o modelo lhama3.2. O intervalo é de 90 segundos. Os primeiros retornos sem solicitação de Ollama estão disponíveis com entrada vazia ("nada ouvido."), com "esqueça tudo", com `check_static_guardrails()` e com as palavras instantâneas "imediatamente", "rápido", "instante".

Retorno CLI:

```
scripts/py/service_api.py
```

A função lê o arquivo de saída mais recente e retorna um dict com `status`, `result_text` e `input_text`. A linha de log "API-CLI-Call: Terminado" reduz a entrada e o resultado para 20 caracteres. Isto é puro encurtamento de log e não encurtamento de dados.

# # 4 - Diário observado da entrada CLI

No log estão apenas `reload_performed` e "API-CLI-Call: Terminado". Input="computador preciso," Resultado="computador preciso." Cada linha de `execute()` está faltando (sem "Input:", sem "Cache BYPASS", sem "Resposta de IA sem censura").

Isto não prova que o `execute()` não foi executado porque:

```
config/maps/plugins/z_fallback_llm/de-DE/utils.py
```

abre o FileHandler com `mode='w'`. O arquivo ask ollama.log é substituído pelo `utils` em cada importação. `log_debug` também escreve no stdout, ou seja, no console do programa principal.

# # 5 Perguntas abertas (não usadas)

1- O `execute()` funciona ao entrar no CLI?
2 - Qual regra corresponde, Regra 1, Regra 2 ou Nenhuma?
3- O cliente CLI produz o valor `result_text` no console?
4- O arquivo de saída contém apenas a entrada ou também uma resposta? Os primeiros 20 caracteres de entrada e resultado são idênticos, mais não é visível.
5- Qual é a chamada CLI exata que você usa para soltar o texto? Ainda não foi mencionado.

## 6- Hipóteses Rejeitadas

1- O input não chega cortado, isso foi apenas o corte de 20 caracteres no log.
2- Ollama, palavras de parada e num_predict não são a causa.
3- O cache foi contornado em "witz" e, portanto, não é a causa.

## 7- Erros encontrados fora da tarefa (não mudar nada sem uma tarefa)

1 arquivo:

```
config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py
```

Após `if not raw_text:`, `response = answer_for_all_fallback` é definido. A próxima linha substitui-o com `clean_text_for_typing(raw_text)`. Com uma resposta Ollama vazia, a resposta permanece vazia. Da mesma forma, `response.replace('sl5_config.py', ...)` e `response.replace(' sl5_record_trigger.py ', ...)` não têm efeito porque o resultado não é atribuído.

2 Ficheiro:

```
config/maps/plugins/internals/de-DE/aura_constants.py
```

De acordo com `Overlay`, um `|` está faltando, a variante `OverlayOrange` é criada. Além disso, `_variants` não contém a palavra "computador". A regra 1 não pode, portanto, corresponder exatamente ao "computador ...", a regra 2 pode.

Arquivo 3:

```
config/maps/plugins/z_fallback_llm/de-DE/utils.py
```

`mode='w'` substitui o log em cada importação.

## 8- Próximos passos (apenas após o seu "sim")

Passo A: Solicitar a chamada CLI de você, sem o caractere de prompt.

Etapa B: Encontrar o processamento de `result_text`:

```
tools/search.sh "result_text" .
```

Etapa C: Verifique a saída do console após a entrada. Para isso, solicite o texto completo do console do programa principal a você mesmo.

Passo D: Só depois sugerir alterações, apenas no formato Antes/Depois.

# # 9- Regras de trabalho que o sucessor deve cumprir

1- Comunicação em alemão. Código, comentários, registros e identificadores apenas em inglês, mesmo em blocos de código.
2- Nenhuma declaração sobre o estado do sistema sem prova da sua saída. Não adivinhes, não reconstruas.
3- Nova tarefa: descrever primeiro a compreensão, esperando pelo seu "sim".
4- Sem "Não tenho acesso ao seu repositório".
5- Pesquisa de repositório apenas via tools/search.sh com as opções -i, -E e -w.
6- Para erros, obter o traceback completo primeiro.
7- Os comandos e os caminhos dos arquivos estão cada um em sua própria linha, sem pontuação no final.
8- Numeração no formato 1-, 2-, 3-.
9- O código muda apenas como linhas alteradas no formato antes/depois, sem o código de função circundante.
10- Nenhum código python com indentação principal em blocos de código, em vez de pequenas funções sem indentação.
11- Sem caminhos absolutos, específicos do usuário e sem números de linha sem caminho de arquivo.
12- Sem conjuntos de preenchimento, sem tom emocional, cerca de 1400 caracteres por resposta como alvo.
13- Tratar ações que você já realizou como fez.
14- Ao copiar saídas não copiar o sinal imediato, caso contrário o código de saída 127 é criado.
15- Persistir para encontrar data e hora: ./tools/find-nearest-commit.sh "2026-07-28 17:00"

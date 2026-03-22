# Solução de problemas do SL5 Aura

## Diagnóstico Rápido

Sempre comece aqui:

```bash
# Check the main log:
tail -50 log/aura_engine.log

# Is Aura running?
pgrep -a -f aura_engine.py

# Is the file watcher running?
pgrep -a type_watcher
```

---

## Problema: Aura não inicia

**Sintoma:** Nenhum som de inicialização, nenhum processo visível em `pgrep`.

**Verifique o registro:**
```bash
tail -30 log/aura_engine.log
```

**Causas comuns:**

| Erro no registro | Correção |
|---|---|
| `ModuleNotFoundError` | Execute o script de configuração novamente: `bash setup/manjaro_arch_setup.sh` |
| `Nenhum módulo chamado 'objgraph'` | `.venv` foi recriado - reinstalação: `pip install -r requisitos.txt` |
| `Endereço já em uso` | Elimine o processo antigo: `pkill -9 -f aura_engine` |
| `Modelo não encontrado` | Execute novamente a configuração para baixar modelos ausentes |

---

## Problema: Aura trava após o primeiro ditado

**Sintoma:** Funciona uma vez e depois morre silenciosamente.

**Verifique stderr:**
```bash
cat /tmp/aura_stderr.log | tail -30
```

**Se você vir `Segmentation Fault` ou `double free`:**

Este é um problema conhecido em sistemas com glibc 2.43+ (CachyOS, Arch mais recente).

__CODE_BLOCO_3__

mimalloc é usado automaticamente pelo script de início, se instalado. Confirme se está ativo – você deverá ver isto na inicialização:
```bash
sudo pacman -S mimalloc
```

---

## Problema: a chave de gatilho não faz nada

**Sintoma:** Você pressiona a tecla de atalho, mas nada acontece: nenhum som, nenhum texto.

**Verifique se o inspetor de arquivos está em execução:**
__CODE_BLOCO_5__

Se nada aparecer, reinicie o Aura:
```
Info: Using mimalloc for improved memory management (/usr/lib/libmimalloc.so).
```

**Verifique se o arquivo acionador está sendo criado:**
```bash
pgrep -a type_watcher
```

Se o arquivo nunca for criado, sua configuração de teclas de atalho (CopyQ/AHK) não está funcionando.
Consulte a seção de configuração de teclas de atalho em [README.md](../../README.i18n/README-ptlang.md#configure-your-hotkey).

---

## Problema: o texto aparece, mas sem correções

**Sintoma:** O ditado funciona, mas tudo permanece em letras minúsculas, sem correções gramaticais.

**Verifique se o LanguageTool está em execução:**
```bash
./scripts/restart_venv_and_run-server.sh
```

Se isso retornar um erro, o LanguageTool não está em execução. Aura deveria começar
automaticamente — verifique o log em busca de erros relacionados ao LanguageTool:

__CODE_BLOCO_9__

**Verifique o registro do LanguageTool:**
```bash
ls -la /tmp/sl5_record.trigger
```

---

## Problema: Aura trava em DEV_MODE

**Sintoma:** Com `DEV_MODE = 1`, o Aura trava após o primeiro disparo e para
respondendo.

**Causa:** O alto volume de log de vários threads sobrecarrega o sistema de log.

**Correção:** Adicione um filtro de log em `config/filters/settings_local_log_filter.py`:

```bash
curl -s http://127.0.0.1:8082/v2/languages | head -5
```

Salve o arquivo — o Aura recarrega o filtro automaticamente. Não é necessário reiniciar.

---

## Problema: plugins.zip cresce infinitamente/alta CPU

**Sintoma:** CPU 100%, ventiladores em velocidade máxima, `plugins.zip` cresce sem parar.

**Causa:** O empacotador seguro está reempacotando os arquivos em um loop infinito.

**Correção:** Certifique-se de que os arquivos `.blob` e `.zip` sejam excluídos da verificação de carimbo de data/hora.
Verifique `scripts/py/func/secure_packer_lib.py` na linha 86:

```bash
grep -i "languagetool\|LT\|8082" log/aura_engine.log | tail -10
```

Se esta linha estiver faltando, adicione-a.

---

## Problema: regras não são acionadas

**Sintoma:** Você dita uma frase-gatilho, mas a regra não faz nada.

**Lista de verificação:**

1. A regra está no arquivo correto? (`FUZZY_MAP_pre.py` = antes do LanguageTool,
`FUZZY_MAP.py` = depois)
2. O arquivo do mapa foi salvo? Aura recarrega ao salvar – verifique o log para
`Recarregado com sucesso`.
3. O padrão corresponde ao que Vosk realmente transcreve? Verifique o registro para
a transcrição bruta:
```bash
cat log/languagetool_server.log | tail -20
```
4. `only_in_windows` está definido e a janela errada está ativa?
5. Uma regra mais geral corresponde primeiro? As regras são processadas de cima para baixo -
colocar regras específicas antes das gerais.

---

## Coletando logs para relatórios de bugs

Ao relatar um problema, inclua:

```python
LOG_ONLY = [
    r"Successfully",
    r"CRITICAL",
    r"📢📢📢 #",
    r"window_title",
    r":st:",
]
LOG_EXCLUDE = []
```

Postar em: [GitHub Issues](https://github.com/sl5net/SL5-aura-service/issues)
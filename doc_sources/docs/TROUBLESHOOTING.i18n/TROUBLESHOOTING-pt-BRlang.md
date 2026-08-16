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
| `pygame.mixer não disponível` | Consulte "Sem som na inicialização" abaixo |

---

## Problema: Sem som na inicialização (pygame.mixer)

**Sintoma:** Aviso ou erro sobre `pygame.mixer` não disponível. Aura começa
mas não reproduz sons.

**Causa:** A versão pygame do seu sistema não inclui suporte de áudio ou SDL2
faltam bibliotecas de áudio.

**Correção no Arch/Manjaro:**
```bash
sudo pacman -S sdl2_mixer
pip install pygame-ce --upgrade
```

**Correção no Ubuntu/Debian:**
__CODE_BLOCO_3__

Aura continuará a funcionar sem som – este não é um erro fatal.

---

## Problema: Aura trava após o primeiro ditado

**Sintoma:** Funciona uma vez e depois morre silenciosamente.

**Verifique stderr:**
```bash
sudo apt install libsdl2-mixer-2.0-0
pip install pygame-ce --upgrade
```

**Se você vir `Segmentation Fault` ou `double free`:**

Este é um problema conhecido em sistemas com glibc 2.43+ (CachyOS, Arch mais recente).

__CODE_BLOCO_5__

mimalloc é usado automaticamente pelo script de início, se instalado. Confirme se está ativo – você deverá ver isto na inicialização:
```bash
cat /tmp/aura_stderr.log | tail -30
```

---

## Problema: a chave de gatilho não faz nada

**Sintoma:** Você pressiona a tecla de atalho, mas nada acontece: nenhum som, nenhum texto.

**Verifique se o inspetor de arquivos está em execução:**
```bash
sudo pacman -S mimalloc
```

Se nada aparecer, reinicie o Aura:
```
Info: Using mimalloc for improved memory management (/usr/lib/libmimalloc.so).
```

**Verifique se o arquivo acionador está sendo criado:**
__CODE_BLOCO_9__

Se o arquivo nunca for criado, sua tecla de atalho não está funcionando – veja abaixo.

---

## Problema: a tecla de atalho não funciona no Wayland

**Sintoma:** CopyQ está instalado e configurado, mas pressionar a tecla de atalho não
nada em uma sessão de Wayland.

**Causa:** As teclas de atalho globais do CopyQ não funcionam de maneira confiável no Wayland sem
configuração adicional. Isso afeta o KDE Plasma, GNOME e outros
Compositores Wayland.

### Opção 1: Configurações do sistema KDE (recomendado para KDE Plasma)

1. Abra **Configurações do sistema → Atalhos → Atalhos personalizados**
2. Crie um novo atalho do tipo **Command/URL**
3. Defina o comando para:
```bash
pgrep -a type_watcher
```
4. Atribua sua combinação de teclas preferida (por exemplo, `F9` ou `Ctrl+Alt+Space`)

### Opção 2: dotool (Funciona em qualquer compositor Wayland)

```bash
./scripts/restart_venv_and_run-server.sh
```

Em seguida, use o gerenciador de atalhos da sua área de trabalho para executar:
```bash
ls -la /tmp/sl5_record.trigger
```

### Opção 3: ydotool

   ```bash
   touch /tmp/sl5_record.trigger
   ```

Em seguida, configure seu atalho para executar:
```bash
# Install dotool:
sudo pacman -S dotool        # Arch/Manjaro
# or
sudo apt install dotool      # Ubuntu (if available)
```

### Opção 4: GNOME (usando configurações dconf / GNOME)

1. Abra **Configurações → Teclado → Atalhos personalizados**
2. Adicione um novo atalho com o comando:
```bash
touch /tmp/sl5_record.trigger
```
3. Atribua uma combinação de teclas

### Opção 5: CopyQ com correção do Wayland

Alguns compositores Wayland permitem que o CopyQ funcione se iniciado com:
```bash
sudo pacman -S ydotool
sudo systemctl enable --now ydotool
```

Isso força o CopyQ a usar o XWayland, que oferece suporte a teclas de atalho globais.

---

## Problema: o texto aparece, mas sem correções

**Sintoma:** O ditado funciona, mas tudo permanece em letras minúsculas, sem correções gramaticais.

**Verifique se o LanguageTool está em execução:**
```bash
touch /tmp/sl5_record.trigger
```

Se isso retornar um erro, o LanguageTool não está em execução. Aura deveria começar
automaticamente — verifique o log em busca de erros relacionados ao LanguageTool:

   ```bash
   touch /tmp/sl5_record.trigger
   ```

**Verifique o registro do LanguageTool:**
```bash
QT_QPA_PLATFORM=xcb copyq
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
#Introdução ao Windows

## Etapa 1: execute a configuração
Clique duas vezes em `setup/windows11_setup_with_ahk_copyq.bat`.
- Clique com o botão direito → "Executar como administrador" se solicitado.
- O script instala Python, AutoHotkey v2, CopyQ e baixa os modelos de voz (~4 GB).
- Isso leva aproximadamente 8 a 10 minutos.

## Etapa 2: iniciar o Aura
Clique duas vezes em `start_aura.bat` na pasta do projeto.
Você deverá ouvir um som de inicialização – o Aura está pronto.

**Nada aconteceu?** Verifique o log:
log\aura_engine.log

## Etapa 3: Configure sua tecla de atalho
A configuração instala o CopyQ automaticamente. Para acionar o ditado:
1. Abra CopyQ → Comandos → Adicionar comando
2. Defina o comando para:
cmd /c eco. > C:\tmp\sl5_record.trigger
3. Atribua um atalho global (por exemplo, `F9`)

## Etapa 4: primeiro ditado
1. Clique em qualquer campo de texto
2. Pressione sua tecla de atalho – aguarde a notificação “Ouvindo…”
3. Diga "Olá, mundo"
4. Pressione a tecla de atalho novamente – o texto aparece

## Etapa 5: Encontre comandos de voz
Diga: **"Aura Search"** — uma janela será aberta com todas as regras disponíveis.

## Solução de problemas
| Sintoma | Correção |
|---|---|
| Nenhum som de inicialização | Verifique `log\aura_engine.log` |
| A tecla de atalho não faz nada | Verifique se `C:\tmp\sl5_record.trigger` foi criado |
| Texto não digitado | Verifique se `type_watcher.ahk` está sendo executado no Gerenciador de Tarefas |
| Falha ao iniciar | Execute a configuração novamente como Administrador |

> Solução de problemas completa: [TROUBLESHOOTING.md](../../TROUBLESHOOTING.i18n/TROUBLESHOOTING-pt-BRlang.md)
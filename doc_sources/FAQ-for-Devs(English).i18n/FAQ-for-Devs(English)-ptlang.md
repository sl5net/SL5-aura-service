# regras de expressões regulares

Importante: aplique as expressões regulares na ordem correta.

Você deve usar primeiro a expressão regular composta (mais geral) e depois aplicar a especializada.

A razão é que se a regex especializada mais curta for executada primeiro, ela poderá corresponder a uma parte da string que é essencial para a regex composta maior. Isso tornaria impossível para a regex composta encontrar sua correspondência posteriormente.
(S. 20.10.'25 18:37 Seg)

#Linux/Mac

se você quiser iniciar automaticamente o serviço pode adicionar:
~/projects/py/STT/scripts/restart_venv_and_run-server.sh
para a inicialização automática.

Inicie o serviço somente quando houver conexão com a Internet:
em seguida, defina em settings_local.py :
SERVIÇO_START_OPTION = 1


## adicionar entrar
quando você definir
config/settings_local.py/AUTO_ENTER_AFTER_DICTATION_REGEX_APPS
para 1 adiciona enter.

quando você definir
tmp/sl5_auto_enter.flag
para 1 adiciona enter.

tmp/sl5_auto_enter.flag será substituído quando você iniciar o serviço.
tmp/sl5_auto_enter.flag pode ser mais fácil de analisar para você com outros scripts e talvez seja um pouco mais rápido para lê-lo.

use outros números para disalbe
(S. 13.9.'25 16:12 Sábado)
# reglas de expresiones regulares

Importante: aplique las expresiones regulares en el orden correcto.

Primero debe utilizar la expresión regular compuesta (más general) y luego aplicar la especializada.

La razón es que si la expresión regular más corta y especializada se ejecuta primero, podría coincidir con una parte de la cadena que es esencial para la expresión regular compuesta más grande. Esto haría imposible que la expresión regular compuesta encuentre su coincidencia posteriormente.
(S. 20.10.'25 18:37 lun)

#Linux/Mac

Si desea iniciar automáticamente el servicio puede agregar:
~/projects/py/STT/scripts/restart_venv_and_run-server.sh
al inicio automático.

Inicie el servicio solo cuando haya conexión a Internet:
luego configúrelo en settings_local.py:
SERVICIO_START_OPTION = 1


## añadir entrar
cuando estableces
config/settings_local.py/AUTO_ENTER_AFTER_DICTATION_REGEX_APPS
a 1 agrega enter.

cuando estableces
tmp/sl5_auto_enter.flag
a 1 agrega enter.

tmp/sl5_auto_enter.flag se sobrescribirá cuando inicie el servicio.
tmp/sl5_auto_enter.flag puede ser más fácil de analizar con otros scripts y quizás sea un poco más rápido leerlo.

usar otros números para deshabilitar
(S. 13.9.'25 16:12 Sáb)
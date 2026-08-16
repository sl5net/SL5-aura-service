# Función Zsh: s() - KI-Client con tiempo de espera adaptable

Inglés (inglés)
Objetivo

Esta(s) función(es) de Zsh actúa como un contenedor para el cliente Python (cli_client.py) e implementa un manejo sólido de errores y una estrategia de tiempo de espera adaptable. Está diseñado para detectar rápidamente errores de conexión de servicios y garantizar que se capturen respuestas completas de IA (hasta 70 segundos).
Lógica clave

La función se basa en dos características del shell para su solidez:

tiempo de espera: evita que el script se cuelgue indefinidamente y permite una rápida detección de errores.

mktemp / Archivos temporales: evita los problemas de almacenamiento en búfer de salida del shell leyendo la salida del script desde un archivo después de la terminación.

Uso
código de golpe

  
s <texto de tu pregunta>
# Ejemplo: s Computer Guten Morgen

  
  
### fuente
__CODE_BLOCK_0__
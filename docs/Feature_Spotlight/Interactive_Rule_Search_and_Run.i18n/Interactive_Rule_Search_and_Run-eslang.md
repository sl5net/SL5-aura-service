# Búsqueda y ejecución de reglas interactivas

Este foco destaca el sistema interactivo de búsqueda y ejecución de reglas, que une los comandos vocales, la navegación en vivo y la ejecución instantánea.

## Funciones principales
[1] **Búsqueda en vivo de panel dual (`fzf`):** El panel izquierdo filtra archivos de reglas; El panel derecho muestra una vista previa del contexto de línea a través de `preview_rule.py`.
[2] **Ejecuciones instantáneas (`Enter` / `Ctrl+R`):** Ejecuta el comando de destino extraído instantáneamente a través de `run_palette_command.py` en segundo plano.
[3] **Edición directa (`Ctrl+E`):** Inicia el editor (CudaText con `@line`, Kate/VS Code con `--line`) directamente en la línea de destino.
[4] **Tecla de acceso rápido de ventana flotante:** Vinculada a `Super+S` para un flujo de trabajo rápido e integrado en el escritorio.
[5] **Controlado por comandos de voz:** Numerosos comandos de voz preconfiguran patrones de búsqueda en `search_rules.sh` para búsquedas rápidas y específicas.

## Soporte multiplataforma
- **Linux Bash (`run_rule.sh` / `search_rules.sh`):** Implementación con todas las funciones con seguimiento del historial y operaciones del portapapeles (`Ctrl+X` / `Ctrl+A`).
- **Windows PowerShell (`search_rules.ps1`):** Herramienta complementaria que proporciona capacidades de búsqueda de terminal livianas.

![Interactive Rule Search Console](.././assets/interactive_rule_search_20260727_155546.png)

![Interactive Rule Search Console](.././assets/interactive_rule_search_wie_wetter_heute20260727.png)

![Interactive Rule Search Console](.././assets/interactive_rule_search_20260814.png)
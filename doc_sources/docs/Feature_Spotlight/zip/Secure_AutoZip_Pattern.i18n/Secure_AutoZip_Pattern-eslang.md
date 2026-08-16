# Zip automático seguro y documentación integrada

## Concepto
SL5 Aura monitorea carpetas privadas que comienzan con `_` (por ejemplo, `_my_confidential_data`).
Cuando se detectan cambios, Aura crea automáticamente un archivo zip **cifrado**.

## Requisito previo crítico: clave de cifrado
**El cifrado es obligatorio.** El proceso de compresión automática requiere estrictamente que un archivo de contraseña esté presente en la jerarquía del directorio (carpetas actuales o principales).

* **Requisito de archivo:** El archivo de contraseña debe comenzar con un punto `.` (por ejemplo, `.archive_pass`, `.secret`).
* **Comportamiento:** Si no se encuentra ningún archivo de puntos con una contraseña, el proceso zip se **bloquea**. Este mecanismo de seguridad garantiza que nunca se empaqueten datos no cifrados.

## El patrón "Documentos integrados"
Dado que el sistema de recarga en caliente de Aura escucha **archivos Python válidos**, la actualización de un archivo Léame `.txt` simple no activará un recomprimido.

Para incluir instrucciones para los destinatarios (por ejemplo, "Cómo descomprimir") y al mismo tiempo garantizar que se active el activador, utilice un **Python Docstring File**.

### Implementación
Cree un archivo llamado `README_AUTOZIP.py` dentro de su carpeta monitoreada.

__CODE_BLOCK_0__
# Solución de problemas de SL5 Aura

## Diagnóstico rápido

Empiece siempre aquí:

```bash
# Check the main log:
tail -50 log/aura_engine.log

# Is Aura running?
pgrep -a -f aura_engine.py

# Is the file watcher running?
pgrep -a type_watcher
```

---

## Problema: el aura no se inicia

**Síntoma:** No hay sonido de inicio, no hay ningún proceso visible en `pgrep`.

**Consulta el registro:**
```bash
tail -30 log/aura_engine.log
```

**Causas comunes:**

| Error en el registro | Arreglar |
|---|---|
| `MóduloNotFoundError` | Ejecute el script de configuración nuevamente: `bash setup/manjaro_arch_setup.sh` |
| `Ningún módulo llamado 'objgraph'` | Se recreó `.venv` - reinstalar: `pip install -r requisitos.txt` |
| `Dirección ya en uso` | Elimine el proceso anterior: `pkill -9 -f aura_engine` |
| `Modelo no encontrado` | Vuelva a ejecutar la configuración para descargar los modelos que faltan |
| `pygame.mixer no disponible` | Consulte "No hay sonido al iniciar" a continuación |

---

## Problema: No hay sonido al iniciar (pygame.mixer)

**Síntoma:** Advertencia o error sobre `pygame.mixer` no disponible. Aura comienza
pero no reproduce ningún sonido.

**Causa:** La compilación de pygame de su sistema no incluye soporte de audio ni SDL2.
Faltan bibliotecas de audio.

**Arreglo en Arch/Manjaro:**
```bash
sudo pacman -S sdl2_mixer
pip install pygame-ce --upgrade
```

**Solución en Ubuntu/Debian:**
```bash
sudo apt install libsdl2-mixer-2.0-0
pip install pygame-ce --upgrade
```

Aura seguirá funcionando sin sonido; esto no es un error fatal.

---

## Problema: El aura falla después del primer dictado

**Síntoma:** Funciona una vez y luego muere silenciosamente.

**Verificar estándar:**
```bash
cat /tmp/aura_stderr.log | tail -30
```

**Si ve "Error de segmentación" o "doble liberación":**

Este es un problema conocido en sistemas con glibc 2.43+ (CachyOS, Arch más reciente).

```bash
sudo pacman -S mimalloc
```

mimalloc es utilizado automáticamente por el script de inicio si está instalado. Confirma que esté activo; deberías ver esto al iniciar:
```
Info: Using mimalloc for improved memory management (/usr/lib/libmimalloc.so).
```

---

## Problema: la tecla de activación no hace nada

**Síntoma:** Presionas la tecla de acceso rápido pero no sucede nada: ni sonido ni texto.

**Compruebe si el observador de archivos se está ejecutando:**
```bash
pgrep -a type_watcher
```

Si no aparece nada, reinicie Aura:
```bash
./scripts/restart_venv_and_run-server.sh
```

**Compruebe si se está creando el archivo desencadenante:**
```bash
ls -la /tmp/sl5_record.trigger
```

Si el archivo nunca se crea, su tecla de acceso rápido no funciona; consulte a continuación.

---

## Problema: la tecla de acceso rápido no funciona en Wayland

**Síntoma:** CopyQ está instalado y configurado, pero presionar la tecla de acceso rápido no
nada en una sesión de Wayland.

**Causa:** Las teclas de acceso rápido globales de CopyQ no funcionan de manera confiable en Wayland sin
configuración adicional. Esto afecta a KDE Plasma, GNOME y otros
Compositores de Wayland.

### Opción 1: Configuración del sistema KDE (recomendado para KDE Plasma)

1. Abra **Configuración del sistema → Accesos directos → Accesos directos personalizados**
2. Cree un nuevo acceso directo de tipo **Comando/URL**
3. Establezca el comando en:
   ```bash
   touch /tmp/sl5_record.trigger
   ```
4. Asigne su combinación de teclas preferida (por ejemplo, `F9` o `Ctrl+Alt+Espacio`)

### Opción 2: dotool (funciona en cualquier compositor de Wayland)

```bash
# Install dotool:
sudo pacman -S dotool        # Arch/Manjaro
# or
sudo apt install dotool      # Ubuntu (if available)
```

Luego use el administrador de accesos directos de su escritorio para ejecutar:
```bash
touch /tmp/sl5_record.trigger
```

### Opción 3: ydotool

```bash
sudo pacman -S ydotool
sudo systemctl enable --now ydotool
```

Luego configure su acceso directo para ejecutar:
```bash
touch /tmp/sl5_record.trigger
```

### Opción 4: GNOME (usando la configuración de dconf/GNOME)

1. Abra **Configuración → Teclado → Atajos personalizados**
2. Agregue un nuevo acceso directo con el comando:
   ```bash
   touch /tmp/sl5_record.trigger
   ```
3. Asigna una combinación de teclas

### Opción 5: CopyQ con corrección de Wayland

Algunos compositores de Wayland permiten que CopyQ funcione si se inician con:
```bash
QT_QPA_PLATFORM=xcb copyq
```

Esto obliga a CopyQ a utilizar XWayland, que admite teclas de acceso rápido globales.

---

## Problema: Aparece texto pero sin correcciones

**Síntoma:** El dictado funciona pero todo permanece en minúsculas, sin correcciones gramaticales.

**Compruebe si LanguageTool se está ejecutando:**
```bash
curl -s http://127.0.0.1:8082/v2/languages | head -5
```

Si esto devuelve un error, LanguageTool no se está ejecutando. Aura debería iniciarlo.
automáticamente: verifique el registro en busca de errores relacionados con LanguageTool:

```bash
grep -i "languagetool\|LT\|8082" log/aura_engine.log | tail -10
```

**Verifique el registro de LanguageTool:**
```bash
cat log/languagetool_server.log | tail -20
```

---

## Problema: Aura se bloquea en DEV_MODE

**Síntoma:** Con `DEV_MODE = 1`, Aura se bloquea después del primer activador y se detiene
respondiendo.

**Causa:** El alto volumen de registros de múltiples subprocesos sobrecarga el sistema de registro.

**Solución:** Agregue un filtro de registro en `config/filters/settings_local_log_filter.py`:

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

Guarde el archivo: Aura recarga el filtro automáticamente. No es necesario reiniciar.

---

## Problema: plugins.zip crece sin cesar/alta CPU

**Síntoma:** 100% CPU, ventiladores a máxima velocidad, `plugins.zip` crece sin parar.

**Causa:** El empaquetador seguro está reempaquetando archivos en un bucle infinito.

**Solución:** Asegúrese de que los archivos `.blob` y `.zip` estén excluidos del análisis de marca de tiempo.
Verifique `scripts/py/func/secure_packer_lib.py` alrededor de la línea 86:

```python
if file.startswith('.') or file.endswith('.pyc') or file.endswith('.blob') or file.endswith('.zip'):
    continue
```

Si falta esta línea, agréguela.

---

## Problema: las reglas no se activan

**Síntoma:** Usted dicta una frase desencadenante pero la regla no hace nada.

**Lista de verificación:**

1. ¿Está la regla en el archivo correcto? (`FUZZY_MAP_pre.py` = antes de LanguageTool,
`FUZZY_MAP.py` = después)
2. ¿Se guarda el archivo del mapa? Aura se recarga al guardar: verifique el registro para
`Recargado con éxito`.
3. ¿Coincide el patrón con lo que Vosk realmente transcribe? Verifique el registro para
la transcripción cruda:
   ```bash
   grep "Yielding chunk" log/aura_engine.log | tail -5
   ```
4. ¿Está configurado `only_in_windows` y la ventana incorrecta está activa?
5. ¿Se coincide primero con una regla más general? Las reglas se procesan de arriba a abajo.
anteponer las reglas específicas a las generales.

---

## Recopilación de registros para informes de errores

Al informar un problema, incluya:

```bash
# Last 100 lines of main log:
tail -100 log/aura_engine.log

# Crash output:
cat /tmp/aura_stderr.log

# System info:
uname -a
python3 --version
```

Publicar en: XMLDLINK0X
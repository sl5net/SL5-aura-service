# Integración WSL (Subsistema de Windows para Linux)

WSL le permite ejecutar un entorno Linux completo directamente en Windows. Una vez configurada, la integración del shell STT funciona **de manera idéntica a las guías Linux Bash o Zsh**: no se necesita ninguna adaptación específica de Windows para la función del shell en sí.

> **Recomendado para:** Usuarios de Windows que se sienten cómodos con una terminal Linux o que ya tienen WSL instalado para el trabajo de desarrollo. WSL proporciona la experiencia más fiel y los menores compromisos de compatibilidad.

## Requisitos previos

### Instalar WSL (configuración única)

Abra PowerShell o CMD **como administrador** y ejecute:

```powershell
wsl --install
```

Esto instala WSL2 con Ubuntu de forma predeterminada. Reinicie su máquina cuando se le solicite.

Para instalar una distribución específica:

```powershell
wsl --install -d Ubuntu-24.04
# or
wsl --install -d Debian
```

Lista todas las distribuciones disponibles:

```powershell
wsl --list --online
```

### Verifica tu versión de WSL

```powershell
wsl --list --verbose
```

Asegúrese de que la columna "VERSIÓN" muestre "2". Si muestra "1", actualice con:

```powershell
wsl --set-version <DistroName> 2
```

## Integración de Shell dentro de WSL

Una vez que WSL se esté ejecutando, abra su terminal Linux y siga la **guía de shell de Linux** para su shell preferido:

| Concha | Guía |
|-------|-------|
| Bash (valor predeterminado de WSL) | [bash-integration.md](../../linux/bash-integration.i18n/bash-integration-eslang.md) |
| Zsh | [zsh-integration.md](../../linux/zsh-integration.i18n/zsh-integration-eslang.md) |
| Pescado | [fish-integration.md](../../linux/fish-integration.i18n/fish-integration-eslang.md) |
| ksh | [ksh-integration.md](../../linux/ksh-integration.i18n/ksh-integration-eslang.md) |
| POSIX sh/guión | [posix-sh-integration.md](../../linux/posix-sh-integration.i18n/posix-sh-integration-eslang.md) |

Para la configuración predeterminada de Ubuntu/Debian WSL con Bash, la ruta rápida es:

```bash
nano ~/.bashrc
# Paste the function block from bash-integration.md
source ~/.bashrc
```

## Consideraciones específicas de WSL

### Accediendo a archivos de Windows desde WSL

Sus unidades de Windows están montadas en `/mnt/`:

```bash
/mnt/c/   # → C:\
/mnt/d/   # → D:\
```

Si su proyecto se encuentra en el sistema de archivos de Windows (por ejemplo, `C:\Projects\stt`), configure `PROJECT_ROOT` en:

```bash
export PROJECT_ROOT="/mnt/c/Projects/stt"
```

Agregue esta línea a su `~/.bashrc` (o el equivalente para su shell) **arriba** de la función `s()`.

> **Consejo de rendimiento:** Para obtener el mejor rendimiento de E/S, mantenga los archivos del proyecto dentro del sistema de archivos WSL (por ejemplo, `~/projects/stt`) en lugar de `/mnt/c/...`. El acceso entre sistemas de archivos entre WSL y Windows es significativamente más lento.

### Entorno virtual Python dentro de WSL

Cree y utilice un entorno virtual Linux estándar dentro de WSL:

```bash
cd "$PROJECT_ROOT"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

La ruta `PY_EXEC` en la función ($PROJECT_ROOT/.venv/bin/python3`) funcionará correctamente tal como está.

### Ejecutando `s` desde la terminal de Windows

[Windows Terminal](https://aka.ms/terminal) es la forma recomendada de utilizar WSL en Windows. Admite múltiples pestañas, paneles y perfiles para cada distribución WSL. Instálelo desde Microsoft Store o mediante:

```powershell
winget install Microsoft.WindowsTerminal
```

Configure su distribución WSL como el perfil predeterminado en la configuración de la Terminal de Windows para disfrutar de la experiencia más fluida.

### Docker y Kiwix dentro de WSL

El script auxiliar de Kiwix (`kiwix-docker-start-if-not-running.sh`) requiere Docker. Instale Docker Desktop para Windows y habilite la integración de WSL 2:

1. Descargue e instale [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. En Docker Desktop → Configuración → Recursos → Integración WSL, habilite su distribución WSL.
3. Verifique dentro de WSL:
   ```bash
   docker --version
   ```

### Llamar a la función WSL `s` desde Windows (opcional)

Si desea invocar el acceso directo `s` desde una ventana CMD de Windows o PowerShell sin abrir una terminal WSL, puede ajustarlo:

```powershell
# PowerShell wrapper
function s { wsl bash -i -c "s $args" }
```

```bat
:: CMD wrapper — save as s.bat on your PATH
@echo off
wsl bash -i -c "s %*"
```

> El indicador `-i` carga un shell interactivo para que su `~/.bashrc` (y la función `s`) se genere automáticamente.

## Características

- **Compatibilidad total con Linux**: todas las herramientas de Unix (`timeout`, `pgrep`, `mktemp`, `grep`) funcionan de forma nativa, no se necesitan soluciones alternativas.
- **Rutas dinámicas**: encuentra automáticamente la raíz del proyecto a través de la variable `PROJECT_ROOT` configurada en su configuración de shell.
- **Reinicio automático**: si el backend está inactivo, intenta ejecutar `start_service` y los servicios locales de Wikipedia (Docker debe estar ejecutándose).
- **Tiempos de espera inteligentes**: primero intenta una respuesta rápida de 2 segundos y luego vuelve a un modo de procesamiento profundo de 70 segundos.
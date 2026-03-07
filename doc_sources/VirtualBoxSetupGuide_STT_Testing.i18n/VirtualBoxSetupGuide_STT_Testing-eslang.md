# Guía de configuración de VirtualBox para pruebas de proyectos STT

Esta guía proporciona los pasos recomendados para configurar una máquina virtual Ubuntu 24.04 estable y eficaz en VirtualBox. Seguir estas instrucciones creará un entorno consistente para probar la aplicación STT y evitará problemas comunes como lentitud en la instalación, congelaciones del sistema y falta de funcionalidad del portapapeles.

## Requisitos previos

- VirtualBox instalado en la máquina host.
- Descargado un archivo ISO de escritorio Ubuntu 24.04.

## Hardware del host de referencia

Esta configuración fue probada y validada en el siguiente sistema host. El rendimiento puede variar en otro hardware, pero la configuración de estabilidad debe aplicarse universalmente.

- **Sistema Operativo:** Manjaro Linux
- **Núcleo:** 6.6.94
- **Procesador:** 16 × AMD Ryzen 7 3700X
- **Memoria:** 31,3 GiB de RAM
- **Procesador de gráficos:** NVIDIA GeForce GTX 1050 Ti

---

## Parte 1: Creación y configuración de VM

Estas configuraciones son críticas para el rendimiento y la estabilidad.

### Paso 1.1: Crear la nueva máquina virtual

1. En VirtualBox, haga clic en **Nuevo**.
2. **Nombre:** `Ubuntu STT Tester` (o similar).
3. **Imagen ISO:** Deje este campo en blanco.
4. Marque la casilla: **"Omitir instalación desatendida"**.
5. Haga clic en **Siguiente**.
6. **Equipo:**
- **Memoria base:** `4096 MB` o más.
- **Procesadores:** `4` o más.
7. Haga clic en **Siguiente**.

### Paso 1.2: Crear el disco duro virtual (CRÍTICO)

Este es el paso más importante para una instalación y un rendimiento rápidos.

1. Seleccione **"Crear un disco duro virtual ahora"**.
2. Establezca el tamaño del disco en **40 GB** o más.
3. En la siguiente pantalla, cambie el tipo de almacenamiento a **"Tamaño fijo"**.
> **¿Por qué?** Un disco de tamaño fijo está preasignado y evita el enorme cuello de botella de E/S que se produce cuando un disco "asignado dinámicamente" cambia constantemente de tamaño durante la instalación.
4. Haga clic en **Crear** y espere a que finalice el proceso.

### Paso 1.3: Configuración final de la máquina virtual

Seleccione la VM recién creada y haga clic en **Configuración**. Configure lo siguiente:

- **Sistema -> Placa base:**
- **Conjunto de chips:** `ICH9`
- Marque **"Habilitar EFI (solo sistemas operativos especiales)"**.

- **Pantalla -> Pantalla:**
- **Controlador de gráficos:** `VMSVGA`
- **Desmarque "Habilitar aceleración 3D"**.
> **¿Por qué?** La aceleración 3D es una causa común de bloqueos y congelaciones del sistema en invitados Linux. Deshabilitarlo mejora significativamente la estabilidad.

-   **Almacenamiento:**
- Seleccione el **Controlador SATA**. Marque la casilla **"Usar caché de E/S del host"**.
- Seleccione el archivo del disco virtual (`.vdi`). Marque la casilla **"Unidad de estado sólido"**.
- Seleccione la unidad óptica **Vacía**. Haga clic en el ícono del CD a la derecha y **"Elija un archivo de disco..."** para adjuntar su ISO de Ubuntu 24.04.

Haga clic en **Aceptar** para guardar todas las configuraciones.

---

## Parte 2: Instalación del sistema operativo Ubuntu

1. Inicie la máquina virtual.
2. Continúe con la configuración del idioma y del teclado.
3. Cuando llegue a "Actualizaciones y otro software", seleccione:
- **Instalación mínima**.
- **Desmarque** "Descargar actualizaciones mientras instala Ubuntu".
4. Continúe con la instalación hasta completarla.
5. Cuando termine, reinicie la VM. Cuando se le solicite, elimine el medio de instalación (presione Enter).

---

## Parte 3: Postinstalación (adiciones de invitados)

Este paso permite compartir el portapapeles, arrastrar y soltar y cambiar el tamaño de la pantalla automáticamente.

### Paso 3.1: Instalar ISO de Guest Additions en el host (si es necesario)

En su **máquina host**, asegúrese de que el paquete ISO de Guest Additions esté instalado.

- **Sobre Arco/Manjaro:**
    ```bash
    sudo pacman -S virtualbox-guest-iso
    ```
- **En Debian/Ubuntu:**
    ```bash
    sudo apt install virtualbox-guest-additions-iso
    ```

### Paso 3.2: Instalar Guest Additions dentro de la máquina virtual de Ubuntu

Realice estos pasos **dentro de su máquina virtual Ubuntu en ejecución**.

1. **Prepare Ubuntu:** Abra una terminal y ejecute los siguientes comandos para instalar las dependencias de compilación.
    ```bash
    sudo apt update
    sudo apt install build-essential dkms linux-headers-$(uname -r)
    ```
2. **Inserte el CD:** Desde el menú superior de VirtualBox, vaya a **Dispositivos -> Insertar imagen de CD de Guest Additions...**.
3. **Ejecute el instalador:**
- Puede aparecer un cuadro de diálogo solicitando ejecutar el software. Haga clic en **Ejecutar**.
- Si no aparece ningún cuadro de diálogo, abra el Administrador de archivos, haga clic derecho en el CD `VBox_GAs...`, elija **"Abrir en Terminal"** y ejecute el comando:
      ```bash
      sudo ./VBoxLinuxAdditions.run
      ```
4. **Reiniciar:** Una vez completada la instalación, reinicie la VM.
    ```bash
    reboot
    ```
5. **Habilitar funciones:** Después de reiniciar, vaya al menú **Dispositivos** y habilite **Portapapeles compartido -> Bidireccional** y **Arrastrar y soltar -> Bidireccional**.

Su entorno de pruebas estable y eficaz ya está listo.
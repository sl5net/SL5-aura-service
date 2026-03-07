## Utilidades del proyecto: divisor y descargador de archivos

Este repositorio incluye dos potentes scripts de Python diseñados para gestionar la distribución y descarga de archivos grandes a través de versiones de GitHub.

1. **`split_and_hash.py`**: una utilidad para que los propietarios de repositorios divida archivos grandes en partes más pequeñas y genere un manifiesto de suma de verificación completo y verificable.
2. **`download_all_packages.py`**: una herramienta sólida para que los usuarios finales descarguen, verifiquen y vuelvan a ensamblar automáticamente estos archivos de varias partes, garantizando la integridad de los datos de principio a fin.

---

### 1. Script de generación de suma de comprobación y división de archivos (`split_and_hash.py`)

Este script está destinado al **mantenedor del repositorio**. Prepara archivos grandes para su distribución en plataformas como GitHub Releases, que tienen límites de tamaño de archivo individuales.

#### Objetivo

El objetivo principal es tomar un único archivo grande (por ejemplo, `vosk-model-de-0.21.zip`) y realizar dos acciones críticas:
1. Divida el archivo en una serie de partes más pequeñas y numeradas.
2. Genere un archivo de manifiesto único y completo (`.sha256sums.txt`) que contenga las sumas de verificación para **tanto el archivo original completo como cada parte individual**.

Este manifiesto completo es la clave para garantizar el 100 % de la integridad de los datos para el usuario final.

#### Características clave

* **División estandarizada:** Divide archivos en fragmentos de 100 MB (configurables dentro del script).
* **Nombres consistentes:** Crea piezas con un prefijo `Z_` (por ejemplo, `Z_vosk-model-de-0.21.zip.part.aa`). El prefijo `Z_` garantiza una clasificación y manipulación adecuadas en varios sistemas.
* **Manifiesto de integridad completo:** El archivo `.sha256sums.txt` generado está estructurado para una máxima confiabilidad. Incluye:
* El hash SHA256 del **archivo completo original**.
* El hash SHA256 de **cada parte** que se creó.

#### Uso para una versión de GitHub

1. Coloque el archivo grande (por ejemplo, `vosk-model-de-0.21.zip`) en un directorio con el script `split_and_hash.py`.
2. Ejecute el script desde su terminal:
    ```bash
    python split_and_hash.py <your-large-file.zip>
    ```
3. El script generará todos los archivos `Z_...part.xx` y el archivo `...sha256sums.txt` correspondiente.
4. Al crear una nueva versión de GitHub, cargue **todos** los archivos generados: los archivos parciales y el archivo de manifiesto único.
5. Repita este proceso para cada archivo grande que desee distribuir.

---

### 2. Descargador y verificador de paquetes automatizado (`download_all_packages.py`)

Este script está destinado al **usuario final**. Proporciona una solución simple de un solo comando para descargar y reensamblar de manera confiable todos los paquetes ofrecidos en la versión GitHub.

#### Objetivo

Automatiza el proceso, que de otro modo sería complejo y propenso a errores, de descargar docenas de partes de archivos, verificar cada una y volver a ensamblarlas correctamente. Utiliza los manifiestos de suma de verificación proporcionados en el lanzamiento para garantizar que el archivo final ensamblado sea una copia perfecta y sin daños del original.

#### Características clave

* **Descubrimiento automático:** El script se conecta a la API de GitHub para encontrar automáticamente todos los "paquetes" disponibles en la versión buscando archivos `.sha256sums.txt`. No se necesita configuración manual de nombres de archivos.
* **Proceso de integridad primero:** Para cada paquete, descarga el archivo de manifiesto *primero* para obtener la lista de piezas requeridas y sus sumas de verificación correctas.
* **Verificación parte por parte:** Descarga una parte a la vez y verifica inmediatamente su hash SHA256.
* **Reintento automático en caso de corrupción:** Si una parte descargada está dañada (el hash no coincide), el script la elimina automáticamente y la vuelve a descargar, lo que garantiza una descarga limpia.
* **Reensamblado inteligente:** Una vez que todas las partes de un paquete se descargan y verifican, las combina en el orden alfabético correcto (`.aa`, `.ab`, `.ac`...) para reconstruir el archivo grande original.
* **Verificación final:** Después del reensamblaje, calcula el hash SHA256 del archivo final completo y lo verifica con el hash maestro que se encuentra en el manifiesto. Esto proporciona una confirmación de éxito de un extremo a otro.
* **Resiliente y tolerante:** El script es sólido frente a inconsistencias menores en los nombres, como `Z_` frente a `z_`, lo que garantiza una experiencia de usuario fluida.
* **Limpieza automatizada:** Después de que un paquete se compila y verifica correctamente, el script elimina los archivos de piezas descargados para ahorrar espacio en el disco.

#### Requisitos previos

El usuario debe tener instalado Python y las bibliotecas `requests` y `tqdm`. Se pueden instalar con pip:
```bash
pip install requests tqdm
```

#### Uso

1. Descargue el script `download_all_packages.py`.
2. Ejecútelo desde la terminal sin argumentos:
    ```bash
    python download_all_packages.py
    ```
3. El script se encargará del resto, mostrando barras de progreso y mensajes de estado. Al finalizar, el usuario tendrá todos los archivos ZIP finales verificados listos para usar en el mismo directorio.
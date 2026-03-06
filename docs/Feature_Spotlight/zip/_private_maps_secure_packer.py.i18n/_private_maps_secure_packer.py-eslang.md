importar sistema operativo
subproceso de importación
importar registro
importar Shuil
desde pathlib importar ruta

registrador = logging.getLogger(__nombre__)

def ejecutar(datos):
aprobar

def on_reload():
"""
Erstellt ein 'Matryoshka-ZIP':
Orden -> internal.zip (aura_secure.blob) -> contraseña.zip
Versteckt die komplette Verzeichnisstruktur.
"""
logger.info("🔒 SecurePacker (Matryoshka): Iniciar seguridad...")

current_dir = Ruta(__file__).padre
parent_dir = current_dir.padre

# Name des äußeren ZIPs
zip_name_outer = current_dir.name.lstrip('_') + ".zip"
zip_path_outer = parent_dir / zip_name_outer

# 1. Configuración de contraseña
key_file = siguiente(parent_dir.glob(".*.py"), Ninguno)
si no es archivo_clave:
logger.error("❌ ¡El archivo clave está fehlt!")
devolver

contraseña = _extract_password(archivo_clave)
si no es contraseña:
logger.error("❌ ¡La contraseña no está disponible!")
devolver

# 2. INNERES ZIP erstellen (Der "Blob")
# Wir erstellen es temporär im Parent-Dir um Schreibzugriffe im überwachten Ordner zu minimieren
temp_inner_zip = parent_dir / "aura_secure_temp" # se conecta a .zip

intentar:
# Erzeugt aura_secure_temp.zip
Shutil.make_archive(str(temp_inner_zip), 'zip', str(current_dir))
temp_inner_zip_file = parent_dir / "aura_secure_temp.zip"

# Umbenennen in den neutralen Blob-Namen
blob_name = "aura_secure.blob"
ruta_blob = dir_padre / nombre_blob
shutil.move(str(temp_inner_zip_file), str(blob_path))

# 3. ÄUßERES ZIP erstellen (Verschlüsselt)
si subproceso.call("comando -v zip", shell=True, stdout=subprocess.DEVNULL) != 0:
logger.error("❌ 'zip' Befehl fehlt.")
devolver

# Empaquetaremos NUR el Blob en el ZIP
cmd = [
'zip', '-j', # -j: Rutas basura (keine Pfade speichern, no Dateiname)
'-P', contraseña,
str(zip_path_outer),
str(ruta_blob)
]

proceso = subproceso.run(cmd, capture_output=Verdadero, texto=Verdadero)

# Aufräumen des Blobs
sistema operativo.remove(blob_path)

si proceso.returncode == 0:
logger.info(f"✅ SecurePacker: Struktur versteckt in {zip_name_outer} gespeichert.")
demás:
logger.error(f"❌ Archivo ZIP: {proceso.stderr}")

excepto excepción como e:
logger.error(f"❌ Paquete Fehler: {e}")

def _extract_password(ruta_clave):
intentar:
con open(key_path, 'r', encoding='utf-8') como f:
para la línea en f:
si line.strip().startswith("#"):
limpio = línea.strip().lstrip("#").strip()
si está limpio: regresar limpio
excepto: pasar
regresar Ninguno
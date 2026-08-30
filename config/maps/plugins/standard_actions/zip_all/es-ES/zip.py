# ==============================================================================
# 🌐 AUTOMATICALLY GENERATED / MACHINE-TRANSLATED MAP
# ==============================================================================
# ℹ️  Source Language: German (de-DE)
# ⚙️  Note: Speech recognition regexes (VOSK) and Koan instructions in this
#     file were machine-translated. Spoken patterns may require refinement
#     or tuning for natural speech in the target language.
#
# 🤝  CONTRIBUTIONS WELCOME!
#     We would love your help improving this map! If you test or refine these
#     regex patterns, please open a Pull Request with your improvements.
# ==============================================================================

# config/maps/plugins/standard_actions/zip_all/de-DE/zip.pye

import importlib.util
import json
import logging
import os
import shutil
import sys
from pathlib import Path

# --- Configuración ---

CURRENT_DIR = Path(__file__).parent
JSON_DB_PATH = CURRENT_DIR / "zip_registry.json"
# Sube 7 niveles hasta la raíz del proyecto -> configuración -> mapas

SCAN_ROOT = Path(__file__).resolve().parents[6] / "config" / "maps"

# --- Configurar registro ---

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# --- IMPORTACIONES DINÁMICAS ---


def get_packer_lib():
    """Import secure_packer_lib for PACKING."""
    lib_path = SCAN_ROOT.parents[1] / "scripts" / "py" / "func" / "secure_packer_lib.py"
    if not lib_path.exists():
        logger.error(f"❌ secure_packer_lib not found at {lib_path}")
        return None
    spec = importlib.util.spec_from_file_location("secure_packer_lib", lib_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["secure_packer_lib"] = module
    spec.loader.exec_module(module)
    return module

def get_unpacker_lib():
    """Import private_map_ex for UNPACKING."""
    lib_path = SCAN_ROOT.parents[1]  / "scripts" / "py" / "func" / "private_map_ex.py"
    if not lib_path.exists():
        logger.error(f"❌ private_map_ex not found at {lib_path}")
        return None
    spec = importlib.util.spec_from_file_location("private_map_ex", lib_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["private_map_ex"] = module
    spec.loader.exec_module(module)
    return module

# --- Ayudantes JSON ---

import tempfile
from pathlib import Path
from typing import Any


def load_registry(auto_migrate: bool = True) -> list[Any]:
    if not JSON_DB_PATH.exists():
        logger.debug("Registry file %s does not exist; returning empty list", JSON_DB_PATH)
        return []

    text = JSON_DB_PATH.read_text(encoding="utf-8")
    if not text.strip():
        logger.debug("Registry file %s is empty; returning empty list", JSON_DB_PATH)
        return []

    data = json.loads(text)

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        if not auto_migrate:
            raise ValueError(f"Registry {JSON_DB_PATH} is a dict, expected list")
        # Migración de ejemplo: use los valores como una lista (o alternativamente [datos])

        migrated = list(data.values())
        _atomic_write_json(JSON_DB_PATH, migrated)
        logger.debug("Migrated registry %s from dict -> list (backup created)", JSON_DB_PATH)
        return migrated

    raise ValueError(f"Registry {JSON_DB_PATH} contains unexpected JSON type: {type(data).__name__}")

def _atomic_write_json(path: Path, obj: Any) -> None:
    # escribe atómicamente: temp -> cambiar nombre, mantiene copia de seguridad

    backup = path.with_suffix(path.suffix + ".bak")
    if path.exists():
        shutil.copy2(path, backup)
    fd, tmp = tempfile.mkstemp(dir=path.parent)
    try:
        with open(fd, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        Path(tmp).replace(path)
    finally:
        if Path(tmp).exists():
            Path(tmp).unlink()


def save_registry(folder_list):
    try:
        with open(JSON_DB_PATH, 'w', encoding='utf-8') as f:
            json.dump({"watched_folders": list(set(folder_list))}, f, indent=4)
    except Exception as e: logger.error(f"❌ Failed to save JSON: {e}")

# --- MARCAS DE TIEMPO / LÓGICA DE BÚSQUEDA ---


from enum import Enum


class PackingStatus(Enum):
    NOT_NEEDED = 0
    CONTENT_CHANGED = 1
    ZIP_MISSING = 2

def _needs_packing(source_folder: Path, zip_file: Path) -> PackingStatus:
    """Returns the specific reason why packing is needed or NOT_NEEDED."""
    if not zip_file.exists():
        return PackingStatus.ZIP_MISSING

    zip_time = zip_file.stat().st_mtime

    grace_period = 1.0

    for root, dirs, files in os.walk(source_folder):
        if "__pycache__" in root:
            continue

        for file in files:
            if file.startswith('.') or file.endswith('.pyc') or file.endswith('~'):
                continue

            file_path = Path(root) / file
            file_time = file_path.stat().st_mtime

            if file_time > (zip_time + grace_period):
                # logger.info(f"El archivo {file} es más nuevo que ZIP. Archivo: {file_time}, Zip: {zip_time}")

                return PackingStatus.CONTENT_CHANGED

    return PackingStatus.NOT_NEEDED

def _needs_unpacking(target_folder: Path, zip_file: Path) -> bool:
    """True if Zip is NEWER than Folder (or Folder missing)."""
    if not zip_file.exists(): return False
    if not target_folder.exists(): return True
    # Búfer de 2 segundos para precisiones del sistema de archivos

    return zip_file.stat().st_mtime > (target_folder.stat().st_mtime + 2)

def find_password_file(start_dir: Path) -> Path:
    """
    Search upwards for a file starting with '.' (the key/password).
    Stops at 'config/maps'.
    """
    current = start_dir
    limit = SCAN_ROOT
    i = 0
    while True:
        i += 1
        logger.info(f'i={i}   standard_actions/zip_all/de-DE/zip.py:113')
        if current.exists():
            for item in current.iterdir():
                if item.is_file() and item.name.startswith('.'):
                    # Filtrar archivos del sistema

                    if item.name in ['.DS_Store', '.gitignore', '.gitkeep']:
                        continue
                    return item

        if current == limit: break
        if current.parent == current: break
        current = current.parent

    return None

# --- FLUJOS DE TRABAJO ---


def scan_and_register_folders():
    """MANUAL: Scans disk for '_folders', updates JSON."""
    logger.info(f"🕵️ Scanning for zip-targets in: {SCAN_ROOT}")
    found = []
    for root, dirs, files in os.walk(SCAN_ROOT):
        path_obj = Path(root)
        if path_obj.name.startswith('.') or '__pycache__' in path_obj.parts: continue

        if path_obj.name.startswith('_') and not path_obj.name.startswith('__'):
            found.append(str(path_obj.resolve()))

    save_registry(found)
    return len(found)

def check_and_unpack_zips():
    """
    Checks Registry. If Zip > Folder:
    1. Find key file (upwards).
    2. Copy key file to zip directory (if not already there).
    3. Run existing unpacker.
    4. Delete temporary key copy.
    """
    folders = load_registry()

    if not folders:
        print('2026-0109-1053')
        return

    unpacker_module = get_unpacker_lib()
    print('2026-0109-1049')
    if not unpacker_module:
        print('2026-0109-1107')
        print('2026-0109-1107')
        print('2026-0109-1107')
        print('2026-0109-1107')
        return

    for folder_str in folders:

        print('2026-0109-1050')
        print('2026-0109-1050')
        print('2026-0109-1050')
        print('2026-0109-1050')

        folder_path = Path(folder_str)
        # _t1 -> t1.zip (hermano)

        zip_name = folder_path.name.lstrip('_') + ".zip"
        zip_dir = folder_path.parent

        print('2026-0109-1051')

        zip_path = zip_dir / zip_name

        if _needs_unpacking(folder_path, zip_path):
            logger.info(f"🔓 Update available for {folder_path.name}…")

            # 1. Encuentra la llave (en algún lugar arriba del árbol)

            found_pw_file = find_password_file(folder_path)

            if found_pw_file:
                # 2. Determine la ruta local para la clave (al lado del zip)

                local_key_path = zip_dir / found_pw_file.name
                created_temp_copy = False

                try:
                    # Si la clave está más arriba, cópiela temporalmente

                    if found_pw_file.parent.resolve() != zip_dir.resolve():
                        logger.info(f"   🔑 Copying temp key to: {local_key_path.name}")
                        shutil.copy2(found_pw_file, local_key_path)
                        created_temp_copy = True

                    # 3. Llame al desempaquetador existente con la ruta de la clave LOCAL

                    unpacker_module._private_map_unpack(str(local_key_path), logger)

                    # Toque la carpeta para actualizar mtime (evitar bucle)

                    if folder_path.exists():
                        os.utime(folder_path, None)

                except Exception as e:
                    logger.info(f"❌ Failed to unpack {zip_path.name}: {e}")
                    return

                finally:
                    # 4. Limpieza: eliminar la clave copiada

                    if created_temp_copy and local_key_path.exists():
                        try:
                            local_key_path.unlink()
                            # logger.debug("🧹 Archivo de clave temporal eliminado.")

                        except Exception as cleanup_err:
                            logger.warning(f"⚠️ Could not remove temp key {local_key_path}: {cleanup_err}")
            else:
                logger.warning(f"⚠️ No password file found for {folder_path.name}. Cannot unpack.")
                return
    return


def check_and_pack_zips():
    """Checks Registry. If Folder > Zip, calls secure_packer_lib."""
    folders = load_registry()
    if not folders: return

    packer_lib = get_packer_lib()
    if not packer_lib: return

    for folder_str in folders:
        folder_path = Path(folder_str)
        if not folder_path.exists(): continue

        zip_name = folder_path.name.lstrip('_') + ".zip"
        zip_target = folder_path.parent / zip_name

        if (_needs_packing(folder_path, zip_target) == PackingStatus.CONTENT_CHANGED
                or _needs_unpacking(folder_path, zip_target) == PackingStatus.ZIP_MISSING):
            if _needs_packing(folder_path, zip_target) == PackingStatus.CONTENT_CHANGED:
                logger.info(f"♻️ Content changed. 📦 Zipping: …{str(folder_path)[-30:]}")
                # faltar una cremallera quizás tenga buenas razones

            try:
                packer_lib.execute_packing_logic(folder_path, logger)
            except Exception as e:
                logger.info(f"⚠️ Error packing …{str(folder_path)[-30:]}: {e}")

# ---MANOS---


# config/maps/plugins/standard_actions/zip_all/de-DE/zip.py:234

def on_reload():
    """Runs automatically on every reload."""
    try: # config/maps/plugins/standard_actions/zip_all/de-DE/zip.py:236
        check_and_unpack_zips()
    except Exception as e:
        # STT/config/maps/plugins/standard_actions/zip_all/de-DE/zip.py:241

        m = f"🔥 Error in zip_all/de-DE/zip.py:241 on_reload in check_and_unpack_zips(): {e}"
        # registrador.info(f"{m}")

        logger.debug(f"{m}")
        return f"{m}"
        # salida del sistema (1)

        # 07:40:03,498 - ERROR - 🔥 Error en zip_all/de-DE/zip.py:236 on_reload: intento de importación relativa sin paquete principal conocido

    try: # config/maps/plugins/standard_actions/zip_all/de-DE/zip.py:236
        check_and_pack_zips()
    except Exception as e:
        # STT/config/maps/plugins/standard_actions/zip_all/de-DE/zip.py:241

        m = f"🔥 Error in zip_all/de-DE/zip.py:251 on_reload in check_and_pack_zips(): {e}"
        logger.info("{m")
        logger.error(f"{m}")
        return f"{m}"
        # salida del sistema (1)

        # 07:40:03,498 - ERROR - 🔥 Error en zip_all/de-DE/zip.py:236 on_reload: intento de importación relativa sin paquete principal conocido


def execute(match_data):
    """Manual Voice Command."""
    logger.info("🎤 Voice Command: Full Scan & Sync…")

    count = scan_and_register_folders()

    check_and_unpack_zips()
    check_and_pack_zips()

    return f"Scan complete. {count} targets synced."


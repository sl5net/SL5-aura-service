import os
import subprocess
import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)

def execute(data):
    pass

def on_reload():
    """
    Erstellt ein 'Matryoshka-ZIP':
    Ordner -> inner.zip (aura_secure.blob) -> password.zip
    Versteckt die komplette Verzeichnisstruktur.
    """
    logger.info("🔒 SecurePacker (Matryoshka): Starte Sicherung...")

    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent

    # Name des äußeren ZIPs
    zip_name_outer = current_dir.name.lstrip('_') + ".zip"
    zip_path_outer = parent_dir / zip_name_outer

    # 1. Passwort suchen
    key_file = next(parent_dir.glob(".*.py"), None)
    if not key_file:
        logger.error("❌ Key-File fehlt!")
        return

    password = _extract_password(key_file)
    if not password:
        logger.error("❌ Passwort nicht gefunden!")
        return

    # 2. INNERES ZIP erstellen (Der "Blob")
    # Wir erstellen es temporär im Parent-Dir um Schreibzugriffe im überwachten Ordner zu minimieren
    temp_inner_zip = parent_dir / "aura_secure_temp" # wird zu .zip

    try:
        # Erzeugt aura_secure_temp.zip
        shutil.make_archive(str(temp_inner_zip), 'zip', str(current_dir))
        temp_inner_zip_file = parent_dir / "aura_secure_temp.zip"

        # Umbenennen in den neutralen Blob-Namen
        blob_name = "aura_secure.blob"
        blob_path = parent_dir / blob_name
        shutil.move(str(temp_inner_zip_file), str(blob_path))

        # 3. ÄUßERES ZIP erstellen (Verschlüsselt)
        if subprocess.call("command -v zip", shell=True, stdout=subprocess.DEVNULL) != 0:
            logger.error("❌ 'zip' Befehl fehlt.")
            return

        # Wir packen NUR den Blob in das ZIP
        cmd = [
            'zip', '-j',       # -j: Junk paths (keine Pfade speichern, nur Dateiname)
            '-P', password,
            str(zip_path_outer),
            str(blob_path)
        ]

        process = subprocess.run(cmd, capture_output=True, text=True)

        # Aufräumen des Blobs
        os.remove(blob_path)

        if process.returncode == 0:
            logger.info(f"✅ SecurePacker: Struktur versteckt in {zip_name_outer} gespeichert.")
        else:
            logger.error(f"❌ ZIP Fehler: {process.stderr}")

    except Exception as e:
        logger.error(f"❌ Pack Fehler: {e}")

def _extract_password(key_path):
    try:
        with open(key_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip().startswith("#"):
                    clean = line.strip().lstrip("#").strip()
                    if clean: return clean
    except: pass
    return None


Betriebssystem importieren
Unterprozess importieren
Protokollierung importieren
Shutil importieren
aus pathlib import Path

logger = logging.getLogger(__name__)

defexecute(data):
passieren

def on_reload():
„““
Erstellt ein 'Matryoshka-ZIP':
Ordner -> inner.zip (aura_secure.blob) -> passwort.zip
Versteckt die komplette Verzeichnisstruktur.
„““
logger.info("🔒 SecurePacker (Matryoshka): Starte Sicherung...")

current_dir = Path(__file__).parent
parent_dir = aktuelles_dir.parent

# Name des äußeren ZIPs
zip_name_outer = current_dir.name.lstrip('_') + ".zip"
zip_path_outer = parent_dir / zip_name_outer

# 1. Passwort suchen
key_file = next(parent_dir.glob(".*.py"), None)
wenn nicht key_file:
logger.error("❌ Schlüsseldatei fehlt!")
zurückkehren

Passwort = _extract_password(key_file)
wenn nicht Passwort:
logger.error("❌ Passwort nicht gefunden!")
zurückkehren

# 2. INNERES ZIP erstellen (Der „Blob“)
# Wir erstellen es temporär im Parent-Dir, um den Schreibzugriff im überwachten Ordner zu minimieren
temp_inner_zip = parent_dir / "aura_secure_temp" # wird zu .zip

versuchen:
# Erzeugt aura_secure_temp.zip
Shutil.make_archive(str(temp_inner_zip), 'zip', str(current_dir))
temp_inner_zip_file = parent_dir / "aura_secure_temp.zip"

# Umbenennen in den neutralen Blob-Namen
blob_name = "aura_secure.blob"
blob_path = parent_dir / blob_name
Shutil.move(str(temp_inner_zip_file), str(blob_path))

# 3. ÄUßERES ZIP erstellen (Verschlüsselt)
if subprocess.call("command -v zip", shell=True, stdout=subprocess.DEVNULL) != 0:
logger.error("❌ 'zip' Befehl fehlt.")
zurückkehren

# Wir packen NUR den Blob in das ZIP
cmd = [
'zip', '-j', # -j: Junk-Pfade (keine Pfade speichern, nur Dateiname)
'-P', Passwort,
str(zip_path_outer),
str(blob_path)
]

Prozess = subprocess.run(cmd, capture_output=True, text=True)

# Aufräumen des Blobs
os.remove(blob_path)

wenn process.returncode == 0:
logger.info(f"✅ SecurePacker: Struktur versteckt in {zip_name_outer} gespeichert.")
anders:
logger.error(f"❌ ZIP Fehler: {process.stderr}")

außer Ausnahme als e:
logger.error(f"❌ Packfehler: {e}")

def _extract_password(key_path):
versuchen:
mit open(key_path, 'r',kodierung='utf-8') als f:
für Zeile in f:
if line.strip().startswith("#"):
clean = line.strip().lstrip("#").strip()
wenn sauber: sauber zurückgeben
außer: bestanden
return Keine
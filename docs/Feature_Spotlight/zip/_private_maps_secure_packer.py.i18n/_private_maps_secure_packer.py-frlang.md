importer le système d'exploitation
sous-processus d'importation
journalisation des importations
importer des produits laitiers
à partir du chemin d'importation pathlib

enregistreur = logging.getLogger (__name__)

def exécuter (données):
passer

def on_reload() :
"""
Créer un « Matryoshka-ZIP » :
Ordner -> inner.zip (aura_secure.blob) -> mot de passe.zip
Versteckt die komplette Verzeichnisstruktur.
"""
logger.info("🔒 SecurePacker (Matriochka) : Démarrer la sécurité...")

current_dir = Chemin (__file__).parent
parent_dir = current_dir.parent

# Nom des ZIP utilisés
zip_name_outer = current_dir.name.lstrip('_') + ".zip"
zip_path_outer = rép_parent / zip_name_outer

# 1. Mot de passe tel que
key_file = next(parent_dir.glob(".*.py"), Aucun)
sinon key_file :
logger.error("❌ Key-File fehlt!")
retour

mot de passe = _extract_password (fichier_clé)
sinon mot de passe :
logger.error("❌ Le mot de passe n'est pas financé !")
retour

# 2. INNERES ZIP erstellen (Der "Blob")
# Nous allons travailler temporairement dans la direction des parents dans un tableau de bord dans un ordre de surveillance minimal
temp_inner_zip = parent_dir / "aura_secure_temp" # wird zu .zip

essayer:
# Utiliser aura_secure_temp.zip
shuil.make_archive(str(temp_inner_zip), 'zip', str(current_dir))
temp_inner_zip_file = parent_dir / "aura_secure_temp.zip"

# Umbenennen in den neutralen Blob-Namen
blob_name = "aura_secure.blob"
blob_path = parent_dir / blob_name
shutil.move(str(temp_inner_zip_file), str(blob_path))

# 3. ÄUßERES ZIP erstellen (Verschlüsselt)
si subprocess.call("command -v zip", shell=True, stdout=subprocess.DEVNULL) != 0 :
logger.error("❌ 'zip' Befehl fehlt.")
retour

# Nous emballons NUR le Blob dans le ZIP
cmd = [
'zip', '-j', # -j : chemins indésirables (keine Pfade speichern, nur Dateiname)
'-P', mot de passe,
str(zip_path_outer),
str(chemin_blob)
]

processus = subprocess.run(cmd, capture_output=True, text=True)

# Aufräumen des Blobs
os.remove(blob_path)

si process.returncode == 0 :
logger.info(f"✅ SecurePacker : structure versteckt in {zip_name_outer} utilisé.")
autre:
logger.error(f"❌ ZIP Fehler : {process.stderr}")

sauf exception comme e :
logger.error(f"❌ Pack Fehler : {e}")

def _extract_password(key_path) :
essayer:
avec open(key_path, 'r', encoding='utf-8') comme f :
pour la ligne en f :
si line.strip().startswith("#") :
clean = line.strip().lstrip("#").strip()
si propre : rendre propre
sauf : passer
retourner Aucun
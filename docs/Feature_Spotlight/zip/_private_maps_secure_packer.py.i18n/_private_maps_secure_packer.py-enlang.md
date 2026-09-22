> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../_private_maps_secure_packer.py.md).*

Import os
import subprocessing
Import logging
import shutil
from pathlib import path

logger = logging.getLogger(__name__)

def execute(data):
    Passport

def on reload():
    """
    Created a 'Matryoshka-ZIP':
    Folder -> inner.zip (aura secure.blob) -> password.zip
    Hide the entire directory structure.
    """
    logger.info("🔒 SecurePacker (Matryoshka): Start backup...")

    current dir = Path(__file__).parent
    parent dir = current dir.parent

    # Name of outer ZIP
    zip name outer = current dir.name.lstrip(' ') + ".zip"
    zip path outer = parent dir / zip name outer

    #1 Search for password
    key file = next(parent dir.glob(.*.py)), None
    if not key file:
        logger.error(")"❌ Key file missing!
        Return

    password =  extract password(key file)
    if not password:
        logger.error(")"❌ Password not found!
        Return

    Create INNER ZIP (The "Blob")
    # We create it temporarily in the Parent-Dir to minimize write accesses in the monitored folder
    temp inner zip = parent dir / "aura secure temp" # becomes .zip

    try:
        # Created aura secure temp.zip
        shutil.make archive(str(temp inner zip), 'zip', str(current dir))
        temp inner zip file = parent dir / "aura secure temp.zip"

        # Renaming to the neutral blob name
        blob name = "aura secure.blob"
        blob path = parent dir / blob name
        shutil.move(str(temp inner zip file), str(blob path))

        #3 Create External ZIP (Encrypted)
        if subprocess.call("command -v zip", shell=True, stdout=subprocess.DEVNULL) != 0:
            logger.error("❌ 'zip' command missing.")
            Return

        # We ONLY pack the blob into the ZIP
        cmd = []
            'zip', '-j', # -j: Junk paths (no paths saved, file name only)
            ‘-P’, password,
            str(zip path outer),
            str(blob path)
        ]

        process = subprocess.run(cmd, capture output=True, text=True)

        # Cleaning up the blob
        os.remove(blob path)

        if process.returncode == 0:
            logger.info(f)✅ SecurePacker: Structure hidden stored in {zip name outer}.
        Other:
            logger.error(f"❌ ZIP error: {process.stderr})

    except Exception as e:
        logger.error(f)❌ Pack error: {e}]

def  extract password(key path):
    try:
        with open(key path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip(.startswith("#")):
                    clean = line.strip().lstrip("#").strip()
                    if clean: return clean
    Except: Passport
    return None


importar sistema operacional
subprocesso de importação
registro de importação
importar Shutil
do caminho de importação pathlib

criador de logs = logging.getLogger(__nome__)

def executar (dados):
passar

def on_reload():
"""
Erstellt um 'Matryoshka-ZIP':
Ordem -> inner.zip (aura_secure.blob) -> password.zip
Versteckt die komplette Verzeichnisstruktur.
"""
logger.info("🔒 SecurePacker (Matryoshka): Início da segurança...")

diretório_atual = Caminho(__arquivo__).parent
parent_dir = current_dir.parent

# Nome dos ZIPs originais
zip_name_outer = diretório_atual.nome.lstrip('_') + ".zip"
zip_path_outer = parent_dir / zip_name_outer

# 1. Seleção de senha
arquivo_chave = próximo(parent_dir.glob(".*.py"), Nenhum)
se não for key_file:
logger.error("❌ Arquivo-chave encontrado!")
retornar

senha = _extract_password(key_file)
se não for senha:
logger.error("❌ A senha não foi criada!")
retornar

# 2. INNERES ZIP erstellen (Der "Blob")
# Wir erstellen é temporário no Parent-Dir um Schreibzugriffe im überwachten Ordner zu minimieren
temp_inner_zip = parent_dir / "aura_secure_temp" # wird zu .zip

tentar:
# Erzeugt aura_secure_temp.zip
shutil.make_archive(str(temp_inner_zip), 'zip', str(diretório_atual))
temp_inner_zip_file = parent_dir / "aura_secure_temp.zip"

# Umbenennen no nome neutro do Blob
blob_name = "aura_secure.blob"
blob_path = parent_dir / blob_name
shutil.move(str(temp_inner_zip_file), str(blob_path))

# 3. ÄUßERES ZIP erstellen (Verschlüsselt)
if subprocess.call("command -v zip", shell=True, stdout=subprocess.DEVNULL) != 0:
logger.error("❌ 'zip' Befehl fehlt.")
retornar

# Wir packen NUR den Blob in das ZIP
cmd = [
'zip', '-j', # -j: Caminhos indesejados (nenhum Pfade speichern, nur Dateinaname)
'-P', senha,
str(zip_path_outer),
str(blob_path)
]

processo = subprocess.run(cmd, capture_output=True, text=True)

# Aufraumen des Blobs
os.remove(blob_path)

se process.returncode == 0:
logger.info(f"✅ SecurePacker: Estrutura versteckt em {zip_name_outer} gespeichert.")
outro:
logger.error(f"❌ ZIP Fehler: {process.stderr}")

exceto Exceção como e:
logger.error(f"❌ Pacote Fehler: {e}")

def _extract_password(caminho_chave):
tentar:
com open(key_path, 'r', encoding='utf-8') como f:
para linha em f:
se line.strip().startswith("#"):
limpar = line.strip().lstrip("#").strip()
se estiver limpo: retorne limpo
exceto: passar
retornar Nenhum
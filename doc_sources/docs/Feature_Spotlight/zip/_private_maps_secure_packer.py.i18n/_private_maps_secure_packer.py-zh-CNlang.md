导入操作系统
导入子流程
导入日志记录
进口舒蒂尔
从 pathlib 导入路径

logger =logging.getLogger(__name__)

def 执行（数据）：
经过

def on_reload():
”“”
Erstellt ein 'Matryoshka-ZIP':
Ordner -> 内部.zip (aura_secure.blob) -> 密码.zip
Versteckt die komplette Verzeichnisstruktur。
”“”
logger.info("🔒 SecurePacker (Matryoshka): 开始 Sicherung...")

current_dir = 路径(__file__).parent
父目录 = 当前目录.父目录

# 名称 des äußeren ZIP
zip_name_outer = current_dir.name.lstrip('_') + ".zip"
zip_path_outer = 父目录 / zip_name_outer

# 1. 密码这样
key_file = next(parent_dir.glob(".*.py"), 无)
如果不是密钥文件：
logger.error("❌密钥文件感觉！")
返回

密码 = _extract_password(密钥文件)
如果没有密码：
logger.error("❌ 密码不存在！")
返回

# 2. INNERES ZIP erstellen (Der "Blob")
# Wir erstellen es temporär im Parent-Dir um Schreibzugriffe im überwachten Ordner zu minimieren
temp_inner_zip = Parent_dir / "aura_secure_temp" # 线 zu .zip

尝试：
# Erzeugt aura_secure_temp.zip
Shutil.make_archive(str(temp_inner_zip), 'zip', str(current_dir))
temp_inner_zip_file =parent_dir /“aura_secure_temp.zip”

# 中立的 Blob-Namen 中的 Umbenennen
blob_name =“aura_secure.blob”
blob_path = 父目录 / blob_name
Shutil.move(str(temp_inner_zip_file), str(blob_path))

# 3. AUßERES ZIP erstellen (Verschlüsselt)
if subprocess.call("command -v zip", shell=True, stdout=subprocess.DEVNULL) != 0:
logger.error("❌'zip'Befehl fehlt。")
返回

# 将 NUR den Blob 打包到 das ZIP 中
命令 = [
'zip', '-j', # -j: 垃圾路径 (keine Pfade speichern, nur Dateiname)
'-P'，密码，
str(zip_path_outer),
str(blob_路径)
]

进程 = subprocess.run(cmd, capture_output=True, text=True)

# 斑点的出现
os.remove(blob_path)

如果 process.returncode == 0:
logger.info(f"✅ SecurePacker: Struktur versteckt in {zip_name_outer} gespeichert.")
别的：
logger.error(f"❌ZIP Fehler: {process.stderr}")

除了异常 e：
logger.error(f"❌Pack Fehler: {e}")

def _extract_password(key_path):
尝试：
打开（key_path，'r'，encoding='utf-8'）作为f：
对于 f 中的行：
if line.strip().startswith("#"):
clean = line.strip().lstrip("#").strip()
如果干净：返回干净
除外：通过
返回无
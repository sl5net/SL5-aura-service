수입 OS
하위 프로세스 가져오기
수입 로깅
수입 차단
pathlib import 경로에서

로거 = login.getLogger(__name__)

def 실행(데이터):
통과하다

데프 on_reload():
"""
Erstellt ein 'Matryoshka-ZIP':
Ordner -> inner.zip(aura_secure.blob) -> 비밀번호.zip
Versteckt die komplette Verzeichnisstruktur.
"""
logger.info("🔒 SecurePacker (Matryoshka): 시작 Sicherung...")

current_dir = 경로(__file__).parent
parent_dir = 현재_dir.parent

# 이름 des äußeren ZIP
zip_name_outer = current_dir.name.lstrip('_') + ".zip"
zip_path_outer = parent_dir / zip_name_outer

# 1. 비밀번호 이런첸
key_file = next(parent_dir.glob(".*.py"), 없음)
key_file이 아닌 경우:
logger.error("❌ 키 파일 펠트!")
반품

비밀번호 = _extract_password(key_file)
비밀번호가 아닌 경우:
logger.error("❌ 비밀번호를 입력하세요!")
반품

# 2. INNERES ZIP erstellen (Der "Blob")
# Wir erstellen es temporär im Parent-Dir um Schreibzugriffe im überwachten Ordner zu minimieren
temp_inner_zip = parent_dir / "aura_secure_temp" # wird zu .zip

노력하다:
# Erzeugt aura_secure_temp.zip
shutdown.make_archive(str(temp_inner_zip), 'zip', str(current_dir))
temp_inner_zip_file = parent_dir / "aura_secure_temp.zip"

# 중립적인 Blob-Namen의 Umbenennen
blob_name = "aura_secure.blob"
blob_path = parent_dir / blob_name
shutdown.move(str(temp_inner_zip_file), str(blob_path))

# 3. äUßERES ZIP erstellen(Verschlüsselt)
subprocess.call("command -v zip", shell=True, stdout=subprocess.DEVNULL) != 0인 경우:
logger.error("❌ 'zip' Befehl fehlt.")
반품

# das ZIP의 Wir packen NUR den Blob
명령 = [
'zip', '-j', # -j: 정크 경로(keine Pfade speichern, nur Dateiname)
'-P', 비밀번호,
str(zip_path_outer),
str(blob_path)
]

프로세스 = subprocess.run(cmd, Capture_output=True, text=True)

# Aufräumen des Blobs
os.remove(blob_path)

process.returncode == 0인 경우:
logger.info(f"✅ SecurePacker: Struktur versteckt in {zip_name_outer} gespeichert.")
또 다른:
logger.error(f"❌ ZIP 파일러: {process.stderr}")

e와 같은 예외를 제외하고:
logger.error(f"❌ 팩 파일러: {e}")

def _extract_password(key_path):
노력하다:
open(key_path, 'r', 인코딩='utf-8')을 f로 사용:
f의 라인에 대해:
if line.strip().startswith("#"):
clean = line.strip().lstrip("#").strip()
깨끗한 경우: 깨끗한 상태로 반환
제외: 합격
반환 없음
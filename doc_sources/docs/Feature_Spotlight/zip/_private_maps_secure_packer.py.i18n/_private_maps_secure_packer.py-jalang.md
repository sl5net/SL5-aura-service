OSをインポートする
サブプロセスのインポート
インポートログ
インポートシュティル
pathlibインポートパスから

logger =logging.getLogger(__name__)

def 実行(データ):
合格

def on_reload():
「」
「マトリョーシカ-ZIP」の例:
Ordner -> inner.zip (aura_secure.blob) -> passwd.zip
Versteckt die komplette Verzeichnisstruktur。
「」
logger.info("🔒 SecurePacker (マトリョーシカ): Starte Sicherung...")

current_dir = パス(__file__).parent
親ディレクトリ = 現在のディレクトリ.親

# 使用する ZIP に名前を付ける
zip_name_outer = current_dir.name.lstrip('_') + ".zip"
zip_path_outer = 親ディレクトリ / zip_name_outer

#1. パスワードなど
key_file = next(parent_dir.glob(".*.py"), None)
key_file でない場合:
logger.error("❌ キーファイルが見つかりました!")
戻る

パスワード = _extract_password(key_file)
パスワードでない場合:
logger.error("❌ パスワードが見つかりません!")
戻る

#2. INNERES ZIP erstellen (Der "Blob")
# Wir erstellen es Temporär im Parent-Dir um Schreibzugriffe im überwachten Ordner zu minimieren
temp_inner_zip =parent_dir / "aura_secure_temp" # wird zu .zip

試す：
# エルツァイグト aura_secure_temp.zip
shutil.make_archive(str(temp_inner_zip), 'zip', str(current_dir))
temp_inner_zip_file =parent_dir / "aura_secure_temp.zip"

# ブロブ名を中立化するウンベネンネン
blob_name = "aura_secure.blob"
blob_path = 親ディレクトリ / blob_name
shutil.move(str(temp_inner_zip_file), str(blob_path))

# 3. ÄUßERES ZIP erstellen (Verschlüsselt)
if subprocess.call("command -v zip"、shell=True、stdout=subprocess.DEVNULL) != 0:
logger.error("❌ 'zip' です。")
戻る

# Wir パック NUR den Blob in das ZIP
cmd = [
'zip'、'-j'、# -j: ジャンク パス (keine Pfade speichern、nur Dateiname)
「-P」、パスワード、
str(zip_path_outer),
str(ブロブパス)
]

process = subprocess.run(cmd、capture_output=True、text=True)

# ブロブの分析
os.remove(blob_path)

process.returncode == 0の場合:
logger.info(f"✅ SecurePacker: {zip_name_outer} の構造を確認します。")
それ以外：
logger.error(f"❌ ZIP Fehler: {process.stderr}")


logger.error(f"❌ パック・フェーラー: {e}")

def _extract_password(key_path):
試す：
open(key_path, 'r', encoding='utf-8') を f として使用します:

if line.strip().startswith("#"):
clean = line.strip().lstrip("#").strip()
クリーンの場合: クリーンを返す
例外: パス
なしを返す
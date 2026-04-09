import platform
import importlib.util
from pathlib import Path

def run_wizard(user_language="de-DE"):
    # 1. Find project root via your robust method
    try:
        tmp_dir = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")
        project_root_file = tmp_dir / "sl5_aura" / "sl5net_aura_project_root"
        project_root = Path(project_root_file.read_text(encoding="utf-8").strip())
    except Exception:
        # Fallback if the file does not exist
        project_root = Path(__file__).resolve().parents[2]

    base_path = Path(__file__).parent.resolve()

    # Sprache normalisieren (de -> de-DE)
    lang_folder = user_language
    if lang_folder == "de": lang_folder = "de-DE"
    if lang_folder == "en": lang_folder = "en-US"

    lang_script = base_path / lang_folder / "start.py"

    if lang_script.exists():
        try:
            spec = importlib.util.spec_from_file_location("wizard_start", lang_script)
            wizard_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(wizard_module)

            # Wizard ausführen
            wizard_module.run(project_root)
        except Exception as e:
            # So that debugs are not "washed away", we print them conspicuously:
            print(f"\n{'!'*60}\nAURA WIZARD ERROR: {e}\n{'!'*60}\n")

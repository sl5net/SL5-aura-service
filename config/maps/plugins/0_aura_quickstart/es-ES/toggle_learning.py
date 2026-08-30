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

# config/maps/plugins/0_aura_quickstart/de-DE/toggle_learning.py

import os
import subprocess
from pathlib import Path

from scripts.py.func.config.dynamic_settings import settings
from scripts.py.func.utils.get_leading_whitespace import (
    get_leading_whitespace_before_pos,
)

# ---

# Importaciones requeridas que deben existir en cada FUZZY_MAP_pre.py

# ---

_REQUIRED_IMPORTS = [
    "from pathlib import Path as p;import os as o # noqa: E702",
    "with open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702",
]


def _ensure_required_imports(content: str) -> str:
    """
    Ensure the two required import lines exist at the top of the file.
    Insert them right after the first import block if missing.
    """
    lines = content.splitlines()

    # Compruebe si las importaciones ya existen (no distinguen espacios en blanco)

    content_flat = content.replace(" ", "").replace("\t", "")
    missing = []
    for req in _REQUIRED_IMPORTS:
        req_flat = req.replace(" ", "").replace("\t", "")
        if req_flat not in content_flat:
            missing.append(req)

    if not missing:
        return content

    # Encuentra el final del bloque de importación inicial.

    last_import_idx = -1
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            last_import_idx = i

    # Insertar importaciones faltantes después de la última línea de importación

    insert_idx = last_import_idx + 1 if last_import_idx >= 0 else 0

    to_insert = []
    if insert_idx > 0 and lines[insert_idx - 1].strip():
        to_insert.append("")
    to_insert.extend(missing)
    to_insert.append("")

    new_lines = lines[:insert_idx] + to_insert + lines[insert_idx:]
    return "\n".join(new_lines)

def speak(text):
    try:
        subprocess.run(['espeak', '-v', 'en-US', text], check=True)
    except Exception as e:
        print(f"STDOUT (TTS-Fallback): {text} , {e}")

def execute(match_data):
    # es de config/maps/plugins/0_aura_quickstart/de-DE/FUZZY_MAP_pre.py

    # alemán EJEMPLO: activar y desactivar el modo de aprendizaje

    # español EJEMPLO: modo aprendizaje habilitar deshabilitar


    project_root = os.environ.get('SL5NET_AURA_PROJECT_ROOT', '')
    maps_base_dir = Path(project_root) / "config" / "maps"

    tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
    last_edited_file = tmp_dir / "sl5_aura" / "last_edited_map.txt"
    candidate_path1 = Path(last_edited_file.read_text(encoding="utf-8").strip()).expanduser()
    candidate_path = maps_base_dir / candidate_path1


    if not candidate_path.exists():
        speak(f"Can't find {last_edited_file}")
        print(f"Can't find {last_edited_file}")
        return "Error reading last_edited_map.txt"


    # map_file = Ruta(__file__).parent / "FUZZY_MAP_pre.py"

    map_file = Path(candidate_path)
    if not map_file.exists():
        speak(f"No map file found at {candidate_path}")
        return f"No map file found at {candidate_path}"


    # is = map_file_is_modified tal vez sea lo mismo cuando __file dado es el mismo



    content = map_file.read_text(encoding="utf-8")
    original_text = match_data.get('original_text', '').lower()

    # ¿Qué buscamos en el archivo?

    training_plugin_string = "collect_unmatched.py"

    lines = content.splitlines()
    new_lines = []
    status = "Keine Änderung vorgenommen."

    is_turning_off = any(word in original_text for word in ["aus", "ab", "stopp", "beende", "dea", "dis"])


    for line in lines:
        if training_plugin_string in line:
            if is_turning_off:
                if not line.strip().startswith("#"):

                    # líder_ws = get_leading_whitespace_of_line(línea)


                    # new_lines.append(leading_ws + "# " + línea.strip())

                    # simplemente ya no agregamos esta línea. el mapa entonces es menos desordenado


                    status = "Lernmodus DEAKTIVIERT."
                else:
                    new_lines.append(line)
                    status = "Lernmodus is already deaktivated"
            else:
                # eliminar comentario

                if line.strip().startswith("#"):
                    idx = line.find("#")
                    prefix = line[:idx]
                    suffix = line[idx+1:]
                    suffix = suffix.removeprefix(" ")
                    new_lines.append(prefix + suffix)
                    status = "Lernmodus AKTIVIERT."
                else:
                    new_lines.append(line)
                    status = "Lernmodus ist bereits aktiv."
        else:
            status = "Learn-modus rule not found. "
            if is_turning_off:
                new_lines.append(line)
            if not is_turning_off:
                status = "Learn-modus rule not found. it will be added now."
                new_lines.append(line)

                # Agregar nueva regla si la lista existe

                if "FUZZY_MAP_pre = [" in content:
                    idx = content.rfind("]")
                    if idx != -1:
                        leading_ws = get_leading_whitespace_before_pos(content, idx)
                        if not leading_ws:
                            leading_ws = "    "
                        new_rule = leading_ws + r"(f'{str(__file__)}', r'^(.*)$', 10, {'on_match_exec': [SL5NET_AURA_PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']})," + "\n\n"
                        new_content = content[:idx] + new_rule + content[idx:]

                        # Asegúrese de que existan las importaciones requeridas antes de escribir

                        new_content = _ensure_required_imports(new_content)

                        map_file.write_text(new_content, encoding="utf-8")

                        if settings.AUDIO_GUIDANCE_ENABLED:
                            speak("unmatched is added to your map")
                        return f"unmatched is added to your map …{str(map_file)[-30:]} (20260711_2331)"

    map_file.write_text("\n".join(new_lines), encoding="utf-8")

    if is_turning_off:
        try:
            if last_edited_file.exists():
                last_edited_file.unlink()
            if settings.AUDIO_GUIDANCE_ENABLED:
                speak("last edited file is deleted.")

        except Exception:
            speak(f"Error deleting {last_edited_file}")
            print(f"Error deleting {last_edited_file}")


    if settings.AUDIO_GUIDANCE_ENABLED:
        speak("unmatched is added to your map")
    return status

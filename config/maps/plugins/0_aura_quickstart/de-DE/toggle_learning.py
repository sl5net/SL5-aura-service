# config/maps/plugins/0_aura_quickstart/de-DE/toggle_learning.py
from pathlib import Path

def execute(match_data):
    # 1. Projekt-Root finden (deine robuste Methode)
    #tmp_dir = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")
    #root_file = tmp_dir / "sl5_aura" / "sl5net_aura_project_root"
    # project_root = Path(root_file.read_text(encoding="utf-8").strip())

    # 2. Die Map-Datei in diesem Ordner finden

    map_file_is_modified = Path(__file__).parent / "FUZZY_MAP_pre.py"
    if not map_file_is_modified.exists():
        return "Fehler: FUZZY_MAP_pre.py nicht gefunden."


    # TODO: map_file_with_learn_mode_switch
    map_file_with_learn_mode_switch = "map_file_with_learn_mode_switch"
    print(f'dodo {map_file_with_learn_mode_switch}')
    # is = map_file_is_modified  maybe the same when __file given  is the same


    content = map_file_is_modified.read_text(encoding="utf-8")
    original_text = match_data.get('original_text', '').lower()

    # Wonach suchen wir in der Datei?
    training_plugin_string = "collect_unmatched.py"

    lines = content.splitlines()
    new_lines = []
    status = "Keine Änderung vorgenommen."

    # Logik: An- oder Ausschalten
    is_turning_off = any(word in original_text for word in ["aus", "stopp", "beende", "deaktiviere"])

    import os
    tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
    last_edited_file = tmp_dir / "sl5_aura" / "last_edited_map.txt"

    if is_turning_off:
        try:
            if last_edited_file.exists():
                last_edited_file.unlink()
        except Exception:
            pass

    for line in lines:
        if training_plugin_string in line:
            if is_turning_off:
                if not line.strip().startswith("#"):
                    new_lines.append("# " + line)
                    status = "Lernmodus DEAKTIVIERT."
                else:
                    new_lines.append(line)
                    status = "Lernmodus is already deaktivated"
            else:
                # Aktivieren: Nur wenn es auskommentiert ist
                if line.strip().startswith("#"):
                    # Wir suchen die Position des ersten '#'
                    idx = line.find("#")
                    # Wir nehmen alles VOR dem '#' (die originale Einrückung)
                    prefix = line[:idx]
                    # Wir nehmen alles NACH dem '#' und entfernen EIN optionales Leerzeichen
                    suffix = line[idx+1:]
                    if suffix.startswith(" "):
                        suffix = suffix[1:]

                    # Wir setzen es wieder zusammen: Einrückung + originaler Code
                    new_lines.append(prefix + suffix)
                    status = "Lernmodus AKTIVIERT."
                else:
                    new_lines.append(line)
                    status = "Lernmodus ist bereits aktiv."
        else:
            new_lines.append(line)

    map_file_is_modified.write_text("\n".join(new_lines), encoding="utf-8")
    return status


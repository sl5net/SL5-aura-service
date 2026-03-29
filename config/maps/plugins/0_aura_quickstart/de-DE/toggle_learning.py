from pathlib import Path

def execute(match_data):
    # 1. Projekt-Root finden (deine robuste Methode)
    #tmp_dir = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")
    #root_file = tmp_dir / "sl5_aura" / "sl5net_aura_project_root"
    # project_root = Path(root_file.read_text(encoding="utf-8").strip())

    # 2. Die Map-Datei in diesem Ordner finden
    map_file = Path(__file__).parent / "FUZZY_MAP_pre.py"
    if not map_file.exists():
        return "Fehler: FUZZY_MAP_pre.py nicht gefunden."

    content = map_file.read_text(encoding="utf-8")
    original_text = match_data.get('original_text', '').lower()

    # Wonach suchen wir in der Datei?
    training_plugin_string = "collect_unmatched.py"

    lines = content.splitlines()
    new_lines = []
    status = "Keine Änderung vorgenommen."

    # Logik: An- oder Ausschalten
    is_turning_off = any(word in original_text for word in ["aus", "stopp", "beende", "deaktiviere"])

    for line in lines:
        if training_plugin_string in line:
            if is_turning_off:
                # Deaktivieren: Nur wenn es noch nicht auskommentiert ist
                if not line.strip().startswith("#"):
                    # Wir setzen das '#' ganz an den Anfang der Zeile,
                    # OHNE die Zeile zu strippen. So bleibt die Einrückung dahinter erhalten.
                    new_lines.append("# " + line)
                    status = "Lernmodus DEAKTIVIERT."
                else:
                    new_lines.append(line)
                    status = "Lernmodus war bereits aus."
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

    map_file.write_text("\n".join(new_lines), encoding="utf-8")
    return status


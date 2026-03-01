import os
import re
import time
from pathlib import Path

import os
import re
import time


def check_map_health(file_path, module, logger):
    """
    Validiert frisch geänderte Map-Dateien auf Strukturfehler.
    Sucht automatisch nach Variablen wie 'FUZZY_MAP_pre', 'FUZZY_MAP_post', etc.
    """
    # 1. Zeit-Check: Nur Dateien, die in der letzten Stunde (3600s) geändert wurden
    try:
        if (time.time() - os.path.getmtime(file_path)) > 3600:
            return
    except Exception as e:
        print(f'2026-0301-1434: e')
        return

    # 2. Bekannte Listen-Namen, nach denen wir im Modul suchen
    possible_map_names = ['FUZZY_MAP_pre', 'FUZZY_MAP_post', 'GLOBAL_FUZZY_MAP_PRE', 'GLOBAL_FUZZY_MAP_POST']

    # Wir suchen, welche dieser Listen im Modul existiert
    map_entries = None
    for name in possible_map_names:
        if hasattr(module, name):
            map_entries = getattr(module, name)
            break

    if not map_entries or not isinstance(map_entries, list):
        return

    # 3. Validierung der Einträge
    logger.info(f"🔍 Health-Check: Validating '{os.path.basename(file_path)}'...")
    regex_indicators = r'[\^$|()\[\]\\]'

    for i, entry in enumerate(map_entries):
        if not isinstance(entry, (tuple, list)) or len(entry) < 2:
            continue

        rule_id = str(entry[0])
        pattern = str(entry[1])

        # Heuristik für Vertauschung
        id_has_regex = bool(re.search(regex_indicators, rule_id))
        pattern_is_clean = not bool(re.search(regex_indicators, pattern))

        if id_has_regex and pattern_is_clean:
            logger.error("=" * 60)
            logger.error(f"❌ STRUKTUR-FEHLER GEFUNDEN: {file_path}")
            logger.error(f"   In Zeile/Index {i} sind ID und Regex vermutlich VERTAUSCHT!")
            logger.error(f"   Feld 1 (ID): '{rule_id}'")
            logger.error(f"   Feld 2 (Regex): '{pattern}'")
            logger.error("=" * 60)


import re
import os
import json
from pathlib import Path

def validate_map_structure(map_data, file_path, logger):
    """
    Prüft die Integrität der Mapping-Tupel.
    Erwartet: (ID, Regex, Priority, Settings)
    """
    for i, entry in enumerate(map_data):
        if not isinstance(entry, (tuple, list)) or len(entry) < 4:
            logger.warning(f"⚠️ [Struktur-Fehler] {file_path} Zeile {i}: Ungültiges Format. Erwarte Tupel mit 4 Elementen.")
            continue

        rule_id, pattern, priority, settings = entry[:4]

        # HEURISTIK: Erkennt Vertauschung von ID und Regex
        # Wenn die ID Sonderzeichen enthält, die Regex aber wie ein einfacher Name aussieht
        regex_indicators = r'[\^$|()\[\]\\]'

        id_looks_like_regex = bool(re.search(regex_indicators, str(rule_id)))
        pattern_looks_like_id = not bool(re.search(regex_indicators, str(pattern)))

        if id_looks_like_regex and pattern_looks_like_id:
            logger.error(f"❌ [VERTAUSCHUNGS-ALARM] {file_path}:")
            logger.error(f"   In Eintrag {i} scheint die ID '{rule_id}' ein Regex-Pattern zu sein.")
            logger.error(f"   Prüfe, ob ID und Regex-Pattern vertauscht wurden!")
            return False

        # TYP-CHECK: Priority sollte eine Zahl sein
        if not isinstance(priority, (int, float)):
            logger.warning(f"⚠️ [Typ-Fehler] {file_path}: Priority '{priority}' in Eintrag {i} ist keine Zahl.")

    return True

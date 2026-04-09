import os
import re
import time

def check_map_health(file_path, module, logger):
    try:
        # DEBUG: Show mtime in log if it doesn't trigger
        mtime_diff = time.time() - os.path.getmtime(file_path)
        if mtime_diff > 3600:
            # logger.debug(f"Skipping health-check for {file_path} (too old: {int(mtime_diff)}s)")
            return
    except Exception as e:
        print(f'2026-0301-1511 {e}')
        return

    map_entries = None
    for name in ['FUZZY_MAP_pre', 'FUZZY_MAP_post', 'GLOBAL_FUZZY_MAP_PRE']:
        if hasattr(module, name):
            map_entries = getattr(module, name)
            break

    if not map_entries or not isinstance(map_entries, list):
        return

    regex_indicators = r'[\^$|()\[\]\\]'

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()  # Die ganze Datei als ein String
    except Exception as e:
        print(f'2026-0301-1511 {e}')
        return

    file_changed = False

    for i, entry in enumerate(map_entries):
        if not isinstance(entry, (tuple, list)) or len(entry) < 2:
            continue

        item1 = str(entry[0])  # Sollte ID sein
        item2 = str(entry[1])  # Sollte Regex sein

        # HEURISTICS: Field 1 looks like regex, field 2 doesn't.
        if bool(re.search(regex_indicators, item1)) and not bool(re.search(regex_indicators, item2)):

            # We look for the place in the text where both occur (in the immediate vicinity)
            # We are looking for the pattern: ( 'item1' , 'item2' or ( r'item1' , 'item2'
            # Since the ID is often short ('id'), we look for the combination.

            # We try a "smart swap" in the text
            if item1 in content and item2 in content:
                # We are looking for the positions
                pos1 = content.find(item1)
                pos2 = content.find(item2)

                # If item1 is BEFORE item2, it is swapped (since item1 is the regex)
                if pos1 != -1 and pos2 != -1 and pos1 < pos2:
                    # Check whether they are close to each other (max 200 characters apart for multi-line)
                    if (pos2 - pos1) < 200:
                        logger.warning(f"🛠️  Auto-Repair: Vertauschung in {os.path.basename(file_path)} gefunden!")

                        # In-Memory Tausch
                        new_entry = list(entry)
                        new_entry[0], new_entry[1] = entry[1], entry[0]
                        map_entries[i] = tuple(new_entry)

                        # In-File Tausch
                        # We use a placeholder that certainly does not appear in the file
                        placeholder = "###_AURA_SWAP_###"
                        content = content.replace(item1, placeholder).replace(item2, item1).replace(placeholder, item2)
                        file_changed = True
                else:
                    logger.debug(f"Health-Check: {item1} bereits hinter {item2} oder nicht gefunden.")

    if file_changed:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"✅ DATEI REPARIERT: …{str(file_path)[-30:]}")
        except Exception as e:
            logger.error(f"❌ Fehler beim Schreiben: {e}")



# def check_map_health_online_repairing(file_path, module, logger):
#     """
#     Prüft frische Maps und tauscht Feld 1 und Feld 2 direkt in der Datei,
# if they were obviously swapped.
#     """
#     try:
# Only check files less than 1 hour old
#         if (time.time() - os.path.getmtime(file_path)) > 3600:
#             return
#     except Exception as e:
#         print(f'2026-0301-1511 {e}')
#         return
#
# We are looking for your lists (FUZZY_MAP_pre, etc.)
#     map_entries = None
#     for name in ['FUZZY_MAP_pre', 'FUZZY_MAP_post', 'GLOBAL_FUZZY_MAP_PRE']:
#         if hasattr(module, name):
#             map_entries = getattr(module, name)
#             break
#
#     if not map_entries or not isinstance(map_entries, list):
#         return
#
#     regex_indicators = r'[\^$|()\[\]\\]'
#     file_needs_rewrite = False
#
#     try:
#         with open(file_path, 'r', encoding='utf-8') as f:
#             file_lines = f.readlines()
#     except Exception as e:
#         print(f'2026-0301-1511 {e}')
#         return
#
#     for i, entry in enumerate(map_entries):
#         if not isinstance(entry, (tuple, list)) or len(entry) < 2:
#             continue
#
#         # Feld 1 (normalerweise die ID/Name)
#         item1 = str(entry[0])
#         # Feld 2 (normalerweise das Regex-Pattern)
#         item2 = str(entry[1])
#
# If field 1 has regex characters but field 2 is "clean" -> SWAPED
#         if bool(re.search(regex_indicators, item1)) and not bool(re.search(regex_indicators, item2)):
#             logger.warning(f"🛠️  Auto-Repair: Tausche ID und Pattern in {os.path.basename(file_path)}...")
#
#             # 1. Im Arbeitsspeicher tauschen
#             new_entry = list(entry)
#             new_entry[0], new_entry[1] = entry[1], entry[0]
#             map_entries[i] = tuple(new_entry)
#
#             # 2. Direkt in der Datei tauschen
#             for idx, line in enumerate(file_lines):
# We are looking for the line that contains both values
#                 if item1 in line and item2 in line:
#                     # Sicherer Tausch in der Textzeile
#                     placeholder = "##_TEMP_SWAP_##"
#                     new_line = line.replace(item1, placeholder).replace(item2, item1).replace(placeholder, item2)
#
#                     if new_line != line:
#                         file_lines[idx] = new_line
#                         file_needs_rewrite = True
#                         break
#
#     if file_needs_rewrite:
#         with open(file_path, 'w', encoding='utf-8') as f:
#             f.writelines(file_lines)
# logger.info(f"✅ File was automatically corrected: {file_path}")



# def validate_map_structure(map_data, file_path, logger):
#     """
#     Prüft die Integrität der Mapping-Tupel.
#     Erwartet: (ID, Regex, Priority, Settings)
#     """
#     for i, entry in enumerate(map_data):
#         if not isinstance(entry, (tuple, list)) or len(entry) < 4:
#             logger.warning(f"⚠️ [Struktur-Fehler] {file_path} Zeile {i}: Ungültiges Format. Erwarte Tupel mit 4 Elementen.")
#             continue
#
#         rule_id, pattern, priority, settings = entry[:4]
#
#         # HEURISTIK: Erkennt Vertauschung von ID und Regex
# If the ID contains special characters but the regex looks like a simple name
#         regex_indicators = r'[\^$|()\[\]\\]'
#
#         id_looks_like_regex = bool(re.search(regex_indicators, str(rule_id)))
#         pattern_looks_like_id = not bool(re.search(regex_indicators, str(pattern)))
#
#         if id_looks_like_regex and pattern_looks_like_id:
#             logger.error(f"❌ [VERTAUSCHUNGS-ALARM] {file_path}:")
#             logger.error(f"   In Eintrag {i} scheint die ID '{rule_id}' ein Regex-Pattern zu sein.")
# logger.error(" Check whether ID and regex pattern were swapped!")
#             return False
#
#         # TYP-CHECK: Priority sollte eine Zahl sein
#         if not isinstance(priority, (int, float)):
#             logger.warning(f"⚠️ [Typ-Fehler] {file_path}: Priority '{priority}' in Eintrag {i} ist keine Zahl.")
#
#     return True

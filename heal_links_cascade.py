import os
import re
import glob

# --- KONFIGURATION ---
DRY_RUN = True  # Auf False setzen, um Änderungen wirklich anzuwenden
DRY_RUN = False  # Auf False setzen, um Änderungen wirklich anzuwenden
# ---------------------

def extract_basename(filename):
    """Extrahiert den Basisnamen vor dem Sprachkürzel (z.B. 'README' aus 'README-frlang.md')"""
    # Erkennt Muster wie -delang.md, -frlang.md, -pt-BRlang.md
    match = re.split(r'-[a-z]{2,3}(-[A-Z]{2,3})?lang\.md', filename)
    return match[0] if match else None

def heal_markdown_links():
    all_md_files = glob.glob("**/*.md", recursive=True)
    link_pattern = re.compile(r'(\[!?.*?\])\((.*?)\)')

    print(f"--- Link-Heiler Kaskade: {'DEMO' if DRY_RUN else 'LIVE'} ---")
    total_fixed = 0

    for file_path in all_md_files:
        current_dir = os.path.dirname(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = content
        file_has_changes = False
        matches = list(link_pattern.finditer(content))

        # Von hinten nach vorne ersetzen, damit Indizes stimmen
        for match in reversed(matches):
            full_match = match.group(0)
            prefix = match.group(1)
            url = match.group(2)

            # Ignoriere Externe, Anker, Absolute
            if url.startswith(('http', '#', 'mailto:', '/')):
                continue

            # Komponenten extrahieren
            url_no_anchor = url.split('#')[0]
            anchor = f"#{url.split('#')[1]}" if '#' in url else ""
            if not url_no_anchor: continue

            target_dir = os.path.dirname(url_no_anchor)
            target_filename = os.path.basename(url_no_anchor)
            basename = extract_basename(target_filename)

            # --- DIE KASKADE ---

            # 0. Original prüfen
            path0 = os.path.normpath(os.path.join(current_dir, url_no_anchor))
            if os.path.exists(path0):
                continue

            # 1. Heilungsschritt: Direkt im Unterordner .i18n suchen
            # Pfad/basename.i18n/filename
            if basename:
                path1_rel = os.path.join(target_dir, f"{basename}.i18n", target_filename)
                path1_abs = os.path.normpath(os.path.join(current_dir, path1_rel))
                if os.path.exists(path1_abs):
                    final_url = path1_rel + anchor
                    print(f"[FIX 1] In {file_path}: {url} -> {final_url}")
                    file_has_changes = True
                    total_fixed += 1
                    start, end = match.span()
                    new_content = new_content[:start] + f"{prefix}({final_url})" + new_content[end:]
                    continue

                # 2. Heilungsschritt: Eine Ebene höher und dann in .i18n
                # ../Pfad/basename.i18n/filename
                path2_rel = os.path.join("..", target_dir, f"{basename}.i18n", target_filename)
                # Normpath macht aus ".././" einfach "../"
                path2_rel = os.path.normpath(path2_rel)
                path2_abs = os.path.normpath(os.path.join(current_dir, path2_rel))
                if os.path.exists(path2_abs):
                    final_url = path2_rel + anchor
                    print(f"[FIX 2] In {file_path}: {url} -> {final_url}")
                    file_has_changes = True
                    total_fixed += 1
                    start, end = match.span()
                    new_content = new_content[:start] + f"{prefix}({final_url})" + new_content[end:]
                    continue

        if file_has_changes and not DRY_RUN:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

    print(f"\nFertig. {total_fixed} Links {'würden geheilt werden' if DRY_RUN else 'geheilt'}.")

if __name__ == "__main__":
    heal_markdown_links()


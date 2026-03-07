# peter.py
# Version: 0.6.7
# Ein KI-Agent der Koans liest, FUZZY_MAP-Regeln versteht und neue vorschlägt.
# Basiert auf radio_deep_dive.py von sl5net/SL5-aura-service
#
# Aufruf:
#   python peter.py                  → verarbeitet einen zufälligen Koan
#   python peter.py --koan 01        → verarbeitet Koan 01
#   python peter.py --list           → listet alle verfügbaren Koans auf
#   python peter.py --dry-run        → schlägt Regeln vor, schreibt aber nichts

import re
import json
import time
import random
import shutil
import sqlite3
import datetime
import argparse
import urllib.request
from pathlib import Path
import logging

# --- LOGGING ---
LOG_PATH = Path(__file__).parents[2] / "log" / "ai" / "peter.log"
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler()  # auch auf Konsole
    ]
)
log = logging.getLogger("peter")

# --- KONFIGURATION ---
VERSION = "0.6.7"
def load_model_from_config():
    """Liest Modellname aus config/internal/ai_model.txt, fallback: llama3.2:latest"""
    for candidate in [
        Path(__file__).parents[2] / "config" / "internal" / "ai_model.txt",
    ]:
        if candidate.exists():
            model = candidate.read_text(encoding="utf-8").strip().splitlines()[0].strip()
            if model:
                log.debug(f"Modell aus {candidate}: {model}")
                return model
    return "llama3.2:latest"

MODEL_NAME = load_model_from_config()
OLLAMA_API_URL = "http://localhost:11434/api/generate"

SCRIPT_DIR = Path(__file__).parent
DB_PATH = REPO_ROOT / "data" / "peter_cache.db"
# tools/ai/peter.py -> 2 Ebenen hoch = Repo-Root
REPO_ROOT = Path(__file__).parents[2]
KOANS_ROOT = REPO_ROOT / "config" / "maps"
README_AI_PATH = REPO_ROOT / "README_AI.md"
LANGUAGE = "de-DE"


# --- DATENBANK ---
def init_db():
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS peter_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            koan_path TEXT,
            suggested_rule TEXT,
            mode TEXT,
            accepted INTEGER DEFAULT 0,
            created_at TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_session(koan_path, suggested_rule, mode, accepted):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO peter_sessions (koan_path, suggested_rule, mode, accepted, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (str(koan_path), suggested_rule, mode, 1 if accepted else 0, now))
    conn.commit()
    conn.close()


# --- OLLAMA ---
def call_ollama(prompt, system_prompt="Du bist Peter, ein hilfreicher KI-Agent der Python Regex-Regeln fuer ein Spracherkennungssystem schreibt."):
    log.debug(f"call_ollama: model={MODEL_NAME}, prompt_len={len(prompt)}")
    payload = {"model": MODEL_NAME, "prompt": prompt, "system": system_prompt, "stream": False}
    try:
        req = urllib.request.Request(
            OLLAMA_API_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=120) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get("response", "").strip()
    except Exception as e:
        print(f"  !! Ollama Fehler: {e}")
        return None


# --- KOAN FINDER ---
def find_all_koans():
    koans = []
    for lang_dir in ["koans_2_peter_deutsch", "koans_deutsch", "koans_english"]:
        koan_base = KOANS_ROOT / lang_dir
        if not koan_base.exists():
            continue
        for koan_dir in sorted(koan_base.iterdir()):
            if koan_dir.is_dir() and not koan_dir.name.startswith("_"):
                if (koan_dir / LANGUAGE / "FUZZY_MAP.py").exists() or \
                   (koan_dir / LANGUAGE / "FUZZY_MAP_pre.py").exists():
                    koans.append(koan_dir)
    return koans


def find_koan_by_number(number):
    for k in find_all_koans():
        if k.name.startswith(str(number).zfill(2)):
            return k
    return None


def read_koan_files(koan_dir):
    files = {}
    lang_dir = koan_dir / LANGUAGE
    if not lang_dir.exists():
        return files
    for fname in ["FUZZY_MAP.py", "FUZZY_MAP_pre.py", "__init__.py"]:
        fpath = lang_dir / fname
        if fpath.exists():
            try:
                files[fname] = fpath.read_text(encoding="utf-8")
            except Exception:
                pass
    parent_init = koan_dir / "__init__.py"
    if parent_init.exists():
        try:
            files["parent_init.py"] = parent_init.read_text(encoding="utf-8")
        except Exception:
            pass
    return files


def read_readme_ai():
    if README_AI_PATH.exists():
        try:
            return README_AI_PATH.read_text(encoding="utf-8")
        except Exception:
            pass
    return ""


# --- BACKUP ---
def backup_file(filepath):
    backup_path = str(filepath) + ".peter_backup"
    shutil.copy2(filepath, backup_path)
    print(f"  Backup erstellt: {backup_path}")
    return backup_path


# --- PYTHON-FIRST: Auskommentierte Regel finden ---
def find_commented_rule(files):
    """
    Sucht nach echten auskommentierten Regeln wie:
        # ('hi koan', r'^.*$'),
    Ignoriert Beispiel-Zeilen im Header (enthalten Platzhalter wie 'Ersetzung' oder 'regex_pattern').
    """
    pattern = re.compile(r"^\s*#\s*(\(['\"].*?['\"]\s*,\s*[fFrRbB]*['\"].*?['\"].*?\))\s*,?\s*$")
    PLACEHOLDERS = {"ersetzung", "replacement", "regex_pattern", "irgendwas", "irgendein_pattern"}
    for fname, content in files.items():
        for line in content.splitlines():
            m = pattern.match(line)
            if m:
                activated = m.group(1).strip()
                # Platzhalter-Zeilen überspringen
                first_str = re.search(r"['\"](.+?)['\"]", activated)
                if first_str and first_str.group(1).lower() in PLACEHOLDERS:
                    continue
                return (fname, line, activated)
    return None


# --- REGEL AKTIVIEREN ---
def activate_commented_rule(filepath, original_line):
    """Entfernt das fuehrende '# ' von einer auskommentierten Regelzeile.
    Prueft dass die Zeile innerhalb einer MAP-Liste liegt."""
    file_content = filepath.read_text(encoding="utf-8")
    if original_line not in file_content:
        print(f"  !! Zeile nicht gefunden in {filepath}")
        return False
    # Sicherheitscheck: Zeile muss zwischen [ und ] einer MAP-Variable liegen
    in_list = False
    for line in file_content.splitlines():
        if re.search(r'FUZZY_MAP.*=\s*\[', line):
            in_list = True
        if in_list and original_line.strip() in line:
            break
        if in_list and line.strip() == ']':            in_list = False
    if not in_list:
        print(f"  !! Zeile liegt nicht innerhalb einer MAP-Liste - abgebrochen.")
        return False
    new_line = re.sub(r'^(\s*)#\s*', r'\1', original_line, count=1)
    if not new_line.rstrip().endswith(','):
        new_line = new_line.rstrip() + ','
    new_content = file_content.replace(original_line, new_line, 1)
    filepath.write_text(new_content, encoding="utf-8")
    print(f"  Regel aktiviert in: {filepath}")
    return True


# --- NEUE REGEL SCHREIBEN ---
def write_rule_to_file(filepath, rule_line, map_var_name):
    content = filepath.read_text(encoding="utf-8")
    pattern = rf"({map_var_name}\s*=\s*\[)(.*?)(\])"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        print(f"  !! {map_var_name} Liste nicht gefunden in {filepath}")
        return False
    new_content = content[:match.start(2)] + match.group(2).rstrip() + f"\n    {rule_line},\n" + content[match.end(2):]
    filepath.write_text(new_content, encoding="utf-8")
    print(f"  Neue Regel geschrieben in: {filepath}")
    return True


# --- TEST HINWEIS ---
def explain_rule(rule_str):
    """Erklaert was eine aktivierte Regel macht und schlaegt sinnvollen Test vor."""
    # Pattern extrahieren
    pattern_match = re.search(r",\s*r['\"](.+?)['\"]", rule_str)
    replacement_match = re.search(r"^\(['\"](.+?)['\"]", rule_str)
    pattern = pattern_match.group(1) if pattern_match else ""
    replacement = replacement_match.group(1) if replacement_match else "?"

    print(f"\n  Regel erklaert:")
    print(f"    Ergebnis:  {replacement}")
    print(f"    Pattern:   {pattern}")

    # Spezielle Pattern erkennen und erklaeren
    if pattern in ("^.*$", ".*", "^.+$"):
        print(f"    Bedeutung: Fullmatch - trifft auf ALLES zu!")
        print(f"    Achtung:   Pipeline stoppt danach immer.")
        print(f"    Hinweis:   Fruehere Regeln in der Pipeline haben Vorrang!")
        print(f"               Teste mit verschiedenen Woertern um das zu sehen.")
        test = "hallo"
    elif pattern.startswith("^") and pattern.endswith("$"):
        print(f"    Bedeutung: Fullmatch - trifft nur auf exakten Text zu.")
        # Extrahiere lesbaren Teil aus dem Pattern
        test = re.sub(r"[\^$.*+?()\[\]{{}}|]", "", pattern)[:20].strip() or "testtext"
    elif "\\b" in pattern or r"\b" in pattern:
        print(f"    Bedeutung: Wortgrenze - trifft auf das Wort im Satz zu.")
        test = re.sub(r"[\^$.*+?()\[\]{{}}|\\b]", "", pattern)[:20].strip() or replacement
    else:
        print(f"    Bedeutung: Regex-Muster")
        test = re.sub(r"[\^$.*+?()\[\]{{}}|]", "", pattern)[:20].strip() or replacement

    show_test_hint(test)


def show_test_hint(test_input):
    # Sonderzeichen, Klammern und verbose Phrasen entfernen
    text = test_input.strip()
    for ch in ['"', "'", "„", "“", "”", "«", "»", "(", ")", "[", "]"]:
        text = text.replace(ch, "")
    import re as _re
    text = _re.sub(r"(?i)^\s*(sagen sie|say|zum beispiel|for example)[:\s]*", "", text).strip()
    print(f"\n  Zum Testen (sprechen/eingeben): {text}")
    print(f"  Konsole:                        s {text}\n")


# --- GITHUB URL ---
GITHUB_BASE = "https://github.com/sl5net/SL5-aura-service/blob/master"

def get_github_url(file_path):
    """Erstellt den passenden GitHub-Link aus dem lokalen Pfad."""
    rel_path = ""
    if "STT/" in str(file_path):
        rel_path = str(file_path).split("STT/")[1]
    elif "SL5-aura-service/" in str(file_path):
        rel_path = str(file_path).split("SL5-aura-service/")[1]
    if rel_path:
        url = f"{GITHUB_BASE}/{rel_path}"
        log.debug(f"get_github_url: {file_path} -> {url}")
        return url
    log.warning(f"get_github_url: kein STT/ oder SL5-aura-service/ in Pfad: {file_path}")
    return None


# --- MD DOKUMENT SUCHE ---
MD_SEARCH_DIRS = ["docs", "doc_sources", "config/maps/plugins"]
MD_EXCLUDE = [".venv", ".env", "__pycache__", "i18n", "node_modules", "LanguageTool"]

# Deutsche -> Englische Keyword-Aliases fuer besseres MD-Matching
KEYWORD_ALIASES = {
    "erste":     ["first", "getting", "start"],
    "schritte":  ["steps", "started", "guide"],
    "listen":    ["list", "lists"],
    "namen":     ["names", "difficult"],
    "schwierige":["difficult", "hard"],
    "suche":     ["search", "wiki"],
    "helfer":        ["helper", "tools"],
    "oma":           ["autofix", "auto", "fix", "quick"],
    "modus":         ["autofix", "auto", "fix", "mode"],
    "mathematiker":  ["mathematician", "math", "names", "fuzzy", "autofix"],
    "mathematik":    ["math", "mathematician", "autofix"],
}

def extract_keywords(koan_name):
    """Extrahiert suchbare Keywords aus dem Koan-Namen inkl. englischer Aliases."""
    parts = koan_name.lower().split("_")
    stop = {"koan", "de", "en", "deutsch", "english", "01","02","03","04","05","06","07","08","09","10"}
    keywords = [p for p in parts if p not in stop and len(p) > 2]
    # Englische Aliases hinzufuegen
    aliases = []
    for kw in keywords:
        aliases.extend(KEYWORD_ALIASES.get(kw, []))
    return keywords + aliases


def collect_all_md_files():
    """Sammelt alle relevanten MD-Dateien aus den Suchverzeichnissen."""
    result = []
    for search_dir in MD_SEARCH_DIRS:
        base = REPO_ROOT / search_dir
        if not base.exists():
            continue
        for md_file in base.rglob("*.md"):
            if any(ex in str(md_file) for ex in MD_EXCLUDE):
                continue
            name_lower = md_file.name.lower()
            if any(lang in name_lower for lang in ["arlang", "eslang", "frlang", "hilang",
                                                    "jalang", "kolang", "pllang", "ptlang",
                                                    "zh-cn", "pt-br"]):
                continue
            result.append(md_file)
    return result


def fzf_select_md(all_files):
    """Oeffnet fzf zur manuellen Auswahl. Gibt Path oder None zurueck."""
    import subprocess
    try:
        file_list = "\n".join(str(f.relative_to(REPO_ROOT)) for f in all_files)
        result = subprocess.run(
            ["fzf", "--prompt=Dokument waehlen (ESC=kein Dokument): ",
             "--height=40%", "--layout=reverse"],
            input=file_list, capture_output=True, text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            chosen = REPO_ROOT / result.stdout.strip()
            log.info(f"fzf: Nutzer hat gewaehlt: {chosen}")
            return chosen
        log.debug("fzf: Nutzer hat abgebrochen (ESC)")
        return None
    except FileNotFoundError:
        log.warning("fzf nicht installiert - kein manuelles Auswaehlen moeglich")
        return None


def find_relevant_md(koan_dir):
    """
    Sucht nach passenden MD-Dokumenten fuer einen Koan.
    Strategie 1: Keywords aus Koan-Name gegen Dateinamen matchen.
    Strategie 2: Falls kein Treffer -> fzf zur manuellen Auswahl.
    Gibt (lokaler_pfad, github_url) zurueck oder (None, None).
    """
    keywords = extract_keywords(koan_dir.name)
    log.debug(f"find_relevant_md: keywords={keywords}")
    all_files = collect_all_md_files()
    candidates = []

    for md_file in all_files:
        name_lower = md_file.name.lower()
        score = sum(1 for kw in keywords if kw in name_lower)
        if score > 0:
            candidates.append((score, md_file))

    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        best = candidates[0][1]
        log.debug(f"find_relevant_md: bestes Match = {best.name} (score={candidates[0][0]})")
        log.debug(f"find_relevant_md: Top-5 = {[(s, p.name) for s,p in candidates[:5]]}")
        return best, get_github_url(best)

    # Kein automatischer Treffer -> fzf automatisch oeffnen
    log.debug(f"find_relevant_md: keine Treffer fuer keywords={keywords} -> fzf")
    print(f"  Kein automatischer Treffer – fzf oeffnet zur Auswahl...")
    chosen = fzf_select_md(all_files)
    if chosen:
        return chosen, get_github_url(chosen)
    return None, None


# === HAUPT-LOGIK ===
def process_koan(koan_dir, dry_run=False):
    start_time = time.time()
    print(f"\n{'='*60}")
    print(f"PETER analysiert Koan: {koan_dir.name}")
    print(f"{'='*60}\n")

    files = read_koan_files(koan_dir)
    if not files:
        print(f"  !! Keine Map-Dateien gefunden in {koan_dir}")
        return

    # ─────────────────────────────────────────────────────────
    # FALL 1: Python-first – auskommentierte Regel vorhanden?
    # Kein Ollama, kein Warten – direkt aktivieren.
    # ─────────────────────────────────────────────────────────
    found = find_commented_rule(files)

    if found:
        fname, original_line, activated_rule = found
        elapsed = time.time() - start_time
        print(f"Gefunden in {fname}:")
        print(f"  vorher:  {original_line.strip()}")
        print(f"  nachher: {activated_rule}")
        print(f"  ⏱ {elapsed:.1f}s\n")

        # Passendes MD-Dokument suchen und im Browser oeffnen
        md_path, md_github_url = find_relevant_md(koan_dir)
        if md_path and md_path.exists():
            import webbrowser
            log.debug(f"Browser open: md_path={md_path}, exists={md_path.exists()}")
            log.debug(f"Browser open: md_github_url={md_github_url}")
            url = md_github_url if md_github_url else md_path.as_uri()
            log.info(f"Oeffne Browser: {url}")
            print(f"  Dokument: {md_path.name}")
            print(f"  Browser:  {url}")
            webbrowser.open(url)
            print()
        else:
            log.debug(f"Browser: kein passendes Dokument gefunden (md_path={md_path})")

        if dry_run:
            print("  DRY-RUN: Nichts geaendert.")
            save_session(koan_dir, activated_rule, "python-activate", False)
            return

        answer = input("Kommentar entfernen und Regel aktivieren? [j/n]: ").strip().lower()
        if answer == 'j':
            map_file = koan_dir / LANGUAGE / ("FUZZY_MAP.py" if fname == "FUZZY_MAP.py" else "FUZZY_MAP_pre.py")
            if map_file.exists():
                backup_file(map_file)
                if activate_commented_rule(map_file, original_line):
                    save_session(koan_dir, activated_rule, "python-activate", True)
                    elapsed = time.time() - start_time
                    print(f"\nFertig!  ⏱ {elapsed:.1f}s")
                    explain_rule(activated_rule)
            else:
                print(f"  !! {map_file} nicht gefunden.")
        else:
            save_session(koan_dir, activated_rule, "python-activate", False)
            print(f"  Uebersprungen.  ⏱ {time.time() - start_time:.1f}s")
        return

    # ─────────────────────────────────────────────────────────
    # FALL 2: Keine TODO-Regel – Ollama + README_AI kreativ
    # ─────────────────────────────────────────────────────────
    print("Keine auskommentierte Regel gefunden – Peter wird kreativ...\n")

    # Passendes MD-Dokument suchen
    md_path, md_github_url = find_relevant_md(koan_dir)

    # ── OMA-MODUS: leere Datei + AutoFix-Dokument ──────────────────
    # Kein Ollama noetig. Peter schreibt ein Beispielwort direkt rein.
    # Der Auto-Fix macht daraus automatisch ('wort', 'wort'),
    map_is_empty = not any(
        re.search(r"\(['\"]", line)
        for c in files.values()
        for line in c.splitlines()
        if not line.strip().startswith("#")
    )
    if map_is_empty and md_path and "AutoFix" in md_path.name:
        keywords = extract_keywords(koan_dir.name)
        example_word = keywords[0] if keywords else "beispiel"
        elapsed = time.time() - start_time
        print(f"  Oma-Modus erkannt!")
        print(f"  Beispielwort: {example_word}")
        print(f"  Auto-Fix macht daraus: ('{example_word}', '{example_word}'),")
        print(f"  Danach kannst du die Ersetzung manuell anpassen.")
        print(f"  Zum Testen:  s {example_word}  ⏱ {elapsed:.1f}s\n")
        if dry_run:
            print("  DRY-RUN: Nichts geaendert.")
            save_session(koan_dir, example_word, "oma-modus", False)
            return
        answer = input(f"Beispielwort '{example_word}' in Datei schreiben? [j/n]: ").strip().lower()
        if answer == 'j':
            map_file = koan_dir / LANGUAGE / "FUZZY_MAP_pre.py"
            if map_file.exists():
                backup_file(map_file)
                file_content = map_file.read_text(encoding="utf-8")
                map_file.write_text(file_content.rstrip() + f"\n{example_word}\n", encoding="utf-8")
                save_session(koan_dir, example_word, "oma-modus", True)
                print(f"  Geschrieben! Auto-Fix wird beim naechsten Laden aktiv.")
            else:
                print(f"  !! {map_file} nicht gefunden.")
        else:
            save_session(koan_dir, example_word, "oma-modus", False)
        return
    # ── Ende Oma-Modus ─────────────────────────────────────────────
    md_context = ""
    if md_path:
        import webbrowser
        log.debug(f"Kreativ-Fall Browser: md_path={md_path}, github={md_github_url}")
        url = md_github_url if md_github_url else md_path.as_uri()
        log.info(f"Oeffne Browser: {url}")
        print(f"  Passendes Dokument gefunden: {md_path.name}")
        print(f"  Browser: {url}")
        webbrowser.open(url)
    else:
        log.debug("Kreativ-Fall: kein passendes MD-Dokument gefunden")
        try:
            md_context = md_path.read_text(encoding="utf-8")[:3000]
        except Exception:
            pass
        print()

    readme = read_readme_ai()
    context = "".join(f"\n--- {fn} ---\n{c}\n" for fn, c in files.items())

    # FuzzyMapRuleGuide immer als Basis-Kontext laden
    rule_guide = ""
    guide_path = REPO_ROOT / "docs" / "FuzzyMapRuleGuide.md"
    if guide_path.exists():
        try:
            rule_guide = guide_path.read_text(encoding="utf-8")[:2000]
            log.debug(f"FuzzyMapRuleGuide geladen: {len(rule_guide)} Zeichen")
        except Exception:
            pass

    # Pruefen ob die Map-Datei wirklich leer ist (nur Header, keine Regel)
    map_is_empty = not any(
        re.search(r"\(['\"]", line)
        for c in files.values()
        for line in c.splitlines()
        if not line.strip().startswith("#")
    )

    # Spezial-Hinweis fuer leere Dateien mit Auto-Fix Kontext
    empty_hint = ""
    if map_is_empty and md_path and "AutoFix" in md_path.name:
        empty_hint = """
SPEZIALFALL - LEERE DATEI im Auto-Fix Modus (Oma-Modus):
Die Datei ist leer. Das System kann einfache Woerter automatisch in Regeln umwandeln.

Deine Aufgabe: Schreibe NUR 1-3 einfache deutsche Woerter (keine Syntax, keine Klammern!).
Beispiel:
    oma
    opa
    berlin

Das System wandelt das automatisch um in:
    ('oma', 'oma'),
    ('opa', 'opa'),
    ('berlin', 'berlin'),

WICHTIG:
- Nur einzelne Woerter (keine Zahlen, keine Sonderzeichen, keine Kommas)
- Kein Python-Syntax noetig
- Der Benutzer aendert danach die Ersetzung manuell

Antworte NUR so:
REGEL: wort1
GRUND: (1 Satz warum dieses Wort sinnvoll ist)
TEST: wort1
"""

    rule_prompt = f"""Du bist Peter, ein KI-Agent fuer das SL5 Aura Spracherkennungssystem.

SYSTEM-DOKUMENTATION:
{readme}

REGEL-FORMAT (immer einhalten!):
{rule_guide}

ZUSATZ-KONTEXT ({md_path.name if md_path else "kein Dokument gefunden"}):
{md_context}

KOAN-DATEIEN:
{context}
{empty_hint}
Die FUZZY_MAP ist leer. Schlage GENAU EINE einfache sinnvolle Regel vor.
Fuer leere Dateien: schreibe ein einfaches Wortpaar ohne Regex.
Fuer normale Dateien: schreibe eine Regex-Regel die zum Thema passt.

Antworte NUR in diesem Format:
REGEL: ('Ersetzung', 'wort') ODER ('Ersetzung', r'pattern', 0, {{'flags': re.IGNORECASE}})
GRUND: (1 Satz)
TEST: (ein einfaches Wort ohne Sonderzeichen)
"""

    suggestion = call_ollama(rule_prompt)
    elapsed = time.time() - start_time

    if not suggestion:
        print(f"  !! Ollama nicht erreichbar.  ⏱ {elapsed:.1f}s")
        return

    print(f"PETER schlaegt vor:\n{suggestion}\n")

    rule_line = None
    test_input = None
    for line in suggestion.split('\n'):
        clean_line = re.sub(r'\*+', '', line).strip()
        if re.match(r'^REGEL:', clean_line) and rule_line is None:
            raw = re.sub(r'^REGEL:', '', clean_line).strip()
            raw = raw.split(' ODER')[0].strip()
            rule_line = raw
        if re.match(r'^TEST:', clean_line) and test_input is None:
            raw_test = re.sub(r'^TEST:', '', clean_line).strip()
            raw_test = re.sub(r'["\'\u201e\u201c]', '', raw_test).strip()
            raw_test = raw_test.split(' ODER')[0].strip()
            test_input = raw_test

    # Oma-Modus: wenn rule_line ein einfaches Wort ist (kein Tupel), direkt schreiben
    if rule_line and not rule_line.startswith("(") and re.match(r'^[a-zA-Z_À-ž]+$', rule_line.strip()):
        log.info(f"Oma-Modus erkannt: bare word '{rule_line}' -> wird direkt geschrieben")

    if not rule_line:
        print(f"  !! Kein REGEL: Format erkannt – oben manuell pruefen.  ⏱ {elapsed:.1f}s")
        return

    print(f"Extrahierte Regel: {rule_line}  ⏱ {elapsed:.1f}s\n")
    if test_input:
        show_test_hint(test_input)

    if dry_run:
        print("  DRY-RUN: Nichts geaendert.")
        save_session(koan_dir, rule_line, "ollama-creative", False)
        return

    answer = input("Regel in FUZZY_MAP_pre.py schreiben? [j/n]: ").strip().lower()
    if answer == 'j':
        map_file = koan_dir / LANGUAGE / "FUZZY_MAP_pre.py"
        if map_file.exists():
            backup_file(map_file)
            # Oma-Modus: bare word direkt schreiben, Auto-Fix macht den Rest
            if rule_line and not rule_line.startswith("(") and re.match(r'^[a-zA-Z_À-ž]+$', rule_line.strip()):
                log.info(f"Oma-Modus: schreibe bare word '{rule_line}'")
                file_content = map_file.read_text(encoding="utf-8")
                map_file.write_text(file_content.rstrip() + f"\n{rule_line}\n", encoding="utf-8")
                print(f"  Wort geschrieben: {rule_line}")
            else:
                write_rule_to_file(map_file, rule_line, "FUZZY_MAP_pre")
            save_session(koan_dir, rule_line, "ollama-creative", True)
            print(f"\nFertig!  ⏱ {time.time() - start_time:.1f}s")
        else:
            print(f"  !! {map_file} nicht gefunden.")
    else:
        save_session(koan_dir, rule_line, "ollama-creative", False)
        print(f"  Uebersprungen.  ⏱ {time.time() - start_time:.1f}s")


# --- ENTRY POINT ---
def main():
    global MODEL_NAME
    parser = argparse.ArgumentParser(description=f"Peter v{VERSION} - KI-Agent fuer SL5 Aura Koans")
    parser.add_argument('--koan', type=str, help='Koan-Nummer z.B. 01, 02, ...')
    parser.add_argument('--list', action='store_true', help='Alle Koans auflisten')
    parser.add_argument('--dry-run', action='store_true', help='Nur vorschlagen, nichts schreiben')
    parser.add_argument('--model', type=str, default=MODEL_NAME, help=f'Ollama-Modell (default: {MODEL_NAME})')
    args = parser.parse_args()

    MODEL_NAME = args.model
    init_db()

    print(f"\nPeter v{VERSION} - KI-Agent fuer SL5 Aura")
    print(f"   Modell: {MODEL_NAME}")
    print(f"   Repo:   {REPO_ROOT}")
    print(f"   Koans:  {KOANS_ROOT}\n")

    if args.list:
        koans = find_all_koans()
        print(f"Gefundene Koans ({len(koans)}):")
        for k in koans:
            print(f"  * {k.relative_to(KOANS_ROOT)}")
        return

    if args.koan:
        koan_dir = find_koan_by_number(args.koan)
        if not koan_dir:
            print(f"  !! Koan '{args.koan}' nicht gefunden. --list zeigt alle.")
            return
    else:
        koans = find_all_koans()
        if not koans:
            print(f"  !! Keine Koans gefunden unter {KOANS_ROOT}")
            return
        koan_dir = random.choice(koans)
        print(f"  Zufaelliger Koan (--koan N fuer spezifischen)")

    process_koan(koan_dir, dry_run=args.dry_run)


if __name__ == "__main__":
    main()

"""
todo:


Das --exclude filtert Pakete nach Sprachcode im base_name. Das muss 1:1 in download_release_hybrid.py rein:

bashsed -n '230,260p' tools/download_all_packages.py

danach in meinem Setup (z.B. setup/manjaro_arch_setup.sh ) einfach

    download_all_packages.py

    mit ersetzen?

    download_release_hybrid.py

Also im Script statt
    ./.venv/bin/python tools/download_all_packages.py --exclude "$EXCLUDE_LANGUAGES"
    ./.venv/bin/python tools/download_release_hybrid.py --exclude "$EXCLUDE_LANGUAGES"
?


Da deine Datenbank ein bisschen alt ist benutze lieber Linux Kommandos(arch comatible und ich befinde mich immer im Projekt-Ordner)

Und beachten, dass .gitignore filtert alle ungültigen Namen weg (z.B. mit Leerzeichen usw)  aber im offline Repository sind vorhanden, aber natürlich nicht online. Vielleicht erstmal das .gitignore lesen , damit du weißt was du in Wirklichkeit siehst.

und ganz wichtig: niemals direkt Kommentare in die Konsole Command schreiben, wie z.b. `# Zeigt alle git-sichtbaren Dateien (tracked + untracked, aber nicht ignored)`
weil das gibt immer Fehler erzeugt.

Und auch die tausenden von sprachlichen Übersetzungen ( xxxxx .i18n ) automatisch ausschließen:

Beispiel:

... scripts/py/func/checks/README.i18n/README-pt-BRlang.md scripts/py/func/checks/README.i18n/README-ptlang.md scripts/py/func/checks/README.i18n/README-zh-CNlang.md ...

Die ganzen .i18n Ordner müllen sonst deinen speicher ganz schnell voll. brauche wir nicht.


Sehr wichtige technisches Detail/Anmerkung zu den Umlauten: das ist nur bei der Übertragung von den Daten über die Zwischenablage, nur wenn wenn ich dir dir Daten hier in den Chat sende. Kein Aura Problem

Im Source immer Englisch (auch in den Kommentaren dort), hier im Chat bitte immer Deutsch, Falls du etwas erklären oder besprechen willst mit mir, besser in Deutsch.



download_release_hybrid.py

Downloads GitHub release assets for sl5net/SL5-aura-service.
Priority: BitTorrent (via libtorrent) -> HTTP part-download fallback.

- Torrent mode:   if a .torrent asset exists in the release, libtorrent is used.
                  Web-Seeds embedded in the torrent allow HTTP fallback inside libtorrent.
- HTTP fallback:  calls tools/download_all_packages.py when libtorrent is absent
                  OR when the torrent transfer fails.
- i18n pruning:   *.i18n directories are excluded automatically.
- No inline shell comments after commands (would break subprocess calls).
"""

import os
import sys
import hashlib
import subprocess
import requests
import argparse
import time
from collections import defaultdict

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

try:
    import libtorrent as lt
    LIBTORRENT_AVAILABLE = True
except ImportError:
    LIBTORRENT_AVAILABLE = False
    print("--> Info: 'libtorrent' not found. Hybrid-Torrent disabled. Using HTTP fallback.")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
OWNER   = "sl5net"
REPO    = "SL5-aura-service"
TAG     = "v0.2.0"
API_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/tags/{TAG}"

HTTP_FALLBACK_SCRIPT = os.path.join(
    os.path.dirname(__file__), "tools", "download_all_packages.py"
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def calculate_sha256(filepath: str) -> str:
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            sha256.update(block)
    return sha256.hexdigest()


def _progress_write(desc: str, done: int, total: int) -> None:
    """Simple progress line without tqdm."""
    pct = (done / total * 100) if total else 0
    mb_done  = done  / 1_048_576
    mb_total = total / 1_048_576
    print(f"\r  {desc}: {mb_done:.1f}/{mb_total:.1f} MB  ({pct:.0f}%)", end="", flush=True)


def download_file_http(url: str, filepath: str) -> None:
    """HTTP download with optional tqdm progress bar."""
    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()
    total = int(response.headers.get("content-length", 0))
    chunk = 1024 * 1024

    if TQDM_AVAILABLE:
        with open(filepath, "wb") as f, tqdm(
            desc=os.path.basename(filepath),
            total=total, unit="iB", unit_scale=True
        ) as bar:
            for data in response.iter_content(chunk_size=chunk):
                f.write(data)
                bar.update(len(data))
    else:
        with open(filepath, "wb") as f:
            done = 0
            for data in response.iter_content(chunk_size=chunk):
                f.write(data)
                done += len(data)
                _progress_write(os.path.basename(filepath), done, total)
        print()


def parse_checksum_file(filepath: str) -> dict:
    """Return {filename: sha256hex} from a sha256sums.txt file."""
    hashes: dict = {}
    if not os.path.exists(filepath):
        return hashes
    with open(filepath, "r") as f:
        for line in f:
            parts = line.strip().split(None, 1)
            if len(parts) == 2:
                hashes[parts[1].strip()] = parts[0].strip()
    return hashes

# ---------------------------------------------------------------------------
# Torrent download
# ---------------------------------------------------------------------------

def download_via_torrent(torrent_url: str, save_path: str) -> bool:
    """
    Download via BitTorrent using libtorrent.
    Returns True on success, False on any error.
    """
    if not LIBTORRENT_AVAILABLE:
        return False

    print(f"\n--- Starting Hybrid-Torrent download ---")
    r = requests.get(torrent_url, timeout=30)
    if r.status_code != 200:
        print(f"  Could not fetch .torrent file (HTTP {r.status_code})")
        return False

    try:
        ses  = lt.session({"listen_interfaces": "0.0.0.0:6881"})
        info = lt.torrent_info(lt.bdecode(r.content))
        h    = ses.add_torrent({"ti": info, "save_path": save_path})
        print(f"  Searching peers / web-seeds for: {info.name()}")

        total = info.total_size()
        if TQDM_AVAILABLE:
            pbar = tqdm(total=total, unit="B", unit_scale=True, desc=info.name())
        last_done = 0

        while not h.status().is_seeding:
            s        = h.status()
            new_done = s.total_done

            if TQDM_AVAILABLE:
                pbar.update(new_done - last_done)
                pbar.set_postfix({"Peers": s.num_peers, "Seeds": s.num_seeds})
            else:
                _progress_write(info.name(), new_done, total)

            last_done = new_done
            time.sleep(1)

        if TQDM_AVAILABLE:
            pbar.close()
        print(f"\n  [OK] Torrent finished: {info.name()}")
        return True

    except Exception as exc:
        print(f"  Torrent error: {exc}")
        return False

# ---------------------------------------------------------------------------
# HTTP fallback dispatcher
# ---------------------------------------------------------------------------

def run_http_fallback(exclude_list: list) -> None:
    """Call the existing HTTP download script as subprocess."""
    if not os.path.exists(HTTP_FALLBACK_SCRIPT):
        print(f"  Fallback script not found: {HTTP_FALLBACK_SCRIPT}")
        print("  Please run tools/download_all_packages.py manually.")
        return
    print(f"\n--- Running HTTP fallback: {HTTP_FALLBACK_SCRIPT} ---")
    cmd = [sys.executable, HTTP_FALLBACK_SCRIPT]
    if exclude_list:
        cmd += ["--exclude"] + exclude_list
    subprocess.run(cmd, check=False)

# ---------------------------------------------------------------------------
# Package processing
# ---------------------------------------------------------------------------

def process_package(base_name: str, package_files: dict, all_assets: list) -> bool:
    """
    For one logical package (base_name):
      1. Try torrent if available.
      2. Fall back to HTTP part-download + merge + verify.
    """
    print("=" * 60)
    print(f"Package: {base_name}")
    print("=" * 60)

    torrent_asset = next(
        (a for a in all_assets if a["name"] == f"{base_name}.torrent"), None
    )

    if LIBTORRENT_AVAILABLE and torrent_asset:
        print(f"  .torrent found for {base_name}")
        if download_via_torrent(torrent_asset["browser_download_url"], "."):
            return True
        print("  Torrent failed — switching to HTTP parts.")

    # --- HTTP part download ---
    checksum_asset = package_files.get("checksum_asset")
    if not checksum_asset:
        print(f"  ERROR: No checksum asset for {base_name}")
        return False

    checksum_filename = checksum_asset["name"]
    download_file_http(checksum_asset["browser_download_url"], checksum_filename)
    official_hashes = parse_checksum_file(checksum_filename)

    final_filename = next(
        (k for k in official_hashes if ".part." not in k), base_name
    )
    final_hash = official_hashes.get(final_filename)

    if os.path.exists(final_filename) and calculate_sha256(final_filename) == final_hash:
        print(f"  [SKIP] {final_filename} already present and verified.")
        os.remove(checksum_filename)
        return True

    part_assets = sorted(
        package_files.get("part_assets", []), key=lambda x: x["name"]
    )
    downloaded_parts = []

    for asset in part_assets:
        p_name = asset["name"]
        print(f"  Downloading part: {p_name}")
        download_file_http(asset["browser_download_url"], p_name)
        if calculate_sha256(p_name) == official_hashes.get(p_name):
            downloaded_parts.append(p_name)
        else:
            print(f"  CRITICAL: {p_name} is corrupt! Aborting package.")
            return False

    print(f"  Merging {len(downloaded_parts)} parts -> {final_filename} ...")
    with open(final_filename, "wb") as out:
        for p in downloaded_parts:
            with open(p, "rb") as inp:
                out.write(inp.read())
            os.remove(p)

    if calculate_sha256(final_filename) == final_hash:
        print(f"  [OK] {final_filename} complete.")
        os.remove(checksum_filename)
        return True

    print(f"  ERROR: Final hash mismatch for {final_filename}")
    return False

# ---------------------------------------------------------------------------
# Asset discovery  (excludes .i18n paths)
# ---------------------------------------------------------------------------

def is_i18n_asset(name: str) -> bool:
    return ".i18n" in name


def discover_packages(assets: list) -> dict:
    """
    Group assets into logical packages keyed by base_name.
    Skips .i18n assets automatically.
    Returns:
      { base_name: { 'checksum_asset': asset|None,
                     'part_assets':    [asset, ...] } }
    """
    packages: dict = defaultdict(lambda: {"checksum_asset": None, "part_assets": []})

    for asset in assets:
        name = asset["name"]

        if is_i18n_asset(name):
            continue

        if name.endswith(".sha256sums.txt"):
            bn = name.removesuffix(".sha256sums.txt")
            packages[bn]["checksum_asset"] = asset

        elif ".part." in name:
            bn = name.split(".part.")[0]
            bn = bn.lstrip("zZ_")
            packages[bn]["part_assets"].append(asset)

    return packages

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Hybrid BitTorrent/HTTP downloader for sl5net/SL5-aura-service releases."
    )
    p.add_argument("--exclude", type=str, nargs='*', default=[],
                        help="List of language codes to exclude, e.g. --exclude de en")

    p.add_argument("--tag",   default=TAG,   help="GitHub release tag (default: %(default)s)")
    p.add_argument("--owner", default=OWNER, help="GitHub owner (default: %(default)s)")
    p.add_argument("--repo",  default=REPO,  help="GitHub repo  (default: %(default)s)")
    p.add_argument(
        "--list", action="store_true",
        help="Only list discovered packages, do not download."
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    api_url = f"https://api.github.com/repos/{args.owner}/{args.repo}/releases/tags/{args.tag}"
    print(f"Fetching release info: {args.owner}/{args.repo} @ {args.tag}")



    exclude_list = [x.strip().lower() for x in args.exclude]  # args.exclude is already a list

    # Detect GitHub Actions environment
    is_ci = os.getenv('GITHUB_ACTIONS') == 'true'
    # Define models that should be skipped in CI to save time/bandwidth
    large_models = ['vosk-model-de-0.21', 'vosk-model-en-us-0.22']


    # If in CI, add these to the exclusion list automatically
    if is_ci:
        print("--> GitHub Actions detected. Auto-excluding large models to stabilize build.")
        # Logic to append to your existing exclusion list
        # Assuming your current exclusion list is called 'exclude'
        for model in large_models:
            if model not in exclude_list:
                exclude_list.append(model)
    print(f"============================================")
    print(f"============================================")
    print(f"============================================")
    print(f"--- DEBUG: Parsed exclusion list from arguments: {exclude_list}")
    print(f"============================================")
    # sys.exit(1) # Beenden, um die geparste Liste zu sehen
    # ----------------------------------------------------










    try:
        release_info = requests.get(api_url, timeout=15).json()
    except Exception as exc:
        print(f"ERROR fetching release: {exc}")
        sys.exit(1)

    assets = release_info.get("assets", [])
    if not assets:
        print("No assets found in this release.")
        sys.exit(0)

    packages = discover_packages(assets)

    if args.list:
        print(f"\nDiscovered packages ({len(packages)}):")
        for bn, files in packages.items():
            n_parts = len(files["part_assets"])
            has_chk = files["checksum_asset"] is not None
            has_tor = any(a["name"] == f"{bn}.torrent" for a in assets)
            print(f"  {bn:50s}  parts={n_parts}  checksum={has_chk}  torrent={has_tor}")
        return



# --- Integration Step 3: Apply exclusion filter (1:1 from original) ---
    packages_to_process = {}

    if exclude_list and exclude_list != ['']:
        print(f"Applying exclusion filter: {', '.join(exclude_list)}")

    # Im Hybrid-Script heißt das Dictionary 'packages' statt 'valid_packages'
    for base_name, files in packages.items():
        is_mandatory = base_name.startswith("LanguageTool") or base_name.startswith("lid.")
        is_excluded = False

        if 'all' in exclude_list and not is_mandatory:
            is_excluded = True
        elif 'all' not in exclude_list:
            if 'de' in exclude_list and '-de-' in base_name:
                is_excluded = True
            if 'en' in exclude_list and ('-en-' in base_name or 'en-us' in base_name):
                is_excluded = True

        if is_excluded:
            print(f"    -> Exclusion applied: Skipping {base_name}")
        else:
            packages_to_process[base_name] = files




    any_torrent_used = False
    all_ok = True

    for bn, files in packages_to_process.items():
        has_torrent = any(a["name"] == f"{bn}.torrent" for a in assets)
        if has_torrent:
            any_torrent_used = True
        ok = process_package(bn, files, assets)
        if not ok:
            all_ok = False
            print(f"  FAILED: {bn} — trying global HTTP fallback.")
            run_http_fallback(exclude_list)
            break

    if not any_torrent_used and not LIBTORRENT_AVAILABLE:
        print("\nNote: install 'libtorrent' (python-libtorrent) to enable BitTorrent mode.")

    if all_ok:
        print("\n[DONE] All packages OK.")
    else:
        print("\n[DONE] Some packages failed. Check output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()

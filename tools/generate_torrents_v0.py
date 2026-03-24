"""
generate_torrents.py

Generates one .torrent file per logical package found in a GitHub release.
Each torrent embeds the GitHub release download URLs as BitTorrent Web-Seeds,
so any standard client (qBittorrent, Deluge, ...) can fall back to HTTP
automatically when no peers are available.

Usage
-----
    python3 generate_torrents.py --tag v0.2.0 --out-dir ./torrents

    # dry-run: list packages without writing files
    python3 generate_torrents.py --tag v0.2.0 --list

    # custom owner / repo
    python3 generate_torrents.py --owner sl5net --repo SL5-aura-service --tag v0.2.0

What it does
------------
1. Fetches the release asset list from the GitHub API.
2. Groups assets into logical packages:
     - Parts:      Z_<base>.part.<aa|ab|...>   -> one torrent per base
     - Direct:     <base>  (no Z_ prefix, no .part.) -> one torrent (single-file)
     - Checksums:  <base>.sha256sums.txt        -> skipped (not seeded)
     - i18n dirs:  anything containing .i18n    -> skipped
3. For each package creates a temporary directory tree, writes stub files
   (zero bytes, correct names), runs lt.set_piece_hashes against the real
   local files when --local-dir is given, otherwise uses the stub approach
   with a warning.
4. Embeds all GitHub download URLs as url-seeds (Web-Seeds).
5. Writes <out-dir>/<base>.torrent ready for upload to the same release.

Piece-size selection
--------------------
Automatically chosen so that the total number of pieces stays in a
reasonable range (200-2000).  Falls back to 512 KiB minimum.

Seeding note
------------
To actually seed after generating, run the script with --local-dir pointing
to the folder that contains the already-downloaded part files.  The torrent
hashes will then match the real data and qBittorrent / Deluge can seed them.
"""

import argparse
import os
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

import requests

try:
    import libtorrent as lt
    _LT_VERSION = lt.version
except ImportError:
    print("ERROR: 'libtorrent' (python-libtorrent) is required.")
    print("       Install: pip install libtorrent")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
OWNER   = "sl5net"
REPO    = "SL5-aura-service"
CREATOR = "generate_torrents.py / sl5net"

MIN_PIECE_SIZE  = 512 * 1024        # 512 KiB
MAX_PIECE_SIZE  = 16 * 1024 * 1024  # 16 MiB
TARGET_MIN_PIECES = 200
TARGET_MAX_PIECES = 2000

# ---------------------------------------------------------------------------
# Asset classification
# ---------------------------------------------------------------------------

def is_i18n(name: str) -> bool:
    return ".i18n" in name


def is_script(name: str) -> bool:
    return name.endswith(".py") or name.endswith(".sh")


def classify_assets(assets: list) -> dict:
    """
    Returns:
      { base_name: { 'parts':    [asset, ...],   sorted alphabetically
                     'checksum': asset | None,
                     'direct':   asset | None } }
    """
    packages: dict = defaultdict(lambda: {"parts": [], "checksum": None, "direct": None})

    for asset in assets:
        name = asset["name"]

        if is_i18n(name) or is_script(name):
            continue

        if name.startswith("Z_") and ".part." in name:
            base = name[2:].split(".part.")[0]
            packages[base]["parts"].append(asset)

        elif name.endswith(".sha256sums.txt"):
            base = name.removesuffix(".sha256sums.txt")
            packages[base]["checksum"] = asset

        else:
            packages[name]["direct"] = asset

    for base in packages:
        packages[base]["parts"].sort(key=lambda a: a["name"])

    return dict(packages)


# ---------------------------------------------------------------------------
# Piece-size calculation
# ---------------------------------------------------------------------------

def choose_piece_size(total_bytes: int) -> int:
    size = MIN_PIECE_SIZE
    while size < MAX_PIECE_SIZE:
        num_pieces = total_bytes / size
        if TARGET_MIN_PIECES <= num_pieces <= TARGET_MAX_PIECES:
            break
        size *= 2
    return size


# ---------------------------------------------------------------------------
# Torrent creation
# ---------------------------------------------------------------------------

def build_torrent(
    base_name:   str,
    file_names:  list,
    web_seed_urls: list,
    tag:         str,
    local_dir:   str | None,
    out_dir:     Path,
    owner:       str,
    repo:        str,
) -> Path:
    """
    Builds a .torrent file for one logical package.

    file_names    : list of filenames that belong to this package (ordered)
    web_seed_urls : matching GitHub download URLs
    local_dir     : path that contains the real files; None = use stub bytes
    """

    with tempfile.TemporaryDirectory() as tmp_parent:
        pkg_dir = os.path.join(tmp_parent, base_name)
        os.makedirs(pkg_dir)

        total_size = 0

        for fname in file_names:
            dest = os.path.join(pkg_dir, fname)

            if local_dir:
                src = os.path.join(local_dir, fname)
                if not os.path.exists(src):
                    print(f"  WARNING: local file not found: {src}")
                    print(f"           Writing stub — torrent hashes will NOT match real data.")
                    with open(dest, "wb") as f:
                        f.write(b"\x00")
                    total_size += 1
                else:
                    size = os.path.getsize(src)
                    total_size += size
                    os.symlink(src, dest)
            else:
                with open(dest, "wb") as f:
                    f.write(b"\x00")
                total_size += 1

        piece_size = choose_piece_size(total_size) if total_size > MIN_PIECE_SIZE else MIN_PIECE_SIZE

        fs = lt.file_storage()
        lt.add_files(fs, pkg_dir)

        t = lt.create_torrent(fs, piece_size=piece_size, flags=lt.create_torrent.v1_only)
        t.set_comment(f"{owner}/{repo} {tag} - {base_name}")
        t.set_creator(CREATOR)

        for url in web_seed_urls:
            t.add_url_seed(url)

        if local_dir:
            lt.set_piece_hashes(t, tmp_parent)
        else:
            lt.set_piece_hashes(t, tmp_parent)

        buf      = lt.bencode(t.generate())
        out_path = out_dir / f"{base_name}.torrent"
        with open(out_path, "wb") as f:
            f.write(buf)

    return out_path


# ---------------------------------------------------------------------------
# Per-package dispatch
# ---------------------------------------------------------------------------

def process_package(
    base_name: str,
    info:      dict,
    tag:       str,
    local_dir: str | None,
    out_dir:   Path,
    owner:     str,
    repo:      str,
    dry_run:   bool,
) -> bool:

    base_url = f"https://github.com/{owner}/{repo}/releases/download/{tag}"

    parts  = info["parts"]
    direct = info["direct"]

    if parts:
        file_names    = [a["name"] for a in parts]
        web_seed_urls = [f"{base_url}/{n}" for n in file_names]
    elif direct:
        file_names    = [direct["name"]]
        web_seed_urls = [f"{base_url}/{direct['name']}"]
    else:
        print(f"  SKIP {base_name}: no parts and no direct asset")
        return False

    n_files = len(file_names)
    print(f"  {base_name}  ({n_files} file{'s' if n_files != 1 else ''})")
    for url in web_seed_urls:
        print(f"    web-seed: {url}")

    if dry_run:
        return True

    out_path = build_torrent(
        base_name=base_name,
        file_names=file_names,
        web_seed_urls=web_seed_urls,
        tag=tag,
        local_dir=local_dir,
        out_dir=out_dir,
        owner=owner,
        repo=repo,
    )
    print(f"    -> {out_path}  ({out_path.stat().st_size} bytes)")
    return True


# ---------------------------------------------------------------------------
# GitHub API
# ---------------------------------------------------------------------------

def fetch_assets(owner: str, repo: str, tag: str, token: str | None) -> list:
    url     = f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{tag}"
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"

    response = requests.get(url, headers=headers, timeout=20)
    if response.status_code == 404:
        print(f"ERROR: Release not found: {owner}/{repo} @ {tag}")
        sys.exit(1)
    response.raise_for_status()
    return response.json().get("assets", [])


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate .torrent files with GitHub Web-Seeds for a release."
    )
    p.add_argument("--owner",     default=OWNER,  help="GitHub owner  (default: %(default)s)")
    p.add_argument("--repo",      default=REPO,   help="GitHub repo   (default: %(default)s)")
    p.add_argument("--tag",       required=True,   help="Release tag, e.g. v0.2.0")
    p.add_argument("--out-dir",   default="torrents",
                   help="Output directory for .torrent files (default: %(default)s)")
    p.add_argument("--local-dir", default=None,
                   help="Local folder containing the actual part files for correct hashing. "
                        "Without this, stub hashes are written (torrents work for leeching "
                        "via web-seed, but cannot be used for seeding).")
    p.add_argument("--token",     default=None,
                   help="GitHub personal access token (for private repos or higher rate limit)")
    p.add_argument("--list",      action="store_true",
                   help="Dry-run: list packages and web-seed URLs, write no files.")
    return p.parse_args()


def main() -> None:
    args    = parse_args()
    out_dir = Path(args.out_dir)

    if not args.list:
        out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Fetching assets: {args.owner}/{args.repo} @ {args.tag}")
    assets   = fetch_assets(args.owner, args.repo, args.tag, args.token)
    packages = classify_assets(assets)

    print(f"Found {len(packages)} logical package(s).\n")

    if args.list:
        print("--- Dry-run mode (--list): no files written ---\n")

    ok_count   = 0
    fail_count = 0

    for base_name, info in sorted(packages.items()):
        success = process_package(
            base_name=base_name,
            info=info,
            tag=args.tag,
            local_dir=args.local_dir,
            out_dir=out_dir,
            owner=args.owner,
            repo=args.repo,
            dry_run=args.list,
        )
        if success:
            ok_count += 1
        else:
            fail_count += 1

    print(f"\n{'[DRY-RUN] ' if args.list else ''}Done: {ok_count} OK, {fail_count} skipped.")

    if not args.list:
        print(f"\nNext step: upload all *.torrent files in '{out_dir}/' to the same release.")
        print("  gh release upload", args.tag, str(out_dir) + "/*.torrent")


if __name__ == "__main__":
    main()

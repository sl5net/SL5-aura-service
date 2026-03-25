"""
generate_torrents.py

Generates one .torrent file per logical package found in a GitHub release.
Each torrent embeds Web-Seeds (BEP-19) so any BitTorrent client can fall
back to HTTP when no peers are available.

Dependencies: Python standard library + requests.  No libtorrent required.

Usage
-----
    # Standard: web-seeds point to GitHub
    python3 generate_torrents.py --tag v0.2.0 --local-dir ~/aura_all_packages

    # Local seeding mode: web-seeds point to your home server
    python3 generate_torrents.py --tag v0.2.0 --local-dir ~/aura_all_packages \
        --web-seed-base-url http://192.168.1.10:8832

    # Dry-run
    python3 generate_torrents.py --tag v0.2.0 --list

    # Upload torrents to GitHub release
    gh release upload v0.2.0 torrents/*.torrent --clobber

What --web-seed-base-url does
-----------------------------
Without it:  web-seeds = https://github.com/.../releases/download/<tag>/<file>
With it:     web-seeds = <your-url>/<file>
             Also writes tools/local_seed_manifest.json with the same URLs.
             Commit + push that file so download_release_hybrid.py can find
             your local server automatically.
"""

import argparse
import hashlib
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
OWNER   = "sl5net"
REPO    = "SL5-aura-service"
CREATOR = "generate_torrents.py / sl5net"

MIN_PIECE_SIZE    = 512  * 1024
MAX_PIECE_SIZE    = 16   * 1024 * 1024
TARGET_MIN_PIECES = 200
TARGET_MAX_PIECES = 2000

MANIFEST_PATH = Path(__file__).parent / "local_seed_manifest.json"

# ---------------------------------------------------------------------------
# Bencoding  (BEP-3)
# ---------------------------------------------------------------------------

def bencode(obj) -> bytes:
    if isinstance(obj, int):
        return b"i" + str(obj).encode() + b"e"
    if isinstance(obj, bytes):
        return str(len(obj)).encode() + b":" + obj
    if isinstance(obj, str):
        enc = obj.encode("utf-8")
        return str(len(enc)).encode() + b":" + enc
    if isinstance(obj, list):
        return b"l" + b"".join(bencode(i) for i in obj) + b"e"
    if isinstance(obj, dict):
        body = b""
        for k in sorted(obj.keys()):
            raw_k = k if isinstance(k, bytes) else k.encode("utf-8")
            body += str(len(raw_k)).encode() + b":" + raw_k
            body += bencode(obj[k])
        return b"d" + body + b"e"
    raise TypeError(f"bencode: unsupported type {type(obj)}")

# ---------------------------------------------------------------------------
# Piece hashing
# ---------------------------------------------------------------------------

def compute_pieces(file_paths: list, file_sizes: list, piece_size: int) -> bytes:
    sha1s = b""
    buf   = b""
    for fp, size in zip(file_paths, file_sizes):
        if fp and os.path.exists(fp):
            with open(fp, "rb") as fh:
                while True:
                    need  = piece_size - len(buf)
                    chunk = fh.read(need)
                    if not chunk:
                        break
                    buf += chunk
                    if len(buf) == piece_size:
                        sha1s += hashlib.sha1(buf).digest()
                        buf    = b""
        else:
            remaining = size
            while remaining > 0:
                need       = min(piece_size - len(buf), remaining)
                buf       += b"\x00" * need
                remaining -= need
                if len(buf) == piece_size:
                    sha1s += hashlib.sha1(buf).digest()
                    buf    = b""
    if buf:
        sha1s += hashlib.sha1(buf).digest()
    return sha1s

# ---------------------------------------------------------------------------
# Piece-size selection
# ---------------------------------------------------------------------------

def choose_piece_size(total_bytes: int) -> int:
    size = MIN_PIECE_SIZE
    while size < MAX_PIECE_SIZE:
        if TARGET_MIN_PIECES <= total_bytes / size <= TARGET_MAX_PIECES:
            break
        size *= 2
    return size

# ---------------------------------------------------------------------------
# Torrent building
# ---------------------------------------------------------------------------

def build_torrent(
    base_name:  str,
    file_names: list,
    file_paths: list,
    file_sizes: list,
    web_seeds:  list,
    tag:        str,
    owner:      str,
    repo:       str,
) -> bytes:
    total_size = sum(file_sizes) or 1
    piece_size = choose_piece_size(total_size) if total_size > MIN_PIECE_SIZE else MIN_PIECE_SIZE
    pieces     = compute_pieces(file_paths, file_sizes, piece_size)

    if len(file_names) == 1:
        info = {
            "name":         file_names[0],
            "piece length": piece_size,
            "pieces":       pieces,
            "length":       file_sizes[0] or 1,
        }
    else:
        info = {
            "name":         base_name,
            "piece length": piece_size,
            "pieces":       pieces,
            "files": [
                {"length": sz, "path": [name]}
                for name, sz in zip(file_names, file_sizes)
            ],
        }

    return bencode({
        "info":          info,
        "url-list":      web_seeds,
        "comment":       f"{owner}/{repo} {tag} - {base_name}",
        "created by":    CREATOR,
        "creation date": int(datetime.now(timezone.utc).timestamp()),
    })

# ---------------------------------------------------------------------------
# Asset classification
# ---------------------------------------------------------------------------

def is_i18n(name: str) -> bool:
    return ".i18n" in name

def is_script(name: str) -> bool:
    return name.endswith(".py") or name.endswith(".sh")

def classify_assets(assets: list) -> dict:
    packages: dict = defaultdict(
        lambda: {"parts": [], "checksum": None, "direct": None}
    )
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
# Manifest
# ---------------------------------------------------------------------------

def write_manifest(manifest: dict, tag: str) -> None:
    data = {
        "generated":  datetime.now(timezone.utc).isoformat(),
        "tag":        tag,
        "packages":   manifest,
    }
    with open(MANIFEST_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\n  manifest -> {MANIFEST_PATH}")
    print(f"  Commit + push this file so download_release_hybrid.py can find")
    print(f"  your local server automatically before the course.")

# ---------------------------------------------------------------------------
# Per-package processing
# ---------------------------------------------------------------------------

def process_package(
    base_name:        str,
    info:             dict,
    tag:              str,
    local_dir:        str | None,
    out_dir:          Path,
    owner:            str,
    repo:             str,
    dry_run:          bool,
    web_seed_base_url: str | None,
) -> tuple[bool, dict]:
    """Returns (success, manifest_entry)."""

    github_base = f"https://github.com/{owner}/{repo}/releases/download/{tag}"
    parts       = info["parts"]
    direct      = info["direct"]

    if parts:
        file_names   = [a["name"] for a in parts]
        github_seeds = [f"{github_base}/{n}" for n in file_names]
        api_sizes    = [a.get("size", 0) for a in parts]
    elif direct:
        file_names   = [direct["name"]]
        github_seeds = [f"{github_base}/{direct['name']}"]
        api_sizes    = [direct.get("size", 0)]
    else:
        print(f"  SKIP {base_name}: no parts and no direct asset")
        return False, {}

    if web_seed_base_url:
        base_url = web_seed_base_url.rstrip("/")
        web_seeds = [f"{base_url}/{n}" for n in file_names]
    else:
        web_seeds = github_seeds

    manifest_entry = {
        "files": file_names,
        "urls":  web_seeds,
    }

    n = len(file_names)
    print(f"  {base_name}  ({n} file{'s' if n != 1 else ''})")
    for url in web_seeds:
        print(f"    web-seed: {url}")

    if dry_run:
        return True, manifest_entry

    if local_dir:
        file_paths = [os.path.join(local_dir, name) for name in file_names]
        missing    = [p for p in file_paths if not os.path.exists(p)]
        file_sizes = [
            os.path.getsize(p) if os.path.exists(p) else sz
            for p, sz in zip(file_paths, api_sizes)
        ]
        if missing:
            print(f"    WARNING: {len(missing)} file(s) not found locally - stub hashes used.")
        else:
            print(f"    Hashing {sum(file_sizes) // (1024*1024)} MB from local files...")
    else:
        file_paths = [""] * n
        file_sizes = api_sizes
        total_mb   = sum(file_sizes) / (1024 * 1024)
        print(f"    Stub mode ({total_mb:.0f} MB from API) - seeding requires real files")

    buf = build_torrent(
        base_name=base_name,
        file_names=file_names,
        file_paths=file_paths,
        file_sizes=file_sizes,
        web_seeds=web_seeds,
        tag=tag,
        owner=owner,
        repo=repo,
    )

    out_path = out_dir / f"{base_name}.torrent"
    with open(out_path, "wb") as f:
        f.write(buf)

    total_size = sum(file_sizes)
    piece_size = choose_piece_size(total_size) if total_size > MIN_PIECE_SIZE else MIN_PIECE_SIZE
    n_pieces   = (total_size + piece_size - 1) // piece_size
    print(f"    -> {out_path.name}  ({len(buf)} bytes, {n_pieces} pieces x {piece_size//1024} KiB)")
    return True, manifest_entry

# ---------------------------------------------------------------------------
# GitHub API
# ---------------------------------------------------------------------------

def fetch_assets(owner: str, repo: str, tag: str, token: str | None) -> list:
    url     = f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{tag}"
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = requests.get(url, headers=headers, timeout=20)
    if r.status_code == 404:
        print(f"ERROR: Release not found: {owner}/{repo} @ {tag}")
        sys.exit(1)
    r.raise_for_status()
    return r.json().get("assets", [])

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate .torrent files with GitHub Web-Seeds. Requires only: pip install requests"
    )
    p.add_argument("--owner",     default=OWNER)
    p.add_argument("--repo",      default=REPO)
    p.add_argument("--tag",       required=True,      help="Release tag, e.g. v0.2.0")
    p.add_argument("--out-dir",   default="torrents")
    p.add_argument("--local-dir", default=None,
                   help="Local folder with real part files (correct hashes + seeding)")
    p.add_argument("--web-seed-base-url", default=None,
                   help=(
                       "Override web-seed base URL, e.g. http://192.168.1.10:8832 "
                       "or https://aura.sl5.de:8832. "
                       "Also writes tools/local_seed_manifest.json. "
                       "Without this flag, web-seeds point to GitHub."
                   ))
    p.add_argument("--token",     default=None,       help="GitHub token (raises API rate limit)")
    p.add_argument("--list",      action="store_true", help="Dry-run: list only, write nothing")
    return p.parse_args()


def main() -> None:
    args    = parse_args()
    out_dir = Path(args.out_dir)

    if not args.list:
        out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Fetching assets: {args.owner}/{args.repo} @ {args.tag}")
    assets   = fetch_assets(args.owner, args.repo, args.tag, args.token)
    packages = classify_assets(assets)
    print(f"Found {len(packages)} logical package(s).")

    if args.web_seed_base_url:
        print(f"Web-seed base URL: {args.web_seed_base_url}")
    print()

    if args.list:
        print("--- Dry-run (--list): no files written ---\n")

    ok = fail = 0
    manifest = {}

    for base_name, pkg_info in sorted(packages.items()):
        success, entry = process_package(
            base_name=base_name,
            info=pkg_info,
            tag=args.tag,
            local_dir=args.local_dir,
            out_dir=out_dir,
            owner=args.owner,
            repo=args.repo,
            dry_run=args.list,
            web_seed_base_url=args.web_seed_base_url,
        )
        if success:
            ok += 1
            manifest[base_name] = entry
        else:
            fail += 1

    label = "[DRY-RUN] " if args.list else ""
    print(f"\n{label}Done: {ok} OK, {fail} skipped.")

    if not args.list:
        if args.web_seed_base_url:
            write_manifest(manifest, args.tag)
            print(f"\nNext steps:")
            print(f"  1. git add tools/local_seed_manifest.json && git commit -m 'local seed manifest' && git push")
            print(f"  2. Start HTTP server: python3 -m http.server 8832 --directory {args.local_dir or '<local-dir>'}")
            print(f"  3. Upload torrents:   gh release upload {args.tag} {args.out_dir}/*.torrent --clobber")
        else:
            print(f"\nNext step - upload to release:")
            print(f"  gh release upload {args.tag} {args.out_dir}/*.torrent --clobber")


if __name__ == "__main__":
    main()

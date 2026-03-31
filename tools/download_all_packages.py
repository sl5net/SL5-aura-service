# tools/download_all_packages.py

"""
Empfehlung:
UmgebungEmpfehlungGitHub Actions4 — sicher, stabilLokaler Mac/Linux6-8 — schnell, noch übersichtlichSehr schnelle Leitung8 max — danach kaum Gewinn
"""

from os import remove
import requests
import hashlib
import os
import sys
from tqdm import tqdm
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

# --- Configuration ---
OWNER = "sl5net"
REPO = "SL5-aura-service"
TAG = "v0.2.0"
API_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/tags/{TAG}"

remove_parts = True

is_ci = os.getenv('GITHUB_ACTIONS') == 'true'
MAX_PARALLEL_DOWNLOADS = 4 if is_ci else 6 # Number of parallel part downloads per package

# --- Helper Functions ---

def download_file(url, filepath, do_overwrite=False):
    """
    Downloads a file with a progress bar, with an option to skip if it already exists.
    Uses a .tmp suffix during download to avoid leaving partial files behind.
    """
    if os.path.exists(filepath) and not do_overwrite:
        print(f"  [SKIP] '{os.path.basename(filepath)}' already exists.")
        return True
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        with open(filepath, 'wb') as f, tqdm(
            desc=os.path.basename(filepath), total=total_size, unit='iB',
            unit_scale=True, unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024 * 1024):
                size = f.write(data)
                bar.update(size)
    except requests.exceptions.RequestException as e:
        print(f"\n  [ERROR] Download failed for {url}: {e}")
        return False
    return True


def calculate_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256.update(byte_block)
    return sha256.hexdigest()


def parse_checksum_file(filepath):
    hashes = {}
    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split(None, 1)
            if len(parts) == 2:
                hash_val, filename = parts
                hashes[filename.strip()] = hash_val.strip()
    return hashes


def download_and_verify_part(asset, expected_hash, max_retries=3):
    """
    Downloads and verifies a single part file.
    Uses a .tmp suffix during download — only renames to final name after successful verification.
    This prevents other parallel processes from treating an incomplete download as done.
    """
    part_name = asset['name']
    tmp_name = part_name + ".tmp"

    # If the final file already exists and is correct, skip download entirely.
    if os.path.exists(part_name):
        actual_hash = calculate_sha256(part_name)
        if actual_hash == expected_hash:
            print(f"  [SKIP] '{part_name}' already verified. Skipping download.")
            return part_name
        else:
            print(f"  [WARN] '{part_name}' exists but hash mismatch. Re-downloading.")
            os.remove(part_name)

    for attempt in range(max_retries):
        if not download_file(asset['browser_download_url'], tmp_name, do_overwrite=True):
            print(f"  [RETRY] Download failed for '{part_name}' (attempt {attempt + 1}/{max_retries}).")
            continue

        actual_hash = calculate_sha256(tmp_name)
        if actual_hash == expected_hash:
            os.rename(tmp_name, part_name)  # Atomic: only visible as done after verification
            print(f"  [OK]  Verified: {part_name}")
            return part_name
        else:
            print(f"  [RETRY] Hash mismatch for '{part_name}' (attempt {attempt + 1}/{max_retries}). Retrying...")
            os.remove(tmp_name)

    raise RuntimeError(f"Failed to verify '{part_name}' after {max_retries} attempts.")


# --- Asset Discovery ---

def verbose_discovery(assets):
    """
    Discovers packages with detailed logging to help debug naming mismatches.
    Tolerant to 'z_' or 'Z_' prefix on part files.
    """
    print("\n--- Starting Detailed Asset Discovery ---")
    packages = defaultdict(lambda: {'checksum_asset': None, 'part_assets': []})

    print("\n[Step 1] Searching for package definition files (*.sha256sums.txt)...")
    checksum_assets = [a for a in assets if a['name'].endswith('.sha256sums.txt')]
    if not checksum_assets:
        print("  [WARN] No *.sha256sums.txt files found in release assets!")
    for asset in checksum_assets:
        base_name = asset['name'].replace('.sha256sums.txt', '')
        packages[base_name]['checksum_asset'] = asset
        print(f"  [OK]  Found definition for package: '{base_name}'")

    print("\n[Step 2] Searching for part files (*.part.aa, etc)...")
    part_assets = [a for a in assets if '.part.' in a['name']]
    if not part_assets:
        print("  [WARN] No part files (*.part.*) found in release assets!")
    for asset in part_assets:
        print(f"  - Found potential part file: {asset['name']}")

    print("\n[Step 3] Matching part files to packages (Tolerant to 'z_' and 'Z_')...")
    for asset in part_assets:
        matched = False
        for base_name in packages:
            asset_name_lower = asset['name'].lower()
            if f"_{base_name.lower()}.part." in asset_name_lower and \
               asset_name_lower.startswith('z_'):
                packages[base_name]['part_assets'].append(asset)
                print(f"  [OK]  Matched '{asset['name']}' -> package '{base_name}'")
                matched = True
                break
        if not matched:
            print(f"  [WARN] Could not match part file '{asset['name']}' to any known package.")

    print("--- Discovery Complete ---\n")
    return packages


# --- Exclusion Logic ---

def is_excluded(base_name, exclude_list):
    """
    Checks whether a package should be excluded.

    Accepts both full names and short codes in exclude_list:
      - Full name:  'vosk-model-de-0.21' in exclude_list -> True
      - Short code: 'de' in exclude_list, '-de-' in base_name -> True
      - 'all':      excludes all non-mandatory packages

    Mandatory packages (LanguageTool, lid.) are never excluded.
    """
    is_mandatory = base_name.startswith("LanguageTool") or base_name.startswith("lid.")

    if is_mandatory:
        return False

    # Full name or substring match
    if any(excl in base_name or base_name in excl for excl in exclude_list):
        return True

    # Exclude all non-mandatory
    if 'all' in exclude_list:
        return True

    return False


# --- Package Processing ---

def process_package(base_name, package_files, remove_parts):
    print("=" * 60)
    print(f"Processing Package: {base_name}")
    print("=" * 60)

    checksum_asset = package_files.get('checksum_asset')
    part_assets = package_files.get('part_assets', [])
    checksum_filename = checksum_asset['name']

    print(f"\n--- Step A: Downloading checksum file: {checksum_filename} ---")
    if not download_file(checksum_asset['browser_download_url'], checksum_filename):
        return False

    official_hashes = parse_checksum_file(checksum_filename)
    final_zip_entries = [k for k in official_hashes if '.part.' not in k]

    if len(final_zip_entries) != 1:
        print(f"  [ERROR] Found {len(final_zip_entries)} non-part entries in checksum file. Expected 1. Skipping.")
        return False

    final_merged_filename = final_zip_entries[0]
    final_zip_hash = official_hashes[final_merged_filename]
    print(f"  [OK]  Deduced final filename: '{final_merged_filename}'")

    # Pre-check: skip everything if final file already exists and is correct.
    if os.path.exists(final_merged_filename):
        print(f"\n--- Pre-Verification Check ---")
        local_hash = calculate_sha256(final_merged_filename)
        if local_hash == final_zip_hash:
            print(f"  [OK]  '{final_merged_filename}' already correct. Skipping.")
            return True
        else:
            print(f"  [WARN] Existing file hash mismatch. Will re-download.")

    # --- Step B: Parallel part downloads ---
    part_assets.sort(key=lambda x: x['name'])
    print(f"\n--- Step B: Downloading {len(part_assets)} part(s) "
          f"in parallel (max {MAX_PARALLEL_DOWNLOADS} workers) ---")

    downloaded_parts = []
    failed_parts = []

    with ThreadPoolExecutor(max_workers=MAX_PARALLEL_DOWNLOADS) as executor:
        futures = {}
        for asset in part_assets:
            expected_hash = official_hashes.get(asset['name'])
            if not expected_hash:
                print(f"  [WARN] No hash for '{asset['name']}' in checksum file. Skipping.")
                continue
            future = executor.submit(download_and_verify_part, asset, expected_hash)
            futures[future] = asset['name']

        for future in as_completed(futures):
            part_name = futures[future]
            try:
                result = future.result()
                downloaded_parts.append(result)
            except Exception as e:
                print(f"  [FAIL] '{part_name}': {e}")
                failed_parts.append(part_name)

    if failed_parts:
        print(f"\n  [FAIL] {len(failed_parts)} part(s) failed: {failed_parts}")
        return False

    # Sort parts to ensure correct merge order (aa, ab, ac, ...)
    downloaded_parts.sort()

    # --- Step C: Merge and verify ---
    print(f"\n--- Step C: Merging {len(downloaded_parts)} parts -> '{final_merged_filename}' ---")
    with open(final_merged_filename, 'wb') as f_out:
        for part_file in downloaded_parts:
            with open(part_file, 'rb') as f_in:
                f_out.write(f_in.read())

    final_actual_hash = calculate_sha256(final_merged_filename)
    print(f"  Expected : {final_zip_hash}")
    print(f"  Computed : {final_actual_hash}")

    if final_actual_hash == final_zip_hash:
        print(f"  [OK]  SUCCESS! Package '{final_merged_filename}' verified.")
        if remove_parts:
            for part in downloaded_parts:
                os.remove(part)
            os.remove(checksum_filename)
            print("  [OK]  Cleaned up intermediate files.")
        return True
    else:
        print(f"  [FAIL] CRITICAL: Merged file '{final_merged_filename}' is corrupt!")
        return False


# --- Main ---

def main():
    parser = argparse.ArgumentParser(description="Download and verify assets from a GitHub release.")
    parser.add_argument(
        "--exclude", type=str, nargs='*', default=[],
        help=(
            "Packages to exclude. Accepts full names or short codes. "
            "Examples: --exclude de en  OR  --exclude vosk-model-de-0.21 vosk-model-en-us-0.22"
        )
    )
    args = parser.parse_args()
    exclude_list = [x.strip().lower() for x in args.exclude if x.strip()]

    # Detect GitHub Actions and auto-exclude large models to save time/bandwidth
    is_ci = os.getenv('GITHUB_ACTIONS') == 'true'
    large_models = ['vosk-model-de-0.21', 'vosk-model-en-us-0.22']

    if is_ci:
        print("--> GitHub Actions detected. Auto-excluding large models to stabilize build.")
        for model in large_models:
            if model not in exclude_list:
                exclude_list.append(model)

    print(f"\n{'=' * 60}")
    print(f"  Repository         : {OWNER}/{REPO}")
    print(f"  Tag                : {TAG}")
    print(f"  Parallel downloads : {MAX_PARALLEL_DOWNLOADS}")
    print(f"  Exclusions         : {exclude_list if exclude_list else '(none)'}")
    print(f"{'=' * 60}\n")

    # Fetch release assets from GitHub API
    print(f"Fetching release assets for {OWNER}/{REPO} tag {TAG}...")
    try:
        headers = {}
        token = os.getenv('GITHUB_TOKEN')
        if token:
            headers['Authorization'] = f'Bearer {token}'
        else:
            print("  [WARN] No GITHUB_TOKEN found. Rate limit: 60/h (shared IP).")

        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()

        remaining = response.headers.get('X-RateLimit-Remaining', '?')
        print(f"  [INFO] GitHub API rate limit remaining: {remaining}")

        release_info = response.json()
        assets = release_info.get('assets', [])
        print(f"  [OK]  Found {len(assets)} asset(s) in release '{TAG}'.")

        if not assets:
            print("  [ERROR] Release has no assets. Nothing to download.")
            sys.exit(1)

    except requests.exceptions.RequestException as e:
        print(f"  [FATAL] Could not connect to GitHub API: {e}")
        sys.exit(1)

    packages = verbose_discovery(assets)
    valid_packages = {k: v for k, v in packages.items() if v['checksum_asset'] and v['part_assets']}

    if not valid_packages:
        print("=" * 60)
        print("CRITICAL ERROR: Could not find any complete, valid packages.")
        print("Hint: Release assets need both a *.sha256sums.txt AND *.part.* files.")
        print(f"Total assets on release: {len(assets)}")
        for a in assets:
            print(f"  - {a['name']}")
        print("=" * 60)
        sys.exit(1)

    print(f"Found {len(valid_packages)} valid package(s): {', '.join(valid_packages.keys())}")

    # Apply exclusion filter
    packages_to_process = {}
    for base_name, files in valid_packages.items():
        if is_excluded(base_name, exclude_list):
            print(f"  [SKIP] Excluded: {base_name}")
        else:
            packages_to_process[base_name] = files

    if not packages_to_process:
        print("\n  [INFO] All packages excluded. Nothing to download. Exiting successfully.")
        sys.exit(0)

    print(f"\nProcessing {len(packages_to_process)} package(s): {', '.join(packages_to_process.keys())}")

    all_successful = True
    for base_name, files in packages_to_process.items():
        if not process_package(base_name, files, remove_parts):
            all_successful = False

    print("\n" + "#" * 60)
    if all_successful:
        print("  All packages downloaded and verified successfully!")
    else:
        print("  ERROR: One or more packages failed.")
        sys.exit(1)
    print("#" * 60)


if __name__ == "__main__":
    main()

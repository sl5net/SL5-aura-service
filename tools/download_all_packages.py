# tools/download_all_packages.py
from os import remove

import requests
import hashlib
import os
import sys
from tqdm import tqdm
from collections import defaultdict

import argparse

# --- Configuration ---
OWNER = "sl5net"
REPO = "Vosk-System-Listener"
TAG = "v0.2.0"
API_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/tags/{TAG}"
# https://api.github.com/repos/sl5net/Vosk-System-Listener/releases/tags/v0.2.0
# https://api.github.com/repositories/1006604181/releases/tags/v0.2.0
remove_parts = True #  It can be useful for transporting too many parts.  or, if you want to store only a park somewhere

# --- Helper Functions (Unchanged) ---

def download_file(url, filepath, do_overwrite=False):
    """
    Downloads a file with a progress bar, with an option to skip if it already exists.
    """
    if os.path.exists(filepath) and not do_overwrite:
        print(f"File '{os.path.basename(filepath)}' already exists. Skipping download.")
        return True # Return True because the required file is present.

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        with open(filepath, 'wb') as f, tqdm(
            desc=os.path.basename(filepath), total=total_size, unit='iB',
            unit_scale=True, unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024*1024):
                size = f.write(data)
                bar.update(size)
    except requests.exceptions.RequestException as e:
        print(f"\nError downloading {url}: {e}")
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
            parts = line.strip().split(None, 1) # Split only once
            if len(parts) == 2:
                hash_val, filename = parts
                hashes[filename.strip()] = hash_val.strip()
    return hashes

# --- Final Corrected Discovery and Processing Logic ---

def verbose_discovery(assets):
    """
    Discovers packages with detailed logging to help debug naming mismatches.
    This version is tolerant and accepts 'z_' or 'Z_' as a prefix.
    """
    print("\n--- Starting Detailed Asset Discovery ---")
    packages = defaultdict(lambda: {'checksum_asset': None, 'part_assets': []})

    print("\n[Step 1] Searching for package definition files (*.sha256sums.txt)...")
    checksum_assets = [a for a in assets if a['name'].endswith('.sha256sums.txt')]
    for asset in checksum_assets:
        base_name = asset['name'].replace('.sha256sums.txt', '')
        packages[base_name]['checksum_asset'] = asset
        print(f"   [OK]  Found definition for package: '{base_name}'")

    print("\n[Step 2] Searching for part files (*.part.aa, etc)...")
    part_assets = [a for a in assets if '.part.' in a['name']]
    for asset in part_assets:
        print(f"  - Found potential part file: {asset['name']}")

    print("\n[Step 3] Matching part files to packages (Tolerant to 'z_' and 'Z_')...")
    for asset in part_assets:
        matched = False
        for base_name in packages:
            # --- THE TOLERANT FIX ---
            # We check if the filename, without its prefix, matches the expected pattern.
            asset_name_lower = asset['name'].lower()
            pattern_to_match = f"_{base_name}.part.".lower()

            # Check if the asset name starts with 'z_' or 'Z_' and then matches the rest
            if (asset_name_lower.startswith('z_') or asset_name_lower.startswith('Z_')) and \
               pattern_to_match in asset_name_lower:

                # Further check to ensure the pattern is correct
                # e.g., z_vosk-model-de-0.21.zip.part.aa
                # Check for: _vosk-model-de-0.21.zip.part.
                if f"_{base_name.lower()}.part." in asset_name_lower:
                    packages[base_name]['part_assets'].append(asset)
                    print(f"   [OK]  Matched '{asset['name']}' to package '{base_name}'")
                    matched = True
                    break
        if not matched:
            print(f"   [WARN]  Warning: Could not match part file '{asset['name']}' to any known package.")

    print("--- Discovery Complete ---\n")
    return packages

def process_package(base_name, package_files, remove_parts):
    print("="*60)
    print(f"Processing Package: {base_name}")
    print("="*60)
    checksum_asset = package_files.get('checksum_asset')
    part_assets = package_files.get('part_assets', [])
    checksum_filename = checksum_asset['name']

    print(f"\n--- Step A: Downloading and Analyzing Checksum File: {checksum_filename} ---")
    if not download_file(checksum_asset['browser_download_url'], checksum_filename):
        return False
    official_hashes = parse_checksum_file(checksum_filename)

    # DEDUCE the final filename by finding the one entry that is NOT a part.
    final_zip_entries = [k for k in official_hashes if '.part.' not in k]

    if len(final_zip_entries) != 1:
        print(f"Error: Found {len(final_zip_entries)} non-part entries in checksum file. Expected 1. Check manifest file on GitHub. Skipping.")
        return False

    final_merged_filename = final_zip_entries[0]
    final_zip_hash = official_hashes[final_merged_filename]
    print(f"   [OK]  Deduced final filename from manifest: '{final_merged_filename}'")


    # Pre-check: If the final merged file already exists and is correct, skip everything.
    if os.path.exists(final_merged_filename):
        print(f"\n--- Pre-Verification Check ---")
        print(f"File '{final_merged_filename}' already exists. Calculating its hash...")
        local_hash = calculate_sha256(final_merged_filename)
        if local_hash == final_zip_hash:
            print(f"  Official Hash: {final_zip_hash}")
            print(f"  Computed Hash: {local_hash}")
            print(f"\n[<3] PRE-VERIFIED! Final file '{final_merged_filename}' is already correct. Skipping.")
            return True # This is the crucial part: exit successfully.
        else:
            print(f"  [WARN] Existing file is corrupt. Deleting it and proceeding with download.")

            # os.remove(final_merged_filename)











    print(f"\n--- Step B: Downloading and Verifying {len(part_assets)} Parts ---")
    downloaded_parts = []
    part_assets.sort(key=lambda x: x['name'])
    for asset in part_assets:
        part_name = asset['name']
        expected_hash = official_hashes.get(part_name)
        if not expected_hash:
            print(f"Warning: No hash for {part_name} in checksum file. Skipping.")
            continue

        max_retries = 3
        for attempt in range(max_retries):
            if not download_file(asset['browser_download_url'], part_name):
                return False # Direkter Abbruch bei Download-Fehler

            actual_hash = calculate_sha256(part_name)
            if actual_hash == expected_hash:
                print(f" [OK]  OK: {part_name}\n")
                downloaded_parts.append(part_name)
                break  # Erfolgreich, innere Schleife verlassen
            else:
                print(f"❌ FAILED: Hash mismatch for {part_name} on attempt {attempt + 1}/{max_retries}. Retrying...")
                os.remove(part_name)
        else: # Diese else gehört zur for-Schleife! Wird nur ausgeführt, wenn die Schleife NICHT per break beendet wurde.
            print(f"[XXXX] CRITICAL: Failed to verify {part_name} after {max_retries} attempts. Aborting.")
            return False


    print(f"\n--- Step C: Merging and Verifying Final File: {final_merged_filename} ---")
    with open(final_merged_filename, 'wb') as f_out:
        for part_file in downloaded_parts:
            with open(part_file, 'rb') as f_in:
                f_out.write(f_in.read())
    final_actual_hash = calculate_sha256(final_merged_filename)
    print(f"  Official Hash: {final_zip_hash}")
    print(f"  Computed Hash: {final_actual_hash}")
    if final_actual_hash == final_zip_hash:
        print(f"\n[<3]  SUCCESS! Package '{final_merged_filename}' is correct.")
        if remove_parts:
            for part in downloaded_parts: os.remove(part)
            os.remove(checksum_filename)
            print("Cleaned up intermediate files.")
        return True
    else:
        print(f"\n[XXXXX]  CRITICAL FAILURE! Merged file '{final_merged_filename}' is corrupt.")
        return False


def main():
    # ----------------------------------------------------
    # NEU: 1. Argument-Parser MUSS ZUERST SEIN
    # ----------------------------------------------------
    parser = argparse.ArgumentParser(description="Download and verify assets from a GitHub release.")
    parser.add_argument("--exclude", type=str, default="",
                        help="Comma-separated list of language codes to exclude (e.g., 'de,en') or 'all'.")
    args = parser.parse_args()

    # Sprache(n) auslesen und in eine Liste konvertieren
    exclude_list = [item.strip().lower() for item in args.exclude.split(',')] if args.exclude else []

    print(f"============================================")
    print(f"============================================")
    print(f"============================================")
    print(f"--- DEBUG: Parsed exclusion list from arguments: {exclude_list}")
    print(f"============================================")
    # sys.exit(1) # Beenden, um die geparste Liste zu sehen
    # ----------------------------------------------------



    # ----------------------------------------------------
    # NEU: 2. Nur einmaliger API-Call nach dem Argument-Parsing
    # ----------------------------------------------------
    print(f"Fetching release assets for {OWNER}/{REPO} tag {TAG}...")
    try:
        release_info = requests.get(API_URL).json()
        assets = release_info.get('assets', [])
    except requests.exceptions.RequestException as e:
        print(f"Fatal Error: Could not connect to GitHub API. {e}")
        sys.exit(1)
    # ----------------------------------------------------


    packages = verbose_discovery(assets)
    valid_packages = {k: v for k, v in packages.items() if v['checksum_asset'] and v['part_assets']}

    if not valid_packages:
        print("="*60)
        print("CRITICAL ERROR: Could not find any complete, valid packages to download.")
        print("Please review the discovery log above to debug the filename mismatch.")
        print("="*60)
        sys.exit(1)

    # Diese Ausgabezeile ist irreführend, da sie die UNGEFILTERTE Liste zeigt.
    # Wir ändern den Text, damit es klarer wird, dass dies die "verfügbaren" Pakete sind.
    print(f"Found {len(valid_packages)} valid package(s) available: {', '.join(valid_packages.keys())}")


    # --- Filtering (Bleibt unverändert, aber jetzt greift es auf exclude_list zu!)
    packages_to_process = {}

    if exclude_list and exclude_list != ['']:
        print(f"Applying exclusion filter: {', '.join(exclude_list)}")

    for base_name, files in valid_packages.items():
        is_mandatory = base_name.startswith("LanguageTool") or base_name.startswith("lid.")
        is_excluded = False

        if 'all' in exclude_list and not is_mandatory:
            # Exclude=all: Überspringt alle nicht-obligatorischen Pakete
            is_excluded = True

        elif 'all' not in exclude_list:
            # Check: 'vosk-model-de-0.21' -> 'de'
            if 'de' in exclude_list and '-de-' in base_name:
                is_excluded = True
            if 'en' in exclude_list and ('-en-' in base_name or 'en-us' in base_name):
                is_excluded = True

        if is_excluded:
            print(f"    -> Exclusion applied: Skipping {base_name}")
        else:
            packages_to_process[base_name] = files

    if not packages_to_process:
        print("Warning: All packages were excluded or no packages found to process. Exiting downloader.")
        sys.exit(0)

    print(f"Processing {len(packages_to_process)} package(s) after exclusion: {', '.join(packages_to_process.keys())}")
    # ----------------------------------------------------


    all_successful = True
    for base_name, files in packages_to_process.items():
        if not process_package(base_name, files, remove_parts):
            all_successful = False

    print("\n" + "#"*60)
    if all_successful:
        print("All packages were downloaded and verified successfully!")
    else:
        print("One or more packages failed to download or verify correctly.")
    print("#"*60)

if __name__ == "__main__":
    main()

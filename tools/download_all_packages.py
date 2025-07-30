import requests
import hashlib
import os
import sys
from tqdm import tqdm
from collections import defaultdict

# --- Configuration ---
OWNER = "sl5net"
REPO = "Vosk-System-Listener"
TAG = "v0.2.0"
API_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/tags/{TAG}"

# --- Helper Functions (Unchanged) ---

def download_file(url, filepath):
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
        print(f"  ✅ Found definition for package: '{base_name}'")

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
                    print(f"  ✅ Matched '{asset['name']}' to package '{base_name}'")
                    matched = True
                    break
        if not matched:
            print(f"  ⚠️  Warning: Could not match part file '{asset['name']}' to any known package.")

    print("--- Discovery Complete ---\n")
    return packages

def process_package(base_name, package_files):
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
    print(f"  ✅ Deduced final filename from manifest: '{final_merged_filename}'")

    print(f"\n--- Step B: Downloading and Verifying {len(part_assets)} Parts ---")
    downloaded_parts = []
    part_assets.sort(key=lambda x: x['name'])
    for asset in part_assets:
        part_name = asset['name']
        expected_hash = official_hashes.get(part_name)
        if not expected_hash:
            print(f"Warning: No hash for {part_name} in checksum file. Skipping.")
            continue
        while True:
            if not download_file(asset['browser_download_url'], part_name): return False
            actual_hash = calculate_sha256(part_name)
            if actual_hash == expected_hash:
                print(f"✅ OK: {part_name}\n")
                downloaded_parts.append(part_name)
                break
            else:
                print(f"❌ FAILED: Hash mismatch for {part_name}. Retrying...")
                os.remove(part_name)

    print(f"\n--- Step C: Merging and Verifying Final File: {final_merged_filename} ---")
    with open(final_merged_filename, 'wb') as f_out:
        for part_file in downloaded_parts:
            with open(part_file, 'rb') as f_in:
                f_out.write(f_in.read())
    final_actual_hash = calculate_sha256(final_merged_filename)
    print(f"  Official Hash: {final_zip_hash}")
    print(f"  Computed Hash: {final_actual_hash}")
    if final_actual_hash == final_zip_hash:
        print(f"\n🎉 SUCCESS! Package '{final_merged_filename}' is correct.")
        for part in downloaded_parts: os.remove(part)
        os.remove(checksum_filename)
        print("Cleaned up intermediate files.")
        return True
    else:
        print(f"\n💥 CRITICAL FAILURE! Merged file '{final_merged_filename}' is corrupt.")
        return False

def main():
    print(f"Fetching release assets for {OWNER}/{REPO} tag {TAG}...")
    try:
        release_info = requests.get(API_URL).json()
        assets = release_info.get('assets', [])
    except requests.exceptions.RequestException as e:
        print(f"Fatal Error: Could not connect to GitHub API. {e}")
        sys.exit(1)

    packages = verbose_discovery(assets)
    valid_packages = {k: v for k, v in packages.items() if v['checksum_asset'] and v['part_assets']}

    if not valid_packages:
        print("="*60)
        print("CRITICAL ERROR: Could not find any complete, valid packages to download.")
        print("Please review the discovery log above to debug the filename mismatch.")
        print("="*60)
        sys.exit(1)

    print(f"Found {len(valid_packages)} valid package(s) to process: {', '.join(valid_packages.keys())}")

    all_successful = True
    for base_name, files in valid_packages.items():
        if not process_package(base_name, files):
            all_successful = False

    print("\n" + "#"*60)
    if all_successful:
        print("All packages were downloaded and verified successfully!")
    else:
        print("One or more packages failed to download or verify correctly.")
    print("#"*60)

if __name__ == "__main__":
    main()


# echo "fb45a53025a50830b16bcda94146f90e22166501bb3693b009cabed796dbaaa0 vosk-model-de-0.21.zip" | sha256sum -c
# echo "d410847b53faf1850f2bb99fb7a08adcb49dd236dcba66615397fe57a3cf68f5 vosk-model-en-us-0.22.zip" | sha256sum -c -

import os
import sys
import hashlib

# --- Configuration ---
CHUNK_SIZE = 100 * 1024 * 1024  # 100MB in bytes

def get_part_suffix(part_num):
    """Generates suffixes aa, ab, ac..."""
    if part_num >= 26 * 26:
        raise ValueError("Too many parts, suffix generation not implemented for > zz")
    first_char_code = ord('a') + part_num // 26
    second_char_code = ord('a') + part_num % 26
    return chr(first_char_code) + chr(second_char_code)

def calculate_sha256_of_file(filepath):
    """Helper function to calculate SHA256 of an entire file."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        # Read in chunks to handle large files efficiently
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256.update(byte_block)
    return sha256.hexdigest()

def split_and_hash(filename):
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found!")
        return

    prefix = f"Z_{filename}.part."
    checksum_filename = f"{filename}.sha256sums.txt"

    # --- KORREKTUR, TEIL 1: Hash der kompletten Datei zuerst berechnen ---
    print(f"Calculating SHA256 for the complete file: {filename}...")
    full_file_hash = calculate_sha256_of_file(filename)
    print(f"  -> Hash: {full_file_hash}")

    print(f"Splitting '{filename}' into {CHUNK_SIZE // 1024 // 1024}MB parts...")

    part_num = 0
    with open(filename, 'rb') as f_in, open(checksum_filename, 'w') as f_checksum:

        # --- KORREKTUR, TEIL 2: Den Hash der kompletten Datei als ERSTES schreiben ---
        # Der Name in der Manifest-Datei sollte konsistent sein (mit Z_ Prefix)
        final_zip_name_in_manifest = f"Z_{filename}"
        f_checksum.write(f"{full_file_hash}  {final_zip_name_in_manifest}\n")

        # Der Rest des Skripts bleibt unverändert
        while True:
            chunk = f_in.read(CHUNK_SIZE)
            if not chunk:
                break  # End of file

            part_suffix = get_part_suffix(part_num)
            part_filename = f"{prefix}{part_suffix}"

            # Kein print mehr hier, um die Ausgabe sauber zu halten
            with open(part_filename, 'wb') as f_part:
                f_part.write(chunk)

            sha256_hash = hashlib.sha256(chunk).hexdigest()
            f_checksum.write(f"{sha256_hash}  {part_filename}\n")

            part_num += 1

    print("\n" + "-"*50)
    print("✅ Success!")
    print(f"Split parts created with prefix: '{prefix}'")
    print(f"COMPLETE checksum file saved to: '{checksum_filename}'")
    print("-"*50)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python split_py.py <your-large-file.zip>")
    else:
        split_and_hash(sys.argv[1])

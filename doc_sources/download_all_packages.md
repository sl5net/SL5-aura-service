## Project Utilities: File Splitter & Downloader

This repository includes two powerful Python scripts designed to manage the distribution and download of large files via GitHub Releases.

1.  **`split_and_hash.py`**: A utility for repository owners to split large files into smaller parts and generate a complete and verifiable checksum manifest.
2.  **`download_all_packages.py`**: A robust tool for end-users to automatically download, verify, and reassemble these multi-part files, ensuring data integrity from start to finish.

---

### 1. File Splitting & Checksum Generation Script (`split_and_hash.py`)

This script is intended for the **repository maintainer**. It prepares large files for distribution on platforms like GitHub Releases, which have individual file size limits.

#### Purpose

The primary goal is to take a single large file (e.g., `vosk-model-de-0.21.zip`) and perform two critical actions:
1.  Split the file into a series of smaller, numbered parts.
2.  Generate a single, comprehensive manifest file (`.sha256sums.txt`) that contains the checksums for **both the original, complete file and every individual part**.

This complete manifest is the key to ensuring 100% data integrity for the end-user.

#### Key Features

*   **Standardized Splitting:** Splits files into 100MB chunks (configurable within the script).
*   **Consistent Naming:** Creates parts with a `Z_` prefix (e.g., `Z_vosk-model-de-0.21.zip.part.aa`). The `Z_` prefix ensures proper sorting and handling in various systems.
*   **Complete Integrity Manifest:** The generated `.sha256sums.txt` file is structured for maximum reliability. It includes:
    *   The SHA256 hash of the **original, complete file**.
    *   The SHA256 hash of **every single part** that was created.

#### Usage for a GitHub Release

1.  Place the large file (e.g., `vosk-model-de-0.21.zip`) in a directory with the `split_and_hash.py` script.
2.  Run the script from your terminal:
    ```bash
    python split_and_hash.py <your-large-file.zip>
    ```
3.  The script will generate all the `Z_...part.xx` files and the corresponding `...sha256sums.txt` file.
4.  When creating a new GitHub Release, upload **all** the generated files: the part files and the single manifest file.
5.  Repeat this process for every large file you want to distribute.

---

### 2. Automated Package Downloader & Verifier (`download_all_packages.py`)

This script is intended for the **end-user**. It provides a simple, one-command solution to reliably download and reassemble all packages offered in the GitHub Release.

#### Purpose

It automates the otherwise complex and error-prone process of downloading dozens of file parts, verifying each one, and correctly reassembling them. It uses the checksum manifests provided in the release to guarantee that the final, assembled file is a perfect, uncorrupted copy of the original.

#### Key Features

*   **Automatic Discovery:** The script connects to the GitHub API to automatically find all available "packages" in the release by looking for `.sha256sums.txt` files. No manual configuration of filenames is needed.
*   **Integrity-First Process:** For each package, it downloads the manifest file *first* to get the list of required parts and their correct checksums.
*   **Part-by-Part Verification:** It downloads one part at a time and immediately verifies its SHA256 hash.
*   **Auto-Retry on Corruption:** If a downloaded part is corrupt (the hash does not match), the script automatically deletes it and re-downloads it, ensuring a clean download.
*   **Intelligent Reassembly:** Once all parts of a package are downloaded and verified, it merges them in the correct alphabetical order (`.aa`, `.ab`, `.ac`...) to reconstruct the original large file.
*   **Final Verification:** After reassembly, it calculates the SHA256 hash of the final, complete file and verifies it against the master hash found in the manifest. This provides end-to-end confirmation of success.
*   **Resilient and Tolerant:** The script is robust against minor naming inconsistencies, such as `Z_` vs. `z_`, ensuring a smooth user experience.
*   **Automated Cleanup:** After a package is successfully built and verified, the script deletes the downloaded part files to save disk space.

#### Prerequisites

The user must have Python and the `requests` and `tqdm` libraries installed. They can be installed with pip:
```bash
pip install requests tqdm
```

#### Usage

1.  Download the `download_all_packages.py` script.
2.  Run it from the terminal with no arguments:
    ```bash
    python download_all_packages.py
    ```
3.  The script will handle the rest, displaying progress bars and status messages. Upon completion, the user will have all the final, verified ZIP files ready for use in the same directory.

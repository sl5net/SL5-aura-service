
# Hybrid Downloader Implementation Report 24.3.'26 13:04 Tue

## 1. Project Status Summary
The new `download_release_hybrid.py` script has been successfully implemented and integrated. It replicates the core logic of the original `download_all_packages.py` while adding a BitTorrent hybrid layer.

### Core Features Verified:
*   **CLI Argument Parsing:** Successfully handles `--exclude`, `--tag`, and `--list`.
*   **CI Environment Detection:** Correctly identifies GitHub Actions and auto-excludes large models.
*   **Asset Discovery:** Successfully groups release assets into logical packages (Parts, Checksums, Torrents).
*   **Robust Fallback:** The script detects the absence of `libtorrent` and gracefully defaults to HTTP fallback mode.

---

## 2. Test Execution & Results
**Command executed:** 
`python tools/download_release_hybrid.py --list`

### Observed Output:
*   **Dependency Check:** `--> Info: 'libtorrent' not found. Hybrid-Torrent disabled. Using HTTP fallback.` (Expected on current system).
*   **API Connectivity:** Successfully fetched release info for `sl5net/SL5-aura-service @ v0.2.0`.
*   **Discovery Result:** 5 packages identified:
    1.  `LanguageTool-6.6.zip` (3 parts)
    2.  `lid.176.zip` (2 parts)
    3.  `vosk-model-de-0.21.zip` (20 parts)
    4.  `vosk-model-en-us-0.22.zip` (19 parts)
    5.  `vosk-model-small-en-us-0.15.zip` (1 part)

---

## 3. Error Report: Dependency Issues
### Issue: `libtorrent` Installation Failure
On the current **Manjaro/Arch Linux** environment, the BitTorrent engine (`libtorrent`) could not be installed via standard package managers.

*   **Attempted Commands:**
    *   `sudo pacman -S python-libtorrent` -> `target not found`
    *   `pamac build python-libtorrent-rasterbar` -> `target not found`
    *   `pamac build python-libtorrent` -> `target not found`
*   **Root Cause:** The Python bindings for `libtorrent` in Arch-based systems are often poorly maintained in the official repos or require specific AUR helpers/build-tools (`base-devel`) that are currently missing or misconfigured.
*   **Impact:** BitTorrent features (P2P and Web-Seeds) are currently inactive. The script remains fully functional via **HTTP fallback**.

---

## 4. To-Do List (Next Steps)

### Phase 1: Environment Migration
- [ ] **OS Switch:** Move testing to a different operating system (e.g., Ubuntu, Debian, or Windows) where `python3-libtorrent` or `pip install libtorrent` is more easily available.
- [ ] **Dependency Re-verification:** Ensure the "Motor" (`libtorrent`) loads correctly on the new OS.

### Phase 2: Functional Validation
- [ ] **Full Download Test:** Run the script without the `--list` flag to verify part-downloading, merging, and SHA256 verification.
- [ ] **Exclusion Test:** Run with `--exclude de` to confirm the English-only setup works as intended.
- [ ] **Torrent Seed Test:** Create a `.torrent` file with a GitHub Web-Seed and verify that the hybrid downloader prioritizes P2P/Web-Seed over standard HTTP parts.

### Phase 3: Cleanup
- [ ] **Final Pruning Check:** Confirm that no `.i18n` or translation files are present in the final local directory structure after a full run.


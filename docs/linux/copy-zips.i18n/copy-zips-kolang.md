```bash
#!/bin/bash

# 1. Detect OS to set the correct temp directory path
if [ "${OS:-}" = "Windows_NT" ] || [ -n "${WINDIR:-}" ]; then
  tmp_dir='C:/tmp'
else
  tmp_dir='/tmp'
fi

# 2. Resolve Project Root and Target Directory dynamically
# Reads the project root from a tracking file, removing Windows-style carriage returns (\r)
PROJECT_ROOT="$(realpath "$(tr -d '\r' < "$tmp_dir/sl5_aura/sl5net_aura_project_root")")"

SOURCE_DIR="$PROJECT_ROOT/config/maps"

TARGET_DIR="$(realpath "$PROJECT_ROOT/../zip_backup")"

# Ensure target directory exists
mkdir -p "$TARGET_DIR"

# Check if the source directory exists within the project
if [ ! -d "$PROJECT_ROOT/$SOURCE_DIR" ]; then
    echo "Error: Source directory '$PROJECT_ROOT/$SOURCE_DIR' does not exist."
    exit 1
fi

echo "Mirroring ZIP files..."
echo "Source: $PROJECT_ROOT/$SOURCE_DIR"
echo "Target: $TARGET_DIR"

# Navigate to the source directory so paths remain relative during the copy process
cd "$PROJECT_ROOT/$SOURCE_DIR" || exit 1

# Find all .zip files recursively and copy them preserving the directory structure
find . -type f -iname "*.zip" -exec cp --parents -v {} "$TARGET_DIR" \;

echo "Mirroring completed successfully!"
```

---

### 문서(README.md 템플릿)

```markdown
# Map Mirroring & Syncthing Synchronization

This project includes an automated script to collect all map `.zip` files and mirror them into a structured backup folder. This allows you to easily synchronize your maps to external devices (such as an Android phone) using file-sharing tools like **Syncthing**.

## How the Script Works

1. **Cross-Platform Compatibility**: The script automatically detects whether it is running on Linux or Windows to locate the correct local temp folder.
2. **Dynamic Paths**: It reads the project's root directory path from a tracking file located in your system's temporary directory (`sl5net_aura_project_root`).
3. **Directory Mirroring**: It scans the `config/maps` directory recursively, finds all `.zip` files, and copies them to a `zip_backup` folder located one level above your project root (preserving the original nested folder structure).

## Why not use `/tmp` directly?

On modern Linux distributions (such as Manjaro or Arch), system services like Syncthing often run with restricted permissions (`PrivateTmp=true` via systemd) or inside sandboxed environments (like Flatpak or Snap). 

If the script copied files directly to `/tmp`, Syncthing would see the target directory as completely empty. By dynamically placing the `zip_backup` folder inside your user's home directory structure (relative to the project root), Syncthing can read and sync the files without permission or isolation issues.

## Setup Instructions

### 1. Prerequisites
Ensure that the tracking file containing your absolute project root path exists on your machine:
- **Linux**: `/tmp/sl5_aura/sl5net_aura_project_root`
- **Windows**: `C:/tmp/sl5_aura/sl5net_aura_project_root`

The file should contain a single line pointing to your project directory.

### 2. Run the Script
Make the script executable (on Linux) and run it:
```bash
chmod +x copy_zips.sh
./copy_zips.sh
```
This will create the `zip_backup` folder next to your project folder and populate it.

### 3. Configure Syncthing
1. Open your **Syncthing Web GUI** on your computer.
2. Click **Add Folder** and set the folder path to the newly created `zip_backup` directory (e.g., `/home/username/projects/zip_backup`).
3. Share this folder with your Android device.
4. On your **Android device**, accept the shared folder in the Syncthing app and select your destination folder. 
5. Any future maps you add to `config/maps` will be mirrored and synced automatically whenever you run the script.
```
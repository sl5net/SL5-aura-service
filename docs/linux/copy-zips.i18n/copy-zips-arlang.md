```bash
#!/bin/bash

if [ "${OS:-}" = "Windows_NT" ] || [ -n "${WINDIR:-}" ]; then
  tmp_dir='C:/tmp'
else
  tmp_dir='/tmp'
fi

# TARGET_DIR="/tmp/sl5_aura/zip_backup" # dont work

PROJECT_ROOT="$(realpath "$(tr -d '\r' < "$tmp_dir/sl5_aura/sl5net_aura_project_root")")"

#PROJECT_ROOT="(realpath"(realpath"(tr -d '\r' < "$tmp_dir/sl5_aura/sl5net_aura_project_root")")"

TARGET_DIR="$(realpath "$PROJECT_ROOT/../zip_backup")"
# ----------------------

if [ ! -d "$SOURCE_DIR" ]; then
    echo "error:  '$SOURCE_DIR' SOURCE_DIR not existiert."
    exit 1
fi

mkdir -p "$TARGET_DIR"

SOURCE_DIR=$(realpath "$SOURCE_DIR")
TARGET_DIR=$(realpath "$TARGET_DIR")

echo "start copy..."
echo "s: $SOURCE_DIR"
echo "t: $TARGET_DIR"

cd "$SOURCE_DIR" || exit 1

# Erläuterung der Parameter:
# -type f: Nur Dateien finden (keine Ordner direkt)
# -iname "*.zip": Sucht nach .zip-Dateien (Groß-/Kleinschreibung wird ignoriert)
# --parents: Kopiert die Datei inklusive ihres relativen Pfads in das Zielverzeichnis
# find . -type f -iname "*.zip" -exec cp --parents -v {} "$TARGET_DIR" \;
find . -type d -name '_*' -prune -o -type f -iname '*.zip' -print -exec rsync --relative -R {} "$TARGET_DIR"/ \;


echo "Mirroring completed successfully!"
```

                                                                          ---

                                      ### التوثيق (قالب README.md)

```markdown
# Map Mirroring & Syncthing Synchronization

This project includes an automated script to collect all map `.zip` files (that are not in "/_..." folders) and mirror them into a structured backup folder. This allows you to easily synchronize your maps to external devices (such as an Android phone) using file-sharing tools like **Syncthing**.

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
                                                        chmod +x Copy_zips.sh
                                                               ./copy_zips.sh
```
This will create the `zip_backup` folder next to your project folder and populate it.

### 3. Configure Syncthing
1. Open your **Syncthing Web GUI** on your computer.
2. Click **Add Folder** and set the folder path to the newly created `zip_backup` directory (e.g., `/home/username/projects/zip_backup`).
- set send-only !
3. Share this folder with your Android device.
4. On your **Android device**, accept the shared folder in the Syncthing app and select your destination folder. 
5. Any future maps you add to `config/maps` will be mirrored and synced automatically whenever you run the script.

dont use ignore filter in Syncthing. may not works and you may have no control before use it that it works.

## Setup Syncthing

1. Run the copy script once to generate the `zip_backup` folder.
2. Open your Syncthing GUI on your PC.
3. Add a new folder pointing to the newly created `zip_backup` directory (e.g., `/home/seeh/projects/py/zip_backup`).
4. Share this folder with your Android device via Syncthing.
5. On your phone, accept the share and choose the destination folder. The mirrored maps will now sync automatically.

---

## Troubleshooting

### Error: "folder marker missing"
If Syncthing halts and displays an error message similar to this:
> `Failed initial scan (error="folder marker missing...")`

#### Why this happens:
Syncthing creates a hidden safety folder called `.stfolder` inside your synced directory to prevent accidental data loss. If you manually delete, clear, or recreate the `zip_backup` folder (or if a cleanup process wipes it), this hidden marker is lost. Syncthing will stop syncing immediately to protect your files on other devices.

#### How to fix:
You simply need to recreate this hidden folder manually inside your target directory:

* **On Linux**:
  Run this command in your terminal (replace the path with your actual backup path):
  ```bash
                                          mkdir -p .... /zip_backup/.stfolder
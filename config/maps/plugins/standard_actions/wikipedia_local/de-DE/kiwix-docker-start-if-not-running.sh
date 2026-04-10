#!/usr/bin/env bash
set -euo pipefail

# --- KONFIGURATION ---
ZIM_FILE_NAME="wikipedia_de_all_mini_2025-09.zim"
CONTAINER_NAME="kiwix_zim_server"
HOST_PORT="8080"
CONTAINER_PORT="8080"

if [ "${OS:-}" = "Windows_NT" ] || [ -n "${WINDIR:-}" ]; then
  tmp_dir='C:/tmp'
else
  tmp_dir='/tmp'
fi


PROJECT_ROOT="$(realpath "$(tr -d '\r' < "$tmp_dir/sl5_aura/sl5net_aura_project_root")")"

# 1. Absoluter Pfad zur Datei auf dem Host ermitteln
# SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ZIM_FILE_PATH_host="$(realpath "$PROJECT_ROOT/data/$ZIM_FILE_NAME")"

# ZIM_FILE_PATH_host="$(realpath "$SCRIPT_DIR/../../../../../../data/$ZIM_FILE_NAME")"

# 2. Download-URL
ZIM_URL="https://download.kiwix.org/zim/wikipedia/$ZIM_FILE_NAME"

# 3. Welcher Downloader ist verfügbar? (aria2c bevorzugt)
if command -v aria2c >/dev/null 2>&1; then
  DOWNLOADER="aria2c"
elif command -v wget >/dev/null 2>&1; then
  DOWNLOADER="wget"
else
  echo "Kein Downloader (aria2c oder wget) gefunden. Bitte installieren."
  exit 1
fi

# Funktion: Datei herunterladen (resume/fallback)
download_zim() {
  mkdir -p "$(dirname "$ZIM_FILE_PATH_host")"
  echo "Herunterladen: $ZIM_URL -> $ZIM_FILE_PATH_host (mit $DOWNLOADER)"
  if [ "$DOWNLOADER" = "aria2c" ]; then
    # -x 8 -s 8 für Multithread; --continue=true für Resume
    aria2c --continue=true -x 8 -s 8 -d "$(dirname "$ZIM_FILE_PATH_host")" -o "$(basename "$ZIM_FILE_PATH_host")" "$ZIM_URL"
  else
    # wget -c resume; -O wird nur verwendet falls wir explizit Zielnamen wollen
    wget -c -O "$ZIM_FILE_PATH_host" "$ZIM_URL"
  fi
}

# 4. Conditional download: nur wenn Datei nicht existiert
if [ -f "$ZIM_FILE_PATH_host" ]; then
  echo "Datei existiert bereits: $ZIM_FILE_PATH_host — überspringe Download."
else
  echo "Datei nicht gefunden: $ZIM_FILE_PATH_host"
  download_zim
fi

# Optional: kurze Validierung (Dateigröße > 0)
if [ ! -s "$ZIM_FILE_PATH_host" ]; then
  echo "Fehler: Datei ist nicht vorhanden oder leer nach dem Download: $ZIM_FILE_PATH_host"
  exit 1
fi


echo "Prüfe Datei: $ZIM_FILE_PATH_host"

# --- SICHERHEITS-CHECK ---
# Falls die Datei nicht existiert, DARF Docker nicht starten.
# Sonst erstellt Docker einen ORDNER namens 'wikipedia...zim' auf deinem Host!
if [ ! -f "$ZIM_FILE_PATH_host" ]; then
    echo "❌ FEHLER: Die Datei $ZIM_FILE_PATH_host wurde nicht gefunden."
    echo "Bitte prüfe, ob der Pfad (6 Ebenen hoch) wirklich stimmt."
    exit 1
fi

# Prüfen, ob der Pfad versehentlich ein Verzeichnis ist (Docker-Fehler von vorherigen Versuchen)
if [ -d "$ZIM_FILE_PATH_host" ]; then
    echo "❌ FEHLER: $ZIM_FILE_PATH_host ist ein Verzeichnis, keine Datei!"
    echo "Docker hat hier wohl einen leeren Ordner erstellt. Bitte lösche diesen Ordner:"
    echo "rm -rf '$ZIM_FILE_PATH_host'"
    exit 1
fi

# --- DOCKER BEREINIGUNG ---
docker rm -f $CONTAINER_NAME > /dev/null 2>&1

echo "--- Starte Kiwix-Server (Nur Datei-Mount) ---"

# --- DOCKER RUN ---
# Wir mounten NUR die eine Datei direkt in den Pfad /data/file.zim im Container

# Verzeichnis des ZIM-Files ermitteln
ZIM_DIR_host="$(dirname "$ZIM_FILE_PATH_host")"

docker run -d \
    --name "$CONTAINER_NAME" \
    --user "$(id -u):$(id -g)" \
    -p "$HOST_PORT":"$CONTAINER_PORT" \
    -v "$ZIM_DIR_host":/data:ro \
    ghcr.io/kiwix/kiwix-tools \
    kiwix-serve --port "$CONTAINER_PORT" /data/"$ZIM_FILE_NAME"

sleep 3

# Finaler Check
if docker ps | grep -q "$CONTAINER_NAME"; then
    echo "✅ ERFOLG! Container läuft."
    echo "URL: http://localhost:$HOST_PORT/"
else
    echo "❌ FEHLER: Start fehlgeschlagen. Logs:"
    docker logs "$CONTAINER_NAME"
fi

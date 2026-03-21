#!/bin/bash

# --- download: ---
# cd ~/projects/py/STT/data/
# Mit wget + Fortsetzung falls Abbruch:
wget -c "https://download.kiwix.org/zim/wikipedia/wikipedia_de_all_mini_2025-09.zim"
# Oder mit aria2 (schneller, Multithreaded):
aria2c -x 8 -s 8 "https://download.kiwix.org/zim/wikipedia/wikipedia_de_all_mini_2025-09.zim"


# --- KONFIGURATION ---
ZIM_FILE_NAME="wikipedia_de_all_mini_2025-09.zim"
CONTAINER_NAME="kiwix_zim_server"
HOST_PORT="8080"
CONTAINER_PORT="8080"

# 1. Absoluten Pfad zur Datei auf dem Host ermitteln
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# Gehe 6 Ebenen hoch zum Projekt-Root, dann in /data/
ZIM_FILE_PATH_host="$(realpath "$SCRIPT_DIR/../../../../../../data/$ZIM_FILE_NAME")"

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

#!/bin/bash

# Initialisierung und Information
clear
# Ausgabe des Skriptnamens
echo "--- Starte: kiwix-docker-start-if-not-running.sh ---"
ls *.zim
echo ""

# --- KONFIGURATION (Nur diese Werte bei Bedarf ändern) ---
# 1. Der reine Dateiname des ZIM-Archivs
ZIM_FILE_host="wikipedia_de_all_mini_2025-09.zim"
echo "ZIM_FILE_host=$ZIM_FILE_host"

# 2. Der vollständige Pfad zur ZIM-Datei auf deinem PC
ZIM_FILE_PATH_host="$HOME/Downloads/$ZIM_FILE_host"

# 3. Identischer Name im Container
CONTAINER_ZIM_NAME="$ZIM_FILE_host"
CONTAINER_NAME="kiwix_zim_server"

# 4. Ports
HOST_PORT="8080"
CONTAINER_PORT="8080"
# --- ENDE KONFIGURATION ---


echo "--- 1. Prüfe Status des Kiwix-Servers ($CONTAINER_NAME) auf Port $HOST_PORT..."

# Prüfen, ob ein Container mit diesem Namen läuft
if docker ps -f "name=$CONTAINER_NAME" | grep -q "$CONTAINER_NAME"; then
    echo ""
    echo "✅ Kiwix-Server läuft bereits."
    echo "   URL: http://localhost:8080/viewer#wikipedia_de_all_mini_2025-09/Latein"
    exit 0
fi

# Prüfen, ob der Container gestoppt existiert (muss gelöscht werden, um Port neu zu belegen)
if docker ps -a -f "name=$CONTAINER_NAME" | grep -q "$CONTAINER_NAME"; then
    echo "⚠️ Gestoppte Instanz gefunden. Muss bereinigt werden, um Port $HOST_PORT freizugeben."
    docker rm -f $CONTAINER_NAME > /dev/null
fi


echo "--- 2. Starte Kiwix-Server im Docker-Container..."

# Führe den Docker-Befehl aus (Präzises Mounten der einzelnen Datei)
CONTAINER_ID=$(docker run -d --name $CONTAINER_NAME -p $HOST_PORT:$CONTAINER_PORT \
    -v "$ZIM_FILE_PATH_host":/data/$CONTAINER_ZIM_NAME \
    ghcr.io/kiwix/kiwix-tools /usr/local/bin/kiwix-serve --port $CONTAINER_PORT /data/$CONTAINER_ZIM_NAME)

sleep 4

# Finaler Prüfschritt
if docker ps | grep -q "$CONTAINER_ID"; then
    echo ""
    echo "✅ ERFOLG! Kiwix-Server gestartet."
    echo "   URL: http://localhost:$HOST_PORT/viewer#$CONTAINER_ZIM_NAME/Krankenhaus_J%C3%BClich"
else
    echo ""
    echo "❌ FEHLER: Container ist sofort beendet. Siehe Logs für den Grund."
    echo "--- AKTUELLE LOGS (Grund für Fehler) ---"
    docker logs $CONTAINER_NAME
    echo "----------------------------------------"

    sudo systemctl start docker
    echo "   docker daemon running?"
    echo "sudo systemctl start docker"
    echo "   Mögliche Gründe: 1. Port $HOST_PORT ist belegt."
    echo "   2. ZIM-Datei korrupt oder Pfad falsch."


fi

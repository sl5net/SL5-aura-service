#!/bin/bash
# file: update/update_for_linux_users.sh
# Description: Downloads the latest version and updates the application
#              while preserving user settings. For non-developer use.

# Stoppt das Script sofort bei einem Fehler
set -e

# Farbdefinitionen für die Konsole
COLOR_CYAN='\e[36m'
COLOR_GREEN='\e[32m'
COLOR_RED='\e[31m'
COLOR_YELLOW='\e[33m'
COLOR_RESET='\e[0m'

# Variablen
repoUrl="https://github.com/sl5net/SL5-aura-service/archive/refs/heads/master.zip"

# Den Installationspfad ermitteln (zwei Ebenen über dem Script-Pfad)
# Annahme: Script liegt in 'installDir/update/'
scriptDir="$(dirname "$0")"
installDir="$(dirname "$scriptDir")"
tempDir="/tmp/sl5_update_temp"
localSettingsPath="$installDir/config/settings_local.py"
backupPath="$tempDir/settings_local.py.bak"
zipPath="$tempDir/latest.zip"

# Funktion zur Fehlerbehandlung
cleanup_on_error() {
    echo -e "${COLOR_RED}FATAL: Ein Fehler ist während des Updates aufgetreten.${COLOR_RESET}" >&2
    if [ -d "$tempDir" ]; then
        echo -e "${COLOR_YELLOW}INFO: Lösche temporären Ordner...${COLOR_RESET}"
        rm -rf "$tempDir"
    fi
    read -p "Drücken Sie die Eingabetaste, um das Script zu beenden."
    exit 1
}

# Fange Fehler ab (trap)
trap cleanup_on_error ERR

echo -e "${COLOR_CYAN}--- SL5 Aura Updater ---${COLOR_RESET}"
echo "Dies lädt die neueste Version herunter und ersetzt alle Anwendungsdateien."
echo "Ihre persönlichen Einstellungen in 'config/settings_local.py' werden gespeichert."
if [ "$CI" != "true" ]; then
    echo "Bitte schließen Sie die Hauptanwendung, falls sie läuft."
    read -p "Drücken Sie die Eingabetaste, um fortzufahren, oder CTRL+C, um abzubrechen"
fi

# 1. Alte temporäre Dateien bereinigen und neuen Ordner erstellen
if [ -d "$tempDir" ]; then
    echo "INFO: Entferne alten temporären Update-Ordner..."
    rm -rf "$tempDir"
fi
mkdir -p "$tempDir"

# 2. Lokale Einstellungen sichern, falls vorhanden
if [ -f "$localSettingsPath" ]; then
    echo -e "${COLOR_GREEN}INFO: Sichern Ihrer lokalen Einstellungen...${COLOR_RESET}"
    cp "$localSettingsPath" "$backupPath"
fi

# 3. Neueste Version herunterladen (curl oder wget erforderlich)
echo "INFO: Lade neueste Version von GitHub herunter..."
curl -L -o "$zipPath" "$repoUrl"

# 4. Archiv entpacken (unzip erforderlich)
echo "INFO: Entpacke Update..."
unzip -q "$zipPath" -d "$tempDir"

# Den extrahierten Ordner finden (der normalerweise auf '-master' endet)
extractedFolder=$(find "$tempDir" -maxdepth 1 -type d -name "*-master" | head -n 1)
if [ -z "$extractedFolder" ]; then
    echo -e "${COLOR_RED}FATAL: Konnte den extrahierten '*-master' Ordner nicht finden.${COLOR_RESET}"
    exit 1
fi

# 5. Lokale Einstellungen in die neue Version wiederherstellen
if [ -f "$backupPath" ]; then
    echo -e "${COLOR_GREEN}INFO: Stelle Ihre lokalen Einstellungen in die neue Version wieder her...${COLOR_RESET}"
    cp "$backupPath" "$extractedFolder/config/"
fi

# 6. Dateien ersetzen (rsync erforderlich)
# Mit rsync die Dateien aus dem temporären Ordner in den Installationsordner kopieren und die alten Dateien löschen.
echo "INFO: Finalisiere Update und ersetze Dateien. Bitte warten..."
# Die '-a' Option bewahrt Berechtigungen, Zeiten etc.
# Die '--delete' Option entfernt Dateien, die im Quellverzeichnis nicht vorhanden sind.
# Der abschließende Schrägstrich bei "$extractedFolder/" ist wichtig, um den *Inhalt* zu kopieren.
rsync -a --delete --force "$extractedFolder/" "$installDir"

# 7. Aufräumen
echo "INFO: Bereinige temporäre Dateien..."
rm -rf "$tempDir"

echo ""
echo -e "${COLOR_GREEN}Update abgeschlossen! Sie können die Anwendung jetzt neu starten.${COLOR_RESET}"

# Keine Fehlerbehandlung notwendig, wenn das Script bis hierher kommt
trap - ERR
read -p "Drücken Sie die Eingabetaste, um das Script zu beenden."
exit 0


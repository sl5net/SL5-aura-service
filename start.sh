#!/bin/bash

PROJECT_DIR="/home/seeh/projects/py/STT"
cd "$PROJECT_DIR"

# 1. Virtuelle Umgebung prüfen/erstellen
if [ ! -d ".venv" ]; then
    echo "Erstelle neue virtuelle Umgebung..."
    python3 -m venv .venv
fi

# 2. Venv aktivieren
source .venv/bin/activate

# 3. Wichtige Pakete sicherstellen (installiert nur, wenn sie fehlen)
echo "Prüfe Abhängigkeiten..."
pip install --upgrade pip
pip install uvicorn fastapi requests streamlit  # Füge hier alle benötigten Module hinzu

# 4. Alte Prozesse killen
echo "Bereinige Ports..."
fuser -k 8830/tcp 2>/dev/null
fuser -k 8831/tcp 2>/dev/null

# 5. API starten
echo "Starte API Service..."
python3 scripts/py/start_uvicorn_service.py &

sleep 2

# 6. Streamlit starten
echo "Starte Streamlit..."
streamlit run scripts/py/chat/streamlit-chat.py \
--server.sslCertFile /etc/letsencrypt/live/aura.sl5.de/fullchain.pem \
--server.sslKeyFile /etc/letsencrypt/live/aura.sl5.de/privkey.pem \
--server.port 8831

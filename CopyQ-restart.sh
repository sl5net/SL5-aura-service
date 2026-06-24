#!/bin/bash

# CopyQ-restart.sh
# CopyQ-Dienst sauber beenden
copyq exit
sleep 1

# CopyQ mit expliziter UTF-8-Umgebung im Hintergrund starten
export PYTHONUTF8=1
export LC_ALL=de_DE.UTF-8
export LANG=de_DE.UTF-8
copyq &

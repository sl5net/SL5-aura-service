# config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
from pathlib import Path; import os; PROJECT_ROOT = Path(os.environ["SL5NET_AURA_PROJECT_ROOT"]) # noqa: E702

# too<-from
FUZZY_MAP_pre = [
    ('nix', r'^(nix|laut|Programm geladen. Viel Spaß|mit guten|english einschalten|finish einschalten|flug|er hat es)$'),

    # Overlay Modus aktiviert Aura Lernmodus aktiviert Blumen Korn Ahorn werden Modus einschaltenAura der Modus einschalten
    # Aura leer Modus einschalten Keine Änderung vorgenommen.Fußball zähltlkjhlkjhlkh
    # kjhlkjhkjhk
    # lhlkjhLernmodus DEAKTIVIERT.Lernmodus AKTIVIERT.Mondgestein Lernmodus DEAKTIVIERT.

    #a sdfasdf blumen


]


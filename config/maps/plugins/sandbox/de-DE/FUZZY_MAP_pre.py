# config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
from pathlib import Path; import os; PROJECT_ROOT = Path(os.environ["SL5NET_AURA_PROJECT_ROOT"]) # noqa: E702

# too<-from
FUZZY_MAP_pre = [
    ('nix', r'^(nix|fußball|hurra lernen modus ausschalten|Learn-modus rule not found. |lernen lernmodus einschalten|ok)$'),

    # Overlay Modus aktiviert Aura Lernmodus aktiviert Blumen Korn Ahorn werden Modus einschaltenAura der Modus einschalten
    # Aura leer Modus einschalten Keine Änderung vorgenommen.Fußball zähltlkjhlkjhlkh
    # kjhlkjhkjhkDas istSo kann man arbeiten
    # lhlkjhLernmodus DEAKTIVIERT.Lernmodus AKTIVIERT.Mondgestein Lernmodus DEAKTIVIERT.sdfHurra Lernmodusnix
    # Learn-modus rule ot fohalloFlug Aura lernen Modus einschaltenAura leeren Modus einschalten
    # Aura lernen Modus einschaltenRealität ist
    #     (f'{str(__file__)}', r'^(.*)$', 10, {'on_match_exec': [PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),

    # (f'{str(__file__)}', r'^(.*)$', 10, {'on_match_exec': [PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),

]
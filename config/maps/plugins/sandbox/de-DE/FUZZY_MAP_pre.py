# config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401

# too<-from
FUZZY_MAP_pre = [
    ('überraschung', r'^überraschung$'),
    ('meine_funktion', r'^meine_funktion$'),
    ('return 42', r'^return\ 42$'),
    ('rote grütze', r'^rote\ grütze$'),
]

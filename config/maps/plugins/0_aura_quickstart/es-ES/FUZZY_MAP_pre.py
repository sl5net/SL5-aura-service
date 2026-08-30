# ==============================================================================
# 🌐 AUTOMATICALLY GENERATED / MACHINE-TRANSLATED MAP
# ==============================================================================
# ℹ️  Source Language: German (de-DE)
# ⚙️  Note: Speech recognition regexes (VOSK) and Koan instructions in this
#     file were machine-translated. Spoken patterns may require refinement
#     or tuning for natural speech in the target language.
#
# 🤝  CONTRIBUTIONS WELCOME!
#     We would love your help improving this map! If you test or refine these
#     regex patterns, please open a Pull Request with your improvements.
# ==============================================================================

# config/maps/plugins/0_aura_quickstart/de-DE/FUZZY_MAP_pre.py

import os
import re
import runpy

# desde pathlib importar ruta como p; importar sistema operativo como o
# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())
from pathlib import Path

from scripts.py.func.get_project_root import get_aura_project_root

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
SL5NET_AURA_PROJECT_ROOT = get_aura_project_root()

CONFIG_DIR = Path(__file__).parent

acp = SL5NET_AURA_PROJECT_ROOT / "config" / "maps"/"plugins"/"internals"/"de-DE"/"aura_constants.py"
AURA_VARIANTS = runpy.run_path(acp)["AURA_VARIANTS"]
suche = r'(buscar|buscar|buscar tú|busca|buscar|seguro|Zapatos|aspiradora|libro|tren|tren|botas|sueño)'

_meta_run_search_result = {
    'command_flags': re.IGNORECASE,
    'on_match_exec': [Path(__file__).resolve().parent / "run_search_the_result.py"],
    # EXAMPLE: py

    'only_in_windows': [ r'\.py'],
}
# sherlock

FUZZY_MAP_pre = [

    # EXAMPLE: registro

    ('log', r'^(registro|mirar|programa cargado. Mucho Divertido|qué modo de aprendizaje desactivar|intentar|coliflor|el es sorprendente)$', 70, _meta_run_search_result),

    # EXAMPLE: registro

    ('log', fr'^{AURA_VARIANTS}\s*(lógica|archivos de registro|registro-archivo|archivos de registro|explotación florestal|lluvia|a roca|tienta tiene|a Oct tiene|registro-archivo|archivo de registro|uno archivo de registro|a octeto|a registro-archivo)$', 70, _meta_run_search_result),

    # EXAMPLE: registro

    ('log', fr'^{AURA_VARIANTS}\s*(registro|mirar)$', 70, _meta_run_search_result),

    # config/maps/plugins/0_aura_quickstart/de-DE/FUZZY_MAP_pre.py:38

    # aprende a encender



    # Aprende el aura, eliminando así el

    # EXAMPLE: Activar y desactivar el modo de aprendizaje

    ('Lernmodus...', fr'^({AURA_VARIANTS}|Lauer vacío).*(aprender|vacío|aprender|Ruido|Señor)?\s*(modo|moda|debe|a través del cual)\s*(a\w*|a\w*|fuera de\w*|Excª\w+|absch\w+|comenzar|detener|activar\w+|DESACTIVAR\w*)?\s*\w*$', 100, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_learning.py']
    }),



    # --- Complemento de entrenamiento (activado/desactivado por el script anterior) ---



    # rojo anaranjado


    # EXAMPLE: código fuente de aura

    ('scripts', fr'^{AURA_VARIANTS}\s*(como)?\s*(código fuente|código fuente|negro cita|negro|obras\w+|metodos|como esto|pastel código fuente)$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [Path(__file__).resolve().parent / "run_search_the_result.py"],
    }),

    # EXAMPLE: Código fuente de búsqueda de aura

    (r'guiones', fr'^{AURA_VARIANTS}\s+{suche}\s+(código fuente|código fuente|negro|negro # cita|obras\w+|metodos|como esto|pastel código fuente)$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [Path(__file__).resolve().parent / "run_search_the_result.py"],
    }),


    # EXAMPLE: Configuración del aura

    (r'configuración', fr'^{AURA_VARIANTS}\s+(configuración\w*|configuración\w*|Ajustes\w*|confitar\w*)$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [Path(__file__).resolve().parent / "run_search_the_result.py"],
    }),

    # mermelada de aura


    # EXAMPLE: Resultado de búsqueda de Aura # Documentos de búsqueda de Homero

    ('~/Dokumente', fr'^{AURA_VARIANTS}\s+{suche}\s+(?P<camino sucio>(doc\w+|pato))$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [Path(__file__).resolve().parent / "run_search_the_result.py"],
    }),

    # método obsoleto? ¿Quizás usar run_search_the_result.py?

    # EXAMPLE: Asunto de búsqueda de aura

    ('Suche Subject wird gestartet...', fr'^{AURA_VARIANTS}\s+{suche}\s+(?P<camino sucio>\w+)$', 90, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [Path(__file__).resolve().parent / "run_search_subject.py"],
    }),

    # método obsoleto? ¿Quizás usar run_search_the_result.py?

    # Búsqueda de auras

    # EXAMPLE: AURA_VARIANTS x búsqueda

    ('Suche wird gestartet...', fr'^{AURA_VARIANTS}[^\w]?.*{suche}$', 100, {
    'command_flags': re.IGNORECASE,
    'on_match_exec': [Path(__file__).resolve().parent / "run_search.py"],
    }),

    # EXAMPLE: tuberías cerradas

    ('Suche wird gestartet...', r'^(tubo a|Rohrer buscar|naranja alto)$', 100, {
    'command_flags': re.IGNORECASE,
    'on_match_exec': [Path(__file__).resolve().parent / "run_search.py"],
    }),


    # método obsoleto? ¿Quizás usar run_search_the_result.py?

    # Buscando manual...

    # EXAMPLE: AURA_VARIANTS x dokux

    ('Handbuch wird durchsucht...', fr'^{AURA_VARIANTS}[^\w]?.*(documental\w*|manual\w*|instrucciones\w*|resultado|ayuda\w*|tú gunter|el convento tocar|impresora mediante|logo pabellón)\s*(a|buscar|\w+)?$', 100, {
        'command_flags': re.IGNORECASE,
        'on_match_exec': [Path(__file__).resolve().parent /  'run_doc_search.py']
    }),

]

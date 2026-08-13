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

# config/maps/koans_2_peter_deutsch/07_koan_auto_fix_map_errors/de-DE/FUZZY_MAP_pre.py

import re  # noqa: F401
FUZZY_MAP_pre = [
    ('fuzzy1', 'handuch', 1, {'command_flags': re.IGNORECASE}),
]

# ============================================================
# Koan 07: Reparación automática: Aura repara archivos de mapas corruptos

# ============================================================
#
# QUÉ HACE:

# Si un archivo de mapa contiene una "palabra simple" (no un formato de tupla),

# El Auto-Fix de Aura lo corrige automáticamente al cargar.

#
# IMPORTANTE:

# La reparación automática solo funciona en archivos de menos de ~1 KB.

# Esto es intencional: reescritura incontrolada de grandes obras.

# Esto evita que los archivos de mapas.

#
# TAREA:

# 1. Inserte una sola palabra en FUZZY_MAP_pre (no una tupla):

# toalla de mano

# 2. Guardar. Aura lo corrige automáticamente según una regla válida.

# 3. Verifique el registro para ver si hay "Reparación automática".

#
# PRÓXIMO PASO: Koan 08

# ============================================================

import re # noqa: F401
# desde pathlib importar ruta como p; importar sistema operativo como o # noqa: E702

# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip()) # noqa: E702



# Formato de regla: ('texto de reemplazo', r'patrón', umbral, banderas)

# Lógica: De arriba hacia abajo, el primer golpe gana. Fullmatch (^...$) detiene la canalización.


# TAREA DE PETER para Koan: 07_koan_auto_fix_map_errors

# No se encontraron reglas comentadas.

# -> Crea una nueva regla significativa para este koan.

FUZZY_MAP_pre = [
    ('fuzzy1', 'handuch',1,{'command_flags': re.IGNORECASE}),
]

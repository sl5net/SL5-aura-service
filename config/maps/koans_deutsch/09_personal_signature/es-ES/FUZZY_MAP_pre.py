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

# configmaps/koans deutsch/09_personal_signature/de-DE/FUZZY_MAP_pre.py

import re  # noqa: F401

# desde pathlib importar ruta como p; importar sistema operativo como o

# con open(('C:/tmp'if o.name=='nt'else'/tmp')+'/sl5_aura/sl5net_aura_project_root',encoding='utf-8') as f:SL5NET_AURA_PROJECT_ROOT=p(f.read().strip())




# desde la configuración de importación de configuración



# ============================================================
# Koan 09: Firma personal – Contenido de la regla dinámica

# ============================================================
#
# OBJETIVO DE APRENDIZAJE:

# Las reglas pueden contener variables de Python, p. Su nombre

# desde config/settings_local.py

#
# TAREA:

# 1. Establezca USER_NAME en config/settings_local.py

# 2. Di: “saludos cordiales” o “saludos cordiales”

#
# RESULTADO ESPERADO:

# "Atentamente, [tu nombre]"

#
# PRÓXIMO PASO: Koan 10

# ============================================================

# nombre_usuario = getattr(configuración, "NOMBRE_USUARIO", "[falta nombre]")

user_name = "Sebastian"
FUZZY_MAP_pre = [
    # EXAMPLE: Atentamente

    # (f"Con un cordial saludo, {nombre_usuario}\n", r"^(un cordial saludo|con un cordial saludo)\w*$"),


    # Atentamente

    # (f"Saludos cordiales {nombre_usuario}\n", r"^(muchos tamaños|todos los tamaños)$",

    # 81, {'command_flags': re.IGNORECASE}),

]

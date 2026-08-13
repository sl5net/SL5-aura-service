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

# config/maps/koans_deutsch/03_koan_schwierige_namen/de-DE/FUZZY_MAP_pre.py

# ============================================================
# Koan 03: Nombres difíciles – concordancia difusa en la práctica

# ============================================================
#
# OBJETIVO DE APRENDIZAJE:

# Vosk a menudo no reconoce bien los nombres difíciles. Con expresiones regulares puedes

# Aún puedes hacer coincidencias de manera confiable, incluso si hay errores tipográficos.

#
# TAREA:

# Intenta decir este título:

# “Su Reverendísimo Archioficial Consejero de Silesia”

#
# Luego mire el registro para ver qué escuchó realmente Vosk:

# grep "📢📢📢" log/aura_engine.log | cola -5

#
# Luego active la regla que mejor se ajuste (elimine #).

#
# PREGUNTA PARA PENSAR:

# ¿Qué regla es más sólida: la exacta o la que tiene .*?

# ¿Cuáles son las ventajas y desventajas de r'^Su Alteza.*$'?

#
# PRÓXIMO PASO: Koan 04

# ============================================================

FUZZY_MAP_pre = [


    # EXAMPLE: tía

    ('Tante Emmelie', r'^(tía|tandy|Y|a el|y en|y Cómo) (Emmelie|emilio\w*|Enémentir|vivien)*$'),


    # Coincidencia exacta (precisa pero frágil):

    # ('Genial :) Felicitaciones', r'^Su Mayor Honor.*Silesia.*$'),


    # Coincidencia robusta (flexible pero no específica):

    # ('Genial :) Felicitaciones', r'^Su Señoría.*$'),


    # Coincidencia aproximada para el nombre:

    # ('¡Condesa reconocida!', r'^.*gr[äa]fin.*$', 0, {'command_flags': re.IGNORECASE}),

]

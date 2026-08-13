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

import subprocess

# UNICODE_NUMS = {1: "⓵", 2: "⓶", 3: "⓷"}

UNICODE_NUMS = {1: "1️", 2: "2️", 3: "3️"}


def execute(match_data):
    # Lógica para la siguiente pregunta aquí...

    subprocess.run(["espeak", "-v", "de", "Hervorragend! Nächste Frage."])
    # Aquí luego llamaremos a la función que muestra la siguiente tarjeta en CopyQ

    return "Nächste Frage wird geladen…"


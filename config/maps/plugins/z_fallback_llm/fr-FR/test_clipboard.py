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

# config/maps/plugins/z_fallback_llm/de-DE/test_clipboard.py

# test_clipboard.py


# source .venv/bin/activer

# python config/maps/plugins/z_fallback_llm/de-DE/test_clipboard.py


# importer le système d'exploitation

import pyperclip

# print(f"Utilisateur : {os.environ.get('USER')}")

# print(f"Affichage : {os.environ.get('DISPLAY')}")

# print(f"Wayland : {os.environ.get('WAYLAND_DISPLAY')}")


try:
    content = pyperclip.paste()
    # print(f"✅ Contenu du presse-papier : '{content}'")

except Exception as e:
    print(f"❌ Fehler: {e}")

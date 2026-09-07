# scripts/py/func/audio/piper_engine.py

# import os
#
# _voice = None # SingletonPIPER_SERER_PATH = "~/projects/py/TTS"
#
# def speak_with_piper(text, model_path):
#     global _voice
#     try:
#         from piper.voice import PiperVoice
#         if _voice is None:
# Load model once
#             if not os.path.exists(model_path):
#                 return False
#             _voice = PiperVoice.load(model_path)
#
#         # Synthese direkt in den Audio-Stream / Temp-WAV
#         import tempfile
#         import subprocess
#         with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
#             _voice.synthesize(text, tmp)
#             # Nur das Abspielen ist ein kurzer Subprocess (extrem schnell)
#             subprocess.run(["aplay", tmp.name], stderr=subprocess.DEVNULL)
#             return True
#     except Exception as e:
#         print("Piper engine says: {e}")
#         return False

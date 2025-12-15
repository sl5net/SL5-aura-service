# test_clipboard.py

# source .venv/bin/activate
# python config/maps/plugins/z_fallback_llm/de-DE/test_clipboard.py

#import os
import pyperclip

# print(f"User: {os.environ.get('USER')}")
# print(f"Display: {os.environ.get('DISPLAY')}")
# print(f"Wayland: {os.environ.get('WAYLAND_DISPLAY')}")

try:
    content = pyperclip.paste()
    # print(f"✅ Inhalt der Zwischenablage: '{content}'")
except Exception as e:
    print(f"❌ Fehler: {e}")

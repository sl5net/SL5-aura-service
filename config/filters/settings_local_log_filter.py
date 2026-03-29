# config/filters/settings_local_log_filter.py
# r"▉",

# LOG_EXCLUDE = []

LOG_EXCLUDE_asdfsdf = [
    r"📦",
    r"PUNCTUATION_MAP",
    r"〃",
    r"🗑",
    r"process_text_in_background.py:365",
    r"🗺Starting recursive map",
    r"🗺 Map loading complete",
    r"#####",
]

LOG_EXCLUDE = [
    r"heartbeat.*status: OK",
    r"cleaning up temp file",
    r"(?i)debug: rule \d+ skipped",
    r"🥳",
    r"↩",
    r"🛑",
    r"🚨",
    r"💥",
    r"⚠",
    r"📂",
    r"📦",
    r"🚀",
    r"❌",
    r"🎯",
    r"🔍",
    r"⏱",
    r"🏗",
    r"📤",
    r"🗺",
    r"🌍",
    r"✅",
    r"💾",
    r"🗣",
    r"▉",
    r"〃",
    # r"👀",
    r"⏳",
    r"start_languagetool_server",
    r"Server is ALREADY online",
    r"Set auto-enter flag",
    r"lang_code:",
    r"Learned new max model footprint:",
    r"run_mode_override",
    r"⚙",
    r"🎤",
    r"==",
    r"current_dir:",
    r"ZIP Date:",
    r"Source Date:",
    r"Datei gefunden:",
    r"Schlüssel erstellt:",
    r"Key created",
    r"_apply_fix_name_error",

    r"microphone mute state",
    r"🎬🏁",
    r"Target model name",
    r"Using model for lang",
    r"manage_audio_routing",
    r"AUTO_ENTER_AFTER_DICTATION",
    r"initial_timeout",
    r"transcribe_audio_with_feedback",
    r"Dictation Session started",
    r"Speech detected",
    r"mute_microphone",
    r"Muted sound",
    r"Test action completed",
    r"Manual stop detected",
    r"Switching VAD mode",
    r"Graceful shutdown initiated",
    r"Yielding chunk",
    r"Stop signal received",
    r"Session has ended",
    r"Maintenance",


]
# OPTIONAL: Wenn nicht leer, wird NUR das geloggt, was hier matcht (ONLY und oder logig: Mindes eines aus LOG_ONLY muss matchen)
LOG_ONLY = []
LOG_ONLY_asfsdf = [
     r"Successfully",
     r"CRITICAL",
     r"📢📢📢 #",
     r"Title",
     r"window",
     r":st:",
]


# LOG_ONLY = [
#     r"oma",
#     r"00_koan",
#     r"Hallo Welt",
#     r"hallo",
#     r"map.*load\|load.*map",
# ]


LOG_ONLY_off = [
    r"oma",
    r"00_koan",
    r"Hallo Welt",
    r"hallo",
    r"load",
    r"map",
    r"🗺",
    r"plugin",
    r"koan",
    r"window",

]

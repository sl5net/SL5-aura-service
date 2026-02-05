# file: scripts/py/func/checks/integrity_rules.py

"""
This file defines critical code fragments that must exist in specific files.
The integrity checker will verify their presence on startup in DEV_MODE.
If a check fails, the application will exit to prevent running with broken logic.

Format:
{
    "path/to/file_relative_to_project_root.py": [
        "exact_code_fragment_to_find",
        "another_fragment_for_the_same_file"
    ]
}
"""

UNSAFE_LINE_STARTS = [
    "from config.settings_local import",
    "import config.settings_local"
]

FORBIDDEN_PATTERNS = [
    "if settings.DEV_MODE_memory:",
    "if settings.DEV_MODE_all_processing:",
]

INTEGRITY_CHECKS = {

    'README.md': [
        'setup/windows11_setup.ps1',
        'https://www.autohotkey.com/',
        './scripts/restart_venv_and_run-server.sh',
        'start_dictation_v2.0.bat',
        'https://github.com/hluk/CopyQ',
        'touch /tmp/sl5_record.trigger',
        'c:/tmp/sl5_record.trigger',
        'config/settings_local.py_Example.txt',
        'config/settings_local.py',
        'config/settings.py',
        'setup/setup.bat',
        'https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml',
        'update.bat',
        'aura_engine.py',
        'get_suggestions.py',
        'type_watcher.ahk',
        'trigger-hotkeys.ahk',
        '![pydeps -v -o dependencies.svg scripts/py/func/main.py](doc_sources/dependencies.svg)',
        'https://github.com/sl5net/SL5-aura-service/releases/tag/v0.2.0.1',
        '[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)',
        '`mv vosk-model-*.zip models/`'
    ],

    'requirements.txt': [

        "comtypes==1.4.11; sys_platform == 'win32'",
        "pycaw==20240210; sys_platform == 'win32'",
        
        "fasttext-wheel==0.9.2; sys_platform == 'win32'",
        "fasttext==0.9.3; sys_platform != 'win32'",
    ],

    'tools/download_all_packages.py': [
        "nargs='*'",
        'default=[]',
    ],

    # don't use . notation in this settings part. if we don't hava s settings part we need delete following checks:
    'config/settings.py': [
        "game",
        '"standard_actions/wikipedia_local": False,',
        '"empty_all": False,'
    ],

    # don't use . notation in this settings part. if we don't hava s settings part we need delete following checks:
    'config/settings_local.py': [
        "game",
        '"standard_actions/wikipedia_local": True,',
    ],

    #     logger.info(f"Using timeouts: Initial Wait={INITIAL_WAIT_TIMEOUT}s, Speech Pause={SPEECH_PAUSE_TIMEOUT}s")
#         'logger.info(f"initial_timeout , timeout: {initial_silence_timeout} , {SPEECH_PAUSE_TIMEOUT}")',
#         'logger.info(f"⏹️ Loop finished (timeout of {current_timeout:.1f}s reached).")',
    "scripts/py/func/transcribe_audio_with_feedback.py": [
        'logger.info(f"initial_timeout , timeout: {initial_silence_timeout} , {SPEECH_PAUSE_TIMEOUT}")',
        'logger.info(f"⏹️ Loop finished (timeout of {current_timeout:.1f}s reached).")',
        '        return audio_np[::3, 0].tobytes()',
        '        audio_np = np.frombuffer(raw_data, dtype=np.int16)',
        'device_id = get_device_id(device_name,logger)',
        # "blocksize=4000"
    ],

    "scripts/py/func/audio_manager.py": [
        "if not settings.PLUGIN_HELPER_TTS_ENABLED:"
    ],



    'scripts/py/func/handle_trigger.py': [
        'info("🎬🏁 Trigger received',
        '🎬⏹️ Manual 🛑 stop trigger detected. Signaling session to end.',
        "Processing chunk:",
        "Gracefully exiting recording loop.",
        "Finalizing recording session:",
    ],

    # make sure buzzword Tests is in
    "scripts/py/func/checks/self_tester.py": [
        "{failed_count} Tests",
        " == expected"
    ],

    "scripts/py/func/model_manager.py": [
        "Reactive Loading" ,
        'Memory Monitoring' ,
        'Proactive Unloading'
    ],

    "scripts/py/func/get_active_window_title.py": [
        "0o600)"
    ],
    # Path(X11_CACHE_FILE).chmod(0o600)
    # or
    # os.chmod(X11_CACHE_FILE, 0o600)


    # Protects the regex substitution logic in the main processing function.
    # germen umlauts needs this to could read correct for e.g. from script like autokey
    # Ensures critical text processing logic is present.
    "scripts/py/func/process_text_in_background.py": [
        "settings = DynamicSettings()",
        "new_text = re.sub(",
        'encoding="utf-8-sig"',
        'f"✅ Background processing for',
        'f"✅ 💾 THREAD: Successfully wrote to '
    ],
    # settings = DynamicSettings() is important ! check the fist rule in self_tester and try it to change it 2026-0104-1829 4.1.'26 18:29 Sun



    # should_remove_zips_after_unpack=true It's eventually useful to have it sometimes longer but maybe not online and not at costumers

    # --- Start of Ensures language selection is included ---

    # Ensures language selection is included in the macOS setup.
    "setup/macos_setup.sh": [
        'source "$(dirname "${BASH_SOURCE[0]}")/../scripts/sh/get_lang.sh"',
        'should_remove_zips_after_unpack=true'
    ],

    # Ensures language selection is included in the Ubuntu setup.
    "setup/ubuntu_setup.sh": [
        'source "$(dirname "${BASH_SOURCE[0]}")/../scripts/sh/get_lang.sh"',
        'should_remove_zips_after_unpack=true'

    ],

    # Ensures language selection is included in the Manjaro/Arch setup.
    "setup/manjaro_arch_setup.sh": [
        'source "$(dirname "${BASH_SOURCE[0]}")/../scripts/sh/get_lang.sh"',
        'should_remove_zips_after_unpack=true'
    ],

    # Ensures language selection is included in the Windows setup.
    "setup/windows11_setup.ps1": [
        'setup_initial_model.py',
        '$should_remove_zips_after_unpack = $true'
    ],

    # --- End of Ensures language selection is included ---

}

# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY
# scripts/py/func/cleanup.py
import sys
import traceback
import os


def cleanup(logger, files_to_remove):
    # Check if an exception triggered this
    exc_type, exc_value, exc_traceback = sys.exc_info()

    if exc_type:
        logger.error("❌ AURA CRASHED WITH EXCEPTION:")
        logger.error("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
    else:
        # Check if it was a signal or just a regular exit
        logger.info(f"ℹ️ Aura reached a clean exit (PID: {os.getpid()}). No active Exception.")

        # --- Ghost Plugin / Deactivation Hint ---
        logger.info("❓ UNEXPECTED SHUTDOWN? Check for 'ghost' plugins!")
        logger.info("💡 PRO-TIP: Renaming 'file.py' to 'file OFF.py' does NOT deactivate it.")
        logger.info("💡 The engine still loads any file ending in '.py'.")
        logger.info("💡 To truly deactivate a plugin, change the extension to '.py_bak' or move it out of the folder.")

        # CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY
        logger.info(
            "💡 Run this command to check for suspicious ghost map files:"
            "\n\npython3 -c \"import pathlib, re; maps_dir=pathlib.Path('config') / 'maps'; p=list(maps_dir.rglob('*.py')); rx=re.compile(r'(\\s|\\.py\\.|\\b(off|bak|old|copy|tmp|disabled|backup)\\b|(?<=[-_])(off|bak|old|copy|tmp|disabled|backup)(?=[-_.]))', re.I); s=[f for f in p if rx.search(f.name)]; print(f'⚠️ Found {len(s)} suspicious map(s):\\n' + '\\n'.join(f' - {f}' for f in s) if s else f'✅ All {len(p)} map files look clean.')\"\n\n"  
        )
        
        logger.info(
            "💡 Run this command to check syntax of recent map files:"
            "\n\npython3 -c \"import pathlib, datetime, py_compile; maps_dir=pathlib.Path('config') / 'maps'; maps=sorted(maps_dir.rglob('*.py'), key=lambda x: x.stat().st_mtime, reverse=True)[:5]; print('🕒 Checking syntax of 5 most recent maps:'); [print(f' ✅ [{datetime.datetime.fromtimestamp(p.stat().st_mtime):%Y-%m-%d %H:%M}] {p}' if py_compile.compile(str(p), doraise=False) else f' ❌ [{datetime.datetime.fromtimestamp(p.stat().st_mtime):%Y-%m-%d %H:%M}] {p} -> SYNTAX ERROR') for p in maps]\"\n\n"  
        )
        # ----------------------------------------------

        # CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY
        # --- Automatic Check of Recent Maps ---
        logger.info("🔍 Checking syntax of 5 most recently modified map files:")
        import pathlib
        import datetime
        import ast

        maps_dir = pathlib.Path("config") / "maps"
        
        if maps_dir.exists():
            recent_maps = sorted(
                maps_dir.rglob("*.py"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )[:5]
            for map_file in recent_maps:
                mtime_str = datetime.datetime.fromtimestamp(map_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                try:
                    ast.parse(map_file.read_text(encoding="utf-8", errors="ignore"))
                    logger.info(f"   ✅ [{mtime_str}] {map_file}")
                except SyntaxError as err:
                    logger.error(f"\n\n   ❌ [{mtime_str}] \n\n{map_file}:{err.lineno}\n\n -> Line {err.lineno}: {err.msg}\n\n")
                except Exception as err:
                    logger.error(f"\n\n   ❌ [{mtime_str}] {map_file} -> {err}\n\n")
        # ----------------------------------------------


    # Final location check
    logger.info("🏁 Cleanup Stack-Trace (where the process ended):\n " + "".join(traceback.format_stack()))

    for f in files_to_remove:
        logger.info(f"Removing file: {f}")
        f.unlink(missing_ok=True)
    logger.info("✅ Cleanup complete.")

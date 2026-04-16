import sys
import os
import logging
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from scripts.py.func.get_active_window_title import get_active_window_title_safe
import scripts.py.func.process_text_in_background as ptib
from scripts.py.func.process_text_in_background import process_text_in_background


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 aura_cli.py '<text>' [lang_code]")
        sys.exit(1)

    raw_text = sys.argv[1]
    lang_code = sys.argv[2] if len(sys.argv) > 2 else "de-DE"

    # FIX: Fenstertitel ins Modul-Global schreiben, nicht nur lokal halten
    window_title = get_active_window_title_safe()
    ptib._active_window_title = window_title

    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logger = logging.getLogger("aura_cli")

    logger.info(f"[aura_cli] window_title='{window_title}'")
    logger.info(f"[aura_cli] raw_text='{raw_text}'")

    output_dir = project_root / "log" / "cli_output"
    output_dir.mkdir(parents=True, exist_ok=True)

    active_lt_url = "http://localhost:8082/v2/check"

    process_text_in_background(
        logger=logger,
        LT_LANGUAGE=lang_code,
        raw_text=raw_text,
        output_dir=output_dir,
        recording_time=0,
        active_lt_url=active_lt_url,
    )


if __name__ == "__main__":
    main()

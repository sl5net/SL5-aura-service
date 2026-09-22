
import logging
import subprocess
from pathlib import Path

logger = logging.getLogger("i18n_argos")

LANG_MAP = {
    "pt-BR": "pt",
    "zh-CN": "zh",
}


def ensure_argos_package(src_lang: str, tgt_lang: str) -> bool:
    pkg_name = f"translate-{src_lang}_{tgt_lang}"
    try:

        check_proc = subprocess.run(
            ["argospm", "list"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )

        if pkg_name in check_proc.stdout:
            return True

        logger.info("Argos package '%s' missing. Attempting on-the-fly installation...", pkg_name)
        install_proc = subprocess.run(
            ["argospm", "install", pkg_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        
        if install_proc.returncode == 0:
            logger.info("Argos package '%s' installed successfully.", pkg_name)
            return True

        logger.warning("Failed to install Argos package '%s'.", pkg_name)
        return False
    except Exception as exc:
        logger.warning("Error verifying/installing Argos package '%s': %s", pkg_name, exc)
        return False


def translate_with_argos(text: str, source_lang: str, target_lang: str) -> list[str] | None:
    src = LANG_MAP.get(source_lang, source_lang)
    tgt = LANG_MAP.get(target_lang, target_lang)

    if not ensure_argos_package(src, tgt):
        logger.warning("Argos model translate-%s_%s unavailable.", src, tgt)
        return None

    try:
        logger.info("Executing local Argos translation: %d chars (%s->%s)", len(text), src, tgt)

        result = subprocess.run(
            ["argos-translate", "--from-lang", src, "--to-lang", tgt, text],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=True,
        )

        lines = result.stdout.strip().split("\n")
        logger.info("Argos translation completed successfully (%d lines returned).", len(lines))
        return lines
    except Exception as exc:
        logger.warning("Argos translation execution failed: %s", exc)
        return None

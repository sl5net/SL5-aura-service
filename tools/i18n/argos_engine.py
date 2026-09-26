
import logging
import subprocess
from pathlib import Path

logger = logging.getLogger("i18n_argos")

LANG_MAP = {
    "pt-BR": "pt",
    "zh-CN": "zh",
}

FAILED_PACKAGES: set[str] = set()


def ensure_argos_package(src_lang: str, tgt_lang: str) -> bool:
    pkg_name = f"translate-{src_lang}_{tgt_lang}"
    if pkg_name in FAILED_PACKAGES:
        return False

    try:

        check_proc = subprocess.run(
            ["argospm", "list"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )

        if pkg_name in check_proc.stdout:
            return True

        logger.info("Argos package '%s' missing. Attempting on-the-fly installation", pkg_name)
        install_proc = subprocess.run(
            ["argospm", "install", pkg_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        
        if install_proc.returncode == 0:
            logger.info("Argos package '%s' installed successfully.", pkg_name)
            return True

        FAILED_PACKAGES.add(pkg_name)
        logger.warning("Failed to install Argos package '%s'.", pkg_name)
        return False
    except Exception as exc:
        FAILED_PACKAGES.add(pkg_name)
        logger.warning("Error verifying/installing Argos package '%s': %s", pkg_name, exc)
        return False


def _execute_argos_cli(text: str, src: str, tgt: str) -> list[str] | None:
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


def translate_with_argos(text: str, source_lang: str, target_lang: str) -> list[str] | None:
    src = LANG_MAP.get(source_lang, source_lang)
    tgt = LANG_MAP.get(target_lang, target_lang)

    if ensure_argos_package(src, tgt):
        return _execute_argos_cli(text, src, tgt)

    pivot_lang = "en"
    can_pivot = (
        src != pivot_lang
        and tgt != pivot_lang
        and ensure_argos_package(src, pivot_lang)
        and ensure_argos_package(pivot_lang, tgt)
    )

    if can_pivot:
        logger.info("Pivoting Argos translation via '%s': %s -> %s -> %s", pivot_lang, src, pivot_lang, tgt)
        intermediate = _execute_argos_cli(text, src, pivot_lang)
        if intermediate is None:
            return None
        return _execute_argos_cli("\n".join(intermediate), pivot_lang, tgt)

    logger.warning("Argos model translate-%s_%s unavailable (direct and pivot).", src, tgt)
    return None

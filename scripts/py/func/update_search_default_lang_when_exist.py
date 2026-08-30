import re
from pathlib import Path


def update_search_default_lang_when_exist(
    project_root: Path,
    lang_code: str,
    logger: object | None = None,
) -> bool:
    """Safely updates the default language in docs/search_online.html if the file exists."""
    if not project_root or not lang_code:
        return False

    target_file = project_root / "docs" / "search_online.html"
    if not target_file.is_file():
        msg = f"Could not find file {target_file} in {project_root}"
        if logger and hasattr(logger, "error"):
            logger.error(msg)
        else:
            print(msg)
        return False

    try:
        content = target_file.read_text(encoding="utf-8")
        updated = content

        updated = re.sub(
            r'(<meta\s+name=["\']default-language["\']\s+content=["\'])[^"\']*(["\'])',
            rf'\g<1>{lang_code}\2',
            updated,
            flags=re.IGNORECASE,
        )

        updated = re.sub(
            r'(const\s+DEFAULT_LANG\s*=\s*["\'])[^"\']*(["\'];)',
            rf'\g<1>{lang_code}\2',
            updated,
        )

        if updated != content:
            target_file.write_text(updated, encoding="utf-8")
            msg = f"Updated Algolia search default language in '{lang_code}' in {target_file}"
            if logger and hasattr(logger, "info"):
                logger.info(msg)
            else:
                print(msg)
            return True

    except Exception as e:
        msg = f"Could not update Algolia search default language in {target_file}: {e}"
        if logger and hasattr(logger, "warning"):
            logger.warning(msg)
        else:
            print(msg)
        return False

    return False

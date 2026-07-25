# scripts/py/func/process_text_in_background_helper/resolve_file_replacement.py:1
import os

from scripts.py.func.config.dynamic_settings import settings

def resolve_file_replacement(replacement, options_dict, logger=None):
    if not settings.FILE4REPLACEMENT_USE:
        return replacement

    if not isinstance(replacement, str) or not replacement or not options_dict:
        return replacement

    prefixes = tuple(getattr(settings, 'FILE4REPLACEMENT_PREFIX_CHARS', ()) or ())
    if prefixes:
        if not replacement.startswith(prefixes):
            return replacement
    elif replacement[0].isalpha():
        return replacement

    source_path = options_dict.get('source_path', '')
    project_root = os.environ.get('SL5NET_AURA_PROJECT_ROOT', '')

    try:
        plugin_dir = os.path.dirname(os.path.join(project_root, source_path))
        candidate_file = os.path.abspath(os.path.join(plugin_dir, replacement))
        plugin_dir_real = os.path.abspath(plugin_dir)

        if (not settings.FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL
        and ( not (candidate_file == plugin_dir_real or candidate_file.startswith(plugin_dir_real + os.sep)))):
            error_msg = f"Rejected path traversal attempt: '{replacement}'"
            if logger:
                logger.error(error_msg)
            return error_msg
        if os.path.isfile(candidate_file):
            with open(candidate_file, 'r', encoding='utf-8') as f:
                file_content = f.read().strip()
                return file_content
        else:
            return replacement
    except Exception as e:
        error_msg = f"Error resolving file-based replacement for '{replacement}': {e}"
        logger.error(error_msg)
        return error_msg


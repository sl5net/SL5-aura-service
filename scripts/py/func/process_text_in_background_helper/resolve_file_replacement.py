import os

def resolve_file_replacement(replacement, options_dict, logger=None):
    if not isinstance(replacement, str) or not replacement or not options_dict:
        return replacement
    if not replacement.startswith('-') and not replacement.startswith('.'):
        return replacement
    source_path = options_dict.get('source_path', '')
    project_root = os.environ.get('SL5NET_AURA_PROJECT_ROOT', '')

    try:
        plugin_dir = os.path.dirname(os.path.join(project_root, source_path))
        candidate_file = os.path.abspath(os.path.join(plugin_dir, replacement))
        plugin_dir_real = os.path.abspath(plugin_dir)
        if not (candidate_file == plugin_dir_real or candidate_file.startswith(plugin_dir_real + os.sep)):
            error_msg = f"Rejected path traversal attempt: '{replacement}'"
            if logger:
                logger.error(error_msg)
            return error_msg
        if os.path.isfile(candidate_file):
            with open(candidate_file, 'r', encoding='utf-8') as f:
                file_content = f.read().strip()
                return file_content
        else:
            error_msg = f"Error its not a file: '{replacement}'"
            return error_msg
    except Exception as e:
        error_msg = f"Error resolving file-based replacement for '{replacement}': {e}"
        logger.error(error_msg)
        return error_msg


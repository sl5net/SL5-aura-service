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
        candidate_file = os.path.join(plugin_dir, replacement)
        if os.path.isfile(candidate_file):
            with open(candidate_file, 'r', encoding='utf-8') as f:
                file_content = f.read().strip()
                return file_content
        else:
            return f"Error its not a file: '{replacement}'"
    except Exception as e:
        # if logger:
        #     logger.error(f"Error resolving file-based replacement for '{replacement}': {e}")
        return f"Error resolving file-based replacement for '{replacement}': {e}"

